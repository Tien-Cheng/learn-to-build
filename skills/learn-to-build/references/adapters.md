# Enforcement adapters

The Project's `AGENTS.md` sets what each Assistance mode lets an agent write, by instruction. An adapter adds a mechanical block for one harness: a hook that stops file edits the current mode does not allow (Solo: none; Pair: only the named files; Lead: only after the Approach exists; never during a Drill). Shell commands that write files are not covered. It is optional: offer it, explain it in two lines, and respect a no.

## Shared guard

Copy `assets/adapters/ltb-guard.py` to `.ltb/guard.py` in the Project. Both adapters call it; it finds the Project from its own location.

## Claude Code

Merge `assets/adapters/claude-code/settings.json` into the Project's `.claude/settings.json`: create the file if it is missing; otherwise append its `PreToolUse` entry to the existing `hooks.PreToolUse` list. The hook applies when Claude Code is started from the Project directory or below it.

## Codex

Merge `assets/adapters/codex/hooks.json` into the Project's `.codex/hooks.json` the same way. Codex runs project hooks only after the Learner trusts them: tell them to open `/hooks` in Codex once and trust the learn-to-build hook (and to trust the project if asked). Codex re-asks whenever the hook changes.

## Check

From the Project root, both of these must exit with code 2 (`echo $?`) while the current Stage is in Solo mode:

```sh
echo '{"tool_name":"Write","tool_input":{"file_path":"main.py"},"cwd":"'"$PWD"'"}' | python3 .ltb/guard.py
printf '%s' '{"tool_name":"apply_patch","tool_input":{"command":"*** Begin Patch\n*** Add File: main.py\n+x\n*** End Patch"},"cwd":"'"$PWD"'"}' | python3 .ltb/guard.py
```

**Done when** the guard is in place, each chosen harness's hook file is merged, and the check exits 2.

## Other harnesses

No adapter ships yet; `AGENTS.md` is the protection there.
