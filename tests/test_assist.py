def test_assist_default_and_stage_override(make_project):
    project = make_project(stages=("01", "02"))
    code, out = project.run("assist")
    assert "Default: solo" in out and "Current Stage 02: solo" in out
    assert project.run("assist", "lead", "--default")[0] == 0
    assert project.run("assist", "pair", "--stage", "02", "--paths", "cli.py", "io/*")[0] == 0
    config = (project.root / ".ltb" / "config").read_text()
    assert "default = lead" in config and "02 = pair" in config and "pair_paths = cli.py io/*" in config
    assert "[dials]" in config and "design = 3" in config
    out = project.run("status")[1]
    assert "Assist:  pair for Stage 02 (agent may write: cli.py io/*)" in out


def test_lead_status_asks_for_approach(make_project):
    project = make_project(stages=("01",))
    project.run("assist", "lead")
    assert "Approach missing: write .ltb/stages/01-set-get/approach.md" in project.run("status")[1]
    (project.root / ".ltb" / "stages" / "01-set-get" / "approach.md").write_text("plan\n")
    assert "Approach missing" not in project.run("status")[1]


def test_assist_rejects_unknown_mode(make_project):
    assert make_project().run("assist", "autopilot")[0] == 4


def test_log_assist_and_summary_mode(make_project):
    project = make_project()
    project.run("assist", "lead")
    assert project.run("log", "assist", "--stage", "01", "--paths", "kv.py", "--note", "from Approach")[0] == 0
    assert '"event": "edit"' in (project.root / ".ltb" / "log" / "assist.jsonl").read_text()
    project.run("log", "summary", "--stage", "01")
    assert '"mode": "lead"' in (project.root / ".ltb" / "log" / "dials.jsonl").read_text()
