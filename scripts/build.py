"""Build every logo, icon and social image from one geometry and two fonts.

    uv run python scripts/build.py

Writes logo/*.svg (the masters) and export/* (what gets uploaded or copied into
a site). Nothing in either folder is edited by hand: change this script, run it,
commit the result.

All text is converted to outlines with the fonts in fonts/, shaped by HarfBuzz
so kerning applies. The old wordmark SVG asked for Montserrat and embedded a
truncated copy of it, so every viewer drew it in whatever bold sans they had.
An outlined wordmark looks the same everywhere and needs no font at all.
"""
import io
from functools import lru_cache
from pathlib import Path

import cairosvg
import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LOGO, EXPORT, FONTS = ROOT / "logo", ROOT / "export", ROOT / "fonts"

OXBLOOD = "#892122"      # --hm-oxblood-700
ROSE = "#E88E8B"         # --hm-oxblood-400, the brand on dark backgrounds
OX_600 = "#B63B39"
OX_200 = "#FDD5D1"
INK = "#1C1716"          # --hm-neutral-900
WHITE = "#FFFFFF"

# ── The mark ────────────────────────────────────────────────────────────────
# The head profile and the five-node graph from the 2024 logo, unchanged in
# shape. Drawn in a 500-unit box; the head's own transform places it there.
HEAD = ("M288.8,0.457C178.31-6.342,85.278,63.166,87.382,176.416l-0.084,10.25l-48.003,84.767"
        "c-2.582,4.567-2.812,10.097-0.613,14.876c2.181,4.78,6.535,8.213,11.682,9.218l29.666,8.188"
        "l9.312,89.896c0.256,8.656,4.107,16.802,10.634,22.51c6.535,5.674,15.166,8.376,23.771,7.412"
        "l23.694,1.892c4.618-0.519,9.254,0.954,12.712,4.056c3.468,3.11,5.445,7.548,5.445,12.2V512"
        "h200.419c0,0,0-33.936,0-47.602c0-13.666,4.712-44.909,13.675-59.206"
        "c32.488-51.948,85.381-79.587,94.301-186.14C482.914,112.515,419.328,8.5,288.8,0.457z")
NODES = [(50, 50), (150, 100), (250, 50), (200, 200), (340, 150)]
EDGES = [(0, 1), (1, 2), (1, 3), (2, 4), (3, 4)]
NODE_R = 25


def _trimmed_edges(r):
    """Edges from circle edge to circle edge, so hollow nodes stay hollow."""
    out = []
    for a, b in EDGES:
        (x1, y1), (x2, y2) = NODES[a], NODES[b]
        dx, dy = x2 - x1, y2 - y1
        d = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / d, dy / d
        out.append((x1 + ux * r, y1 + uy * r, x2 - ux * r, y2 - uy * r))
    return out


def mark_outline(color, head_w=22, graph_w=16):
    """The logo mark: outlined head, hollow nodes. For 32px and up."""
    lines = "".join(f'<line x1="{a:.1f}" y1="{b:.1f}" x2="{c:.1f}" y2="{d:.1f}"/>' for a, b, c, d in _trimmed_edges(NODE_R))
    nodes = "".join(f'<circle cx="{x}" cy="{y}" r="{NODE_R}"/>' for x, y in NODES)
    return (f'<g transform="translate(15,15) scale(0.9)" fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path stroke-width="{head_w}" d="{HEAD}"/>'
            f'<g transform="translate(90,70)" stroke-width="{graph_w}">{lines}{nodes}</g></g>')


def head_filled(fill, graph):
    """Solid head with the graph drawn on it. Reads at 16px where outlines vanish."""
    lines = "".join(f'<line x1="{NODES[a][0]}" y1="{NODES[a][1]}" x2="{NODES[b][0]}" y2="{NODES[b][1]}"/>' for a, b in EDGES)
    nodes = "".join(f'<circle cx="{x}" cy="{y}" r="36"/>' for x, y in NODES)
    return (f'<g transform="translate(15,15) scale(0.9)"><path fill="{fill}" d="{HEAD}"/>'
            f'<g transform="translate(90,70)" stroke="{graph}" stroke-width="28" stroke-linecap="round" fill="none">{lines}</g>'
            f'<g transform="translate(90,70)" fill="{graph}">{nodes}</g></g>')


