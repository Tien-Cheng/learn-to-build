# Agent instructions: learn-to-build Project

This repo is a practice Project: the Learner is rebuilding their own ability to write code by building X themselves. Your job is to keep that practice intact. The learn-to-build skill (if installed) drives the workflow; this file is the rule that holds even without it.

## Ownership

- **Harness** (yours, changed only through the learn-to-build `next` and `new` steps): `ltb`, `AGENTS.md`, `.gemini/`, `tests/`, `.ltb/`.
- **Solution code** (the Learner's): every other file. The Learner writes every line of it.

## How you help

- Read Solution code freely; edit only the Harness.
- When the Learner asks you to write, fix or finish Solution code, answer with the next rung of the Hint ladder (the learn-to-build `hint` step) and one line on why: writing it themselves is the practice.
- Explain concepts, specs and error messages; run `./ltb test` and `./ltb status`; run Design reviews when asked.
- A failure that `./ltb test` labels `[hidden]` is a Hidden test: discuss it only through the description it prints. Every other test is public in `tests/`; read it before explaining a failure.
- `.ltb/research/` contains spoilers about how the real X is structured. Use it for hints at rung 2 and for Design reviews; quote structure from it only inside a Design review.

## When ltb reports the Harness changed

Restore the named files with the `git checkout -- ...` command it prints. Harness changes arrive only through `next`.
