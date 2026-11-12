# Decisions

Why the HumemAI brand is what it is. Newest decisions go at the end of their section. Dates are when the decision was made.

## Before this repo (state on 2026-09-27)

HumemAI had no single brand colour. Four choices had been made separately:

- the logo: teal `#1A5F7A`
- the website illustrations: the same teal plus a coral highlight (`#FF8A6B`)
- the card placeholders: an orange-and-green gradient (`--card-media-gradient`)
- the site's buttons and links: black (`--accent: #111111`)

The four documentation sites each used a different MkDocs Material palette:

- humemdb: teal and lime
- cypherglot: cyan and orange
- audit-ready-memory: deep orange and amber
- arcadedb: blue and indigo

The logo teal sits at OKLCH hue 229°, in the blue band that most technology brands use. The site used Geist, the create-next-app default font.

The wordmark SVGs asked for Montserrat and embedded it as a base64 font whose data was truncated (`...AAAAY...`). No viewer could load it, so the wordmark always rendered in the viewer's fallback bold sans. The PNG exports show Arial-like letterforms, not Montserrat.

## Colour: oxblood (2026-09-27)

Four candidates were compared on the same page mock, in light and dark, with measured contrast: oxblood (hue 25°), amber (72°), rubine (4°) and moss (128°).

- **Rarity.** Published counts of big-brand logos give blue 33–39%, black 25–28%, red 16–23%, yellow and gold 5–15%, green 5–8% and purple about 1%, with brown and pink the least used. `#892122` is closest to the CSS named colour "brown", the rarest family; people read it as dark red. Moss (dark olive green) is probably rarer still. Rubine was the most common of the four: its nearest named colours include crimson, which appeared in 13% of 15,388 logos in one study.
- **Fit.** Deep red-brown recalls leather bindings, archive boxes and sealing wax, which suits an organization that publishes research on memory.
- **One shade does the work.** At 9.11:1 on white, `#892122` is the logo, links, headings and a button fill with white text. Amber needed two darker shades for text on white, which turned brown.
- **The cost.** Red usually means an error, so danger is a separate burnt orange (below). Dark mode needs the lighter rose `#E88E8B` (8.08:1 on the dark background), which is less distinctive than the oxblood itself.

The ramp is built in OKLCH at hue 25°, with 400 at 22° so the dark-mode brand reads rose rather than salmon. `scripts/check.py` recomputes every hex from the OKLCH value in its comment, so the two cannot drift apart.

### Neutrals lean toward oxblood

The greys have OKLCH chroma of 0.012 or less at hue 25°. A pure grey beside oxblood looks unconsidered; a grey with a slight warm bias belongs to the palette. The difference from pure grey is too small to notice on its own.

### Danger is burnt orange, not red

`#BE4400` (light, 5.23:1 on white) and `#F59569` (dark, 8.75:1). A red error next to an oxblood brand reads as more brand. The hue is 42°, far enough from 25° to separate, and it is always paired with words or an icon.

## Typefaces: Journal (2026-09-27)

Four pairings were compared in real HumemAI content: Journal (Newsreader and Schibsted Grotesk), One grotesk (Schibsted Grotesk only), Book (Literata only) and Paper (Hanken Grotesk and Source Serif 4), with Geist for reference.

- **Newsreader** for headlines. A serif headline reads as research, which is most of what the site publishes: papers, benchmarks and long project pages.
- **Schibsted Grotesk** for body text, tables, buttons and the docs. It handles dense tables well and is rare in technology; it was made for a Norwegian media group.
- **DM Mono** for code. It is a secondary choice and can be swapped without touching anything else.
- **The wordmark** is Schibsted Grotesk 800 at −0.02em, a bold sans like the old logo, so the lockup keeps its shape. Its capital I has small serifs, which is part of the face.

A serif headline with a red accent is close to a popular look (cream background, serif, terracotta). A white background and a much darker red keep it apart.

## Icon: the tile (2026-09-27)