def tile(rounded=True, bg=OXBLOOD, fg=WHITE):
    """The icon: white head on an oxblood square. Rounded for favicons; square
    for avatars, which every platform crops or rounds itself."""
    rx = ' rx="112"' if rounded else ""
    return (f'<rect width="500" height="500"{rx} fill="{bg}"/>'
            f'<g transform="translate(71,73) scale(0.72)">{head_filled(fg, bg)}</g>')


# ── Text to outlines ────────────────────────────────────────────────────────
FACES = {
    # key: (file, variation axes)
    "word": ("SchibstedGrotesk.ttf", {"wght": 800}),
    "text": ("SchibstedGrotesk.ttf", {"wght": 500}),
    "text-semibold": ("SchibstedGrotesk.ttf", {"wght": 600}),
    "display": ("Newsreader.ttf", {"opsz": 72, "wght": 500}),
}


@lru_cache(maxsize=None)
def _face(key):
    file, axes = FACES[key]
    font = instantiateVariableFont(TTFont(FONTS / file), axes)
    buf = io.BytesIO()
    font.save(buf)
    hb_font = hb.Font(hb.Face(buf.getvalue()))
    return font, hb_font


def text_path(key, text, size, x, baseline, tracking=0.0, anchor="start", bounds=None):
    """Return (svg path data, advance width) for text set at `size` px.

    Pass a list as `bounds` to receive the ink box (xMin, yMin, xMax, yMax) in
    output coordinates. Letters overshoot their advance widths, so a canvas
    sized from advances clips them; the old wordmark's final I sat on the edge.

    `tracking` is in em, applied after each glyph like CSS letter-spacing.
    """
    font, hb_font = _face(key)
    upem = font["head"].unitsPerEm
    scale = size / upem
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf, {"kern": True, "liga": True})
    order, glyphs = font.getGlyphOrder(), font.getGlyphSet()
    track = tracking * upem
    infos, positions = buf.glyph_infos, buf.glyph_positions
    width = sum(p.x_advance + track for p in positions) - track
    if anchor == "end":
        x -= width * scale
    elif anchor == "middle":
        x -= width * scale / 2
    pen, box = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip(".")), BoundsPen(glyphs)
    cursor = 0
    for info, pos in zip(infos, positions):
        m = (scale, 0, 0, -scale, x + (cursor + pos.x_offset) * scale, baseline - pos.y_offset * scale)
        glyphs[order[info.codepoint]].draw(TransformPen(pen, m))
        glyphs[order[info.codepoint]].draw(TransformPen(box, m))
        cursor += pos.x_advance + track
    if bounds is not None:
        bounds[:] = box.bounds
    return pen.getCommands(), width * scale


def cap_height(key, size):
    font, _ = _face(key)
    return font["OS/2"].sCapHeight / font["head"].unitsPerEm * size


# ── Compositions ────────────────────────────────────────────────────────────
WORD = "HumemAI"
WORD_TRACK = -0.02
# Beside an 800-weight wordmark the logo's 22/16 strokes look faint; these
# match the letters' stem weight at lockup scale.
LOCKUP_STROKES = (32, 24)


def svg(w, h, body, title=None):
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{t}{body}</svg>\n')


MARGIN = 4  # units of clear space on every side of a master, so nothing touches the edge


def wordmark(color):
    size = 100
    box = []
    d, _ = text_path("word", WORD, size, 0, 0, WORD_TRACK, bounds=box)
    x0, y0, x1, y1 = box
    w, h = x1 - x0 + 2 * MARGIN, y1 - y0 + 2 * MARGIN
    return svg(round(w), round(h), f'<path fill="{color}" transform="translate({MARGIN - x0:.2f},{MARGIN - y0:.2f})" d="{d}"/>', "HumemAI")


