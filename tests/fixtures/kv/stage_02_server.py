from ltb import serve, expect


def test_set_get_over_tcp():
    """The server keeps values across connections."""
    with serve(["serve"]) as s:
        expect(s.request("set k v\n"), b"OK\n")
        expect(s.request("get k\n"), b"v\n")
