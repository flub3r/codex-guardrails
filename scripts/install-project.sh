#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <target-project> [--force]" >&2
  exit 2
fi

TARGET="$(cd "$1" && pwd)"
FORCE="${2:-}"
SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for item in AGENTS.md .codex; do
  if [[ -e "$TARGET/$item" && "$FORCE" != "--force" ]]; then
    echo "$TARGET/$item already exists. Review/merge it manually or rerun with --force only if replacement is intentional." >&2
    exit 1
  fi
done

cp -f "$SOURCE_ROOT/AGENTS.md" "$TARGET/AGENTS.md"
rm -rf "$TARGET/.codex"
cp -R "$SOURCE_ROOT/.codex" "$TARGET/.codex"

echo "Installed Codex Guardrails into $TARGET"
echo "Review AGENTS.md and .codex/config.toml for project-specific adjustments before committing."
