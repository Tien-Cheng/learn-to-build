# Dials

Three Dials, each 1 to 5, live in `.ltb/config` under `[dials]`. They decide how the Harness is pitched to this Learner. Change them only with `./ltb dial <name> <value> --evidence "<why>"`, which records the change.

## What each level changes

| Dial | 1–2 | 3 | 4–5 |
|---|---|---|---|
| **language** | Primers include a "Language you'll need" section; Stages split smaller | Language notes only for features new in this Stage | No language notes; Design reviews also judge idiom |
| **domain** | Primers explain concepts from first principles with worked examples | Primers explain the concept and cite the spec | Primers state the contract and cite sources; the Learner digs |
| **design** | Each Stage ships a Skeleton; reviews focus on one or two structural points | No Skeleton; normal reviews | No Skeleton; strict reviews; Pressure Stages come sooner |

The **Goal's Dial** gets the extra difficulty: when a choice is close, pitch that Dial's area one level harder than its value (for example, a Design Goal withdraws the Skeleton one level earlier).

## Adjusting at `next`

Gather the evidence for the Stage just reviewed:

- `./ltb log summary --stage NN` (runs and minutes to green; it records itself);
- this Stage's entries in `.ltb/log/hints.jsonl` (count, highest rung, and whether stuck points were about the language or the concept);
- `.ltb/log/review-NN.md` (number and kind of findings);
- this Stage's entries in `.ltb/log/checks.jsonl` (Concept-check misses).

Speed and an absence of hints show skill only for code the Learner wrote: in **Lead** Stages, skip the rules that raise a Dial, and in **Pair** Stages, apply them only to the concept the Learner wrote. Review findings count in every mode.

Then apply these rules, moving each Dial **at most one step** per `next`:

- Highest hint rung 4 or 5 on a language-mechanics problem: language down one. On a concept problem: domain down one.
- No hints, green within 20 minutes, Concept check all correct: raise the Goal's Dial one step (or domain, if the Goal's Dial is already 5).
- Three or more under-engineering findings: design down one. No findings, or only minor ones, on two Stages running: design up one.
- Two or more Concept-check misses: domain down one.
- After Stage 01's review, set design to the reviewer's estimate instead.

## Announce

Tell the Learner every change in one line with its evidence, for example: "design 3 → 2: the review found parsing, I/O and formatting in one function; the next Stage comes with a Skeleton." If nothing changed, say so in one line. If the Learner disagrees, use their value and record their reason as the evidence.

**Done when** every change is recorded with `./ltb dial` and announced, or "no change" is announced.
