from conftest import KV


def test_seal_releases_staged_stage(make_project):
    project = make_project(stages=("01",))
    assert (project.root / "tests" / "stage_01_set_get.py").is_file()
    assert (project.root / ".ltb" / "stages" / "01-set-get" / "primer.md").is_file()
    assert not (project.root / ".ltb" / "staging" / "01-set-get").exists()
    assert "tests/stage_01_set_get.py" in (project.root / ".ltb" / "checksums").read_text()


def test_seal_is_deterministic(make_project):
    project = make_project()
    before = (project.root / ".ltb" / "checksums").read_text()
    assert project.run("seal")[0] == 0
    assert (project.root / ".ltb" / "checksums").read_text() == before


def test_seal_refuses_when_harness_tampered(make_project):
    project = make_project()
    test_file = project.root / "tests" / "stage_01_set_get.py"
    test_file.write_text(test_file.read_text() + "\n")
    project.stage("02", "server", (KV / "stage_02_server.py").read_text())
    code, out = project.run("seal")
    assert code == 2
    assert (project.root / ".ltb" / "staging" / "02-server").exists()


def test_seal_allow_changed_for_pressure_stage(make_project):
    project = make_project()
    test_file = project.root / "tests" / "stage_01_set_get.py"
    test_file.write_text(test_file.read_text() + "\n# requirement changed\n")
    code, out = project.run("seal", "--allow-changed", "tests/stage_01_set_get.py")
    assert code == 0, out
    assert project.run("verify")[0] == 0
    assert "allow_changed" in (project.root / ".ltb" / "log" / "seals.jsonl").read_text()


def test_seal_rejects_missing_docstring(make_project):
    project = make_project(stages=())
    project.stage("01", "bad", "def test_x():\n    pass\n")
    code, out = project.run("seal")
    assert code == 4
    assert "no docstring" in out


def test_seal_rejects_rereleasing_a_stage(make_project):
    project = make_project()
    project.stage("01", "again", (KV / "stage_01_set_get.py").read_text())
    code, out = project.run("seal")
    assert code == 4
    assert "already released" in out


def test_status_reports_progress(make_project):
    project = make_project(stages=("01", "02"))
    project.run("test")
    code, out = project.run("status")
    assert code == 0, out
    assert "build your own kv" in out
    assert "3/3 passing" in out
    assert "Primer:  .ltb/stages/02-server/primer.md" in out


def test_api_prints_helpers(make_project):
    code, out = make_project().run("api")
    assert code == 0
    for name in ("run(", "serve(", "expect(", "tmpdir("):
        assert name in out
