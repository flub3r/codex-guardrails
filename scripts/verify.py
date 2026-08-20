from __future__ import annotations

from pathlib import Path
import sys
import tomllib

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "AGENTS.md",
    ROOT / ".codex" / "config.toml",
    ROOT / ".codex" / "rules" / "default.rules",
    ROOT / ".codex" / "agents" / "explorer.toml",
    ROOT / ".codex" / "agents" / "reviewer.toml",
    ROOT / ".codex" / "agents" / "verifier.toml",
    ROOT / ".codex" / "agents" / "test-runner.toml",
]

errors: list[str] = []
for path in REQUIRED:
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

for path in (ROOT / ".codex").rglob("*.toml"):
    try:
        with path.open("rb") as fh:
            tomllib.load(fh)
    except Exception as exc:
        errors.append(f"invalid TOML {path.relative_to(ROOT)}: {exc}")

if (ROOT / "AGENTS.md").is_file():
    agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for required_text in ("Subagent policy", "Git safety", "Completion standard"):
        if required_text not in agents_text:
            errors.append(f"AGENTS.md missing section marker: {required_text}")

if errors:
    print("Guardrails validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Guardrails structure and TOML validation passed.")
