# learn-to-build

An agent skill that turns "build your own X" into a practice Project where **you write all the code** and the agent writes everything around it: the research, the plan, the Primers, the black-box tests, and (soon) hints and design reviews.

**Status**: v0.1, early. Expect rough edges; issues welcome.

It exists because AI-assisted work can quietly stop you learning. In a 2026 randomised study, developers who learned a new library with an AI assistant scored 50% on a follow-up quiz against 67% for those who coded by hand ([Shen & Tamkin, 2026](https://arxiv.org/abs/2601.20245)). Learning modes that let the agent write most of the code and leave you a few `TODO`s don't fix that. This skill keeps the agent out of your code and gives you a test loop that runs without AI.

## How it works

1. **`new`**: pick a Goal (a language, a domain, or design skill), an X and a language, and optionally take a two-minute placement check. The agent researches the real X from primary sources, plans a Core path of 20–45 minute Stages (with Pressure Stages and optional Branches), and generates a Project repo.
2. **Each Stage** comes with a Primer (what to build and the concepts behind it, never how to structure your code), a one-minute Concept check (`./ltb check`), public black-box tests, and Hidden tests that show only their description when they fail. Before you see a Stage, a separate agent proves its tests pass on a throwaway Reference solution and fail on your current code.
3. **You code and run `./ltb test`** until it prints `green`. No agent in the loop. `ltb` refuses to grade if the tests were edited.
4. **`hint`** when stuck climbs a Hint ladder one rung at a time (restate the test, point to the spec, ask a question, show an analogous example, pseudocode). It never writes your code.
5. **`review`** when green: a fresh reviewer critiques your structure, flagging over-engineering as readily as a monolith, and shows how the real X does it. You fix each point or defend it.
6. **`next`** adjusts the difficulty from the evidence (hints, review findings, time to green), schedules a Drill for the concept you just built, and releases the next Stage. Pressure Stages bring the real requirement changes X went through, so poor structure hurts. After the Core path, a **Retrospective** compares your architecture with the real X.
7. **`drill`**: spaced, 15-minute rebuilds from memory. Your own files for a concept are removed on a throwaway branch and you restore them until that Stage's tests pass. Due means ready, never owed.

**Assistance modes** let you choose how much code the agent writes, per Project or per Stage: **Solo** (none; rebuild unassisted coding), **Pair** (boilerplate around each Stage's concept, which you then walk through), or **Lead** (you write an Approach, the agent implements it, you walk through and debug it; practises AI-assisted development). In every mode, debugging, Drills, Concept checks and reviews stay yours.

The Project's `AGENTS.md` tells any coding agent what your mode lets it write. In Claude Code and Codex, an optional hook also blocks file edits your mode doesn't allow (Codex asks you to trust it once in `/hooks`).

Design notes, decisions and the research behind them: [docs/design.md](docs/design.md).

## Install

The skill follows the [Agent Skills](https://agentskills.io/specification) format. Install it with the [skills CLI](https://skills.sh):

```sh
npx skills add OWNER/learn-to-build -g          # all your projects; pick your agents when prompted
npx skills add OWNER/learn-to-build -a claude-code -a codex   # this project only, for named agents
```

The CLI writes to each agent's skill directory (`.claude/skills/` for Claude Code, `.agents/skills/` for Codex, Pi, OpenCode and Cursor).

Requirements: `python3` 3.9+, `git`, a POSIX shell (macOS, Linux or WSL), and the toolchain for the language you choose.

## Use

Ask your agent to use learn-to-build, or invoke it directly:

| Harness | Invoke |
|---|---|
| Claude Code, Cursor | `/learn-to-build new sqlite`, then `/learn-to-build hint`, `review`, `next`, `drill` |
| Codex | `$learn-to-build new sqlite` |
| Pi | `/skill:learn-to-build new sqlite` |
| OpenCode | "use learn-to-build to start a new sqlite project" |

## Repo

- `skills/learn-to-build/`: the skill (`SKILL.md`, `references/`, `assets/ltb`, Project templates)
- `docs/`: design, decision records, and the research behind them
- `tests/`: tests for `ltb` and the skill's structure

Development: see [AGENTS.md](AGENTS.md). License: [MIT](LICENSE).
