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
- **Line length:** prose lines of 60 to 75 characters (`--hm-measure: 68ch`), body line height 1.65.
- **Spacing:** a 4px grid.
- **Review sizes:** 360×800, 390×844, 768×1024, 984×1092, 1280×720, and 1920×1080 CSS pixels. 1920 is where desktop reviews happen. 984×1092 (an unfolded foldable) was added on 2026-10-02: it is the only size between 920 and 1024, where the website switches layouts.

## Wide content (2026-10-02)

The prose column is set by the line length above, so it stays narrow on every screen. Content that is not prose does not have to:

- **Data tables** are as wide as their columns need, never narrower than the prose column and never wider than the screen less the page gutters, centred on the column. Holding them to the prose column made most of a benchmark page's tables scroll sideways while half a 1920 screen stayed empty. A limit at the page frame (the website's 1180px) still left a third of them scrolling at every desktop size, so the limit is the screen.
- **Table headers** wrap when the table is out of room, never inside a hyphenated word, and a direction arrow stays with the word before it.
- **Figures** stay in the prose column. An image scales instead of scrolling, so a wider box only makes it bigger; a figure gets more width only if it is drawn wide.
- Captions and notes stay in the prose column with the paragraphs.

The website implements this in humemai/humem.ai#10 and records the numbers in its `docs/design/layout-widths.md`.

## Words: tagline and descriptor (2026-09-27)

- **Tagline:** "Machines with human-like memory". Taewoon's line, first on the LinkedIn page. It's short, and it ties to the name (human + memory) and to the mark (a head holding a graph). On banners and cards it's the headline, in Newsreader.
- **Descriptor:** "Open source memory systems for agentic AI". It says what HumemAI actually makes. It's the GitHub organization description, and the smaller second line under the tagline.

Wherever there's room for both, use both: the tagline alone is memorable but vague.

## How much system (2026-09-27)

HumemAI is one person's organization, so this is deliberately smaller than a company design system: tokens, one theme file for the docs, assets, and one checker. There are no shared components. The website keeps its own components and reads the tokens. Add a rule here when a real inconsistency shows up, not before.
