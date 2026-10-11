import importlib.machinery
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "learn-to-build"
LTB = SKILL / "assets" / "ltb"
KV = Path(__file__).resolve().parent / "fixtures" / "kv"


def load_ltb():
    loader = importlib.machinery.SourceFileLoader("ltb_runner", str(LTB))
    spec = importlib.util.spec_from_loader("ltb_runner", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def ltb():
    return load_ltb()


class Project:
    """A throwaway Project repo wired to the toy key-value X."""

    def __init__(self, root):
        self.root = root

    def run(self, *args, env=None):
        proc = subprocess.run(
            [sys.executable, str(self.root / "ltb"), *args],
            cwd=str(self.root), capture_output=True, text=True, env=env, timeout=120,
        )
        return proc.returncode, proc.stdout + proc.stderr

    def stage(self, number, slug, source, primer="# Primer\n"):
        d = self.root / ".ltb" / "staging" / ("%s-%s" % (number, slug))
        d.mkdir(parents=True)
        (d / "public.py").write_text(source)
        (d / "primer.md").write_text(primer)
        return d

    def write_config(self, program="kv.py", build="", extra=""):
        (self.root / ".ltb" / "config").write_text(
            "[project]\nx = kv\ngoal = design\nlanguage = python\nformat = 1\n\n"
            "[commands]\nbuild = %s\nrun = %s %s\ntimeout = 5\n%s\n"
            "[dials]\nlanguage = 3\ndomain = 3\ndesign = 3\n" % (build, sys.executable, program, extra)
        )


@pytest.fixture
def make_project(tmp_path):
    """make_project(solution="kv"|"starter", stages=("01", "02"), sealed=True)."""

    def make(solution="kv", stages=("01",), sealed=True):
        root = tmp_path / "proj"
        (root / ".ltb").mkdir(parents=True)
        shutil.copy(str(LTB), str(root / "ltb"))
        shutil.copy(str(SKILL / "assets" / "project" / "AGENTS.md"), str(root / "AGENTS.md"))
        src = KV / ("kv.py" if solution == "kv" else "starter.py")
        shutil.copy(str(src), str(root / "kv.py"))
        project = Project(root)
        project.write_config()
        for path in sorted(KV.glob("stage_*.py")):
            number = path.name[6:8]
            if number in stages:
                slug = path.stem[9:].replace("_", "-")
                project.stage(number, slug, path.read_text(), (KV / "primer.md").read_text())
        if sealed:
            code, out = project.run("seal")
            assert code == 0, out
        return project

    return make
