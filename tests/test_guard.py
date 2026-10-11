import json
import os
import shutil
import subprocess
import sys

from conftest import SKILL

GUARD = SKILL / "assets" / "adapters" / "ltb-guard.py"


def guard(project, tool, path):
    payload = {"tool_name": tool, "tool_input": {"file_path": str(path)}, "cwd": str(project)}
    return call(project, payload)


def call(project, payload):
    proc = subprocess.run([sys.executable, str(project / ".ltb" / "guard.py")],
                          input=json.dumps(payload), capture_output=True, text=True)
    return proc.returncode, proc.stderr


def install(tmp_path, assist=""):
    project = tmp_path / "proj"
    (project / "tests").mkdir(parents=True)
    (project / "tests" / "stage_01_x.py").write_text("")
    (project / ".ltb" / "stages" / "01-x").mkdir(parents=True)
    (project / ".ltb" / "config").write_text("[project]\nx = x\n[commands]\nrun = true\n" + assist)
    shutil.copy(str(GUARD), str(project / ".ltb" / "guard.py"))
    return project


def test_blocks_solution_code(tmp_path):
    project = install(tmp_path)
    code, err = guard(project, "Write", project / "src" / "main.rs")
    assert code == 2 and "Solution code" in err
    assert guard(project, "Edit", "main.py")[0] == 2


def test_allows_harness_and_outside_paths(tmp_path):
    project = install(tmp_path)
    for rel in ("tests/stage_01_x.py", ".ltb/plan.md", "AGENTS.md", "ltb", ".claude/settings.json"):
        assert guard(project, "Write", project / rel)[0] == 0, rel
    assert guard(project, "Write", tmp_path / "elsewhere.txt")[0] == 0


def test_hook_configs_point_at_the_guard():
    for rel in ("claude-code/settings.json", "codex/hooks.json"):
        entry = json.loads((GUARD.parent / rel).read_text())["hooks"]["PreToolUse"][0]
        assert "Write" in entry["matcher"] and ".ltb/guard.py" in entry["hooks"][0]["command"]


def patch(*lines):
    return "*** Begin Patch\n" + "\n".join(lines) + "\n*** End Patch\n"


def test_codex_apply_patch_paths(tmp_path):
    project = install(tmp_path)
    blocked = {"tool_name": "apply_patch", "cwd": str(project),
               "tool_input": {"command": patch("*** Update File: tests/stage_01_x.py", "@@", "-a", "+b",
                                                "*** Add File: src/main.py", "+print(1)")}}
    code, err = call(project, blocked)
    assert code == 2 and "src/main.py" in err
    harness_only = {"tool_name": "apply_patch", "cwd": str(project),
                    "tool_input": {"command": patch("*** Add File: .ltb/plan.md", "+x")}}
    assert call(project, harness_only)[0] == 0


def hook_command(rel):
    return json.loads((GUARD.parent / rel).read_text())["hooks"]["PreToolUse"][0]["hooks"][0]["command"]


def test_claude_hook_uses_project_dir_and_tolerates_missing_guard(tmp_path):
    project = install(tmp_path)
    payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": "main.py"}, "cwd": str(project)})
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    proc = subprocess.run(["sh", "-c", hook_command("claude-code/settings.json")], cwd=str(project), input=payload,
                          capture_output=True, text=True, env=env)
    assert proc.returncode == 2
    env["CLAUDE_PROJECT_DIR"] = str(tmp_path)
    proc = subprocess.run(["sh", "-c", hook_command("claude-code/settings.json")], cwd=str(tmp_path), input=payload,
                          capture_output=True, text=True, env=env)
    assert proc.returncode == 0


def test_codex_hook_uses_git_root_and_project_path(tmp_path):
    project = install(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=str(tmp_path), check=True)
    (project / "src").mkdir()
    command = hook_command("codex/hooks.json").replace("{PROJECT_PATH}", "proj/")
    payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": "main.py"}, "cwd": str(project / "src")})
    proc = subprocess.run(["sh", "-c", command], cwd=str(project / "src"), input=payload, capture_output=True, text=True)
    assert proc.returncode == 2
    missing = command.replace("proj/", "nowhere/")
    proc = subprocess.run(["sh", "-c", missing], cwd=str(project), input=payload, capture_output=True, text=True)
    assert proc.returncode == 0


def test_pair_mode_allows_named_paths_only(tmp_path):
    project = install(tmp_path, "[assist]\ndefault = solo\n01 = pair\npair_paths = cli.py io/*\n")
    assert guard(project, "Write", project / "cli.py")[0] == 0
    assert guard(project, "Write", project / "io" / "read.py")[0] == 0
    code, err = guard(project, "Write", project / "btree.py")
    assert code == 2 and "pair mode" in err


def test_lead_mode_needs_approach(tmp_path):
    project = install(tmp_path, "[assist]\ndefault = lead\n")
    code, err = guard(project, "Write", project / "main.py")
    assert code == 2 and "Approach" in err
    (project / ".ltb" / "stages" / "01-x" / "approach.md").write_text("plan")
    assert guard(project, "Write", project / "main.py")[0] == 0


def test_drill_blocks_every_mode(tmp_path):
    project = install(tmp_path, "[assist]\ndefault = lead\n")
    (project / ".ltb" / "stages" / "01-x" / "approach.md").write_text("plan")
    (project / ".ltb" / "drill-active.json").write_text("{}")
    code, err = guard(project, "Write", project / "main.py")
    assert code == 2 and "Drill" in err


def bash(project, command, cwd=None):
    return call(project, {"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd or project)})


def test_bash_writes_to_solution_code_are_blocked(tmp_path):
    project = install(tmp_path)
    for command in (
        "cat > main.py <<'EOF'\nprint(1)\nEOF",
        "echo x >> src/lib.py",
        "printf 'a' | tee main.py",
        "sed -i '' 's/a/b/' main.py",
        "cp /tmp/solution.py main.py",
        "mv main.py old.py",
        "rm -f main.py",
        "cd src && echo x > lib.py",
        "git checkout -- main.py",
        "git reset --hard",
        "python3 -c 'print(1)' > out.txt",
    ):
        code, err = bash(project, command)
        assert code == 2, command


def test_bash_reads_and_harness_writes_are_allowed(tmp_path):
    project = install(tmp_path)
    for command in (
        "./ltb test",
        "cat main.py | grep def",
        "python3 main.py 2>&1 | head",
        "./ltb test > /tmp/out.txt 2>/dev/null",
        "echo note >> .ltb/log/notes.md",
        "git status && git log --oneline",
        "git add -- ltb .ltb tests && git commit -m 'ltb: x'",
        "sed -n '1,5p' main.py",
        "ls >&2",
    ):
        code, err = bash(project, command)
        assert code == 0, (command, err)


def test_bash_respects_lead_mode(tmp_path):
    project = install(tmp_path, "[assist]\ndefault = lead\n")
    (project / ".ltb" / "stages" / "01-x" / "approach.md").write_text("plan")
    assert bash(project, "cat > main.py <<'EOF'\nx\nEOF")[0] == 0
