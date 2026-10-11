# learn-to-build: v1 design

A portable agent skill that turns "build your own X" into a Project the Learner writes entirely themselves, with black-box Test suites per Stage and a Design review after each one. Terms are defined in [`GLOSSARY.md`](../GLOSSARY.md); the irreversible calls are in [`docs/adr/`](adr/).

## Why

- At AI-heavy jobs the agent does the part you would have learned from. The strongest evidence is for **Acquisition**: unrestricted AI help while learning cut later unaided performance (Anthropic 2026: 50% vs 67%, biggest gap in debugging); hint-not-answer guardrails removed most of the harm. **Atrophy** is plausible but unproven. See [learning science](research/ai-skill-atrophy-and-learning-science.md).
- Claude Code's Learning style hands the Learner 2–10 lines per 20+ the agent writes, and nothing enforces it. CodeCrafters gets authorship right but its tests never judge design, and it has paused new challenges. `0sakura721/build-your-own-x-skill` is a tutorial index. See [existing skills](research/existing-skills.md), [landscape](research/learning-tools-landscape.md).

## Principles

1. The Learner writes Solution code; the agent writes the Harness, plus only what the Learner's chosen Assistance mode allows ([ADR 0001](adr/0001-learner-authors-all-solution-code.md)).
2. Tests judge behaviour through X's external interface; Design reviews judge structure ([ADR 0002](adr/0002-black-box-test-suites.md)).
3. The code → test → fix loop runs with no agent at all (`./ltb test`). The agent appears only at Stage boundaries.
4. Struggle before explanation for structure; explanation before struggle for specs (Primer = "what", review = "how real X does it").
5. Practice tool, not exam: prevent accidents, don't police a Learner who chooses to bypass.
6. Calibrate from evidence, and announce every adjustment.
7. Avoid over-engineering in the skill and in what the Design review rewards.

## Assistance modes

The Learner picks how much Solution code the agent may write, per Project at `new` and per Stage at `next`: **Solo** (none, the default), **Pair** (boilerplate around the Stage's concept in files the Learner names; the Learner walks through it), **Lead** (the agent implements the Learner's written Approach; the Learner walks through and debugs it). Debugging, Drills, Concept checks and Design reviews stay the Learner's in every mode; agent edits are logged; Dials rise only on evidence from code the Learner wrote. See [ADR 0001](adr/0001-learner-authors-all-solution-code.md).

## Flow

Invoked as `/learn-to-build <verb>`; one router skill, each verb's instructions in its own disclosed file.

### `new [X]`

1. **Goal**: language, domain, or design. With no X given, suggest one fitting the Goal.
2. **Language**: any that produces a runnable program; the agent works out build/run commands into `.ltb/config`.
3. **Diagnostic** (skippable; built in milestone 3, until then Dials start at 3/3/3): adaptive "what does this print" quiz for language fluency (3–6 questions), 2–3 concept questions for domain. Design skill is read from Stage 1's Design review. Use the harness's structured-question tool if it has one, numbered options otherwise.
4. **Research** X with subagents into `.ltb/research/` (plain text, marked spoilers), citing primary sources. Includes real requirement changes X went through, to seed Pressure Stages.
5. **Plan**: Core path plus Branches, Pressure Stages placed at Branch points. The Learner may cut, reorder or add once; then it locks.
6. **Generate** the Project repo at a Learner-chosen path (default `./<x>`), standalone or inside a learning monorepo.

### Stage loop

