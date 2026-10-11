from ltb import run, expect


def test_set_then_get():
    """A value stored with set is returned by get."""
    r = run(stdin="set a 1\nget a\n")
    expect(r.stdout, "OK\n1\n")


def test_get_missing():
    """get on an unknown key replies (nil)."""
    r = run(stdin="get nope\n")
    expect(r.stdout, "(nil)\n")


def test_unknown_command():
    """Unknown commands reply with an error line."""
    r = run(stdin="frobnicate\n")
    assert r.stdout.startswith("ERR"), "expected a line starting with ERR, got %r" % r.stdout
