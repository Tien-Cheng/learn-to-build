import json

from conftest import KV

HIDDEN = '''from ltb import run, expect


def test_overwrite():
    """set on an existing key replaces its value."""
    r = run(stdin="set k SENTINEL_IN\\nset k 2\\nget k\\n")
    expect(r.stdout, "OK\\nOK\\n2\\n")
'''


def stage_with_hidden(make_project, solution="kv"):
    project = make_project(solution=solution, stages=())
    d = project.stage("01", "set-get", (KV / "stage_01_set_get.py").read_text())
    (d / "hidden.py").write_text(HIDDEN)
    code, out = project.run("seal")
    assert code == 0, out
    return project


def test_encoding_round_trips_and_is_deterministic(ltb):
    stages = {"03": {"slug": "x", "source": "print('hi')\n"}}
    text = ltb.encode_hidden(stages)
    assert text.startswith("LTB-HIDDEN 1\n")
    assert "print" not in text
    assert ltb.decode_hidden(text) == stages
    assert ltb.encode_hidden(stages) == text


def test_seal_moves_hidden_tests_into_hidden_bin(make_project):
    project = stage_with_hidden(make_project)
    assert (project.root / ".ltb" / "hidden.bin").is_file()
    assert ".ltb/hidden.bin" in (project.root / ".ltb" / "checksums").read_text()
    assert "SENTINEL_IN" not in (project.root / ".ltb" / "hidden.bin").read_text()
    code, out = project.run("test")
    assert code == 0, out
    assert "4/4 (1 hidden)" in out


def test_hidden_failure_shows_description_only(make_project):
    project = stage_with_hidden(make_project, solution="starter")
    code, out = project.run("test", "-v")
    assert code == 1
    assert "[hidden] set on an existing key replaces its value. (wrong result)" in out
    assert "SENTINEL_IN" not in out
    assert "test_overwrite" not in out


def test_reference_run_includes_staged_hidden(make_project, tmp_path):
    project = make_project(solution="kv", stages=())
    d = project.stage("01", "set-get", (KV / "stage_01_set_get.py").read_text())
    (d / "hidden.py").write_text(HIDDEN)
    code, out = project.run("test", "--staging", "--stage", "01")
    assert code == 0, out
    assert "(1 hidden)" in out


def test_seal_hashes_concept_check(make_project):
    project = make_project(stages=())
    d = project.stage("01", "set-get", (KV / "stage_01_set_get.py").read_text())
    (d / "check.src.json").write_text(json.dumps({"questions": [
        {"id": "q1", "kind": "choice", "prompt": "What does get print for a missing key?",
         "choices": ["a) nothing", "b) (nil)"], "answers": ["b"], "on_miss": "Primer: Replies"},
    ]}))
    assert project.run("seal")[0] == 0
    sealed = (project.root / ".ltb" / "stages" / "01-set-get" / "check.json").read_text()
    assert '"b"' not in sealed and "(nil)" in sealed
    assert not (project.root / ".ltb" / "staging").exists() or not any((project.root / ".ltb" / "staging").iterdir())
    assert ".ltb/stages/01-set-get/check.json" in (project.root / ".ltb" / "checksums").read_text()
