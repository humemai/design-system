# Changelog

Versions are in `pyproject.toml`. A tag is the bare version (`0.2.0`, no `v`) on the commit that carries it, and a vendored copy records it in its `VERSION.md`.

## 0.2.0 (2026-11-12)

Layout across screen sizes (humemai/design-system#18).

- Added `css/layout.css`: `.hm-container` and `.hm-container--wide` (the page frame), `.hm-measure`, `.hm-cols` (an intrinsic column grid), `.hm-split` (a label and its content, side by side from 1000px), and `.hm-fit` with `.hm-fit__pair` (a container query, one column by default).
- Added tokens: `--hm-page-max`, `--hm-page-max-wide`, `--hm-page-gutter`, `--hm-col-min`, `--hm-split-label-max`, `--hm-split-body-max`.
- Changed the two `px` media queries (`tokens.css`, `components.css`) to rem range queries, `(width >= 62.5rem)` and `(width < 62.5rem)`: the same at the default font size.
- Changed `.hm-card-grid` to `minmax(min(100%, var(--hm-col-min)), 1fr)`: it no longer overflows a 320px window at a 200% root font size. Equal-height rows and the card markup are unchanged.
- Added checks: eight static layout rules in `scripts/check_css.py` and a headless Chrome smoke in `scripts/check_layout.py`, each with a fixture it fails on, both in CI.
- `VERSION.md` of a vendored copy now carries `Version:`.
- README: "Layout across screen sizes", and 2560x1440 and the zoom checks in "Checking pages". Decision and open item (`--hm-text-display`) in `docs/decisions.md`.

A copy is behind by its hash: every consumer needs `scripts/vendor-all.sh`.

## 0.1.0 (2026-11-11)

The state at commit 19edee0, before the layout work: the tokens, `css/base.css`, the card grid, the "?" hint, the table and the badge, `css/mkdocs.css`, the logo and export assets, the checks, and the vendoring scripts. Tagged afterwards.
