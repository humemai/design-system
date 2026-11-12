"""Check that every css/*.css file parses and follows the layout rules.

    uv run --no-project --with tinycss2==1.4.0 python -I scripts/check_css.py
    uv run --no-project --with tinycss2==1.4.0 python -I scripts/check_css.py FILE...
    uv run --no-project --with tinycss2==1.4.0 python -I scripts/check_css.py --self-test

tinycss2 follows the CSS Syntax spec, which closes any block still open at the
end of the file without an error. So there are two syntax checks: tinycss2
reports malformed rules and declarations, and a small scanner reports
unbalanced braces, brackets and parentheses and unclosed strings or comments,
which browsers would silently repair.

Then the layout rules of the README ("Layout across screen sizes"), each with
an id. A fixture in scripts/fixtures/css/bad-<id>.css fails on exactly that
rule, and --self-test proves it, and that good.css passes:

  media-px          a media condition with a px length (write rem)
  media-range       min-width or max-width in a media condition (write a range)
  column            column-count or columns (prose is one column), or a
                    column-width that is not in rem
  column-height     a multi-column box with a height, which adds columns sideways
  autofit           repeat(auto-fit|auto-fill, ...) without minmax(min(100%, X), ...)
  container         container-type other than inline-size, or on a box that
                    shrinks to its content (flex item, inline, float, fit-content)
  container-self    an @container rule that styles its own container
  font-viewport     a font size in a viewport or container unit (WCAG F94)

This is a static check of this repository's css/. The headless counterpart,
which measures the rendered page, is scripts/check_layout.py.
"""
import re
import sys
from pathlib import Path

import tinycss2

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "scripts" / "fixtures" / "css"
RULES = ("media-px", "media-range", "column", "column-height", "autofit", "container", "container-self", "font-viewport")

# A font size that reads a viewport unit does not follow the reader's zoom.
# --hm-text-display is the one known case; it is an open item in
# docs/decisions.md ("Layout across screen sizes", 2026-11-12), not a pattern.
FONT_VIEWPORT_ALLOWED = {"--hm-text-display"}


def errors(nodes, name):
    """Yield (line, message) for every parse error, descending into blocks."""
    for node in nodes:
        if node.type == "error":
            yield node.source_line, node.message
        elif node.type == "qualified-rule" and node.content is not None:
            # Style rules hold declarations, which may nest further rules.
            yield from errors(tinycss2.parse_blocks_contents(node.content), name)
        elif node.type == "at-rule" and node.content is not None:
            yield from errors(tinycss2.parse_blocks_contents(node.content), name)


TOKEN = re.compile(r"""/\*.*?\*/|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'|[{}()\[\]]|/\*|["']""", re.S)
PAIRS = {"}": "{", ")": "(", "]": "["}


def balance(text):
    """Yield (line, message) for an unbalanced bracket, string or comment."""
    stack = []
    for m in TOKEN.finditer(text):
        tok, line = m.group(), text.count("\n", 0, m.start()) + 1
        if tok in ("/*", '"', "'"):
            yield line, f"unclosed {'comment' if tok == '/*' else 'string'}"
        elif tok in "{([":
            stack.append((tok, line))
        elif tok in PAIRS:
            if not stack or stack[-1][0] != PAIRS[tok]:
                yield line, f"unmatched {tok!r}"
            else:
                stack.pop()
    for tok, line in stack:
        yield line, f"unclosed {tok!r}"


# ---- layout rules -----------------------------------------------------------

PX = re.compile(r"(?<![\w.-])\d*\.?\d+px\b", re.I)
LEGACY = re.compile(r"\b(?:min|max)-(?:width|height|inline-size|block-size)\b", re.I)
VIEWPORT_UNIT = re.compile(r"[\d.](?:[dsl]?v(?:w|h|i|b|min|max)|cq(?:w|h|i|b|min|max))\b", re.I)
REM = re.compile(r"^\s*\d*\.?\d+rem\s*$", re.I)
HEIGHT_PROPS = {"height", "max-height", "block-size", "max-block-size"}
# What makes a box shrink to its content, so inline-size containment makes it 0 wide.
SHRINK = {
    "display": {"inline", "inline-block", "inline-flex", "inline-grid", "inline-table"},
    "float": {"left", "right", "inline-start", "inline-end"},
    "position": {"absolute", "fixed"},
}
SHRINK_PROPS = {"flex", "flex-basis", "flex-grow", "flex-shrink"}
SHRINK_WIDTHS = re.compile(r"\b(?:fit-content|max-content|min-content)\b", re.I)


