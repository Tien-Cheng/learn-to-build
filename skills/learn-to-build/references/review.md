# review: the Design review

Once a Stage is green, a fresh reviewer critiques the structure of the Learner's code. Each finding ends fixed or defended; then the Stage is done.

## 1. Gate

Run `./ltb test`. It must print `green` (public and Hidden). If not, say which Stage is failing and stop; `hint` helps there. In Lead mode, the Stage's `approach.md` must also exist.

**Done when** the suite is green (and, in Lead mode, the Approach exists).

## 2. Dispatch the reviewer

**dispatch** a reviewer with [reviewer-brief.md](reviewer-brief.md) in Stage mode. Inputs:

- the Solution code: every file in the Project from `git ls-files --cached --others --exclude-standard`, minus the Harness (`ltb`, `AGENTS.md`, `.claude/`, `.codex/`, `tests/`, `.ltb/`);
- this Stage's number, slug, plan row and Primer;
- `.ltb/research/` (spoilers are fine for the reviewer);
- this Stage's lines from `.ltb/log/hints.jsonl`;
- the Stage's Assistance mode (`./ltb assist`), its lines from `.ltb/log/assist.jsonl`, and in Lead mode its `approach.md`;
- Goal and Dials from `.ltb/config`;
- earlier `.ltb/log/review-*.md` files, so defended points are not re-raised.

**Done when** the report is back in the format the brief defines.

## 3. Record

Write the report to `.ltb/log/review-NN.md`, every finding with `Status: open`.

## 4. Walkthrough (Pair and Lead only)

Ask the Learner the report's Walkthrough questions about the agent-written code, one at a time. After each answer, say what it got right and fill any gap. If an answer shows they do not understand the code, explain it and ask them to restate it in their own words. Record the questions and answers under `## Walkthrough` in `review-NN.md`.

**Done when** every Walkthrough question has an answer the Learner restated correctly.

## 5. Walk the findings

Take the findings in order. For each, present it and **ask**: fix it, or defend the current design?

- **Fix**: the Learner changes their code and runs `./ltb test`, which must stay green. Re-read what they changed. If it addresses the finding, set `Status: fixed`; if not, say what is still missing (in words, not code) and let them try again or defend.
- **Defend**: record the Learner's reasoning verbatim under `Defence:`. Reply once under `Rebuttal:` with the strongest specific counterpoint, or accept it. Record their answer under `Reply:`; it is final. Set `Status: defended`.

**Done when** `review-NN.md` has no `Status: open`.

## 6. Close

- Present the report's "How the real X does it" section.
- After Stage 01, set the design Dial to the reviewer's estimate: `./ltb dial design <n> --evidence "Stage 01 review: <reason>"`, and tell the Learner what it means (see [dials.md](dials.md)).
- In `.ltb/plan.md`, set this Stage's Status to `reviewed`.
- **commit Harness** with `ltb: review Stage NN`.
- Tell the Learner to commit their own code, then ask for `next`. If this was the last Core Stage, `next` runs the Retrospective.

**Done when** the plan row says `reviewed` and the Harness is committed.
