def test_green_on_reference(make_project):
    project = make_project(stages=("01", "02"))
    code, out = project.run("test")
    assert code == 0, out
    assert "green: 4 passed" in out


def test_red_on_starter(make_project):
    project = make_project(solution="starter")
    code, out = project.run("test")
    assert code == 1
    assert "A value stored with set is returned by get." in out
    assert "expected" in out and "actual" in out


def test_no_stages_released(make_project):
    project = make_project(stages=())
    code, out = project.run("test")
    assert code == 0
    assert "No Stages released" in out


def test_timeout_is_reported(make_project):
    project = make_project(stages=())
    project.stage("01", "hang", "from ltb import run\n\ndef test_hang():\n    '''hangs'''\n    run(['sleep'], timeout=0.5)\n")
    assert project.run("seal")[0] == 0
    code, out = project.run("test")
    assert code == 1
    assert "(timeout)" in out


def test_crash_shows_input_and_message(make_project):
    project = make_project(stages=())
    project.stage("01", "crash", "from ltb import run, expect\n\ndef test_c():\n    '''exits cleanly'''\n    r = run(['crash'])\n    expect(r.code, 0, 'exit code')\n")
    assert project.run("seal")[0] == 0
    code, out = project.run("test")
    assert code == 1
    assert "args:  crash" in out
    assert "exit code" in out


def test_build_failure_exits_3(make_project):
    project = make_project()
    project.write_config(build="false")
    code, out = project.run("test")
    assert code == 3
    assert "Build failed" in out


def test_stage_selection(make_project):
    project = make_project(stages=("01", "02"))
    code, out = project.run("test", "--stage", "2")
    assert code == 0
    assert "Stage 02" in out and "Stage 01" not in out


def test_run_log_written_and_skipped_for_external_config(make_project):
    project = make_project()
    project.run("test")
    log = project.root / ".ltb" / "log" / "runs.jsonl"
    assert len(log.read_text().splitlines()) == 1


def test_external_config_runs_in_its_own_directory(make_project, tmp_path):
    """Reference validation: tests run against a program living outside the Project."""
    project = make_project(solution="starter")
    ref = tmp_path / "ref"
    ref.mkdir()
    from conftest import KV
    import shutil
    import sys

    shutil.copy(str(KV / "kv.py"), str(ref / "kv.py"))
    (ref / "ltb.ini").write_text("[project]\nx = kv\n[commands]\nrun = %s kv.py\n" % sys.executable)
    code, out = project.run("test", "--config", str(ref / "ltb.ini"))
    assert code == 0, out
    assert not (project.root / ".ltb" / "log" / "runs.jsonl").exists()


def test_regression_flagged_only_when_previously_green(make_project):
    project = make_project(stages=("01",))
    code, out = project.run("test")
    assert code == 0 and "regression" not in out
    (project.root / "kv.py").write_text((project.root / "kv.py").read_text().replace('"(nil)"', '"nil"'))
    code, out = project.run("test")
    assert code == 1
    assert "regression (was green)" in out


def test_skip_does_not_fail_the_run(make_project):
    project = make_project(stages=())
    project.stage("01", "env", "from ltb import run, skip\n\ndef test_needs_tool():\n    '''uses an optional tool'''\n    skip('tool not installed')\n\ndef test_real():\n    '''real behaviour'''\n    assert run(stdin='get x\\n').stdout == '(nil)\\n'\n")
    assert project.run("seal")[0] == 0
    code, out = project.run("test")
    assert code == 0, out
    assert "skipped: Stage 01: uses an optional tool (tool not installed)" in out
    assert "green: 1 passed, 0 failing, 1 skipped" in out
