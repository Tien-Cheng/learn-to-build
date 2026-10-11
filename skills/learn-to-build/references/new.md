# new: start a Project

Turn "build your own X" into a Project repo with a locked plan and Stage 01 released. The Learner answers questions; you do the research, planning and Harness.

## 1. Check the tools

Run `python3 --version` and `git --version`.

**Done when** both print, and Python is 3.9 or newer. If either is missing, tell the Learner what to install and stop.

## 2. Goal

**ask** what this Project is for:

1. **Language**: learning or regaining a programming language
2. **Domain**: understanding how X works inside
3. **Design**: structuring a mid-size program well

The Goal decides where the difficulty goes (see the Dial entries in the glossary).

**Done when** the Learner has picked one Goal.

## 3. X

If the Learner named an X, use it. Otherwise suggest three that fit the Goal, each with a one-line reason, and **ask**. Any concept works, not only famous projects: "a token-bucket rate limiter" is as valid as "SQLite".

Prefer an X with a clean external interface (a CLI, a wire protocol, a file format), because every Test suite is black-box.

**Done when** X is chosen.

## 4. Language and commands

**ask** which language the Learner wants to write X in; when the Goal is Language, that language is the point of the Project.

Then decide, for that language and X:

- **build**: the command that compiles the Learner's code (empty for interpreted languages).
- **run**: the command that launches the Learner's program. For a server-style X, the program reads its port from the `PORT` environment variable, or the run command contains `{port}`.

Run the toolchain's version command (for example `cargo --version`, `go version`, `node --version`).

**Done when** the version prints and both commands are decided.

## 5. Location

**ask** where the Project should live, suggesting `./<x>` (a short lowercase name). It can be a standalone repo or a folder inside the Learner's existing learning repo.

Create the directory and `.ltb/` inside it. Run `git init` there unless the directory is already inside a git repo.

**Done when** the directory exists and `git rev-parse --show-toplevel` succeeds from it.

## 6. Research

**dispatch** a researcher with [research-brief.md](research-brief.md). Inputs: X, the language, the Goal, and the output directory `<project>/.ltb/research/`.

When it returns, open each file and check it against the brief's **Done when**.

**Done when** `overview.md`, `spec.md`, `architecture.md` and `history.md` exist in `.ltb/research/`, each claim carries a source link, and `history.md` lists at least three requirement changes the real X went through.

## 7. Plan

Follow [planning.md](planning.md) to draft `.ltb/plan.md`. Show the Learner the Core path and **ask** whether they want to cut, reorder or add Stages. Apply their edits once, then add the `Locked:` line.

**Done when** `.ltb/plan.md` exists with a `Locked:` line.

## 8. Generate the Harness and starter

From the skill dir, copy into the Project root:

| From | To |
|---|---|
| `assets/ltb` | `ltb` (then `chmod +x ltb`) |
| `assets/project/AGENTS.md` | `AGENTS.md` |
| `assets/project/gemini-settings.json` | `.gemini/settings.json` |
| `assets/project/gitignore` | append to `.gitignore` |

Write `.ltb/config`:

```ini
[project]
x = <x>
goal = <language | domain | design>
language = <language>
format = 1

[commands]
build = <build command, or empty>
run = <run command>
timeout = 10

[dials]
language = 3
domain = 3
design = 3
```

Dials start at 3 until the Diagnostic exists; the first Design review will set the design Dial.

Write the starter: the language's build file and an entry point that builds and does nothing (for example `Cargo.toml` plus an empty `main`). This boilerplate is the only Solution code you ever write; everything after it is the Learner's. Add the language's build outputs to `.gitignore`.

Run `./ltb seal` to record the first checksums.

**Done when** the build command succeeds, `./ltb verify` prints `Harness ok`, and `./ltb test` prints `No Stages released yet`.

## 9. Stage 01

Follow [stage-release.md](stage-release.md) for the first Core Stage in the plan.

**Done when** `./ltb status` lists Stage 01.

## 10. Commit and hand off

Commit everything in the Project directory, starter included, with the message `ltb: new <x>`.

Then tell the Learner, briefly:

- where the Primer is (from `./ltb status`), and to read it first;
- to write their code and run `./ltb test` until it prints `green`, without AI help; that loop is the practice;
- that the Hint ladder and Design review arrive in a later version of this skill, and until then you will explain concepts and failing tests but leave the code to them.

**Done when** the commit exists and the Learner has the Primer path.
