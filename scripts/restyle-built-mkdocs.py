"""Give already-built MkDocs Material sites the HumemAI theme, in place.

    uv run python scripts/restyle-built-mkdocs.py <built site dir>...

For docs versions that were published before the design system existed (the
mike versions in humemai-docs). Rebuilding old versions means checking out old
code with its old dependencies; this edits the built pages instead, and only
their theme:

- the palette attributes become `custom`, which hands colour to mkdocs.css
- Roboto and Roboto Mono become Schibsted Grotesk and DM Mono
- /brand/css/mkdocs.css is linked before the site's own extra.css, as the
  source mkdocs.yml files now do
- the favicon link points at the tile, and every bundled favicon.png is the tile
- the header and drawer logo (Material's default book icon) becomes the white mark
- humemdb's old extra.css hero box moves from teal and lime to oxblood and rose

Page text is untouched. Links are root-absolute (/brand/...), so the site must
be served with the design system vendored at /brand, as docs.humem.ai is.
Running it twice changes nothing the second time.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TILE_PNG = ROOT / "export" / "icon-192.png"

FONTS_OLD = re.compile(r'https://fonts\.googleapis\.com/css\?family=Roboto[^"]*')
FONTS_NEW = ("https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500"
             "&family=Schibsted+Grotesk:wght@400..700&display=fallback")
FONT_VARS = re.compile(r'<style>:root\{--md-text-font:"[^"]*";--md-code-font:"[^"]*"\}</style>')
FONT_VARS_NEW = '<style>:root{--md-text-font:"Schibsted Grotesk";--md-code-font:"DM Mono"}</style>'
PALETTE = re.compile(r'data-md-color-(primary|accent)="(?!custom")[^"]*"')
ICON = re.compile(r'<link rel="icon" href="[^"]*favicon\.png">')
ICON_NEW = ('<link rel="icon" href="/brand/export/favicon.svg" type="image/svg+xml">'
            '<link rel="icon" href="/brand/export/favicon.ico" sizes="48x48">')
LOGO = re.compile(r'(<a [^>]*class="md-(?:header|nav)__button md-logo"[^>]*>)\s*<svg .*?</svg>', re.S)
LOGO_NEW = r'\1<img src="/brand/logo/mark-white.svg" alt="logo">'
BRAND_CSS = '<link rel="stylesheet" href="/brand/css/mkdocs.css">'
HERO_OLD = {
    "rgba(13, 148, 136, 0.14), rgba(132, 204, 22, 0.16)": "rgba(137, 33, 34, 0.07), rgba(232, 142, 139, 0.16)",
    "rgba(13, 148, 136, 0.28)": "rgba(137, 33, 34, 0.24)",
}


def restyle_html(s):
    if 'class="md-header' not in s:  # mike's redirect pages, not Material pages
        return s
    s = FONTS_OLD.sub(FONTS_NEW, s)
    s = FONT_VARS.sub(FONT_VARS_NEW, s)
    s = PALETTE.sub(lambda m: f'data-md-color-{m.group(1)}="custom"', s)
    s = ICON.sub(ICON_NEW, s)
    s = LOGO.sub(LOGO_NEW, s)
    if BRAND_CSS not in s:
        # Before the site's own stylesheets if it has any, else at the end of
        # <head>: brand first, project overrides after, as in mkdocs.yml.
        m = re.search(r'<link rel="stylesheet" href="[^"]*stylesheets/extra\.css">', s)
        at = m.start() if m else s.index("</head>")
        s = s[:at] + BRAND_CSS + "\n" + s[at:]
    return s


def main():
    changed = 0
    for site in map(Path, sys.argv[1:]):
        for f in site.rglob("*.html"):
            old = f.read_text()
            new = restyle_html(old)
            if new != old:
                f.write_text(new)
                changed += 1
        for f in site.rglob("assets/images/favicon.png"):
            if f.read_bytes() != TILE_PNG.read_bytes():
                shutil.copyfile(TILE_PNG, f)
                changed += 1
        for f in site.rglob("stylesheets/extra.css"):
            old = f.read_text()
            new = old
            for a, b in HERO_OLD.items():
                new = new.replace(a, b)
            if new != old:
                f.write_text(new)
                changed += 1
    print(f"restyled {changed} files")


if __name__ == "__main__":
    main()
