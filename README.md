# learn-to-build

An agent skill that turns "build your own X" into a practice Project where **you write all the code** and the agent writes everything around it: the research, the plan, the Primers, the black-box tests, and (soon) hints and design reviews.

It exists because AI-assisted work can quietly stop you learning. In a 2026 randomised study, developers who learned a new library with an AI assistant scored 50% on a follow-up quiz against 67% for those who coded by hand ([Shen & Tamkin, 2026](https://arxiv.org/abs/2601.20245)). Learning modes that let the agent write most of the code and leave you a few `TODO`s don't fix that. This skill keeps the agent out of your code and gives you a test loop that runs without AI.

## How it works

1. **`new`**: pick a Goal (a language, a domain, or design skill), an X and a language. The agent researches the real X from primary sources, plans a Core path of 20–45 minute Stages, and generates a Project repo.
2. **Each Stage** comes with a Primer (what to build and the concepts behind it, never how to structure your code) and a black-box Test suite.
3. **You code and run `./ltb test`** until it prints `green`. No agent in the loop. `ltb` refuses to grade if the tests were edited.
4. The Project's `AGENTS.md` tells any coding agent that your code is yours: ask for help and you get a hint, not a patch.

Planned next (see [docs/design.md](docs/design.md)): Reference-validated tests, a Hint ladder that never reaches code, Design reviews you can defend against, Pressure Stages that punish poor structure, Hidden tests, Concept checks, a Retrospective comparing your design with the real X, and spaced Drills that make you rebuild pieces from memory.

**Status**: milestone 1 (walking skeleton): `new` and one Stage at a time.

## Install

The skill follows the [Agent Skills](https://agentskills.io/specification) format. Install it with the [skills CLI](https://skills.sh):

```sh
npx skills add OWNER/learn-to-build -g          # all your projects; pick your agents when prompted
npx skills add OWNER/learn-to-build -a claude-code -a codex   # this project only, for named agents
```

The CLI writes to each agent's skill directory (`.claude/skills/` for Claude Code, `.agents/skills/` for Codex, Pi, OpenCode, Cursor and Gemini CLI).

Requirements: `python3` 3.9+, `git`, a POSIX shell (macOS, Linux or WSL), and the toolchain for the language you choose.

## Use

Ask your agent to use learn-to-build, or invoke it directly:

| Harness | Invoke |
|---|---|
| Claude Code, Cursor | `/learn-to-build new sqlite` |
| Codex | `$learn-to-build new sqlite` |
| Pi | `/skill:learn-to-build new sqlite` |
| OpenCode, Gemini CLI | "use learn-to-build to start a new sqlite project" |

## Repo

- `skills/learn-to-build/`: the skill (`SKILL.md`, `references/`, `assets/ltb`, Project templates)
- `docs/`: design, decision records, and the research behind them
- `tests/`: tests for `ltb` and the skill's structure

Development: see [AGENTS.md](AGENTS.md). License: [MIT](LICENSE).
