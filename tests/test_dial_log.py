import json
import os

from conftest import KV


def test_dial_rewrites_config_and_logs(make_project):
    project = make_project()
    code, out = project.run("dial", "design", "2", "--evidence", "monolith in Stage 01 review")
    assert code == 0, out
    assert "design = 2" in (project.root / ".ltb" / "config").read_text()
    entry = json.loads((project.root / ".ltb" / "log" / "dials.jsonl").read_text().splitlines()[-1])
    assert entry["from"] == 3 and entry["to"] == 2 and "monolith" in entry["evidence"]


def test_dial_rejects_bad_values(make_project):
    project = make_project()
    assert project.run("dial", "design", "9")[0] == 4
    assert project.run("dial", "vibes", "3")[0] == 4


def test_log_hint_and_status(make_project):
    project = make_project()
    assert project.run("log", "hint", "--stage", "1", "--test", "test_get_missing", "--rung", "2")[0] == 0
    entry = json.loads((project.root / ".ltb" / "log" / "hints.jsonl").read_text())
    assert entry["stage"] == "01" and entry["rung"] == 2
    assert "highest rung 2" in project.run("status")[1]


def test_summary_minutes_to_green(make_project):
    project = make_project(solution="starter")
    env = dict(os.environ, LTB_NOW="2026-10-11T10:00:00+08:00")
    project.run("test", env=env)
    (project.root / "kv.py").write_text((KV / "kv.py").read_text())
    env["LTB_NOW"] = "2026-10-11T10:25:00+08:00"
    project.run("test", env=env)
    code, out = project.run("log", "summary", "--stage", "01")
    assert code == 0
    assert "2 runs, 25 minutes" in out