def lockup(color):
    """Mark left, wordmark right, the wordmark's cap height centred on the mark."""
    size = 100
    mark_h = 138                       # mark box is 500 units; drawn at 138px
    gap = 22
    ch = cap_height("word", size)
    baseline = mark_h / 2 + ch / 2 + 4  # +4: the head's visual centre sits low in its box
    box = []
    d, _ = text_path("word", WORD, size, mark_h + gap, baseline, WORD_TRACK, bounds=box)
    width = box[2] + MARGIN
    body = (f'<g transform="scale({mark_h / 500})">{mark_outline(color, *LOCKUP_STROKES)}</g>'
            f'<path fill="{color}" d="{d}"/>')
    return svg(round(width), mark_h, body, "HumemAI")


def lockup_stacked(color):
    size = 100
    mark_h = 300
    box = []
    text_path("word", WORD, size, 0, 0, WORD_TRACK, bounds=box)
    width = max(box[2] - box[0], mark_h) + 2 * MARGIN
    ch = cap_height("word", size)
    height = mark_h + 26 + ch + MARGIN
    d, _ = text_path("word", WORD, size, width / 2, height - MARGIN, WORD_TRACK, anchor="middle")
    body = (f'<g transform="translate({(width - mark_h) / 2:.1f},0) scale({mark_h / 500})">{mark_outline(color, *LOCKUP_STROKES)}</g>'
            f'<path fill="{color}" d="{d}"/>')
    return svg(round(width), round(height), body, "HumemAI")


def motif(x, y, scale, color, width=6):
    """The five-node graph, large, as a quiet background figure."""
    lines = "".join(f'<line x1="{NODES[a][0]}" y1="{NODES[a][1]}" x2="{NODES[b][0]}" y2="{NODES[b][1]}"/>' for a, b in EDGES)
    nodes = "".join(f'<circle cx="{nx}" cy="{ny}" r="18"/>' for nx, ny in NODES)
    return (f'<g transform="translate({x},{y}) scale({scale})" stroke="{color}" stroke-width="{width / scale:.2f}" fill="none">'
            f'{lines}</g><g transform="translate({x},{y}) scale({scale})" fill="{color}">{nodes}</g>')


def card(w, h, headline, sub, lock_h, head_size, pad, motif_spec, head_baseline=None, align="left"):
    """An oxblood card: lockup, one Newsreader headline, one small line."""
    mark = lock_h
    word_size = mark / 1.38
    ch = cap_height("word", word_size)
    if align == "right":
        # measure the lockup, then place it flush right
        _, ww = text_path("word", WORD, word_size, 0, 0, WORD_TRACK)
        lx = w - pad - (mark + mark * 0.16 + ww)
    else:
        lx = pad
    ly = pad
    wd, _ = text_path("word", WORD, word_size, lx + mark + mark * 0.16, ly + mark / 2 + ch / 2 + mark * 0.03, WORD_TRACK)
    anchor = "end" if align == "right" else "start"
    hx = w - pad if align == "right" else pad
    hb_ = head_baseline if head_baseline is not None else h - pad - head_size * 0.9
    hd, _ = text_path("display", headline, head_size, hx, hb_, -0.01, anchor=anchor)
    parts = [f'<rect width="{w}" height="{h}" fill="{OXBLOOD}"/>', motif(*motif_spec),
             f'<g transform="translate({lx},{ly}) scale({mark / 500})">{mark_outline(WHITE, 26, 20)}</g>',
             f'<path fill="{WHITE}" d="{wd}"/>', f'<path fill="{WHITE}" d="{hd}"/>']
    if sub:
        sd, _ = text_path("text-semibold", sub, head_size * 0.36, hx, h - pad, 0.01, anchor=anchor)
        parts.append(f'<path fill="{OX_200}" d="{sd}"/>')
    return svg(w, h, "".join(parts), "HumemAI")


