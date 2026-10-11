import os
import time


def test_server_stage_passes_and_is_torn_down(make_project, tmp_path):
    project = make_project(stages=("02",))
    pidfile = tmp_path / "pid"
    env = dict(os.environ, KV_PIDFILE=str(pidfile))
    code, out = project.run("test", env=env)
    assert code == 0, out
    pid = int(pidfile.read_text())
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return
        time.sleep(0.05)
    raise AssertionError("server process %d outlived the test" % pid)


def test_server_that_never_listens_fails_cleanly(make_project):
    project = make_project(solution="starter", stages=("02",))
    code, out = project.run("test")
    assert code == 1
    assert "server exited" in out