The old logo's outline is 16 units thick in a 500-unit box. At 16px, a browser tab, that is half a pixel, and it disappears. The icon is instead a white filled head on an oxblood square, with the graph drawn in oxblood on the head.

- One icon for every small place: favicon, GitHub, LinkedIn, X, Hugging Face. People learn one shape.
- The square carries its own contrast, so it reads on light tabs, dark tabs and circular crops.
- `tile.svg` has rounded corners for favicons. `avatar.svg` is full-bleed, because every platform rounds or crops avatars itself, and transparent corners would show as white on some of them.
- The outline mark stays the logo at 32px and above: site header, lockups, banners. In lockups its strokes are 32 and 24 units rather than 22 and 16, to match the wordmark's stem weight.

## Contrast, size and spacing (2026-09-27)

- **Contrast:** WCAG AA. 4.5:1 for all text, including large text; 3:1 for icons, control borders and focus rings. `scripts/check.py` checks 25 semantic pairings in each theme.
- **Type size:** 16px body on phones, 17px from 1000px up. Scale ratio 1.25. Nothing below 12px, and 12px is for uppercase labels only.
- **Line length:** prose lines of about 70 to 85 characters, a median above 80 on desktop (changed 2026-10-03, see "Line length" below), body line height 1.65.
- **Spacing:** a 4px grid.
- **Review sizes:** 360×800, 390×844, 768×1024, 984×1092, 1280×720, and 1920×1080 CSS pixels. 1920 is where desktop reviews happen. 984×1092 (an unfolded foldable) was added on 2026-10-02: it is the only size between 920 and 1024, where the website switches layouts.

## Line length (2026-10-03)

The first rule was 60 to 75 characters (`--hm-measure: 68ch`). It is now about 70 to 85, with a median above 80 on desktop, and the 16px and 17px body sizes stay as they are.

- **Why it moved.** `ch` is the width of a "0", and in Schibsted Grotesk that is wider than the average letter, so 68ch holds about 80 characters, not 68. The old range was never what the token produced. The website's 736px column, measured on its longest page, gave a median of 83 to 87 and read well.
- **What others do.** Long-form pages of research-lab sites, measured on 2026-10-03 at a 1916px viewport, one article each: Anthropic 71, DeepMind 70, OpenAI 81, Meta 83, World Labs 85, Google Research 107. Columns are 600 to 720px at 16 to 17.5px. The sites worth copying sit at 70 to 85.
- **The benchmark is World Labs:** a 720px column at 17px, median 85. WCAG 1.4.8 (AAA) puts the ceiling at 80 characters; being a little over it, on a page that is mostly tables and figures, was a choice (humemai/humem.ai#9).
- **The token.** `--hm-measure` stays 68ch for pages that want a cap, and it lands at about 80. Count characters per line on the rendered page; do not trust the `ch` number. Narrowing the website to 62ch (median 71) was tried and not kept.
- **Limits.** Under 60 gets choppy and over 90 loses the next line. Phones are narrower than any of this and are not touched.

## Wide content (2026-10-02)

The prose column is set by the line length, so it stays narrow on every screen. Content that is not prose does not have to:

- **Data tables** are as wide as their columns need, never narrower than the prose column and never wider than the screen less the page gutters, centred on the column. Holding them to the prose column made most of a benchmark page's tables scroll sideways while half a 1920 screen stayed empty. A limit at the page frame (the website's 1180px) still left a third of them scrolling at every desktop size, so the limit is the screen.
- **Table headers** wrap when the table is out of room, never inside a hyphenated word, and a direction arrow stays with the word before it.
- **Figures** stay in the prose column. An image scales instead of scrolling, so a wider box only makes it bigger; a figure gets more width only if it is drawn wide.
- Captions and notes stay in the prose column with the paragraphs.

The website implements this in humemai/humem.ai#10 and records the numbers in its `docs/design/layout-widths.md`.

## Card grid (2026-11-06)

