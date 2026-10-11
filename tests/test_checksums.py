def test_verify_ok_after_seal(make_project):
    project = make_project()
    code, out = project.run("verify")
    assert code == 0, out


def test_edited_test_refuses_to_grade(make_project):
    project = make_project()
    test_file = next((project.root / "tests").glob("stage_01_*.py"))
    test_file.write_text(test_file.read_text() + "\n# loosened\n")
    code, out = project.run("test")
    assert code == 2
    assert "changed" in out and "git checkout -- tests/stage_01_set_get.py" in out
    assert "seal" not in out


def test_missing_and_unreleased_files(make_project):
    project = make_project()
    (project.root / "AGENTS.md").unlink()
    (project.root / "tests" / "stage_09_extra.py").write_text("def test_x():\n    '''x'''\n")
    code, out = project.run("verify")
    assert code == 2
    assert "missing" in out and "AGENTS.md" in out
    assert "unreleased" in out and "rm tests/stage_09_extra.py" in out


def test_solution_and_config_edits_are_fine(make_project):
    project = make_project()
    (project.root / "kv.py").write_text((project.root / "kv.py").read_text() + "\n# refactor\n")
    project.write_config(extra="; tweaked")
    assert project.run("verify")[0] == 0


def test_checksums_are_sha256sum_compatible(make_project, ltb):
    project = make_project()
    for line in (project.root / ".ltb" / "checksums").read_text().splitlines():
        digest, rel = line.split("  ", 1)
        assert digest == ltb.sha256(project.root / rel)
