# AGENTS.md: humemai/design-system

The HumemAI brand in one repository: tokens, components, the logo and the export assets. humem.ai, docs.humem.ai, the audit-ready-memory docs, the ArcadeDB bindings docs and the Humem Tower carry vendored copies. Read `README.md` first, then `docs/decisions.md` for why a value is what it is.

## Before you push

- `uv sync --locked`, then `uv run python scripts/check.py` and `uv run --no-project --with tinycss2==1.4.0 python -I scripts/check_css.py`.
- `uv run --no-project --with tinycss2==1.4.0 python -I scripts/check_css.py --self-test`: every static layout rule fails on its fixture.
- `node scripts/test-hint.mjs`.
- `uv run python scripts/check_layout.py`, then `--self-test`: the headless Chrome layout smoke and its bad variants.
- `uv run python scripts/build.py`, then `git status --porcelain -- logo 'export/*.svg'` must print nothing.
- A change to what a copy holds bumps `version` in `pyproject.toml` and adds a `CHANGELOG.md` section; tag the merge commit with the bare version (`0.2.0`, no `v`).
- After a merge to `main`: pull the checkout, then `scripts/vendor-all.sh --check`. A copy that is behind is a pull request in that repository (`scripts/vendor-into.sh`, then its own checks).

## Rules

- Never hand-edit `logo/` or `export/`: change `scripts/build.py` and run it.
- Every new check ships with a fixture it fails on. Show it red once, then green.
- Mirror Stateloop's design-system structure, not its look. The brand is oxblood, Newsreader headlines, Schibsted Grotesk text and DM Mono code. Never blue or violet, and Stateloop's colours stay in Stateloop's repository.
- A component or token goes here first and is vendored. Add one when two consumers need it, with its contrast pairings in `scripts/check.py`, a README section and a dated entry in `docs/decisions.md`.
- Stage files by explicit path. Issue and PR bodies have no hard wraps and no em dashes.
