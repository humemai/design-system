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
css/components.css  shared components: the card grid (equal-height rows) and its card, and the "?" hint
js/hint.js          the hint's behaviour (placing the bubble, hover) and termHint for a glossary; a plain ES module, no dependency
assets/fonts.html   the Google Fonts block for plain HTML pages
logo/               SVG masters: mark, tile, avatar, wordmark, lockups (light, dark, white)
export/             PNG, ICO and social images, generated from logo/ and the fonts
fonts/              the two brand fonts (SIL Open Font License), used to outline text
scripts/build.py    generates logo/ and export/
scripts/check.py    checks the tokens, every contrast pairing, and the export sizes
scripts/check_css.py  checks that every css/*.css file parses and its brackets balance
scripts/test-hint.mjs  checks that js/hint.js parses as a module and that termHint gives the documented markup
scripts/vendor-into.sh  copies the system (css, js, logo, assets, icons) into a site, with a pinned VERSION.md
scripts/vendor-all.sh   vendors into every HumemAI repo at once, or reports which copies are behind
scripts/recolor.py  converts an illustration drawn in the 2024 teal and coral palette to oxblood and rose
.github/workflows/check.yml  CI on every pull request and push to main: check.py, check_css.py, test-hint.mjs, and that logo/ and export/*.svg match build.py
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
- **Tap targets:** `--hm-tap-min` (24px, the floor for a mouse) and `--hm-tap-comfort` (44px, at 999px and narrower)

Dark mode follows the operating system. `data-theme="light"` or `"dark"` on `<html>` pins it.

## Behaviour

How a page acts, as opposed to how it looks. These rules apply to every HumemAI page and app. Today `scripts/check.py` checks only the contrast pairings (the focus ring, danger text, the hint) and `scripts/check_css.py` only that the CSS parses; everything else here is a convention, checked by measuring the rendered page.

- **Touch targets.** Make every control at least 44×44px at 999px and narrower, by padding, not by a bigger font. This is a convention, not yet in a script.
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

## Using it

Four repositories carry a vendored copy: humem.ai, audit-ready-memory, humemai-docs, and arcadedb-embedded-python. After a change here is merged, update all of them from sibling checkouts in one run, then commit in each:

```bash
scripts/vendor-all.sh --check   # which copies are behind, and which files differ
scripts/vendor-all.sh           # re-vendor every copy that is behind
```

`vendor-all.sh` skips a repository whose brand directory has uncommitted changes, and refuses a design-system commit that is not on `origin/main`. To add a consumer, add it to `CONSUMERS` in the script. A single copy can still be made by hand:

```bash
scripts/vendor-into.sh ../humem.ai/public/brand        # the website
scripts/vendor-into.sh ../audit-ready-memory/docs/brand  # an MkDocs project
```

The copy holds `css/`, `js/`, `logo/`, `assets/` and the icon files, and carries `verify.sh`, which fails if a vendored file was edited in place. `css/mkdocs.css` lists the `mkdocs.yml` settings that go with it.

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
