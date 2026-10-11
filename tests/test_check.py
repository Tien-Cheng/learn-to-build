import json

from conftest import KV


def checked_project(make_project):
    project = make_project(stages=())
    d = project.stage("01", "set-get", (KV / "stage_01_set_get.py").read_text())
    (d / "check.src.json").write_text(json.dumps({"questions": [
        {"id": "q1", "kind": "choice", "prompt": "Missing key?", "choices": ["a) nothing", "b) (nil)"],
         "answers": ["b"], "on_miss": "Primer: Replies"},
        {"id": "q2", "kind": "text", "prompt": "Output of set a 1?", "answers": ["OK"], "on_miss": "Primer: set"},
    ]}))
    assert project.run("seal")[0] == 0
    return project


def test_normalisation(ltb):
    assert ltb.normalize_answer("choice", " B) ") == "b"
    assert ltb.normalize_answer("text", "  hello   world ") == "hello world"
    assert ltb.normalize_answer("number", "4096.0") == "4096"
    assert ltb.normalize_answer("number", "0.50") == "0.5"


def test_tests_locked_until_check_attempted(make_project):
    project = checked_project(make_project)
    code, out = project.run("test")
    assert code == 1
    assert "locked until you answer its Concept check" in out
    code, out = project.run("check", "01", "--question", "q1", "--answer", "a")
    assert code == 0
    assert "not quite: revisit Primer: Replies" in out
    code, out = project.run("test")
    assert code == 0, out


def test_correct_answer_and_log(make_project):
    project = checked_project(make_project)
    code, out = project.run("check", "--question", "q2", "--answer", " ok ".upper())
    assert "correct" in out and "not quite" not in out
    log = (project.root / ".ltb" / "log" / "checks.jsonl").read_text()
    assert '"correct": true' in log


def test_status_flags_unanswered_check(make_project):
    project = checked_project(make_project)
    assert "Concept check unanswered" in project.run("status")[1]
