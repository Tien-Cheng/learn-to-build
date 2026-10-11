"""Toy X for ltb's own tests: a line-protocol key-value store.

  python kv.py            read commands from stdin, one reply per line
  python kv.py serve      same protocol over TCP on $PORT, one command per connection line
  python kv.py sleep      hang (timeout tests)
  python kv.py crash      exit 3 with a message on stderr
"""
import os
import socket
import sys


def handle(store, line):
    parts = line.split()
    if parts[:1] == ["set"] and len(parts) == 3:
        store[parts[1]] = parts[2]
        return "OK"
    if parts[:1] == ["get"] and len(parts) == 2:
        return store.get(parts[1], "(nil)")
    return "ERR unknown command"


def serve():
    pidfile = os.environ.get("KV_PIDFILE")
    if pidfile:
        with open(pidfile, "w") as f:
            f.write(str(os.getpid()))
    store = {}
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", int(os.environ["PORT"])))
    srv.listen()
    while True:
        conn, _ = srv.accept()
        with conn:
            buf = b""
            while not buf.endswith(b"\n"):
                chunk = conn.recv(1024)
                if not chunk:
                    break
                buf += chunk
            if buf:
                conn.sendall((handle(store, buf.decode().strip()) + "\n").encode())


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "serve":
        serve()
    elif mode == "sleep":
        import time

        time.sleep(60)
    elif mode == "crash":
        sys.stderr.write("boom\n")
        sys.exit(3)
    else:
        store = {}
        for line in sys.stdin:
            if line.strip():
                print(handle(store, line.strip()))


if __name__ == "__main__":
    main()
