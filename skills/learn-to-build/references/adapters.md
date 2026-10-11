# Enforcement adapters

The Project's `AGENTS.md` sets what each Assistance mode lets an agent write, by instruction. An adapter adds a mechanical block for one harness: a `PreToolUse` hook that runs a small, read-only Python check (`.ltb/guard.py`) before each file edit or shell command, and stops the ones the current mode does not allow (Solo: none; Pair: only the named files; Lead: only after the Approach exists; never during a Drill). It reads file-editing tools exactly, and shell commands by their common write patterns (redirections, `tee`, `sed -i`, `cp`, `mv`, `rm`, `git checkout`, ...); a program that opens files itself is not covered.

## Ask first

It is optional. **ask** the Learner, saying in two or three lines: what gets installed (the guard script and one hook entry per harness), that it runs on every file edit and shell command in this Project only, and how to remove it (delete the hook entry). Install only on a yes.

## Shared guard

Copy `assets/adapters/ltb-guard.py` to `.ltb/guard.py` in the Project.

## Claude Code

Merge `assets/adapters/claude-code/settings.json` into the Project's `.claude/settings.local.json` (personal settings, not committed): create the file if it is missing, otherwise append its `PreToolUse` entry to the existing `hooks.PreToolUse` list. The hook applies when Claude Code is started from the Project directory; on another machine, offer the adapter again.

## Codex

Merge `assets/adapters/codex/hooks.json` into the Project's `.codex/hooks.json` the same way, replacing `{PROJECT_PATH}` with the Project's path relative to the git root followed by `/` (an empty string when the Project is the repo root). Codex runs project hooks only after the Learner trusts them: tell them to open `/hooks` in Codex once and trust the learn-to-build hook. Codex asks again whenever the hook changes.

## Check

From the Project root, both of these must exit with code 2 (`echo $?`) while the current Stage is in Solo mode:

```sh
echo '{"tool_name":"Write","tool_input":{"file_path":"main.py"},"cwd":"'"$PWD"'"}' | python3 .ltb/guard.py
echo '{"tool_name":"Bash","tool_input":{"command":"echo x > main.py"},"cwd":"'"$PWD"'"}' | python3 .ltb/guard.py
```

**Done when** the Learner said no, or the guard is in place, each chosen harness's hook file is merged, and the check exits 2.

## Other harnesses

No adapter ships yet; `AGENTS.md` is the protection there.
