import json
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


def test_hook_command_finds_guard_from_subdirectory(tmp_path):
    project = install(tmp_path)
    (project / "src").mkdir()
    command = json.loads((GUARD.parent / "codex" / "hooks.json").read_text())["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": "main.py"}, "cwd": str(project / "src")})
    proc = subprocess.run(["sh", "-c", command], cwd=str(project / "src"), input=payload, capture_output=True, text=True)
    assert proc.returncode == 2
    outside = subprocess.run(["sh", "-c", command], cwd=str(tmp_path), input=payload, capture_output=True, text=True)
    assert outside.returncode == 0


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
