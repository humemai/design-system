# HumemAI design system

The HumemAI brand in one place: the colour, the typefaces, the logo and icon, and the rules that keep them readable. Everything HumemAI publishes takes its brand from here: the website [humem.ai](https://humem.ai), the documentation at [docs.humem.ai](https://docs.humem.ai), the GitHub organization and the social accounts.

The reasons behind each choice are in [docs/decisions.md](docs/decisions.md). Where the brand has been rolled out, platform by platform, is in [docs/rollout-2026-09.md](docs/rollout-2026-09.md).

## The short version

| | |
|---|---|
| Brand colour | Oxblood `#892122` on light backgrounds, rose `#E88E8B` on dark |
| Headlines | [Newsreader](https://fonts.google.com/specimen/Newsreader), weight 500 |
| Everything else | [Schibsted Grotesk](https://fonts.google.com/specimen/Schibsted+Grotesk), 400 to 700 |
| Code | [DM Mono](https://fonts.google.com/specimen/DM+Mono) |
| Wordmark | Schibsted Grotesk 800, converted to outlines |
| Icon | White head on an oxblood square (`logo/tile.svg`) |
| Contrast | WCAG AA: 4.5:1 for all text, 3:1 for icons, control borders and focus rings |

## What is in it

```
css/tokens.css      colour ramps, neutrals, type, spacing, and the semantic layer for light and dark
css/mkdocs.css      the theme for MkDocs Material documentation sites
assets/fonts.html   the Google Fonts block for plain HTML pages
logo/               SVG masters: mark, tile, avatar, wordmark, lockups (light, dark, white)
export/             PNG, ICO and social images, generated from logo/ and the fonts
fonts/              the two brand fonts (SIL Open Font License), used to outline text
scripts/build.py    generates logo/ and export/
scripts/check.py    checks the tokens, every contrast pairing, and the export sizes
scripts/vendor-into.sh  copies the system into a site, with a pinned VERSION.md
scripts/recolor.py  converts an illustration drawn in the 2024 teal and coral palette to oxblood and rose
```

Nothing in `logo/` or `export/` is edited by hand. Change `scripts/build.py`, then:

```bash
uv sync
uv run python scripts/build.py
uv run python scripts/check.py
```

## Tokens

Read the semantic names; the ramps exist for the semantic layer to point at.

- **Surfaces:** `--hm-bg`, `--hm-surface`, `--hm-surface-muted`, `--hm-surface-sunken`
- **Text:** `--hm-text`, `--hm-text-muted`, `--hm-text-subtle` (on `--hm-bg` and `--hm-surface` only)
- **Brand:** `--hm-brand`, `--hm-brand-hover`, `--hm-on-brand`, `--hm-link`, `--hm-link-hover`, `--hm-tint`, `--hm-tint-text`
- **Lines:** `--hm-border`, `--hm-border-strong`, `--hm-border-control` (inputs), `--hm-focus`
- **State:** `--hm-danger`, a burnt orange, always with words or an icon
- **Type:** `--hm-font-display`, `--hm-font-text`, `--hm-font-mono`; sizes `--hm-text-xs` (12, labels only) to `--hm-text-4xl` on a 1.25 ratio, and `--hm-text-base` is 16px on phones and 17px from 1000px up
- **Space:** a 4px grid, `--hm-space-1` (4px) to `--hm-space-24` (96px)

Dark mode follows the operating system. `data-theme="light"` or `"dark"` on `<html>` pins it.

## Using it

Vendor a copy from a clean checkout:

```bash
scripts/vendor-into.sh ../humem.ai/public/brand        # the website
scripts/vendor-into.sh ../humemdb/docs/brand           # an MkDocs project
```

The copy carries `verify.sh`, which fails if a vendored file was edited in place. `css/mkdocs.css` lists the `mkdocs.yml` settings that go with it.

## Where each asset goes

| File | Where |
|---|---|
| `export/favicon.svg`, `favicon.ico`, `apple-touch-icon.png` | every site's `<head>` |
| `export/avatar-500.png` | GitHub organization, Hugging Face, LinkedIn page logo, X |
| `export/og-1200x630.png` | the site's default social card |
| `export/github-social-1280x640.png` | each repository's social preview (Settings → General) |
| `export/linkedin-banner-1128x191.png` | LinkedIn page cover |
| `export/x-header-1500x500.png` | X header |
| `export/youtube-banner-2560x1440.png` | YouTube channel banner (content inside the 1546×423 area every device shows) |
| `export/substack-header-2688x512.png` | Substack profile header |
| `export/avatar-1024.png` | platforms that want 1000px or more (Medium, Substack) |
| `export/lockup.png`, `lockup-dark.png` | README headers, with a `<picture>` element so dark mode gets the rose version |
| `export/qr-humem-ai.svg`, `qr-humem-ai.png` | slides, posters and cards: a QR code for https://humem.ai in oxblood |

## Checking pages

Review pages at these sizes (CSS pixels): 360×800 and 390×844 (phones), 768×1024 (tablet), 984×1092 (unfolded foldable), 1280×720 (laptop), and 1920×1080 (desktop, the main review size). Prose stays at the measure on every screen; data tables may be wider (see `docs/decisions.md`, Wide content).

## Licence

The HumemAI name, logo and icon identify the organization; don't use them for other projects. The fonts in `fonts/` are under the SIL Open Font License (see the `*-OFL.txt` files).
