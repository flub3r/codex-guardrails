#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <target-project>" >&2
  exit 2
fi

TARGET="$(cd "$1" && pwd)"
SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for item in AGENTS.md .codex; do
  if [[ -e "$TARGET/$item" ]]; then
    echo "$TARGET/$item already exists. Nothing was changed; review and merge the existing configuration manually." >&2
    exit 1
  fi
done

cp "$SOURCE_ROOT/AGENTS.md" "$TARGET/AGENTS.md"
cp -R "$SOURCE_ROOT/.codex" "$TARGET/.codex"

echo "Installed Codex Guardrails into $TARGET"
echo "Review AGENTS.md and .codex/config.toml for project-specific adjustments before committing."
