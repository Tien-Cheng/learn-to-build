import json


def stage_with_unit(project, number="02", slug="framing"):
    d = project.stage(number, slug, "from ltb import run\n\ndef test_x():\n    '''x'''\n    run(stdin='get a\\n')\n")
    (d / "unit" / "tests" / "unit").mkdir(parents=True)
    (d / "unit" / "tests" / "unit" / "test_framing.py").write_text("print('unit ok')\n")
    (d / "unit.json").write_text(json.dumps({"command": "python3 tests/unit/test_framing.py"}))
    return d


def test_seal_installs_and_protects_unit_tests(make_project):
    project = make_project(stages=("01",))
    stage_with_unit(project)
    code, out = project.run("seal")
    assert code == 0, out
    assert (project.root / "tests" / "unit" / "test_framing.py").is_file()
    config = (project.root / ".ltb" / "config").read_text()
    assert "files = tests/unit/test_framing.py" in config
    assert "unit = python3 tests/unit/test_framing.py" in config
    assert "tests/unit/test_framing.py" in (project.root / ".ltb" / "checksums").read_text()
    code, out = project.run("test")
    assert "Skeleton unit tests" in out

    (project.root / "tests" / "unit" / "test_framing.py").write_text("raise SystemExit(0)\n")
    code, out = project.run("test")
    assert code == 2 and "tests/unit/test_framing.py" in out


def test_unit_tests_can_be_retired(make_project):
    project = make_project(stages=("01",))
    stage_with_unit(project)
    assert project.run("seal")[0] == 0
    unit = project.root / "tests" / "unit" / "test_framing.py"
    unit.unlink()
    config = project.root / ".ltb" / "config"
    config.write_text(config.read_text().replace("files = tests/unit/test_framing.py", "files =")
                      .replace("unit = python3 tests/unit/test_framing.py", "unit ="))
    code, out = project.run("seal", "--allow-changed", "tests/unit/test_framing.py")
    assert code == 0, out
    assert project.run("verify")[0] == 0


def test_unit_needs_both_parts(make_project):
    project = make_project(stages=("01",))
    d = stage_with_unit(project)
    (d / "unit.json").unlink()
    code, out = project.run("seal")
    assert code == 4 and "need both" in out
