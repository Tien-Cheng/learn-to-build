"""Golden Stages captured from dogfood runs: green on their reference, red on the starter."""
import re
import shutil
import sys

import pytest

from conftest import LTB, SKILL, Project

GOLDEN = sorted((p for p in (SKILL.parent.parent / "tests" / "fixtures").glob("*-stage-*") if p.is_dir()))


@pytest.mark.parametrize("golden", GOLDEN, ids=[g.name for g in GOLDEN])
def test_golden_stage(golden, tmp_path):
    root = tmp_path / "proj"
    shutil.copytree(str(golden / "starter"), str(root))
    shutil.copy(str(LTB), str(root / "ltb"))
    shutil.copy(str(SKILL / "assets" / "project" / "AGENTS.md"), str(root / "AGENTS.md"))
    (root / ".ltb").mkdir(exist_ok=True)
    config = (golden / "config.ini").read_text().replace("{python}", sys.executable)
    (root / ".ltb" / "config").write_text(config)
    stage = next(golden.glob("stage_*.py"))
    number, slug = stage.name[6:8], stage.stem[9:].replace("_", "-")
    project = Project(root)
    project.stage(number, slug, stage.read_text(), (golden / "primer.md").read_text())
    code, out = project.run("seal")
    assert code == 0, out

    code, out = project.run("test", "-v")
    assert code == 1, out
    assert not re.search(r"^\s+pass\s", out, re.M), "every test must fail on the starter:\n" + out

    ref = tmp_path / "ref"
    shutil.copytree(str(golden / "ref"), str(ref))
    ini = ref / "ltb.ini"
    ini.write_text(ini.read_text().replace("{python}", sys.executable))
    code, out = project.run("test", "--config", str(ini))
    assert code == 0, out
