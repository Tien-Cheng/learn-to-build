# next: close the current Stage and release the next one

## 1. Orient

Run `./ltb status`. If a Drill is active, ask the Learner to run `./ltb drill finish` or `./ltb drill discard` first, and stop.

If the Project's `ltb` differs from the skill's `assets/ltb` (`cmp`), the skill was updated: copy the new runner over, run `./ltb seal --allow-changed ltb`, and **commit Harness** with `ltb: update runner`.

If `.ltb/guard.py` exists, compare it with `assets/adapters/ltb-guard.py` the same way; if it differs, reinstall the adapter as [adapters.md](adapters.md) describes (the guard is not checksummed, so no seal is needed) and **commit Harness** with `ltb: update guard`. Codex will ask the Learner to trust the changed hook.

**Done when** no Drill is active, and the runner and any guard match the skill's copies.

## 2. Gate

The current Stage (the plan row with Status `current`) is done when `./ltb test` prints `green` and `.ltb/log/review-NN.md` exists with no `Status: open`. If a review is missing, say the Stage needs `review` first, and stop. If no Stage has been released yet, skip to step 6.

**Done when** the current Stage is green and reviewed, or there is none.

## 3. Retrospective

If every Core path row is `reviewed` (or `cut`) and `.ltb/log/retrospective.md` does not exist, follow [retrospective.md](retrospective.md), then stop.

## 4. Calibrate

Follow [dials.md](dials.md) for the Stage just reviewed.

If the design Dial is now 3 or more and `.ltb/config` lists Skeleton unit tests under `[harness] files`, retire them: delete those files, clear `[harness] files` and `[commands] unit`, run `./ltb seal --allow-changed <each file>`, and tell the Learner the structure is theirs from here.

**Done when** the Dial changes, or "no change", are announced, and retired unit tests are sealed out.

## 5. Drill

Schedule a Drill for the Stage just reviewed: its concept tag from the plan row and the `Concept paths:` line of its review.

`./ltb drill add --concept <concept tag> --stage NN --paths <paths>`

If `./ltb drill list --due` shows a ready Drill, mention it in one line ("`<concept>` is ready for a 15-minute Drill whenever you have time"). It is an offer: carry on either way.

**Done when** the Drill is scheduled.

## 6. Choose the next Stage

- Normally: the first `planned` row of the Core path.
- At a Branch point (the plan says a Branch leaves after the Stage just reviewed): **ask** whether to continue the Core path or take the Branch.
- After the Retrospective: **ask** which Branch to take, if any remain.

**Done when** you have one plan row. If none remain, congratulate the Learner on finishing and stop.

## 7. Release

Follow [stage-release.md](stage-release.md) for that row.

## 8. Assistance mode

**ask** which Assistance mode this Stage uses, offering the Project default first (`./ltb assist` shows it). For Pair, also ask which files the agent may write. Record it: `./ltb assist <mode> --stage NN [--paths <files or globs>]`.

**Done when** `./ltb status` shows the Stage's mode.

## 9. Hand off

Tell the Learner, briefly: the Primer path; that `./ltb check NN` unlocks the tests with a quick Concept check; the Skeleton path if there is one; for Lead, to write `.ltb/stages/NN-<slug>/approach.md` (decomposition, data, edge cases) before asking you to implement; and to come back with `hint` when stuck or `review` when green.

**Done when** the Learner has the Primer path.
