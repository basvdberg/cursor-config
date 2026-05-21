#!/bin/sh
# Point a consumer repository at cursor-config Git hooks.
set -e
CONFIG_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="${1:-$(pwd)}"
cd "$REPO_ROOT"

git config core.hooksPath "$CONFIG_ROOT/githooks"
git config cursor.configPath "$CONFIG_ROOT"
echo "Configured hooks for $(git rev-parse --show-toplevel)"
echo "  core.hooksPath = $CONFIG_ROOT/githooks"
echo "  cursor.configPath = $CONFIG_ROOT"