`css/components.css` holds the card grid that docs.humem.ai wrote inline: `.hm-card-grid` and `.hm-card`. Its rows are equal height (`grid-auto-rows: 1fr`). The hub's first version let each row size to its own cards, so the last row, one short card, was 85 px shorter than the rows above (217 px against 302 px at 1920 wide). Widths were always equal, which is why only the heights looked wrong. A pattern two pages need goes here first and is vendored, like the colours.

## Behaviour section (2026-11-06)

The README's Behaviour section copies the structure of Stateloop's design-system README (short imperative rules about how a page acts, each with how it is checked), not its look or its wording. The rules are written in HumemAI's own tokens and names. Two points are new here and not yet in any script: the 44px touch-target rule at 999px and narrower, and the filled `--hm-danger` confirm button. The section says plainly that only the focus and danger contrast pairings are checked by `scripts/check.py` today, and that the rest are conventions measured on the rendered page. Add a script check when a rule is broken in practice, as with the card grid.

## Hint component (2026-11-11)

`css/components.css` and `js/hint.js` hold the "?" hint: `.hm-hint` and `.hm-hint__bubble`, `bindHints`, `termHint` and `termHintElement` (humemai/design-system#12). The Humem Tower needs it for its lane names, state words and column heads ("Est.", "Starts after", "Done in", "Started"), and a native `title` tooltip never shows on a touch screen and cannot be reached by keyboard. A pattern a page needs goes here first and is vendored, like the colours and the card grid.

The structure is mirrored from Stateloop's design system (its `.stl-hint` and `js/hint.js`, the rule of 2026-11-06, Stateloop design-system #334 and #181): the same Popover API behaviour, the same markup, the same rules for when to use it (never `title` alone, ONE legend hint in a list header, 1 sentence under about 140 characters, anything needed to act stays visible). The look is not: the hover, focus and open state are oxblood (rose in dark mode) where Stateloop's turn to the text colour, the border is `--hm-border-control` (3:1 on every page surface) where Stateloop's is a softer line, and the bubble has rounded corners. The tokens are HumemAI's own (`--hm-*`).

Three semantic tokens are new for it: `--hm-surface-raised` (white in light, `--hm-neutral-800` in dark, so a bubble reads as lifted in both), `--hm-shadow-md`, and the two sizes `--hm-tap-min` (24px) and `--hm-tap-comfort` (44px). `scripts/check.py` checks the pairings the hint uses in both themes. `js/` is part of the vendored copy and of its hash, so `verify.sh` covers it. The JS is a plain ES module with no dependency; CI parses it and runs `scripts/test-hint.mjs`.

## Port from the Stateloop audit (2026-11-11)

An audit of Stateloop's design system against this one (humemai/design-system#14) ranked what to carry over. Six items went in, all in HumemAI tokens and none in Stateloop's look; the rest is listed below as later or never so it is not proposed twice.

- **`css/base.css`**: the `:focus-visible` ring, `.hm-skip` and one reduced-motion block. The ring was written twice (the Tower's stylesheet and the website's `globals.css`). The skip link is a HumemAI original, not a Stateloop port: Stateloop's design system has none, the Tower has one, the website has none. The website had no `prefers-reduced-motion` rule in 25 stylesheets against 18 `transition:` declarations. The skip link is fixed with `z-index: 100`, above the website's sticky header (40), and `--hm-sticky-offset` lets a page keep jumps and focus scrolls clear of its header. Body and link rules stay out: the Tower underlines links and the website does not.
- **`--hm-control-h`**: 44px, 36px from 1000px, the Tower's `--tw-control-min` under a system name. The website has five heights for one job (2.6, 2.7, 2.8, 2.9 and 3rem). The tap rule and its two numbers are written in the README's Behaviour section: 24px is the AA floor, 44px the comfortable target. No script yet; the audit's tap-size check is 307 lines and needs a locked Playwright project, and the website's own six-device precheck is the place for a 25-line assertion.
- **`.hm-table-scroll`, `.hm-table`, `.hm-num`**: from the Tower's tables. Numeric cells are DM Mono, not `tabular-nums` on Schibsted Grotesk: the Tower measured the tabular figures widening the punctuation, and the website's benchmark tables use `tabular-nums`, so the two consumers disagreed on one cell. The wrapper's `role`, `tabindex` and `aria-label` are the page's to supply; the system names the rule. The Tower's column roles (`data-role` key, long, short) and the website's wide-table layout stay private.
- **`.hm-badge`**: brand, danger and tint, because the brand has one voice and one warning (Stateloop's variants lean on accent-2, warning and success hues). The state-to-symbol map stays in the app. No new contrast pairing: each variant uses a pairing `scripts/check.py` already lists.
- **`AGENTS.md` and `CLAUDE.md`** for this repository: the checks to run, `vendor-all.sh --check` after a merge, no hand edits to `logo/` or `export/`, and Stateloop's fail-first rule (every new check ships with a fixture it fails on). Not copied: its tiered prechecks, which answer a CI budget this public repository does not have.
- **`vendor-all.sh` covers the Tower** (`../tae898/control-plane`), so five copies are checked in one run. A `CONSUMERS` entry may be a path from this repository's parent. With it, each consumer calls its vendored `verify.sh` in its own checks: a guard nobody runs is not a guard (Stateloop runs a consumer check in every repository for the same reason; here it is one line per repository).

Later, until a consumer is hurt: a z-index scale (adopt with the control height if the website is touched), a shadow scale, a breakpoint set (the website uses 560, 640, 720, 920, 1024 and 1200, so a check would be red on day one), buttons and form controls (needs the pill or square decision first), one glossary table, a static callout, a hex lint, one device list. Never, for HumemAI: Stateloop's empty state, toolbar, tabs, dialog and product components, its rendered audit suite, and its layers and themes.

## Layout across screen sizes (2026-11-12)

The system had tokens and components but no layout rules, so the Humem Tower and the sites met widths differently (humemai/design-system#18): humem.ai caps its frame at 1180px with a 1rem gutter under 720px and 1.5rem from 720px; the Tower's `.container` is 87.5rem on `main` and 100rem in its open tables pull request (control-plane#176, with `max(100rem, 90vw)` on table pages) with 1rem and 1.5rem gutters (the step at 1000px); MkDocs Material's own grid is 61rem. Their media queries sit at 560, 640, 720, 920, 1024 and 1200 (site) and 640 and 1000 (Tower). The README's "Layout across screen sizes" has the rules; this entry has the reasons. Every figure was read on the page named.

**What the evidence says**

- Every public system read caps and centres the page container, and extra width becomes margin. Atlassian: 864 (reading), 1296 (default), fluid on request, and it advises against fluid dashboards. Primer: 768, 1012, 1280 (default), full. Polaris: small, base, large. Only Material (1600), Atlassian (1768) and Carbon (max 1584) define anything above 1440, and none gives 2560 its own rule. Sources: atlassian.design/foundations/grid, Primer's `PageLayout.module.css`, shopify.dev Page, m3.material.io breakpoints, carbondesignsystem.com 2x-grid.
- Phone to tablet is 600 to 770 and desktop starts at 1000 to 1056 (Material 600, Atlassian 768 and 1024, Primer 768 and 1012, Polaris 768 and 1040, Carbon 672 and 1056, USWDS 640 and 1024, GOV.UK 641 and 769). The existing 1000px step sits in the band, so it stays, and 600 is the new lower step.
- Reading width is its own narrower container or column share, not the page width: Atlassian 864, GOV.UK two thirds with "no more than 75 characters", Material 40 to 60. The settled 70 to 85 range and `--hm-measure` stay (see "Line length"); those figures are lower and are not proposals.
- Columns place blocks and prose stays one column: Primer panes stack below 768, Polaris hides the aside unless the page is base width, Material goes 1, 2, then up to 3 panes in app shells. No page read has a rule for multi-column body text.
- Attention: NN/g eyetracking at 1024x768 found 69% of viewing time on the left half and 1% beyond the first 1,024px; at 1920x1080 (120 participants) 57% above the fold. Spare width is better spent as margin or on tables than on more prose. Old screens, and no study of ultrawide pages exists in what I read. 2560x1440 is 3.79% of desktop visits in one StatCounter chart (top six rows only), and OS scaling can make a 2560 screen about 1707 CSS px wide.
- Platform (headless Chrome 157, MDN browser-compat-data of 2026-11-11, WCAG 2.2): `px` media queries ignore the reader's default font size and `rem` ones follow it (`(width >= 62.5rem)` still matched at 1280 under `html { font-size: 200% }`); `.hm-card-grid`'s bare `minmax(16.25rem, 1fr)` overflows a 320px window at a 200% root size (552px) and `min(100%, 16.25rem)` does not (320px); multi-column with a constrained height adds columns sideways (`scrollWidth` 3709 for a 12rem box at 1000px; css-multicol-1 section 8); container queries are Baseline widely since 2025-08-14, and a container on a flex item or an inline-block is 0px wide while an `@container` rule does not style its own container; WCAG 1.4.10 excepts data tables, so a table in its own scroller is compliant; F94 says viewport units cannot be resized by zooming.

**Decided**

- Four size classes in `rem` range syntax (under 600, 600 to 999, 1000 to 1599, 1600 and up). The two px queries (`min-width: 1000px` in `tokens.css`, `max-width: 999px` in `components.css`) became `(width >= 62.5rem)` and `(width < 62.5rem)`: the same at the default font size (`check_layout.py` checks the control height, the body size, the hint's hit area and the split at 599, 600, 999, 1000, 1599 and 1600px), with no gap at 999.5px, and they follow a reader who raised the default size.
- Page container: `--hm-page-max` 73.75rem (1180px, humem.ai's frame, which is also what the site shows at 1440 and 2560) and `--hm-page-max-wide` 97rem. The gutter is outside the cap, as on the site, so `.hm-container` is `calc(max + 2 * gutter)` with padding. 97rem is not a round number: with the Tower's 1.5rem gutters it is the Tower's 100rem frame exactly, so the Tower adopts the wide variant with no change at any width (2304px at 2560, which is `max(100rem, 90vw)`). The wide variant grows to 90% because "Wide content" (2026-10-02) already settled that a data table is limited by the screen, not by the frame. The 90% is of the parent, where the Tower's was 90vw: the same unless a classic scrollbar is showing.
- The gutter is `--hm-space-4` under 600px and `--hm-space-6` from 600px. humem.ai steps at 720px and the Tower at 1000px, so each differs from it by 0.5rem a side in part of 600 to 999px (the site at 600 to 719px, the Tower at 600 to 999px); both match at every review size from 1280px up, and the site matches at 768 and 984 too. A consumer that needs its own step sets `--hm-page-gutter` itself.
- `.hm-cols` and `.hm-card-grid` use `repeat(auto-fit, minmax(min(100%, var(--hm-col-min)), 1fr))`. The docs hub (`humemai-docs/index.html`, its real markup) renders identically before and after at 320, 360, 390, 768, 984, 1280, 1440, 1920 and 2560px at the default root size (every card rect equal). Equal-height rows, no fixed heights and the card markup are unchanged.
- `.hm-split` follows the site's "Why memory" sections (`.sectionRoot` in `section-blocks.module.css`: a `1fr` label column and a `minmax(18rem, 30rem)` content column, a label capped at 34rem, a 1rem gap, `align-items: start`), with the content column also capped at the measure. It splits from 1000px as decided. The site splits from 720px, with a 22rem column to 1023px, so the site changes at 720 to 999px if it adopts `.hm-split`, and decides that then.
- Container queries only through `.hm-fit` and `.hm-fit__pair`, with a one-column base. `.hm-card` itself is not a container: it is often a grid item, and a container cannot style itself, so a card that changes with its width goes inside `.hm-fit`. I did not add a note component: the Tower's notes are the Tower's.
- No `column-count` or `columns` anywhere, and `column-width` only in `rem` and without a height. No study of short text in columns exists in what I read; WCAG 1.4.8 and NN/g both name the reading-order cost, and a 3 to 10 line block at 80 characters is 1 to 5 lines of 40 characters.
- Tables are unchanged. The README's "Checking pages" gains 2560x1440 and two zoom checks (320 CSS px wide, a 200% root font size).
- Checks: `scripts/check_css.py` has eight static rules (`media-px`, `media-range`, `column`, `column-height`, `autofit`, `container`, `container-self`, `font-viewport`), each with a fixture in `scripts/fixtures/css/` it fails on (`--self-test`); `scripts/check_layout.py` is a headless Chrome smoke of nine measurements, each with a bad variant of `scripts/fixtures/layout/page.html` it fails on (`--self-test`). CI runs both. Roots are 100% and 200%: at 300% a single word of a card no longer fits 320px whatever the grid does, and WCAG 1.4.4 asks for 200%.
- Versions: `pyproject.toml` already held 0.1.0 and stays the one source. `vendor-into.sh` writes `Version:` into a copy's `VERSION.md` beside the commit and the hash. 0.1.0 is tagged on 19edee0 (the state before this change) and 0.2.0 on this change's merge commit; tags are bare versions. A copy is still behind or not by its hash alone, so a bump that changes no file does not mark every copy stale.

**Open item: `--hm-text-display`**

`clamp(2.4375rem, 6vw, 4.75rem)` is a WCAG F94 risk: at a 1280px window it is 76px at a 100% root size and 78px at 200%, so the text does not reach 200% (1.03x). I tried adding a rem term. `clamp(2.4375rem, 0.2rem + 5.7vw, 4.75rem)` stays within 1px of today at 390, 768, 1280, 1440, 1920 and 2560 (39, 46.98 against 46.08, then 76 four times), but at 1280 and a 200% root it is 79.36px, no better. The slope between 650 and 1267px has to be 6vw to hold today's sizes, and a vw term does not scale with the root size, so no linear form does both; it would need the window width as a count of rems, which I did not find a plain `calc` for. So the token is left as it is, and `check_css.py` allows only this name to carry a viewport unit. No consumer reads `--hm-text-display` (searched the site, the docs sites and the Tower on 2026-11-12), so changing it later breaks nothing: decide it with the owner (stepped sizes in rem, or drop the token).

**What the research could not settle**

No study of short text flowed into columns; Carbon states no maximum page width on the page read; Material's canonical-layout pages gave 404 at the URLs tried; GOV.UK's page says 1020 and its source 960, unresolved; Stripe docs and Linear were not measured; the Braganza et al. (2009) PDF returned 403; Primer's docs give no pixels (they come from its source); the line-length experiments are old and small (1998 to 2006) and nobody tested Schibsted Grotesk or 17px.

**Not yet checked, later**

From the platform findings: text spacing (WCAG 1.4.12, line height 1.5 and the rest, nothing clipped), target sizes at 320px and 1280px (and 44px under `(any-pointer: coarse)`; `any-pointer` is the better gate than width), a focused control not covered by a sticky header (2.4.11), `text-wrap: wrap` forced in the overflow tests, forced-colours borders, `text-wrap: balance` for headings, `svh` for a hero, subgrid for card internals, and a computed-size test that no text token shrinks between 1280 and 640 beyond the 17px to 16px step.

## Words: tagline and descriptor (2026-09-27)

- **Tagline:** "Machines with human-like memory". Taewoon's line, first on the LinkedIn page. It's short, and it ties to the name (human + memory) and to the mark (a head holding a graph). On banners and cards it's the headline, in Newsreader.
- **Descriptor:** "Open source memory systems for agentic AI". It says what HumemAI actually makes. It's the GitHub organization description, and the smaller second line under the tagline.

Wherever there's room for both, use both: the tagline alone is memorable but vague.

## How much system (2026-09-27)

HumemAI is one person's organization, so this is deliberately smaller than a company design system: tokens, one theme file for the docs, assets, and one checker. There are no shared components. The website keeps its own components and reads the tokens. Add a rule here when a real inconsistency shows up, not before.