1. `next` generates the Stage just in time, through a Stage author subagent so the tutoring agent never holds Hidden test inputs or Concept-check answers: Primer (adapted to the Dials; includes a "language you'll need" section when the Goal is language), Concept check, public tests, Hidden tests. A Skeleton is included while the design Dial is low and is withdrawn over later Stages.
2. A subagent writes a Reference solution in a temp dir, confirms the Test suite passes on it and fails on the current code, then deletes it ([ADR 0003](adr/0003-reference-solutions-validate-tests.md)). The tutoring agent never sees it.
3. Learner answers the Concept check (1–3 questions; a wrong answer points back to the Primer, never blocks).
4. Learner codes and runs `./ltb test`: all Stages 1..N, public and Hidden. Hidden failures show the description, not the input. `./ltb` refuses to grade if Harness checksums changed; only `next` updates them.
5. `hint` climbs the Hint ladder one rung per request: restate the failing test → concept/doc pointer → guiding question → worked example on an analogous problem → pseudocode. Never code for this Stage. Logged.
6. `review` once green: a fresh subagent sees only the code, Stage spec, research notes and hint log. Each point is fixed or Defended; the agent gets one rebuttal, then the Learner's reply is final. Calibrated to this Stage, so over-engineering is flagged too. Closes with how the real X solves it.
7. `next` adjusts the Dials from hints, review findings and Concept-check misses, announces the change, creates a Drill for the reviewed Stage's concept, mentions one ready Drill, and generates the next Stage. Stages are numbered in release order (`tests/stage_NN_slug.py`); `plan.md` maps each number to its Core or Branch entry.

### Retrospective

Required after the last Core Stage: whole-codebase review, architecture side by side with the real X, Defences revisited against later Pressure Stages, three design lessons, Drills seeded for concepts spanning several Stages. Branches remain open afterwards.

### `drill`

Offers one ready Drill, the most overdue relative to its gap (1 → 3 → 7 → 21 days; pass advances, fail resets). On a `drill/<concept>` branch the Learner's own files for that concept are deleted; 15 minutes to restore them from memory until the original Stage's tests pass; branch discarded. "Due" means ready, never owed: no backlog, streaks or missed counts. Abandoning a Drill (`ltb drill discard`) records nothing; running out of time is a fail.

## Project repo

```
<x>/
├── AGENTS.md          # Solution code paths are Learner-owned; agent limited to hints and reviews
├── ltb                # Python 3, stdlib only: test runner, checksum guard, Hidden test decoder
├── tests/             # public black-box tests, Stages 1..N
├── <learner's code>
└── .ltb/
    ├── config         # build/run commands, Goal, Dials
    ├── plan.md        # Core path, Branches, Stage status
    ├── stages/        # Primers, Concept checks (answers hashed)
    ├── hidden.bin     # Hidden tests, compressed and encoded
    ├── checksums
    ├── research/      # spoilers
    └── log/           # hints, review findings, Defences, Dial changes, Drill schedule; raw test-run log gitignored
```

Committed in full except the raw test-run log (summarised per Stage into the Dial log at each `next`), so progress is git history and the Project resumes on any machine. Optional per-harness hard enforcement (Claude Code hooks, deny rules and sandbox first) is offered at `new`; see [harness portability](research/harness-portability.md).

## Skill repo

This repo holds only the skill, at `skills/learn-to-build/`, installed with the skills CLI (`npx skills add <owner>/learn-to-build`), which writes to both `.claude/skills/` (Claude Code) and `.agents/skills/` (Codex, Pi, OpenCode, Cursor). Standard SKILL.md frontmatter only. Assume the harness can spawn subagents. POSIX only (macOS, Linux, WSL).

## Build order

Each step dogfooded on SQLite before the next.

1. Walking skeleton: `new` (plan), one Stage with Primer and public tests, `./ltb test`, AGENTS.md.
2. Reference validation, Design review with Defences, Hint ladder.
3. Pressure Stages, Hidden tests, Concept checks.
4. Drills, Skeleton, Branches, Retrospective.

## Success

v1 works if the author finishes the SQLite Core path and Retrospective, passes at least 3 Drills after gaps of 7 days or more, and can say the Design reviews changed how they structure code; and if a second Learner runs one Project in another language and the Dials visibly change the experience. No tracking beyond `.ltb/` history.

## Later

- **v2 Replay**: Projects generated from a concept the Learner saw AI implement at work, rebuilt outside the work codebase. The `new` generator should already accept any concept, not only a famous X.
