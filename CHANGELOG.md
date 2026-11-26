# Changelog

Versions are in `pyproject.toml`. A tag is the bare version (`0.2.0`, no `v`) on the commit that carries it, and a vendored copy records it in its `VERSION.md`.

## 0.3.0 (2026-11-27)

Tabs, label and value rows, and the static card, promoted from the Humem Tower (humemai/design-system#16, #17).

- Added `.hm-tabs` and `.hm-tabs__count` (`css/components.css`): a named `nav` of links, the open one marked with `aria-current="page"`.
- Added `.hm-kv`: a definition list as label and value rows, the label column `min(8.5rem, 40%)`.
- Added `.hm-card--static`: a card that is not a link, with no hover lift and rows sized to their content.
- Added checks: `tabs`, `key-values` and `static-card` in `scripts/check_layout.py`, each with a bad variant.
- README: "Tabs" and "Label and value rows". Reasons in `docs/decisions.md`.
- No token and no existing rule changed.

A copy is behind by its hash: every consumer needs `scripts/vendor-all.sh`.

## 0.2.1 (2026-11-17)

The scroll cue on the table scroller (humem-ops#348, U1). This release also carries the two docs-only entries below it, which had no version of their own.

- Changed `.hm-table-scroll` (`css/components.css`): while more of the table is to the right, the scroller shows a shadow on its right edge. Pure CSS: the `background` shorthand becomes `background-color` plus two background layers (a surface-coloured cover with `background-attachment: local`, and the shadow with `scroll`), no markup, class or token is new. The shadow is `--hm-text` at 22%, so it reads in light and dark. A page that sets the `background` shorthand on the scroller removes it. A header cell has its own fill and covers the shadow, so it shows beside the body rows.
- Added a check: `scroll-cue` in `scripts/check_layout.py` reads one pixel of a screenshot at the right edge of the scroller, at 320, 360 and 2560px, in light and dark: a shadow at scrollLeft 0 when the table scrolls, none at the far end and none when nothing scrolls. Its bad variant removes the background image.
- README: a "Scroll cue" bullet under Tables. Reason and rejected options in `docs/decisions.md`.
- README: "Grouping" (humemai/design-system#26): a hairline separates groups, not rows; a figure that explains a row lives in that row's value column; less space inside a thing than between things. One bullet under Tables (the answering columns first) and two additions to Data display (rule 4: a non-breaking space between number and unit; rule 6: where an identifier may break and how a long title is cut). Docs only: nothing under `css/`, `js/` or `scripts/`.
- README: "Data display" (humemai/design-system#20): how numbers, units, durations, dates, identifiers and empty values are shown, and the slashed zero of DM Mono. Docs only: nothing under `css/`, `js/`, `logo/`, `assets/` or `export/` changed, so a vendored copy's hash and `VERSION.md` stay as they are and no consumer needs `scripts/vendor-all.sh` for it. Released in 0.2.1.

A copy is behind by its hash: every consumer needs `scripts/vendor-all.sh`.

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
