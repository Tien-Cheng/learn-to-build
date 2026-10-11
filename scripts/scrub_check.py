#!/usr/bin/env python3
"""Fail if the repo contains personal details.

Generic patterns are committed here. Personal terms (names, employers, ...) live
untracked in .git/info/scrub-terms, one per line, so the deny list itself is
never published. Run before every public push; CI runs the generic patterns only.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERIC = [
    (re.compile(r"/Users/[A-Za-z]"), "home path"),
    (re.compile(r"/home/[a-z]"), "home path"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]*[a-z]{2,}"), "email address"),
    (re.compile(r"\bthe user's\b"), "reference to a specific user"),
]
SKIP_GENERIC = {"scripts/scrub_check.py", "uv.lock"}
SKIP_PERSONAL = {"LICENSE"}  # copyright line names the author by choice
ALLOWED_EMAILS = re.compile(r"noreply|example\.(com|org)|git@github\.com")


def repo_files():
    out = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [p for p in out.splitlines() if (ROOT / p).is_file()]


def personal_terms():
    path = ROOT / ".git" / "info" / "scrub-terms"
    if not path.exists():
        return []
    terms = [t.strip() for t in path.read_text().splitlines()]
    return [re.compile(r"\b" + re.escape(t) + r"\b", re.I) for t in terms if t and not t.startswith("#")]


def main():
    terms = personal_terms()
    hits = []
    for rel in repo_files():
        try:
            text = (ROOT / rel).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if rel not in SKIP_GENERIC:
                for pattern, label in GENERIC:
                    for m in pattern.finditer(line):
                        if label == "email address" and ALLOWED_EMAILS.search(m.group()):
                            continue
                        hits.append(f"{rel}:{lineno}: {label}: {m.group()}")
            if rel not in SKIP_PERSONAL:
                for pattern in terms:
                    if pattern.search(line):
                        hits.append(f"{rel}:{lineno}: personal term: {pattern.pattern}")
    if not terms:
        print("note: no .git/info/scrub-terms; checked generic patterns only")
    for h in hits:
        print(h)
    print(f"{len(hits)} finding(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
