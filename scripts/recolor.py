"""Recolour flat illustrations from the 2024 palette to the oxblood palette.

    uv run python scripts/recolor.py <png>... [--out-dir DIR]

The site's illustrations use four colours (docs/design/image-prompts.md in
humem.ai): a warm off-white ground, teal ink, one coral highlight, and a
charcoal for anything rejected. Each pixel is treated as a blend of the ground
and ONE ink: it is projected onto each ground-to-ink line in OKLab, the ink with
the smallest residual wins, and the pixel is redrawn as the same blend of the
ground and that ink's replacement. Anti-aliased edges keep their softness and
slightly-off inks (a generator's #155A73 for #1A5F7A) all land on the exact
brand value. Overwrites in place unless --out-dir is given.
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image

GROUND = "#FAF8F5"  # kept as is: the warm paper the illustrations sit on
MAP = {
    "#1A5F7A": "#892122",  # teal ink       -> oxblood (--hm-oxblood-700)
    "#FF8F70": "#E88E8B",  # coral highlight -> rose, --hm-oxblood-400: apart from the ink by lightness
    "#2A2A2A": "#2E2827",  # charcoal        -> charcoal leaning to hue 25
}


def _lin(rgb):
    rgb = rgb / 255.0
    return np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)


def _to_oklab(rgb):
    r, g, b = np.moveaxis(_lin(rgb), -1, 0)
    l = np.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = np.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = np.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], -1)


def _hex(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=float)


def recolor(img):
    rgba = np.asarray(img.convert("RGBA")).astype(float)
    rgb, alpha = rgba[..., :3], rgba[..., 3:]
    lab = _to_oklab(rgb)
    g_lab = _to_oklab(_hex(GROUND))
    best_res = np.full(rgb.shape[:2], np.inf)
    out = np.empty_like(rgb)
    for old, new in MAP.items():
        d = _to_oklab(_hex(old)) - g_lab
        t = np.clip(((lab - g_lab) @ d) / (d @ d), 0, 1.08)
        res = np.linalg.norm(lab - (g_lab + t[..., None] * d), axis=-1)
        take = res < best_res
        best_res = np.where(take, res, best_res)
        # Blend in sRGB, as the original anti-aliasing was.
        blend = _hex(GROUND) + np.clip(t, 0, 1)[..., None] * (_hex(new) - _hex(GROUND))
        out[take] = blend[take]
    return Image.fromarray(np.concatenate([np.clip(out, 0, 255), alpha], -1).round().astype(np.uint8), "RGBA")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--out-dir", type=Path)
    args = ap.parse_args()
    for f in args.files:
        src = Image.open(f)
        mode = src.mode
        res = recolor(src)
        if "A" not in mode and "transparency" not in src.info:
            res = res.convert("RGB")
        dest = (args.out_dir / f.name) if args.out_dir else f
        dest.parent.mkdir(parents=True, exist_ok=True)
        res.save(dest, optimize=True)
        print(f"recoloured {f} -> {dest}")


if __name__ == "__main__":
    main()
