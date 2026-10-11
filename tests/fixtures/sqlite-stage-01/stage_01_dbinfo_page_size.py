"""Stage 01: `.dbinfo` prints `database page size:` read from the file header."""

import shutil
import sqlite3
import subprocess

from ltb import run, expect, tmpdir

LABEL = "database page size:"


def make_db(path, page_size=None, tables=1):
    """Create a real SQLite file with Python's sqlite3 module (the oracle library)."""
    conn = sqlite3.connect(str(path))
    if page_size is not None:
        conn.execute("PRAGMA page_size=%d" % page_size)
    for i in range(tables):
        conn.execute("CREATE TABLE t%d (id integer primary key, name text)" % i)
    conn.commit()
    conn.close()
    return path


def expected_line(page_size):
    # spec.md section 3: C format "%-20s %d"
    return "%-20s %d" % (LABEL, page_size)


def page_size_line(result):
    """Exit 0, then exactly one stdout line starting with the label (spec.md section 7)."""
    expect(result.code, 0, "exit code")
    lines = [l for l in result.stdout.splitlines() if l.startswith(LABEL)]
    assert len(lines) == 1, (
        "expected exactly one stdout line starting with %r, found %d.\nstdout was:\n%s"
        % (LABEL, len(lines), result.stdout)
    )
    return lines[0]


def test_default_page_size():
    """`.dbinfo` on a database made with default settings prints `database page size:  4096`."""
    db = make_db(tmpdir() / "default.db")
    expect(page_size_line(run([str(db), ".dbinfo"])), expected_line(4096), "page size line")


def test_smallest_page_size():
    """`.dbinfo` prints `database page size:  512` for a database with the smallest page size."""
    db = make_db(tmpdir() / "small.db", 512)
    expect(page_size_line(run([str(db), ".dbinfo"])), expected_line(512), "page size line")


def test_other_page_sizes():
    """`.dbinfo` prints the right page size for 1024, 2048, 8192, 16384 and 32768-byte pages."""
    d = tmpdir()
    for size in (1024, 2048, 8192, 16384, 32768):
        db = make_db(d / ("p%d.db" % size), size)
        line = page_size_line(run([str(db), ".dbinfo"]))
        expect(line, expected_line(size), "page size line for a %d-byte-page database" % size)


def test_page_size_65536():
    """`.dbinfo` prints `database page size:  65536` for a file whose header stores the page size as 00 01."""
    db = make_db(tmpdir() / "big.db", 65536)
    raw = db.read_bytes()[16:18]
    assert raw == b"\x00\x01", "fixture problem: expected bytes 00 01 at offset 16, got %s" % raw.hex()
    expect(page_size_line(run([str(db), ".dbinfo"])), expected_line(65536), "page size line")


def test_page_size_comes_from_header():
    """Three files of identical size (16384 bytes) with 2048, 4096 and 8192-byte pages each report their own page size."""
    d = tmpdir()
    # pages = 1 schema page + 1 root page per table, so each file is 16384 bytes
    fixtures = [(2048, 7), (4096, 3), (8192, 1)]
    for size, tables in fixtures:
        db = make_db(d / ("same%d.db" % size), size, tables)
        assert db.stat().st_size == 16384, "fixture problem: %s is %d bytes" % (db.name, db.stat().st_size)
    for size, _ in fixtures:
        db = d / ("same%d.db" % size)
        line = page_size_line(run([str(db), ".dbinfo"]))
        expect(line, expected_line(size), "page size line for %s" % db.name)


def test_matches_sqlite3_cli():
    """The `database page size:` line is byte-for-byte the same as the real `sqlite3` CLI's for 512, 4096 and 65536."""
    sqlite3_cli = shutil.which("sqlite3")
    assert sqlite3_cli, (
        "the oracle `sqlite3` CLI is not on PATH; install it "
        "(macOS: preinstalled or `brew install sqlite`; Debian/Ubuntu: `sudo apt install sqlite3`)"
    )
    d = tmpdir()
    for size in (512, 4096, 65536):
        db = make_db(d / ("oracle%d.db" % size), size)
        oracle = subprocess.run(
            [sqlite3_cli, "-readonly", str(db), ".dbinfo"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=10,
        )
        assert oracle.returncode == 0, "oracle sqlite3 failed: %s" % oracle.stderr
        want = [l for l in oracle.stdout.splitlines() if l.startswith(LABEL)][0]
        line = page_size_line(run([str(db), ".dbinfo"]))
        expect(line, want, "page size line vs sqlite3 for %d-byte pages" % size)


def test_output_ends_with_newline():
    """`.dbinfo` output ends with a newline, including the last line."""
    db = make_db(tmpdir() / "nl.db")
    result = run([str(db), ".dbinfo"])
    page_size_line(result)
    assert result.stdout.endswith("\n"), "stdout must end with \\n; got %r" % result.stdout[-40:]