def split_top(text, sep=","):
    """Split on a separator that is not inside parentheses."""
    parts, depth, cur = [], 0, []
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def call_args(text, start):
    """The text inside the parentheses that open at text[start] == '('."""
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                return text[start + 1:i]
    return text[start + 1:]


def autofit_problems(value):
    """Yield a message for each repeat(auto-fit|auto-fill, ...) with no guarded minmax."""
    for m in re.finditer(r"repeat\(\s*auto-(?:fit|fill)\s*,", value, re.I):
        args = call_args(value, m.start() + len("repeat"))
        track = args.split(",", 1)[1].strip() if "," in args else ""
        if not track.lower().startswith("minmax("):
            yield f"auto-fit/auto-fill track {track!r} is not minmax(min(100%, X), ...)"
            continue
        first = split_top(call_args(track, len("minmax")))[0].strip()
        if not re.match(r"^min\(\s*100%\s*,", first, re.I) and first not in ("0", "0px", "0%"):
            yield f"auto-fit/auto-fill minimum {first!r} overflows a narrow box; use min(100%, X)"


def selectors(prelude):
    return [re.sub(r"\s+", " ", s).strip() for s in split_top(tinycss2.serialize(prelude))]


def declarations(content):
    return [d for d in tinycss2.parse_blocks_contents(content, skip_comments=True, skip_whitespace=True)]


def lint(text):
    """Yield (line, rule id, message) for every layout-rule violation in text."""
    nodes = tinycss2.parse_stylesheet(text, skip_comments=True, skip_whitespace=True)
    container_selectors = set()

    def collect(rule_nodes):
        for node in rule_nodes:
            if node.type == "qualified-rule" and node.content is not None:
                if any(d.type == "declaration" and d.lower_name in ("container-type", "container") for d in declarations(node.content)):
                    container_selectors.update(selectors(node.prelude))
            elif node.type == "at-rule" and node.content is not None:
                collect(tinycss2.parse_rule_list(node.content, skip_comments=True, skip_whitespace=True))

    collect(nodes)

    def walk(rule_nodes, in_container):
        for node in rule_nodes:
            if node.type == "at-rule":
                prelude = tinycss2.serialize(node.prelude)
                if node.lower_at_keyword == "media":
                    if PX.search(prelude):
                        yield node.source_line, "media-px", f"@media {prelude.strip()}: write the width in rem (62.5rem, not 1000px)"
                    if LEGACY.search(prelude):
                        yield node.source_line, "media-range", f"@media {prelude.strip()}: use the range syntax, (width >= 62.5rem)"
                if node.content is not None:
                    inner = tinycss2.parse_rule_list(node.content, skip_comments=True, skip_whitespace=True)
                    yield from walk(inner, in_container or node.lower_at_keyword == "container")
            elif node.type == "qualified-rule" and node.content is not None:
                items = declarations(node.content)
                decls = {d.lower_name: tinycss2.serialize(d.value).strip() for d in items if d.type == "declaration"}
                line = node.source_line
                names = set(decls)
                if in_container:
                    for sel in selectors(node.prelude):
                        if sel in container_selectors:
                            yield line, "container-self", f"{sel} styles itself inside an @container rule; a container cannot, style a child"
                for name in ("column-count", "columns"):
                    if name in decls:
                        yield line, "column", f"{name}: prose is one column; the only multi-column use is column-width in rem on a list"
                if "column-width" in decls and not REM.match(decls["column-width"]):
                    yield line, "column", f"column-width: {decls['column-width']} is not a single rem length"
                if names & {"column-width", "column-count", "columns"}:
                    for name in sorted(HEIGHT_PROPS & names):
                        yield line, "column-height", f"{name} on a multi-column box adds columns sideways (WCAG 1.4.10)"
                    if decls.get("column-fill") == "auto":
                        yield line, "column-height", "column-fill: auto on a multi-column box adds columns sideways"
                for name, value in decls.items():
                    if name in ("grid-template-columns", "grid-template-rows", "grid-template", "grid"):
                        for message in autofit_problems(value):
                            yield line, "autofit", message
                    if name == "font-size" or (name.startswith("--hm-text-") and name not in FONT_VIEWPORT_ALLOWED):
                        if VIEWPORT_UNIT.search(value):
                            yield line, "font-viewport", f"{name}: {value} does not follow the reader's zoom (WCAG F94); use rem"
                if "container-type" in decls or "container" in decls:
                    kind = decls.get("container-type") or decls["container"].split("/")[-1].strip()
                    if kind not in ("inline-size", "normal"):
                        yield line, "container", f"container type {kind!r}: use inline-size ('size' needs a height of its own)"
                    for prop, bad in SHRINK.items():
                        if decls.get(prop) in bad:
                            yield line, "container", f"{prop}: {decls[prop]} shrinks to its content, so the container is 0 wide; use a block wrapper"
                    if names & SHRINK_PROPS:
                        yield line, "container", "a flex item shrinks to its content, so the container is 0 wide; use a block wrapper"
                    for name in ("width", "inline-size"):
                        if SHRINK_WIDTHS.search(decls.get(name, "")):
                            yield line, "container", f"{name}: {decls[name]} shrinks to its content, so the container is 0 wide"
                # Nested rules (CSS nesting) are checked as their own rules.
                yield from walk([n for n in items if n.type in ("qualified-rule", "at-rule")], in_container)

    yield from walk(nodes, False)


