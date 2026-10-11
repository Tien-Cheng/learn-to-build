# Stage release

Release the next Stage from `.ltb/plan.md`: author it, check it, seal it, record it. Used by `new` (for Stage 01) and later by `next`.

## 1. Pick the Stage

Take the first `planned` row of the Core path. Its number **NN** is the next unused two-digit number (Stages are numbered in release order: count the files in `tests/` and add one). Its **slug** is two to four lowercase words from the behaviour, joined by hyphens.

**Done when** you have NN, the slug and the plan row.

## 2. Author it

**dispatch** a Stage author with [stage-author-brief.md](stage-author-brief.md). Inputs:

- the plan row, and the full plan for context;
- `.ltb/research/overview.md`, `spec.md` and `history.md` (not `architecture.md`: the Stage author describes behaviour, not structure);
- Goal, language and Dials from `.ltb/config`;
- the paths of earlier Primers in `.ltb/stages/`;
- the output of `./ltb api`;
- the staging directory `.ltb/staging/NN-slug/`.

**Done when** `.ltb/staging/NN-slug/` contains `primer.md` and `public.py`, and `./ltb test --staging --stage NN` runs to completion.

## 3. Check the tests against the current code

Run `./ltb test --staging --stage NN -v`. Every test of the new Stage must fail on the Learner's current code, because a test that already passes teaches nothing. If any passes, send it back to the Stage author with the output.

Then read each test against `spec.md`: is the expected output exactly what the spec (or the oracle named in `overview.md`) says? Reference validation by an isolated subagent arrives in a later version; until then this reading is the check.

**Done when** every test in Stage NN fails, and each expected value traces to `spec.md` or the oracle.

## 4. Seal

Run `./ltb seal`.

**Done when** it prints `Released Stage(s) NN` and `./ltb verify` prints `Harness ok`.

## 5. Record

In `.ltb/plan.md`, set the row's **Released as** to NN and **Status** to `current`. Then **commit Harness** with `ltb: release Stage NN <slug>` (inside `new`, the final commit covers this).

**Done when** the plan row shows NN and `current`, and the Harness is committed.
