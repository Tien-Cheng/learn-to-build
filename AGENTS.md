# Contributing to learn-to-build

This repo holds the `learn-to-build` agent skill (`skills/learn-to-build/`), its runner `ltb`, and the design record. Read `docs/design.md` and `GLOSSARY.md` before changing behaviour.

## Rules

- **Vocabulary**: `GLOSSARY.md` is the single source of terms. After editing it, copy it to `skills/learn-to-build/references/glossary.md` (a test enforces the copy).
- **Decisions**: record hard-to-reverse, surprising trade-offs in `docs/adr/` (format: short title plus one paragraph).
- **`ltb`** (`skills/learn-to-build/assets/ltb`) is one file, Python 3.9+ standard library only, because it is copied into every Project repo and must run with the system `python3`.
- **Skill markdown** is read by agents: steps in order, each ending in a checkable **Done when**; glossary terms used exactly; positive instructions; each rule stated in one place. Keep `SKILL.md` frontmatter to the Agent Skills spec fields so it stays portable across harnesses.
- **Privacy**: the repo is public. Keep names, employers, emails and home paths out of every file; `python3 scripts/scrub_check.py` must pass.

## Commands

- Tests: `uv run pytest` and `uv run --python 3.9 pytest`
- Check the skills CLI still finds the skill: `npx skills add ./ --list`
- Try the skill locally with live edits: `scripts/dev-install.sh` (symlinks into `~/.claude/skills` and `~/.agents/skills`), or `scripts/dev-install.sh --project <scratch dir>`
