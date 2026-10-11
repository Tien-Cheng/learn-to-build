# hint: the next rung of the Hint ladder

The Learner is stuck. Give exactly one rung of help, never code for this Stage, and log it.

## 1. Orient

Run `./ltb status`. If a Drill is active, the only help during a Drill is the Stage's Primer: point to it and stop.

**Done when** you know the current Stage and whether a Drill is running.

## 2. Find the target

Run `./ltb test -v`. The target is the first failing test of the lowest failing Stage, unless the Learner named what they are stuck on. If everything is green, suggest `review` and stop.

For a public test, read it in `tests/`. For a Hidden test (labelled `[hidden]`), work only from the description `ltb` prints.

**Done when** you have the target test and what it expects.

## 3. Pick the rung

In `.ltb/log/hints.jsonl`, find the highest rung already given for this Stage and test. The next rung is one above it, capped at 5. A Learner who asks for a lower rung gets that one.

**Done when** you have the rung number.

## 4. Read their code

Read the Learner's code around the failure, so the rung fits what they actually wrote. Read only; their files stay theirs.

## 5. Give that rung

1. **Restate**: what the test does, what it expects, and what their program did instead, in plain words.
2. **Point**: the Primer section, or the primary source in `.ltb/research/spec.md`, that answers it, with the specific detail to look at.
3. **Question**: one question about their own code that leads them to the bug or the missing idea.
4. **Analogy**: a short worked example in their language that solves an analogous problem in a different domain (different data, different names), so they see the pattern and do the transfer themselves.
5. **Pseudocode**: the approach as numbered steps in plain words, independent of their file layout and free of their language's syntax.

The Learner's own code is above the top rung: it is theirs to write. Asked again at rung 5, explain rung 5 another way, or suggest a short break.

**Done when** you have given one rung and nothing more.

## 6. Log it

`./ltb log hint --stage NN --test <test name or description> --rung R --note "<what they were stuck on, in a few words>"`

Tell the Learner that asking again climbs one rung.

**Done when** the log command printed `Logged hint rung`.
