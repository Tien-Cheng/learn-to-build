#!/bin/sh
# Symlink the skill into agent skill directories so edits here are live.
#   scripts/dev-install.sh              -> ~/.claude/skills and ~/.agents/skills
#   scripts/dev-install.sh --project D  -> D/.claude/skills and D/.agents/skills
set -eu

src="$(cd "$(dirname "$0")/.." && pwd)/skills/learn-to-build"
base="$HOME"
if [ "${1:-}" = "--project" ]; then
  base="$(cd "${2:?usage: dev-install.sh --project DIR}" && pwd)"
fi

for dir in "$base/.claude/skills" "$base/.agents/skills"; do
  mkdir -p "$dir"
  dest="$dir/learn-to-build"
  if [ -L "$dest" ]; then
    rm "$dest"
  elif [ -e "$dest" ]; then
    echo "skip $dest: exists and is not a symlink" >&2
    continue
  fi
  ln -s "$src" "$dest"
  echo "linked $dest -> $src"
done
