# Stage release

Release the next Stage from `.ltb/plan.md`: author it, prove its tests, seal it, record it. Used by `new` (for Stage 01) and by `next`.

## 1. Pick the Stage

You have the plan row from the calling step. Its number **NN** is the next unused two-digit number (Stages are numbered in release order: one more than the highest `tests/stage_NN_*.py`). Its **slug** is two to four lowercase words from the behaviour, joined by hyphens.

**Done when** you have NN, the slug and the plan row.

## 2. Author it

**dispatch** a Stage author with [stage-author-brief.md](stage-author-brief.md). Inputs:

- the plan row (including its Kind), and the full plan for context;
- `.ltb/research/overview.md`, `spec.md` and `history.md` (not `architecture.md`: the Stage author describes behaviour, not structure);
- Goal, language and Dials from `.ltb/config`, with [dials.md](dials.md) for what each level means;
- the paths of earlier Primers in `.ltb/stages/`, and of `tests/`;
- the output of `./ltb api`;
- the staging directory `.ltb/staging/NN-slug/`.

The Stage author writes the Hidden tests and Concept-check answers; you see them only as descriptions, which keeps your hints honest.

**Done when** `.ltb/staging/NN-slug/` contains at least `primer.md`, `public.py`, `hidden.py` and `check.src.json` (plus `skeleton.md` when the design Dial is 2 or lower, and `unit/` with `unit.json` when that Skeleton names a pure boundary), and the report lists any earlier test files it changed.

## 3. The new tests fail on the current code

Run `./ltb test --staging --stage NN -v`. Every test of Stage NN, public and Hidden, must fail on the Learner's current code: a test that already passes teaches nothing. If one passes, send it back to the Stage author with the output.

**Done when** every Stage NN test fails.

## 4. The tests pass on a Reference solution

**dispatch** a Reference author with [reference-brief.md](reference-brief.md). Inputs: the Project root, the staging directory, and a fresh temp directory outside the Project (`mktemp -d`).

- **Green**: go on.
- **Red with test defects**: send the report to the Stage author to fix the named tests, then repeat steps 3 and 4. After two rounds still red, stop and tell the Learner the Stage could not be validated.

**Done when** the Reference run is green and its temp directory is gone.

## 5. Seal

Run `./ltb seal`, adding `--allow-changed <path> ...` for each earlier test file the Stage author changed (a Pressure Stage).

**Done when** it prints `Released Stage(s) NN` and `./ltb verify` prints `Harness ok`.

## 6. Record

In `.ltb/plan.md`, set the row's **Released as** to NN and **Status** to `current`. Then **commit Harness** with `ltb: release Stage NN <slug>` (inside `new`, the final commit covers this).

**Done when** the plan row shows NN and `current`, and the Harness is committed.
