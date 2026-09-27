"""Check the design system against its own rules.

    uv run python scripts/check.py

1. Every primitive whose comment gives an OKLCH value still converts to the hex
   written beside it, so the comment and the colour cannot drift apart.
2. The two dark blocks (OS preference, and data-theme="dark") are identical.
3. Every semantic pairing the system uses passes WCAG AA in both themes:
   4.5:1 for text, 3:1 for icons, control borders and focus rings.
4. The generated assets exist at the sizes each platform asks for.

Exits non-zero on the first category that fails, after printing all of it.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from oklch import contrast, oklch_to_hex  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / "css" / "tokens.css").read_text()

TEXT, NON_TEXT = 4.5, 3.0
PAIRS = [
    # (foreground, background, minimum)
    ("text", "bg", TEXT), ("text", "surface", TEXT), ("text", "surface-muted", TEXT), ("text", "surface-sunken", TEXT),
    ("text-muted", "bg", TEXT), ("text-muted", "surface", TEXT), ("text-muted", "surface-muted", TEXT), ("text-muted", "surface-sunken", TEXT),
    ("text-subtle", "bg", TEXT), ("text-subtle", "surface", TEXT),
    ("brand", "bg", TEXT), ("brand", "surface", TEXT),
    ("link", "bg", TEXT), ("link", "surface", TEXT), ("link", "surface-muted", TEXT),
    ("link-hover", "bg", TEXT),
    ("on-brand", "brand", TEXT), ("on-brand", "brand-hover", TEXT),
    ("tint-text", "tint", TEXT),
    ("danger", "bg", TEXT), ("danger", "surface", TEXT),
    ("focus", "bg", NON_TEXT), ("focus", "surface", NON_TEXT),
    ("border-control", "bg", NON_TEXT), ("border-control", "surface", NON_TEXT),
]

ASSETS = {
    "export/favicon.ico": None,
    "export/favicon.svg": None,
    "export/icon-192.png": (192, 192),
    "export/icon-512.png": (512, 512),
    "export/apple-touch-icon.png": (180, 180),
    "export/avatar-500.png": (500, 500),
    "export/og-1200x630.png": (1200, 630),
    "export/github-social-1280x640.png": (1280, 640),
    "export/linkedin-banner-1128x191.png": (1128, 191),
    "export/x-header-1500x500.png": (1500, 500),
}


def block(selector_regex):
    m = re.search(selector_regex + r"\s*\{(.*?)\n\s*\}", CSS, re.S | re.M)
    if not m:
        sys.exit(f"tokens.css: no block matching {selector_regex}")
    return dict(re.findall(r"--hm-([\w-]+):\s*([^;]+);", m.group(1)))


def main():
    failures = 0
    root = block(r"^:root")
    prims = {k: v.strip() for k, v in root.items() if v.strip().startswith("#")}

    # 1. OKLCH comments match their hex.
    for name, L, C, h in re.findall(r"--hm-([\w-]+):\s*#[0-9A-Fa-f]{6};\s*/\*\s*oklch\(([\d.]+) ([\d.]+) ([\d.]+)\)", CSS):
        want, _ = oklch_to_hex(float(L), float(C), float(h))
        if want.upper() != prims[name].upper():
            print(f"✗ --hm-{name} is {prims[name]} but its comment oklch({L} {C} {h}) is {want}")
            failures += 1

    # 2. The two dark blocks agree.
    dark_os = block(r":root:not\(\[data-theme=\"light\"\]\)")
    dark_pin = block(r"^:root\[data-theme=\"dark\"\]")
    if dark_os != dark_pin:
        diff = sorted(set(dark_os.items()) ^ set(dark_pin.items()))
        print(f"✗ the two dark blocks differ: {diff}")
        failures += 1

    # 3. Contrast.
    def resolve(theme, name):
        v = theme.get(name, root.get(name)).strip()
        while v.startswith("var("):
            v = root[re.match(r"var\(--hm-([\w-]+)\)", v).group(1)].strip()
        return v

    for label, theme in (("light", root), ("dark", {**root, **dark_os})):
        for fg, bg, minimum in PAIRS:
            a, b = resolve(theme, fg), resolve(theme, bg)
            r = contrast(a, b)
            ok = r >= minimum
            failures += not ok
            if not ok or "-v" in sys.argv:
                print(f"{'✓' if ok else '✗'} {label:5} {fg:15} on {bg:15} {a} / {b}  {r:5.2f}:1  (min {minimum})")

    # 4. Assets.
    try:
        from PIL import Image
    except ImportError:
        Image = None
    for rel, size in ASSETS.items():
        p = ROOT / rel
        if not p.exists():
            print(f"✗ missing {rel} (run scripts/build.py)")
            failures += 1
        elif size and Image and Image.open(p).size != size:
            print(f"✗ {rel} is {Image.open(p).size}, expected {size}")
            failures += 1

    if failures:
        sys.exit(f"{failures} check(s) failed")
    print(f"✓ tokens, {len(PAIRS) * 2} contrast pairs and {len(ASSETS)} assets pass")


if __name__ == "__main__":
    main()
