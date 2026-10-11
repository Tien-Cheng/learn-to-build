#!/usr/bin/env python3
"""PreToolUse hook for Claude Code and Codex: keep file edits to what the Assistance mode allows.

Installed at <project>/.ltb/guard.py. Reads the current Stage's mode from .ltb/config:
Solo blocks every Solution-code edit, Pair allows only the Stage's pair_paths, Lead allows
edits once the Learner's Approach exists, and a running Drill blocks everything.
Exit code 2 blocks the tool call and shows stderr to the agent.

Claude Code sends the edited file in tool_input.file_path (or notebook_path); Codex sends an
apply_patch whose "*** Add/Update/Delete File:" lines name the files.
"""
import configparser
import fnmatch
import json
import os
import re
import sys
from pathlib import Path

HARNESS = ("ltb", "AGENTS.md", ".claude", ".codex", "tests", ".ltb")
PATCH_PATH = re.compile(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+?)\s*$", re.M)


def project_state(project):
    parser = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
    parser.read(str(project / ".ltb" / "config"))
    numbers = sorted(m.group(1) for m in (re.match(r"stage_(\d{2})_", p.name) for p in (project / "tests").glob("stage_*.py")) if m)
    stage = numbers[-1] if numbers else None
    mode = parser.get("assist", stage, fallback=None) if stage else None
    mode = (mode or parser.get("assist", "default", fallback="solo")).strip()
    pair_paths = parser.get("assist", "pair_paths", fallback="").split()
    approach = bool(stage and list((project / ".ltb" / "stages").glob("%s-*/approach.md" % stage)))
    return stage, mode, pair_paths, approach


def verdict(project, file_path, cwd):
    """None to allow, or the reason to block."""
    target = Path(file_path)
    if not target.is_absolute():
        target = Path(cwd) / target
    try:
        rel = target.resolve().relative_to(project.resolve())
    except ValueError:
        return None
    if rel.parts and rel.parts[0] in HARNESS:
        return None
    if (project / ".ltb" / "drill-active.json").is_file():
        return "a Drill is running; the Learner rebuilds from memory alone"
    stage, mode, pair_paths, approach = project_state(project)
    if mode == "lead":
        return None if approach else "Lead mode needs the Learner's Approach (.ltb/stages/%s-*/approach.md) first" % stage
    if mode == "pair" and any(fnmatch.fnmatch(str(rel), g) for g in pair_paths):
        return None
    return "%s is the Learner's Solution code in %s mode" % (rel, mode)


def edited_paths(payload):
    tool_input = payload.get("tool_input") or {}
    for key in ("file_path", "notebook_path"):
        if tool_input.get(key):
            return [tool_input[key]]
    command = tool_input.get("command") or tool_input.get("patch") or tool_input.get("input") or ""
    if isinstance(command, list):
        command = "\n".join(str(c) for c in command)
    return PATCH_PATH.findall(str(command))


def main():
    project = Path(__file__).resolve().parent.parent
    payload = json.load(sys.stdin)
    cwd = payload.get("cwd") or os.getcwd()
    for path in edited_paths(payload):
        reason = verdict(project, path, cwd)
        if reason:
            sys.stderr.write("learn-to-build: %s (see AGENTS.md). Give the next Hint ladder rung instead.\n" % reason)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
