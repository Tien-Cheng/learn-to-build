import ast
import sys
import sysconfig
from pathlib import Path

from conftest import LTB, SKILL

STDLIB = Path(sysconfig.get_paths()["stdlib"]).resolve()


def is_stdlib(name):
    if name in sys.builtin_module_names:
        return True
    import importlib.util

    spec = importlib.util.find_spec(name)
    if spec is None or spec.origin in (None, "built-in", "frozen"):
        return spec is not None
    return STDLIB in Path(spec.origin).resolve().parents and "site-packages" not in spec.origin


def imports(path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            yield node.module.split(".")[0]


def test_ltb_imports_only_stdlib():
    bad = sorted({m for m in imports(LTB) if not is_stdlib(m)})
    assert not bad, "ltb must stay stdlib-only: %s" % bad


def test_ltb_is_executable_python3():
    assert LTB.read_text().startswith("#!/usr/bin/env python3\n")
    assert LTB.stat().st_mode & 0o111
