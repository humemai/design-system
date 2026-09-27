# Rollout of the oxblood brand (started 2026-09-27)

Every place the HumemAI brand appears, and where each one stands. Tick items off here as they go live.

## Done locally (committed, not pushed)

| Repo | Branch | What changed |
|---|---|---|
| `design-system` (new, no GitHub repo yet) | `main` | tokens, logo masters, exports, MkDocs theme, checks, recolor script, these docs |
| `humem.ai` | `oxblood-rebrand` | colours, fonts, header/footer logo, favicon, OG card, 17 illustrations recoloured, image prompts, README |
| `humemdb` | `oxblood-rebrand` | docs theme, hero box colour, README badge |
| `audit-ready-memory` | `oxblood-rebrand` | docs theme |
| `cypherglot` (worktree `cypherglot-rebrand`, from `main`) | `oxblood-rebrand` | docs theme, README badge and docs note |
| `arcadedb-embedded-python` | `oxblood-rebrand` | docs theme (`bindings/python`), README badge |
| `humemai-docs` | `main` | docs.humem.ai landing page |
| `.github` | `main` | organization profile: lockup and new text |
| `humemai-research` | `main` | `figures/humemai-with-text-below.png` is the new stacked lockup |

## To publish

- [ ] Create `github.com/humemai/design-system` (public) and push `main`. The other READMEs link to it.
- [ ] Push and merge `humem.ai` `oxblood-rebrand`; Vercel deploys humem.ai.
- [ ] Push and merge the four docs branches. The live docs only change when `deploy-docs` runs: on the next version tag, or run it by hand for the current version.
- [ ] Push `humemai-docs`, `.github` and `humemai-research`.

## Done on the platforms

- [x] GitHub organization description: "Open source memory systems for agentic AI" (was "A Machine With Human-Like Memory Systems"), 2026-09-27, through the API.

## To upload by hand (platform settings, no API)

| Where | File (`export/`) |
|---|---|
| GitHub organization avatar (Settings → Profile) | `avatar-500.png` |
| Social preview of each public repository (Settings → General) | `github-social-1280x640.png` |
| Hugging Face organization `humemai` avatar | `avatar-500.png` |
| LinkedIn page logo and cover, if HumemAI has a page | `avatar-500.png`, `linkedin-banner-1128x191.png` |
| X account avatar and header, if HumemAI has one | `avatar-500.png`, `x-header-1500x500.png` |

## Left as they are, on purpose

- **Published docs versions** on docs.humem.ai (26 of them) keep the theme they were built with. New builds get the new one.
- **pdoc API pages** at humemai.github.io (explicit-memory, human-like-memory-systems, humemai-research): default pdoc styling with no HumemAI brand in them.
- **Paper figures** (the site's `public/images/papers/`, the ArcadeDB benchmark SVGs): research results, not brand.
- **`~/Drive/humemai`** (the 2024 teal logos and a QR code for https://humem.ai) was deleted on 2026-09-27: this repo is the source, and `export/qr-humem-ai.svg` replaces the QR code.
