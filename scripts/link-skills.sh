#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.claude/skills"

resolve_path() {
  python3 -c "import os; print(os.path.realpath('$1'))" 2>/dev/null \
    || perl -MCwd -e 'print Cwd::realpath($ARGV[0])' "$1" 2>/dev/null \
    || readlink -f "$1" 2>/dev/null \
    || echo "$1"
}

if [ -L "$DEST" ]; then
  resolved="$(resolve_path "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST is a symlink into this repo ($resolved)." >&2
      echo "Remove it (rm \"$DEST\") and re-run." >&2
      exit 1
      ;;
  esac
fi

mkdir -p "$DEST"

find "$REPO/skills" -name SKILL.md -print0 |
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"
  target="$DEST/$name"

  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "warning: $target exists and is not a symlink. Backing up to ${target}.bak" >&2
    mv "$target" "${target}.bak"
  fi

  ln -sfn "$src" "$target"
  echo "linked $name -> $src"
done