TAGLINE = "Memory systems for agentic AI"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def png(svg_text, out, w, h):
    cairosvg.svg2png(bytestring=svg_text.encode(), write_to=str(out), output_width=w, output_height=h)


def main():
    masters = {
        "mark.svg": svg(500, 500, mark_outline(OXBLOOD), "HumemAI"),
        "mark-dark.svg": svg(500, 500, mark_outline(ROSE), "HumemAI"),
        "mark-white.svg": svg(500, 500, mark_outline(WHITE), "HumemAI"),
        "tile.svg": svg(500, 500, tile(rounded=True), "HumemAI"),
        "avatar.svg": svg(500, 500, tile(rounded=False), "HumemAI"),
        "wordmark.svg": wordmark(OXBLOOD),
        "wordmark-dark.svg": wordmark(ROSE),
        "lockup.svg": lockup(OXBLOOD),
        "lockup-dark.svg": lockup(ROSE),
        "lockup-white.svg": lockup(WHITE),
        "lockup-stacked.svg": lockup_stacked(OXBLOOD),
        "lockup-stacked-dark.svg": lockup_stacked(ROSE),
    }
    for name, text in masters.items():
        write(LOGO / name, text)

    EXPORT.mkdir(exist_ok=True)
    tile_svg, avatar_svg = masters["tile.svg"], masters["avatar.svg"]
    write(EXPORT / "favicon.svg", tile_svg)
    for size in (192, 512):
        png(tile_svg, EXPORT / f"icon-{size}.png", size, size)
    png(avatar_svg, EXPORT / "apple-touch-icon.png", 180, 180)
    png(avatar_svg, EXPORT / "avatar-500.png", 500, 500)
    # favicon.ico: render each size from the vector rather than downscaling one
    # bitmap, so 16px gets its own anti-aliasing.
    frames = []
    for size in (16, 32, 48):
        buf = io.BytesIO()
        cairosvg.svg2png(bytestring=tile_svg.encode(), write_to=buf, output_width=size, output_height=size)
        frames.append(Image.open(io.BytesIO(buf.getvalue())).convert("RGBA"))
    frames[-1].save(EXPORT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=frames[:-1])

    # README lockups at 2x a 40px display height.
    for name in ("lockup", "lockup-dark", "lockup-white"):
        text = masters[f"{name}.svg"]
        w = int(text.split('width="')[1].split('"')[0])
        png(text, EXPORT / f"{name}.png", round(w * 80 / 138), 80)
    for name in ("lockup-stacked", "lockup-stacked-dark"):
        text = masters[f"{name}.svg"]
        w, h = (int(text.split(f'{k}="')[1].split('"')[0]) for k in ("width", "height"))
        png(text, EXPORT / f"{name}.png", round(w * 600 / h), 600)

    cards = {
        # name: (w, h, headline, sub, lockup height, headline size, padding, motif(x, y, scale, colour), baseline, align)
        "og-1200x630": (1200, 630, TAGLINE, "humem.ai", 76, 76, 72, (700, 120, 1.05, OX_600, 7), None, "left"),
        "github-social-1280x640": (1280, 640, TAGLINE, "github.com/humemai", 76, 78, 80, (760, 130, 1.05, OX_600, 7), None, "left"),
        "x-header-1500x500": (1500, 500, TAGLINE, "humem.ai", 62, 64, 90, (130, 70, 0.95, OX_600, 6), 330, "right"),
        "linkedin-banner-1128x191": (1128, 191, TAGLINE, None, 40, 38, 36, (40, -8, 0.46, OX_600, 4), 150, "right"),
    }
    for name, (w, h, head, sub, lock_h, head_size, pad, mspec, base, align) in cards.items():
        text = card(w, h, head, sub, lock_h, head_size, pad, mspec, base, align)
        write(EXPORT / f"{name}.svg", text)
        png(text, EXPORT / f"{name}.png", w, h)

    print(f"wrote {len(masters)} masters to logo/ and exports to export/")


if __name__ == "__main__":
    main()
