#!/usr/bin/env python3
"""PreToolUse hook for Claude Code and Codex: keep file edits to what the Assistance mode allows.

Installed at <project>/.ltb/guard.py. Reads the current Stage's mode from .ltb/config:
Solo blocks every Solution-code edit, Pair allows only the Stage's pair_paths, Lead allows
edits once the Learner's Approach exists, and a running Drill blocks everything.
Exit code 2 blocks the tool call and shows stderr to the agent.

Claude Code sends the edited file in tool_input.file_path (or notebook_path); Codex sends an
apply_patch whose "*** Add/Update/Delete File:" lines name the files. For shell commands
(Bash), the guard finds the common ways a command writes or removes files: redirections,
tee, sed/perl -i, cp/mv/install/ln/rm/touch/truncate, dd of=, and git commands that overwrite
the working tree. A program that opens files itself (python -c, a script) is not covered.
"""
import configparser
import fnmatch
import json
import os
import re
import shlex
import sys
from pathlib import Path

HARNESS = ("ltb", "AGENTS.md", ".ignore", ".gitattributes", ".claude", ".codex", "tests", ".ltb")
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


SEPARATORS = {";", "&&", "||", "|", "&", "\n", "(", ")"}
REDIRECTS = {">", ">>", ">|", "&>", "&>>"}
OVERWRITE_GIT = {"checkout", "restore", "reset", "stash", "clean", "switch", "rm", "mv", "apply", "am", "merge", "rebase", "pull"}


def split_segments(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>")
    lexer.whitespace_split = True
    lexer.commenters = ""
    segment = []
    try:
        for token in lexer:
            if token in SEPARATORS:
                if segment:
                    yield segment
                segment = []
            else:
                segment.append(token)
    except ValueError:
        pass
    if segment:
        yield segment


def segment_targets(words):
    """Paths one simple command writes or removes, plus a new cwd if it is a cd."""
    targets, plain = [], []
    i = 0
    while i < len(words):
        w = words[i]
        if w in REDIRECTS or (w.endswith(">") and w.rstrip(">").isdigit()):
            if i + 1 < len(words) and not words[i + 1].startswith("&"):
                targets.append(words[i + 1])
            i += 2
            continue
        if w in ("<", "<<", "<<<", ">&", "<&"):
            i += 2
            continue
        plain.append(w)
        i += 1
    while plain and ("=" in plain[0] and not plain[0].startswith("-") or plain[0] in ("sudo", "command", "env", "nohup", "time")):
        plain = plain[1:]
    if not plain:
        return targets, None
    cmd, args = os.path.basename(plain[0]), plain[1:]
    files = [a for a in args if not a.startswith("-")]
    if cmd == "cd":
        return targets, (files[0] if files else None)
    if cmd == "tee":
        targets += files
    elif cmd in ("sed", "gsed", "perl") and any(a.startswith("-i") or a == "--in-place" or a.startswith("-pi") for a in args):
        has_script_flag = "-e" in args or "--expression" in args
        targets += files if has_script_flag else files[1:]
    elif cmd in ("cp", "install", "ln") and len(files) >= 2:
        targets.append(files[-1])
    elif cmd == "mv" and len(files) >= 2:
        targets += files
    elif cmd in ("rm", "touch", "truncate", "unlink", "shred"):
        targets += files
    elif cmd == "dd":
        targets += [a[3:] for a in args if a.startswith("of=")]
    elif cmd == "git" and args:
        sub = next((a for a in args if not a.startswith("-")), "")
        if sub in OVERWRITE_GIT:
            after = args[args.index("--") + 1:] if "--" in args else []
            targets += after or ["."]
    return targets, None


def bash_targets(command, cwd):
    """(path, cwd) pairs a shell command writes or removes."""
    found = []
    for words in split_segments(command):
        targets, new_cwd = segment_targets(words)
        found += [(t, cwd) for t in targets if t != "/dev/null"]
        if new_cwd:
            cwd = new_cwd if os.path.isabs(new_cwd) else os.path.join(cwd, new_cwd)
    return found


def edited_paths(payload, cwd):
    """(path, cwd) pairs the tool call would write."""
    tool_input = payload.get("tool_input") or {}
    for key in ("file_path", "notebook_path"):
        if tool_input.get(key):
            return [(tool_input[key], cwd)]
    command = tool_input.get("command") or tool_input.get("patch") or tool_input.get("input") or ""
    if isinstance(command, list):
        command = "\n".join(str(c) for c in command)
    command = str(command)
    if payload.get("tool_name") in ("Bash", "shell", "local_shell", "exec_command"):
        return bash_targets(command, cwd)
    return [(p, cwd) for p in PATCH_PATH.findall(command)]


def main():
    project = Path(__file__).resolve().parent.parent
    payload = json.load(sys.stdin)
    cwd = payload.get("cwd") or os.getcwd()
    for path, where in edited_paths(payload, cwd):
        reason = verdict(project, path, where)
        if reason:
            sys.stderr.write("learn-to-build: %s (see AGENTS.md). Give the next Hint ladder rung instead.\n" % reason)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
