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
- [x] LinkedIn page `humemai`: logo and cover. The tagline "Machines with human-like memory" is Taewoon's and stays.
- [x] X `@humem_ai`: avatar, header, and bio "Machines with human-like memory. Open source memory systems for agentic AI."
- [x] Hugging Face organization `humemai`: avatar.

## Left as they are, on purpose

- **pdoc API pages** at humemai.github.io (explicit-memory, human-like-memory-systems, humemai-research): default pdoc styling with no HumemAI brand in them.
- **Paper figures** (the site's `public/images/papers/`, the ArcadeDB benchmark SVGs): they must match the published papers.
- **Google Drive**: `~/Drive/humemai` (the 2024 teal logos and a QR code for https://humem.ai) was deleted; this repo is the source, and `export/qr-humem-ai.svg` replaces the QR code. The benchmark zips in `~/Drive/arcadedb-embedded`, the PyPI recovery codes and the Google Slides in `~/Drive/docs` are not brand files and were not touched.
