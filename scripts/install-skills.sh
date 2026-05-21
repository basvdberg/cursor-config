#!/bin/sh
# Link cursor-config skills into ~/.cursor/skills for Cursor agents.
set -e
CONFIG_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SOURCE="$CONFIG_ROOT/skills"
SKILLS_TARGET="${HOME}/.cursor/skills"

mkdir -p "$SKILLS_TARGET"
for dir in "$SKILLS_SOURCE"/*/; do
  name="$(basename "$dir")"
  target="$SKILLS_TARGET/$name"
  rm -rf "$target"
  ln -s "$dir" "$target"
  echo "Linked $name -> $dir"
done
echo "Skills installed under $SKILLS_TARGET"
