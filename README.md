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
css/base.css        opt-in base rules: the focus ring, the skip link (.hm-skip) and one reduced-motion rule
css/layout.css      opt-in layout: the page container (and its wide variant), the measure, the column grid, the split and the container-query box
css/components.css  shared components: the card grid (equal-height rows) and its card, the "?" hint, the table and its scroller, and the badge
js/hint.js          the hint's behaviour (placing the bubble, hover) and termHint for a glossary; a plain ES module, no dependency
assets/fonts.html   the Google Fonts block for plain HTML pages
logo/               SVG masters: mark, tile, avatar, wordmark, lockups (light, dark, white)
export/             PNG, ICO and social images, generated from logo/ and the fonts
fonts/              the two brand fonts (SIL Open Font License), used to outline text
scripts/build.py    generates logo/ and export/
scripts/check.py    checks the tokens, every contrast pairing, and the export sizes
scripts/check_css.py  checks that every css/*.css file parses, its brackets balance, and the layout rules hold (no px in a media query, no multi-column prose, a guarded auto-fit, a block container); --self-test runs its fixtures
scripts/check_layout.py  measures the layout classes in headless Chrome at several widths and root font sizes; --self-test runs its bad variants
scripts/fixtures/   the fixtures the checks fail on: css/bad-*.css, and layout/page.html with its bad variants in the script
scripts/test-hint.mjs  checks that js/hint.js parses as a module and that termHint gives the documented markup
scripts/vendor-into.sh  copies the system (css, js, logo, assets, icons) into a site, with a pinned VERSION.md (version, commit, hash)
scripts/vendor-all.sh   vendors into every consumer at once (the Tower included), or reports which copies are behind
scripts/recolor.py  converts an illustration drawn in the 2024 teal and coral palette to oxblood and rose
CHANGELOG.md        what each version changed
AGENTS.md           what to run before a push and the rules for an agent (CLAUDE.md just imports it)
.github/workflows/check.yml  CI on every pull request and push to main: check.py, check_css.py and its fixtures, check_layout.py and its variants, test-hint.mjs, and that logo/ and export/*.svg match build.py
```

Nothing in `logo/` or `export/` is edited by hand. Change `scripts/build.py`, then:

```bash
uv sync
uv run python scripts/build.py
uv run python scripts/check.py
```

## Tokens

Read the semantic names; the ramps exist for the semantic layer to point at.

- **Surfaces:** `--hm-bg`, `--hm-surface`, `--hm-surface-muted`, `--hm-surface-sunken`, and `--hm-surface-raised` for what floats above the page (a hint bubble), with `--hm-shadow-md`
- **Text:** `--hm-text`, `--hm-text-muted`, `--hm-text-subtle` (on `--hm-bg` and `--hm-surface` only)
- **Brand:** `--hm-brand`, `--hm-brand-hover`, `--hm-on-brand`, `--hm-link`, `--hm-link-hover`, `--hm-tint`, `--hm-tint-text`
- **Lines:** `--hm-border`, `--hm-border-strong`, `--hm-border-control` (inputs), `--hm-focus`
- **State:** `--hm-danger`, a burnt orange, always with words or an icon
- **Type:** `--hm-font-display`, `--hm-font-text`, `--hm-font-mono`; sizes `--hm-text-xs` (12, labels only) to `--hm-text-4xl` on a 1.25 ratio, and `--hm-text-base` is 16px on phones and 17px from 1000px up
- **Space:** a 4px grid, `--hm-space-1` (4px) to `--hm-space-24` (96px)
- **Layout:** `--hm-page-max` (1180px) and `--hm-page-max-wide` (1552px), `--hm-page-gutter` (16px, 24px from 600px), `--hm-col-min` (the narrowest column), `--hm-split-label-max` and `--hm-split-body-max`. The size classes and the classes that use these are in "Layout across screen sizes".
- **Tap targets:** `--hm-tap-min` (24px, the floor for a mouse), `--hm-tap-comfort` (44px, at 999px and narrower) and `--hm-control-h` (the height of a button, input or select: 44px, and 36px from 1000px up). The rule is in Behaviour, "Touch targets".

Dark mode follows the operating system. `data-theme="light"` or `"dark"` on `<html>` pins it.

## Layout across screen sizes

How a page holds its content at every screen size. The classes are in `css/layout.css` (opt-in: load it after `tokens.css`), the tokens in `css/tokens.css`, the reasons and the sources in `docs/decisions.md` ("Layout across screen sizes", 2026-11-12), and `scripts/check_layout.py` measures them in a browser.

- **Four size classes, in rem.** Under 600px (`(width < 37.5rem)`), 600 to 999 (`(width >= 37.5rem)`), 1000 to 1599 (`(width >= 62.5rem)`) and 1600 and up (`(width >= 100rem)`). Write a media query in `rem` and in the range syntax, never in `px`: a `px` query ignores the reader's default font size, a `rem` one follows it, and the range syntax leaves no gap at 999.5px. `scripts/check_css.py` rejects a `px` length and `min-width` or `max-width` in a media condition. The page's layout follows the window (a media query); a card or a note follows the width its parent gives it (a container query, below). Today the 600 step sets the page gutter, and the 1000 step sets the 17px body, the 36px control and the split.
- **Page container.** `.hm-container` is a block that is `--hm-page-max` (73.75rem, 1180px) wide at most, centred, with `--hm-page-gutter` on each side (16px under 600px, 24px from 600px). The gutter sits outside the cap, so the content is exactly 1180px wide at 1440 and at 2560: extra width becomes margin, not more content. `.hm-container--wide` is for a page that is mostly tables: the content is `--hm-page-max-wide` (97rem, 1552px) wide at most, and the frame grows to 90% of the screen beyond that, because a data table is limited by the screen and not by the frame (`docs/decisions.md`, "Wide content"). Prose does not grow with it.
- **Prose is one column at the measure.** `.hm-measure` caps a block at `--hm-measure` (68ch, about 80 characters), at every size. Never flow prose into columns.
- **Columns for independent items.** `.hm-cols` is `repeat(auto-fit, minmax(min(100%, var(--hm-col-min)), 1fr))` with a `--hm-space-5` gap: as many columns as fit, none narrower than `--hm-col-min` (16.25rem), one column when the box is narrower. The `min(100%, ...)` is required in every `auto-fit` or `auto-fill` track: a bare `minmax(16.25rem, 1fr)` overflowed a 320px window at a 200% root font size. Cards that share one height use `.hm-card-grid` (same rule, equal rows, same card markup).
- **Split.** `.hm-split` puts a label or title (`.hm-split__label`, at most `--hm-split-label-max`, 34rem) and its content (`.hm-split__body`) side by side from 1000px, stacked below with the label first. The content column is 18rem to `--hm-split-body-max` (30rem) and never wider than the measure, as in the "Why memory" sections of humem.ai.
- **Fit: container queries for a card or a note.** `.hm-fit` is a container (`container: hm-fit / inline-size`) and `.hm-fit__pair` is one column that becomes two when `.hm-fit` is 40rem wide, so the same markup works in a narrow aside and in a wide page. The base is one column, so a browser without container queries is still correct. Three rules: put `.hm-fit` on a block wrapper with a width, never on a flex item, an inline-block or a float (inline-size containment gives such a box a width of 0); a container cannot style itself, so the card or note sits inside it; name every container.
- **No multi-column text.** Not for prose and never in a box with a height: extra columns are added sideways, which scrolls a page at 320px (a 12rem box gave a `scrollWidth` of 3709 at 1000px), and the reader must scroll back up for the second column. The one allowed use is `column-width` in `rem` on a list of short items with no height (a glossary, a row of tags). `scripts/check_css.py` rejects `column-count`, `columns`, a `column-width` that is not in `rem`, and any multi-column box with a height.
- **Tables** keep their rule (the Tables section): they may be wider than the measure, and a keyboard-focusable scroller is compliant, because WCAG 1.4.10 excepts data tables. A page of tables takes `.hm-container--wide`.

```html
<main class="hm-container hm-container--wide" id="main">
  <section class="hm-split">
    <div class="hm-split__label"><h2>Why memory</h2></div>
    <div class="hm-split__body"><p class="hm-measure">...</p></div>
  </section>
  <div class="hm-card-grid"><a class="hm-card" href="/a">...</a></div>
</main>
```

`scripts/check_layout.py` loads `scripts/fixtures/layout/page.html` in headless Chrome and measures: the page never scrolls sideways at 320, 360, 768, 1280 and 2560px wide and at a 100% and a 200% root font size; only a named `.hm-table-scroll` scrolls sideways, and a wide table scrolls inside it; cards in a grid share one height; prose is the measure wide; a container is not 0 wide at 320px, and the page fits with every `@container` rule removed; the size classes switch at exactly 600 and 1000px (1600 is named and nothing reads it yet); the container is 1180px of content at 1440 and 2560. It is not yet checked: text spacing (WCAG 1.4.12), target sizes at 320px, focus under a sticky header, forced colours. Those are listed in `docs/decisions.md`.

## Behaviour

How a page acts, as opposed to how it looks. These rules apply to every HumemAI page and app. Today `scripts/check.py` checks only the contrast pairings (the focus ring, danger text, the hint) and `scripts/check_css.py` only that the CSS parses; everything else here is a convention, checked by measuring the rendered page.

- **Touch targets.** Make every standalone control at least 44×44px at 999px and narrower, by padding, not by a bigger font: `min-height: var(--hm-control-h)`, which is 44px there and 36px from 1000px up, where a pointer is enough. Two numbers, two reasons. 24px (`--hm-tap-min`) is the WCAG 2.5.8 AA floor: below it a target fails. 44px (`--hm-tap-comfort`) is the comfortable target (WCAG 2.5.5 at AAA, and the size Apple and Android publish): the floor is where a target stops failing, 44 is where it stops being fiddly. A link inside a run of text is exempt from both, because its line sizes it. Use the tokens and no other number, so the same job does not come out at five heights. This is a convention, not yet in a script.
- **Shorthand after longhand.** A shorthand (`font:`, `padding:`, `margin:`) after a longhand in the same block silently resets it. Search the block and every rule of higher specificity for the shorthand, and confirm by measuring the rendered element.
- **Keep the reader's place.** After any action, notice, list reload or navigation, the page scroll, the position of any inner scroller and the focused element stay where they were. Measure `scrollY`, the inner scroll and `document.activeElement` before and after, at 1920 and 390 wide.
- **Notices float.** A notice never moves the page. Move focus to it with `focus({preventScroll: true})`, and update lists in place.
- **Multi-line fields.** Ctrl+Enter (Cmd+Enter on macOS) submits and Enter adds a newline. Show the hint only while the field has focus.
- **Destructive actions.** Put them in an overflow menu, in `--hm-danger` ink with words, never colour alone. Confirm with a filled button in `--hm-danger`. Place each action next to the thing it acts on.
- **Repeated items.** Cards in a row share one height, with the footer line at the bottom: use `.hm-card-grid` and `.hm-card`, clamp long text, and set no fixed heights. In a list, each control sits at the same x in every row and never wraps. Text that overflows ends in an ellipsis, not a fade.

## Hints

A term, a status or a column head that a reader cannot guess gets a "?" (`.hm-hint`) with a short bubble. A mouse opens the bubble by hovering the button, and leaving closes it unless the button was clicked, which pins it. A click, a tap or Enter opens it everywhere else, and Esc or a tap outside closes it. The browser's Popover API does the opening and the closing. `js/hint.js` adds what it lacks: it places the bubble under its button (above it near the bottom of the screen), keeps it on screen, follows scrolling and resizing, and adds the hover. The button is a 24px circle with a 3:1 border; at 999px and narrower it stays 24px and grows a 44px hit area, so a table head keeps its layout. Hover, focus and the open state turn it oxblood (rose in dark mode), and a keyboard gets the focus ring. The bubble resets every inherited text style, so a hint can sit inside an all-caps, letter-spaced column head and its sentence still reads as body text. `aria-describedby` gives a screen reader the sentence on focus. It needs the Popover API, which every current browser has.

```html
<button type="button" class="hm-hint" popovertarget="hint-est" popovertargetaction="show"
        aria-label="What is Est.?" aria-describedby="hint-est">?</button>
<span id="hint-est" class="hm-hint__bubble" popover role="tooltip">How long the lane expects the job to take.</span>
```

```js
import { bindHints } from "./brand/js/hint.js";
bindHints();   // once: it listens on the document, so hints rendered later need no wiring
```

Pick the type by the situation:

| Situation | Use | Where it sits | Wording |
|---|---|---|---|
| A term, tag, status or column head nobody can guess | `.hm-hint` "?" with a bubble | Right after the word. In a list or table, ONE legend hint in the header, never one per row | 1 sentence, under about 140 characters |
| A choice with a consequence (delete, publish, anything that spends compute, money or data) | Visible helper text | Beside or under the control, always shown, never behind a "?" | 1 sentence: what happens and whether it can be undone |
| An empty list or area | A sentence in the empty state | The empty state | What it is, then the next step, under about 120 characters |
| An icon-only control | `aria-label` (required) and an optional tooltip | On the control. The tooltip is a convenience, not the meaning | 1 to 3 words |
| A longer explanation | A "?" whose last line is a "Learn more" link to a short doc | As the "?" | Bubble 1 to 2 sentences, detail in the doc |

Rules:

- Never `title` as the only carrier of meaning. A touch screen does not show it, and a disabled control cannot be focused.
- No private tooltip classes. The "?" is `.hm-hint`.
- Anything a reader needs in order to act stays visible. A hint explains a word; it never carries an instruction.
- Each app keeps one glossary map (key to `{term, text, learnMore?}`). Every key is used and every term shown has a key; the app's own test checks both.
- The "?" follows the touch-target rule (44px at 999px and narrower), and the bubble stays on screen (`bindHints()`).

For an app that builds its markup in code, `termHint(glossary, key, term)` returns the button and its bubble as an HTML string (for `innerHTML`), and `termHintElement(glossary, key, term, doc)` returns the same markup as a DOM fragment. `term` defaults to the entry's own `term`. The ids are `hm-hint-1`, `hm-hint-2` and so on, from one counter in the module. The sentence is HTML-escaped. A key the glossary lacks throws an `Error` that names it, so a typo never drops a hint quietly. A `learnMore` URL (http(s) or site-relative) adds a last "Learn more" line.

```js
import { bindHints, termHint, termHintElement } from "./brand/js/hint.js";
const GLOSSARY = { est: { term: "the estimate", text: "How long the lane expects the job to take, in hours.", learnMore: "/docs/lanes" } };
bindHints();
head.innerHTML = `Est. ${termHint(GLOSSARY, "est", "the estimate")}`;
head.append("Est. ", termHintElement(GLOSSARY, "est", "the estimate"));
```

`scripts/check.py` checks the hint's contrast pairings in both themes, and `scripts/test-hint.mjs` checks that `js/hint.js` parses as a module and that `termHint` gives the documented markup. Hover, pinning, placement and the sizes are measured in a browser (numbers in humemai/design-system#12).

## Base rules

`css/base.css` is opt-in: load it after `tokens.css`. It sets no colour, font or margin on any element of its own.

- **Focus ring.** `:focus-visible` gets a 2px `--hm-focus` outline, 2px off the edge (3:1 on every page surface, checked by `scripts/check.py`). Write no second copy.
- **Skip link.** The first focusable thing on the page is `<a class="hm-skip" href="#main">Skip to content</a>`, and the target has `id="main"`. It is hidden until a keyboard focuses it, then fixed to the top left corner above a sticky header (`z-index: 100`), in link ink on the surface with a focus-colour border. A page with a sticky header sets `--hm-sticky-offset` on `:root` to the header's height, so the jump and any focus scroll land below it.
- **Reduced motion.** Under `prefers-reduced-motion: reduce`, every transition and animation takes 0.01ms and `scroll-behavior` is `auto`. The duration is not 0 so an animation still ends in its last frame. A hover lift written as a `transform` is zeroed next to its component (`.hm-card` does).

## Tables

A data table is a `.hm-table` inside a `.hm-table-scroll`. Only the wrapper scrolls sideways, and a scroller has a name and a way in from the keyboard, so the wrapper carries `role="region"`, `tabindex="0"` and an `aria-label` naming the table. The system supplies the look, not those attributes.

```html
<div class="hm-table-scroll" role="region" tabindex="0" aria-label="Benchmark results">
  <table class="hm-table">
    <thead><tr><th scope="col">Lane</th><th scope="col" class="hm-num">Hours</th></tr></thead>
    <tbody><tr><td>ingest</td><td class="hm-num">1.6</td></tr></tbody>
  </table>
</div>
```

- **Numbers.** A numeric column takes `.hm-num` on its cells and on its head, inside `.hm-table`: right-aligned, never wrapped, and DM Mono in the body cells. There is no `tabular-nums` on Schibsted Grotesk: the Humem Tower measured that its tabular figures also widen the punctuation ("1 . 6 h"), while its default figures are proportional ("1" is 5.8px and "0" is 10.4px at 17px), so a column of numbers uses the mono face.
- **Sticky head.** `.hm-table--sticky-head` keeps the head row in view while the table scrolls down. It sticks to the wrapper, so give the wrapper a height of its own (`max-block-size: 70vh`).
- **Not here.** Column widths and roles are the page's own: the Tower sets them from its cells, the website lays out wide tables in its own way (see `docs/decisions.md`, Wide content).

## Badges

`.hm-badge` is a state or a label as a pill: always the word, and a fill and a symbol as a second cue, never colour alone. It has three variants: `.hm-badge--brand` (filled oxblood: the active thing), `.hm-badge--danger` (the failed or overdue thing) and `.hm-badge--tint` (the held, paused or stale thing). With no variant it is a quiet outline. The pairing of each variant's text and fill is in `scripts/check.py`. The state-to-symbol map belongs to the app: put the symbol in a `::before` with an empty alt text (`content: "\25B6\FE0E" / ""`) so a screen reader reads the word, not the shape.

```html
<span class="hm-badge hm-badge--brand">running</span>
<span class="hm-badge hm-badge--danger">failed</span>
<span class="hm-badge hm-badge--tint">paused</span>
<span class="hm-badge">idle</span>
```

## Using it

Five repositories carry a vendored copy: humem.ai, audit-ready-memory, humemai-docs, arcadedb-embedded-python, and the Humem Tower (`control-plane`, which sits under `../tae898/` and is written as a path in `CONSUMERS`). After a change here is merged, update all of them from the checkouts in one run, then commit in each:

```bash
scripts/vendor-all.sh --check   # which copies are behind, and which files differ
scripts/vendor-all.sh           # re-vendor every copy that is behind
```

`vendor-all.sh` skips a repository whose brand directory has uncommitted changes, and refuses a design-system commit that is not on `origin/main`. To add a consumer, add it to `CONSUMERS` in the script. A single copy can still be made by hand:

```bash
scripts/vendor-into.sh ../humem.ai/public/brand        # the website
scripts/vendor-into.sh ../audit-ready-memory/docs/brand  # an MkDocs project
```

The copy holds `css/`, `js/`, `logo/`, `assets/` and the icon files, and carries `verify.sh`, which fails if a vendored file was edited in place. Its `VERSION.md` records the design system's version (`Version:`, from `pyproject.toml`), the commit and the hash. Bump the version in the pull request that changes what a copy holds, and tag the merge commit with the bare version, no `v` (`0.2.0`); `CHANGELOG.md` says what each version changed. Each consumer runs it in its own checks (CI, or the pre-push script), so a hand edit of a copy fails there and not in review. `css/mkdocs.css` lists the `mkdocs.yml` settings that go with it.

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

Review pages at these sizes (CSS pixels): 360×800 and 390×844 (phones), 768×1024 (tablet), 984×1092 (unfolded foldable), 1280×720 (laptop), 1920×1080 (desktop, the main review size) and 2560×1440 (a large monitor: the page stays a centred 1180px and the rest is margin). Then two zoom checks, because a size alone does not show them: 320 CSS px wide (a 1280px window at 400% zoom), where the page must not scroll sideways except inside a table's own scroller, and a 200% root font size (`html { font-size: 200% }`) at 320 and at 1280, where nothing may be clipped or overlap. `scripts/check_layout.py` does the width and root-size part on the fixture page; do it by hand on a real page. Prose stays at the measure on every screen; data tables may be wider (see `docs/decisions.md`, Wide content).

## Licence

The HumemAI name, logo and icon identify the organization; don't use them for other projects. The fonts in `fonts/` are under the SIL Open Font License (see the `*-OFL.txt` files).
