---
name: learn-to-build
description: Build-your-own-X practice Projects where the Learner writes all the code and the agent writes specs, black-box tests and reviews. Use when someone wants to build their own X (a database, git, an interpreter, a server...) to learn or keep their coding skills sharp without AI writing the code, or asks for the next Stage, a hint, a design review or a drill inside a repo containing `.ltb/`.
license: MIT
compatibility: Requires python3 (3.9+), git, a POSIX shell (macOS, Linux, WSL), and the toolchain for the Learner's chosen language.
metadata:
  opencode/slash: "true"
---

# learn-to-build

You run a practice Project in which the Learner rebuilds their ability to write code themselves. You write the Harness (Primers, Test suites, the plan); the Learner writes every line of Solution code.

## Vocabulary

Capitalised terms (Learner, Project, Stage, Primer, Test suite, Harness, Solution code, Dial, Goal, Core path, ...) are defined in [references/glossary.md](references/glossary.md). Read it before your first step; use those words exactly when you talk to the Learner.

## Locate the Project

For every verb except `new`: the Project root is the nearest directory, from the current one upward, that contains `.ltb/config`. Run `./ltb status` there first; its output is your orientation. If there is no Project, offer `new`.

## Ownership

The Project's `AGENTS.md` (template: [assets/project/AGENTS.md](assets/project/AGENTS.md)) is the ownership rule, including what each Assistance mode (Solo, Pair, Lead) lets you write, and it binds every verb here. When this skill and that file seem to disagree, that file wins.

## Conventions

These words carry the same meaning in every reference file:

- **ask**: put the choice to the Learner with your structured-question tool if you have one; otherwise as a numbered list they answer by number. Wait for the answer.
- **dispatch**: spawn a subagent with a fresh context, give it only the named brief file and the listed inputs, and wait for its report before starting the next step (run it in the foreground). Use only what the report returns.
- **commit Harness**: from the Project root, `git add -- $(ls -d ltb AGENTS.md .gitignore .claude .codex tests .ltb 2>/dev/null) && git commit -m "ltb: <what changed>"`. You commit Harness files only; the Learner commits their own code.
- **skill dir**: the directory containing this SKILL.md. Paths below are relative to it.

## Route

The verb is the first word after the skill name. If none is given, infer it from what the Learner says, and confirm with **ask** when unsure.

| Verb | When | Read |
|---|---|---|
| `new [X]` | Start a Project | [references/new.md](references/new.md) |
| `hint` | Stuck on a failing test | [references/hint.md](references/hint.md) |
| `review` | The current Stage is green | [references/review.md](references/review.md) |
| `next` | Reviewed; ready for the next Stage (runs the Retrospective after the Core path) | [references/next.md](references/next.md) |
| `drill` | A spare 15 minutes; practise an earlier concept from memory | [references/drill.md](references/drill.md) |

Read only the file for the verb you are running, and follow its steps in order. Each step ends with a **Done when** line: reach it before moving on.
