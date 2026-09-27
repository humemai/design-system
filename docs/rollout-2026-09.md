# Rollout of the oxblood brand (2026-09-27)

Every place the HumemAI brand appears, and where each one stands.

## Repositories

| Repo | How it landed | What changed |
|---|---|---|
| `design-system` | new public repo, `main` | tokens, logo masters, exports, MkDocs theme, checks, recolor and restyle scripts, these docs |
| `humem.ai` | PRs #3 and #4, merged; Vercel deployed | colours, fonts, header/footer logo, favicon, link card, 17 illustrations recoloured, image prompts, README |
| `humemdb` | PR #1, merged | docs theme, hero box colour, README badge |
| `audit-ready-memory` | PR #1, merged | docs theme |
| `cypherglot` | PR #2, merged | docs theme, README badge and docs note |
| `arcadedb-embedded-python` | PR #6 | docs theme (`bindings/python`), README badge |
| `humemai-docs` | `main`, live | docs.humem.ai landing page, root `favicon.ico`, every published version restyled in place |
| `.github` | `main`, live | organization profile: lockup and new text |
| `humemai-research` | `main` | `figures/humemai-with-text-below.png` is the new stacked lockup |

The docs source changes show on docs.humem.ai when `deploy-docs` next runs (a version tag, or by hand). The versions already published were restyled directly in `humemai-docs`, so the site already looks right.

## Platforms

- [x] GitHub organization: avatar, description "Open source memory systems for agentic AI" (was "A Machine With Human-Like Memory Systems"), and links to LinkedIn, X and Hugging Face.
- [x] GitHub social preview on all 18 public repositories (`github-social-1280x640.png`), each checked against the file.
- [x] LinkedIn page `humemai`: logo, cover, and the About text (was "A Machine With Human-Like Memory Systems"; now the site's description of HumemAI and its projects). The tagline "Machines with human-like memory" is Taewoon's and stays.
- [x] X `@humem_ai`: avatar, header, and bio "Machines with human-like memory. Open source memory systems for agentic AI."
- [x] Hugging Face organization `humemai`: avatar.
- [x] YouTube `@HumemAI`: picture, banner (`youtube-banner-2560x1440.png`) and description (was "HumemAI: A Machine With Human-Like Memory Systems").
- [x] GitHub repo details: `humemai` description is the tagline (was "AI with Human-Like Memory"); `humem.ai` homepage is https://humem.ai (was the Vercel preview URL); `humemdb`, `cypherglot` and `humemai-docs` have real descriptions and their docs as homepage.
- [x] Zenodo community `humemai`: logo (checked through the API).
- [x] dev.to `humemai`: avatar, bio (tagline and descriptor), website https://humem.ai, brand colour `#892122`.
- [x] Medium `@humemai`: avatar (1024px) and bio.
- [x] Substack `@humemai`: avatar, bio, header (`substack-header-2688x512.png`) and accent colour `#892122`. Background left white: it is the reading surface.
- [x] PyPI user `humemai`: PyPI shows the Gravatar of its primary email, taewoon@humem.ai. That Gravatar account (separate from the personal tae898@gmail.com one) now has the tile, checked through Gravatar's avatar URL. Every site that uses Gravatar for taewoon@humem.ai shows it too.
- [x] PyPI links (humem.ai footer and About page, the GitHub profile) now go to https://pypi.org/user/humemai/, the account that owns all seven packages; the PyPI organization https://pypi.org/org/HumemAI/ (also owned by that account) holds no projects.
- [x] humem.ai search description is the descriptor, "Open source memory systems for agentic AI." (humem.ai #7).
- [x] `humemai` README no longer announces a hosted HumemAI Cloud (humemai #2).
- [x] The `X.Y.Z` placeholder link in arcadedb's developer docs is code now: source in arcadedb-embedded-python #7, the 12 published copies in humemai-docs.

## Sweep (2026-09-27)

Deterministic checks after the rollout, and a web search for every other place HumemAI appears:

- **humem.ai**, crawled from the home page: 26 pages, 325 assets, none broken. Four fallback gradients still hard-coded the 2024 orange and green, code blocks used the old coral, and the 404 page was Next's unbranded default; all fixed in humem.ai #5, which also added a sitemap and robots.txt (both were 404).
- **Old URLs**: all 19 humem.ai URLs the Wayback Machine holds that answered 404 (old blog posts, tags, "who we are", team, terms, and `/2024-03-01-design-humemai/`, which Google still lists) now redirect to the page that replaced them (humem.ai #6). Checked in production: 19 of 19 resolve.
- **docs.humem.ai**, crawled: 140 pages, 292 assets, no old brand left. One placeholder link, `docs.humem.ai/arcadedb/X.Y.Z/`, is autolinked in arcadedb's `development/documentation.md`.
- **GitHub code search** over every humemai repo: no old logo files, teal hex or teal badges left. All 45 README images across the public repos load.
- **PyPI** pages only change with a release: `cypherglot` 0.1.0 still shows the teal docs badge; `humemai-research` 2.5.7's summary is "A Machine With Human-Like Memory"; `humemai` 0.0.1's is "HumemAI — SDK for Human-Like Memory Systems"; `humemdb` 0.0.0 has a placeholder README.

## Left as they are, on purpose

- **Frozen third-party copies**: the BNAIC 2024 paper PDF (Fig. 1 is the old teal logo), the October 2024 LinkedIn launch post, and Zenodo release records.

- **pdoc API pages** at humemai.github.io (explicit-memory, human-like-memory-systems, humemai-research): default pdoc styling with no HumemAI brand in them.
- **Paper figures** (the site's `public/images/papers/`, the ArcadeDB benchmark SVGs): they must match the published papers.
- **Google Drive**: `~/Drive/humemai` (the 2024 teal logos and a QR code for https://humem.ai) was deleted; this repo is the source, and `export/qr-humem-ai.svg` replaces the QR code. The benchmark zips in `~/Drive/arcadedb-embedded`, the PyPI recovery codes and the Google Slides in `~/Drive/docs` are not brand files and were not touched.
