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

Then **ask** for the default Assistance mode (they can switch per Stage later):

1. **Solo**: you write every line; the agent gives hints (rebuilds unassisted coding)
2. **Pair**: the agent writes boilerplate around each Stage's concept on request; you write the concept and walk through its code
3. **Lead**: you write an Approach, the agent implements it, you walk through and debug it (practises AI-assisted development)

**Done when** the Learner has picked a Goal and a default mode.

## 3. X

If the Learner named an X, use it. Otherwise suggest three that fit the Goal, each with a one-line reason, and **ask**. Any concept works, not only famous projects: "a token-bucket rate limiter" is as valid as "SQLite".

Prefer an X with a clean external interface (a CLI, a wire protocol, a file format), because every Test suite is black-box.

**Done when** X is chosen.

## 4. Language and commands

**ask** which language the Learner wants to write X in; when the Goal is Language, that language is the point of the Project.

Then decide, for that language and X:

- **build**: the command that compiles the Learner's code (empty for interpreted languages).
- **run**: the command that launches the Learner's program.

Both run directly, without a shell: one program and its arguments, no `&&`, pipes or globs. If a build needs more, put it in a script in the starter (for example `build.sh`) and make the command `sh build.sh`. For a server-style X, the program reads its port from the `PORT` environment variable, or the run command contains `{port}`.

Run the toolchain's version command (for example `cargo --version`, `go version`, `node --version`).

**Done when** the version prints and both commands are decided.

## 5. Location

**ask** where the Project should live, suggesting `./<x>` (a short lowercase name). It can be a standalone repo or a folder inside the Learner's existing learning repo.

Create the directory and `.ltb/` inside it. Run `git init` there unless the directory is already inside a git repo.

**Done when** the directory exists and `git rev-parse --show-toplevel` succeeds from it.

## 6. Research

**dispatch** three researchers **in the background**, each with [research-brief.md](research-brief.md). Inputs for each: X, the language, the Goal, the output directory `<project>/.ltb/research/`, and the files it writes:

1. **Spec researcher**: `overview.md` and `spec.md`
2. **History researcher**: `history.md`
3. **Architecture researcher**: `architecture.md`

Tell the Learner, in one line, that research runs for several minutes while you set up the rest.

When a later step waits for a researcher, open the files it wrote and check them against the brief's **Done when**; send it back once with what is missing if they fall short.

**Done when** all three researchers are running (or, without background subagents, have reported).

## 7. Diagnostic

Follow [diagnostic.md](diagnostic.md). Its domain questions need `overview.md`: wait for the Spec researcher before them.

**Done when** you have starting values for the language, domain and design Dials.

## 8. Generate the Harness and starter

From the skill dir, copy into the Project root:

| From | To |
|---|---|
| `assets/ltb` | `ltb` (then `chmod +x ltb`) |
| `assets/project/AGENTS.md` | `AGENTS.md` |
| `assets/project/gitignore` | append to `.gitignore` |
| `assets/project/ignore` | `.ignore` |
| `assets/project/gitattributes` | append to `.gitattributes` |

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

[assist]
default = <solo | pair | lead>

[dials]
language = <from the Diagnostic>
domain = <from the Diagnostic>
design = 3
```

The first Design review sets the design Dial.

Write the starter: the language's build file and an entry point that builds and does nothing (for example `Cargo.toml` plus an empty `main`). This boilerplate is the only Solution code you ever write; everything after it is the Learner's. Add the language's build outputs to `.gitignore`.

Run `./ltb seal` to record the first checksums.

**Done when** the build command succeeds, `./ltb verify` prints `Harness ok`, and `./ltb test` prints `No Stages released yet`.

## 9. Plan

Wait for the Spec and History researchers. Then follow [planning.md](planning.md) to draft `.ltb/plan.md`. Show the Learner the Core path (marking Pressure Stages) and the Branches, and **ask** whether they want to cut, reorder or add Stages. Apply their edits once, then add the `Locked:` line.

**Done when** `.ltb/plan.md` exists with a `Locked:` line.

## 10. Stage 01

Follow [stage-release.md](stage-release.md) for the first Core Stage in the plan.

**Done when** `./ltb status` lists Stage 01.

## 11. Enforcement adapter

Offer the enforcement adapter in [adapters.md](adapters.md) for the harnesses the Learner uses (Claude Code and Codex have one), and install it if they agree.

**Done when** the Learner has answered.

## 12. Commit and hand off

Wait for the Architecture researcher. Then commit everything in the Project directory, starter included, with the message `ltb: new <x>`.

Then tell the Learner, briefly:

- where the Primer is (from `./ltb status`), and to read it first;
- to run `./ltb check 01` (a one-minute Concept check that unlocks the tests);
- what their mode means for this Stage: in Solo, they write the code; in Pair, they name the files you may write (`./ltb assist pair --paths <files>`); in Lead, they write `.ltb/stages/01-<slug>/approach.md` first, then ask you to implement it;
- to run `./ltb test` until it prints `green`; that loop, and any debugging, is theirs;
- to come back with `hint` when stuck (one rung at a time, never code), `review` when green, then `next`.

**Done when** the commit exists, includes all four files in `.ltb/research/`, and the Learner has the Primer path.
