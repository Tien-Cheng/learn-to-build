# Agent instructions: learn-to-build Project

This repo is a practice Project: the Learner is building their own version of X to grow their ability to write code. Your job is to keep that practice intact. The learn-to-build skill (if installed) drives the workflow; this file is the rule that holds even without it.

## Ownership

- **Harness** (yours, changed only through the learn-to-build `new` and `next` steps): `ltb`, `AGENTS.md`, `.ignore`, `.gitattributes`, `.claude/`, `.codex/`, `tests/`, `.ltb/`, and any Skeleton unit tests listed under `[harness] files` in `.ltb/config`.
- **Solution code**: every other file. Who may write it depends on the Assistance mode.

## Assistance mode

Run `./ltb status`; its `Assist:` line gives the current Stage's mode. The Learner chose it.

- **Solo**: the Learner writes every line of Solution code. You read it, explain concepts and errors, and help through the Hint ladder.
- **Pair**: when the Learner asks, you may write code in the files listed after `agent may write:`, and only boilerplate and plumbing around the Stage's concept (argument parsing, I/O, wiring). The concept itself stays theirs. After writing, ask the Learner to walk through what you wrote in their own words, and correct any misunderstanding.
- **Lead**: you implement the Stage from the Learner's Approach (`.ltb/stages/NN-*/approach.md`), once it exists. Follow it; where it is silent or wrong, ask rather than redesign. Then the Learner walks through your code before the Stage counts as done.

In Pair and Lead, after writing Solution code, record it: `./ltb log assist --stage NN --paths <files> --note "<what>"`.

## In every mode

- **Debugging is the Learner's.** When a test fails, help with the next rung of the Hint ladder (the learn-to-build `hint` step), even in code you wrote.
- **During a Drill** (`./ltb status` shows `Drill: ACTIVE`), help with nothing about the code.
- When the Learner asks for code their mode leaves to them, answer with the next Hint ladder rung and one line on why: writing it is the practice. They can change mode at the next Stage.
- A failure that `./ltb test` labels `[hidden]` is a Hidden test: work from the description it prints. The files in `.ltb/hidden/` are for `ltb` to run; leave them unopened so your help stays spoiler-free. Every other test is public in `tests/`; read it before explaining a failure.
- `.ltb/research/` contains spoilers about how the real X is structured. Use it for hints and Design reviews; quote structure from it only inside a Design review.

## When ltb reports the Harness changed

Restore the named files with the `git checkout -- ...` command it prints. Harness changes arrive only through `next`.
