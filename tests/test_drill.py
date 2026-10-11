import datetime
import json
import os
import subprocess

from conftest import KV


def git(root, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True, check=True).stdout


def committed_project(make_project):
    project = make_project(stages=("01",))
    git(project.root, "init", "-q", "-b", "main")
    git(project.root, "config", "user.email", "t@example.com")
    git(project.root, "config", "user.name", "t")
    (project.root / ".gitignore").write_text((KV.parent.parent.parent / "skills" / "learn-to-build" / "assets" / "project" / "gitignore").read_text())
    git(project.root, "add", "-A")
    git(project.root, "commit", "-q", "-m", "init")
    return project


def at(iso):
    return dict(os.environ, LTB_NOW=iso)


def test_schedule_maths(ltb):
    t0 = datetime.datetime(2026, 10, 1, tzinfo=datetime.timezone.utc)
    data = {"gaps": [1, 3, 7, 21], "drills": [
        {"concept": "a", "gap_index": 0, "anchor": t0.isoformat()},
        {"concept": "b", "gap_index": 2, "anchor": t0.isoformat()},
    ]}
    assert ltb.pick_drill(data, t0 + datetime.timedelta(hours=12)) is None
    assert ltb.pick_drill(data, t0 + datetime.timedelta(days=2))["concept"] == "a"
    d = data["drills"][1]
    ltb.advance(d, True, data["gaps"], t0)
    assert d["gap_index"] == 3
    ltb.advance(d, True, data["gaps"], t0)
    assert d["gap_index"] == 3
    ltb.advance(d, False, data["gaps"], t0)
    assert d["gap_index"] == 0


def test_drill_pass_cycle(make_project):
    project = committed_project(make_project)
    code, out = project.run("drill", "add", "--concept", "kv-protocol", "--stage", "01", "--paths", "kv.py",
                            env=at("2026-10-01T09:00:00+00:00"))
    assert code == 0, out
    git(project.root, "add", "-A")
    git(project.root, "commit", "-q", "-m", "drill added")
    assert "ready 2026-10-02" in project.run("drill", "list", env=at("2026-10-01T10:00:00+00:00"))[1]

    day2 = at("2026-10-02T10:00:00+00:00")
    code, out = project.run("drill", "start", env=day2)
    assert code == 0, out
    assert not (project.root / "kv.py").exists()
    assert git(project.root, "branch", "--show-current").strip() == "drill/kv-protocol"
    assert "ACTIVE" in project.run("status", env=day2)[1]
    assert project.run("drill", "check", env=day2)[0] == 1

    (project.root / "kv.py").write_text((KV / "kv.py").read_text())
    code, out = project.run("drill", "check", env=at("2026-10-02T10:09:00+00:00"))
    assert code == 0, out
    code, out = project.run("drill", "finish", env=at("2026-10-02T10:20:00+00:00"))
    assert code == 0, out
    assert "PASS in 9:00" in out
    assert git(project.root, "branch", "--show-current").strip() == "main"
    assert "drill/kv-protocol" not in git(project.root, "branch")
    assert git(project.root, "status", "--porcelain") == ""
    data = json.loads((project.root / ".ltb" / "log" / "drills.json").read_text())
    assert data["drills"][0]["gap_index"] == 1
    assert (project.root / "kv.py").read_text() == (KV / "kv.py").read_text()


def test_drill_timeout_fails_and_discard_records_nothing(make_project):
    project = committed_project(make_project)
    project.run("drill", "add", "--concept", "kv", "--stage", "01", "--paths", "kv.py", env=at("2026-10-01T09:00:00+00:00"))
    git(project.root, "add", "-A")
    git(project.root, "commit", "-q", "-m", "drill added")

    project.run("drill", "start", env=at("2026-10-03T10:00:00+00:00"))
    code, out = project.run("drill", "discard", env=at("2026-10-03T10:05:00+00:00"))
    assert code == 0 and "nothing recorded" in out
    data = json.loads((project.root / ".ltb" / "log" / "drills.json").read_text())
    assert data["drills"][0]["history"] == []

    project.run("drill", "start", env=at("2026-10-03T11:00:00+00:00"))
    code, out = project.run("drill", "finish", env=at("2026-10-03T11:30:00+00:00"))
    assert code == 0, out
    data = json.loads((project.root / ".ltb" / "log" / "drills.json").read_text())
    assert data["drills"][0]["history"][0]["result"] == "fail"
    assert data["drills"][0]["gap_index"] == 0


def test_drill_needs_clean_tree(make_project):
    project = committed_project(make_project)
    project.run("drill", "add", "--concept", "kv", "--stage", "01", "--paths", "kv.py", env=at("2026-10-01T09:00:00+00:00"))
    code, out = project.run("drill", "start", "kv", env=at("2026-10-05T09:00:00+00:00"))
    assert code == 4 and "clean tree" in out


def test_unit_command_runs_with_stages(make_project):
    project = make_project()
    project.write_config(extra="unit = false")
    code, out = project.run("test")
    assert code == 1
    assert "Skeleton unit tests" in out
