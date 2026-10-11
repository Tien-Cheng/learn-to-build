from conftest import KV


def test_tests_collected_in_definition_order(ltb):
    ctx = ltb.Context.__new__(ltb.Context)
    names = [name for name, _ in ltb.collect_tests(KV / "stage_01_set_get.py", ltb.make_helpers(ctx))]
    assert names == ["test_set_then_get", "test_get_missing", "test_unknown_command"]


def test_helpers_are_not_collected(ltb, tmp_path):
    path = tmp_path / "stage_01_x.py"
    path.write_text("from ltb import run\n\ndef helper():\n    pass\n\ndef test_a():\n    '''a'''\n")
    ctx = ltb.Context.__new__(ltb.Context)
    assert [n for n, _ in ltb.collect_tests(path, ltb.make_helpers(ctx))] == ["test_a"]


def test_discover_released_and_staged(make_project):
    project = make_project(stages=("01",))
    project.stage("02", "server", (KV / "stage_02_server.py").read_text())
    from conftest import load_ltb

    ltb = load_ltb()
    assert list(ltb.discover(project.root)) == ["01"]
    assert list(ltb.discover(project.root, staging=True)) == ["01", "02"]


def test_lint_requires_docstrings(ltb):
    problems = ltb.lint_stage_source("def test_x():\n    pass\n", "s.py")
    assert any("no docstring" in p for p in problems)


def test_lint_requires_a_test(ltb):
    assert any("no test_" in p for p in ltb.lint_stage_source("x = 1\n", "s.py"))