def check_file(path):
    """Print every problem in one file; return how many."""
    text = path.read_text()
    nodes = tinycss2.parse_stylesheet(text, skip_comments=True, skip_whitespace=True)
    try:
        shown = path.resolve().relative_to(ROOT)
    except ValueError:
        shown = path
    found = [(line, "syntax", message) for line, message in list(errors(nodes, path.name)) + list(balance(text))]
    found += list(lint(text))
    for line, rule, message in found:
        print(f"{shown}:{line}: [{rule}] {message}")
    return len(found)


def self_test():
    """Every bad-<id>.css fixture fails on its own rule; good.css passes."""
    bad = sorted(FIXTURES.glob("bad-*.css"))
    if not bad:
        sys.exit("no fixtures in scripts/fixtures/css")
    failed = 0
    seen = set()
    for path in bad:
        rule = path.stem[len("bad-"):].split("--")[0]  # bad-<id>.css or bad-<id>--<variant>.css
        seen.add(rule)
        rules = {r for _, r, _ in lint(path.read_text())}
        if rule not in rules:
            print(f"✗ {path.name}: expected [{rule}], found {sorted(rules) or 'nothing'}")
            failed += 1
    for rule in RULES:
        if rule not in seen:
            print(f"✗ no fixture for [{rule}]")
            failed += 1
    for line, rule, message in lint((FIXTURES / "good.css").read_text()):
        print(f"✗ good.css:{line}: [{rule}] {message}")
        failed += 1
    if failed:
        sys.exit(f"{failed} fixture problem(s)")
    print(f"✓ {len(bad)} bad fixtures fail on their own rule, good.css passes")


def main():
    args = sys.argv[1:]
    if args == ["--self-test"]:
        self_test()
        return
    files = [Path(a) for a in args] if args else sorted((ROOT / "css").glob("*.css"))
    if not files:
        sys.exit("no css/*.css found")
    bad = sum(check_file(path) for path in files)
    if bad:
        sys.exit(f"{bad} CSS problem(s)")
    print(f"✓ {len(files)} CSS files parse and follow the layout rules")


if __name__ == "__main__":
    main()
