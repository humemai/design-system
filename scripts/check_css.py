"""Check that every css/*.css file parses.

    uv run --no-project --with tinycss2==1.4.0 python -I scripts/check_css.py

tinycss2 follows the CSS Syntax spec, which closes any block still open at the
end of the file without an error. So there are two checks: tinycss2 reports
malformed rules and declarations, and a small scanner reports unbalanced
braces, brackets and parentheses and unclosed strings or comments, which
browsers would silently repair. This is a syntax check only; scripts/check.py
checks the token values.
"""
import re
import sys
from pathlib import Path

import tinycss2

ROOT = Path(__file__).resolve().parent.parent


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


def main():
    files = sorted((ROOT / "css").glob("*.css"))
    if not files:
        sys.exit("no css/*.css found")
    bad = 0
    for path in files:
        text = path.read_text()
        nodes = tinycss2.parse_stylesheet(text, skip_comments=True, skip_whitespace=True)
        found = list(errors(nodes, path.name)) + list(balance(text))
        for line, message in found:
            print(f"{path.relative_to(ROOT)}:{line}: {message}")
        bad += len(found)
    if bad:
        sys.exit(f"{bad} CSS parse error(s)")
    print(f"✓ {len(files)} CSS files parse")


if __name__ == "__main__":
    main()
