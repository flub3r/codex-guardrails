from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AGENTS_PATH = ROOT / "AGENTS.md"
CONFIG_PATH = ROOT / ".codex" / "config.toml"
AGENT_DIR = ROOT / ".codex" / "agents"
AGENT_FILES = {
    "explorer": AGENT_DIR / "explorer.toml",
    "reviewer": AGENT_DIR / "reviewer.toml",
    "verifier": AGENT_DIR / "verifier.toml",
    "test_runner": AGENT_DIR / "test-runner.toml",
}
REQUIRED = [
    AGENTS_PATH,
    CONFIG_PATH,
    ROOT / ".codex" / "rules" / "default.rules",
    *AGENT_FILES.values(),
    ROOT / "docs" / "REASONING-BUDGET.md",
]
EXPECTED_AGENTS = {
    "explorer.toml": ("explorer", "read-only"),
    "reviewer.toml": ("reviewer", "read-only"),
    "verifier.toml": ("verifier", "read-only"),
    "test-runner.toml": ("test_runner", "workspace-write"),
}
POLICY_CASES = [
    (("git", "reset", "--hard"), "forbidden"),
    (("git", "clean", "-fd"), "forbidden"),
    (("git", "clean", "-dfx"), "forbidden"),
    (("git", "clean", "-d", "-f"), "forbidden"),
    (("git", "clean", "--force", "--directories"), "forbidden"),
    (("git", "push", "--force"), "forbidden"),
    (("git", "push", "origin", "--force-with-lease"), "forbidden"),
    (("git", "push", "origin", "main", "--force"), "forbidden"),
    (("git", "push", "origin", "main", "--force-with-lease"), "forbidden"),
    (("git", "add", "."), "forbidden"),
    (("git", "push", "origin", "main"), "prompt"),
    (("gh", "pr", "create"), "prompt"),
    (("gh", "pr", "update-branch", "42"), "prompt"),
    (("gh", "issue", "close", "42"), "prompt"),
    (("gh", "release", "delete-asset", "v1.0.0", "old.zip"), "prompt"),
    (("gh", "repo", "deploy-key", "delete", "123"), "prompt"),
    (("gh", "repo", "delete", "owner/repo"), "forbidden"),
    (("gh", "workflow", "run", "build.yml"), "prompt"),
    (("gh", "run", "cancel", "123"), "prompt"),
    (("gh", "secret", "set", "TOKEN"), "prompt"),
    (("gh", "variable", "delete", "MODE"), "prompt"),
    (("gh", "label", "edit", "bug"), "prompt"),
    (("gh", "pr", "view", "42"), None),
    (("gh", "issue", "list"), None),
    (("gh", "release", "download", "v1.0.0"), None),
    (("gh", "repo", "view", "owner/repo"), None),
]

ROOT_INSTRUCTION_MAX_BYTES = 3_000
AGENT_INSTRUCTION_MAX_BYTES = 700
TOTAL_AGENT_INSTRUCTION_MAX_BYTES = 2_400
MAX_SUBAGENT_THREADS = 3

errors: list[str] = []
parsed_toml: dict[Path, dict[str, Any]] = {}


def load_toml(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
    except Exception as exc:
        errors.append(f"invalid TOML {path.relative_to(ROOT)}: {exc}")
        return None
    parsed_toml[path] = data
    return data


for path in REQUIRED:
    if not path.is_file():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

if (ROOT / ".codex").is_dir():
    for path in (ROOT / ".codex").rglob("*.toml"):
        load_toml(path)

root_instruction_bytes = 0
if AGENTS_PATH.is_file():
    agents_text = AGENTS_PATH.read_text(encoding="utf-8")
    root_instruction_bytes = len(agents_text.encode("utf-8"))
    for required_text in (
        "Reasoning budget",
        "Subagent policy",
        "Before spawning",
        "Continuity",
        "Default to single-agent",
        "do not auto-spawn `reviewer`",
        "Git safety",
        "Completion",
    ):
        if required_text not in agents_text:
            errors.append(f"AGENTS.md missing section marker: {required_text}")
    if root_instruction_bytes > ROOT_INSTRUCTION_MAX_BYTES:
        errors.append(
            "AGENTS.md exceeds prompt budget: "
            f"{root_instruction_bytes} > {ROOT_INSTRUCTION_MAX_BYTES} bytes"
        )

config = parsed_toml.get(CONFIG_PATH)
if config is not None:
    features = config.get("features", {})
    agents = config.get("agents", {})
    if features.get("multi_agent") is not True:
        errors.append("config must enable features.multi_agent")
    if agents.get("enabled") is not True:
        errors.append("config must enable agents.enabled")
    if agents.get("default_subagent_model") != "gpt-5.6-terra":
        errors.append("default subagent model must be gpt-5.6-terra")
    if agents.get("default_subagent_reasoning_effort") != "low":
        errors.append("default subagent reasoning effort must be low")
    max_threads = agents.get("max_concurrent_threads_per_session")
    if not isinstance(max_threads, int) or isinstance(max_threads, bool):
        errors.append("max_concurrent_threads_per_session must be an integer")
    elif not 1 <= max_threads <= MAX_SUBAGENT_THREADS:
        errors.append(
            "max_concurrent_threads_per_session must be between 1 and "
            f"{MAX_SUBAGENT_THREADS}"
        )

total_agent_instruction_bytes = 0
for expected_name, path in AGENT_FILES.items():
    data = parsed_toml.get(path)
    if data is None:
        continue
    if data.get("name") != expected_name:
        errors.append(
            f"{path.relative_to(ROOT)} name must be {expected_name!r}"
        )
    expected_sandbox = EXPECTED_AGENTS[path.name][1]
    if data.get("sandbox_mode") != expected_sandbox:
        errors.append(
            f"{path.relative_to(ROOT)} sandbox_mode must be {expected_sandbox!r}"
        )
    if not isinstance(data.get("model"), str) or not data["model"].strip():
        errors.append(f"{path.relative_to(ROOT)} must set model")
    if not isinstance(data.get("model_reasoning_effort"), str):
        errors.append(f"{path.relative_to(ROOT)} must set model_reasoning_effort")
    if data.get("model_reasoning_summary") != "none":
        errors.append(f"{path.relative_to(ROOT)} must disable reasoning summaries")
    if data.get("model_verbosity") != "low":
        errors.append(f"{path.relative_to(ROOT)} must use low model verbosity")

    instructions = data.get("developer_instructions")
    if not isinstance(instructions, str) or not instructions.strip():
        errors.append(f"{path.relative_to(ROOT)} has empty developer_instructions")
        continue
    instruction_bytes = len(instructions.encode("utf-8"))
    total_agent_instruction_bytes += instruction_bytes
    if instruction_bytes > AGENT_INSTRUCTION_MAX_BYTES:
        errors.append(
            f"{path.relative_to(ROOT)} instruction budget exceeded: "
            f"{instruction_bytes} > {AGENT_INSTRUCTION_MAX_BYTES} bytes"
        )

reviewer = parsed_toml.get(AGENT_FILES["reviewer"])
if reviewer is not None:
    if reviewer.get("model") not in {"gpt-5.6", "gpt-5.6-sol"}:
        errors.append("reviewer must use gpt-5.6 or gpt-5.6-sol")
    if reviewer.get("model_reasoning_effort") != "high":
        errors.append("reviewer must use high reasoning effort")

for efficient_name in ("verifier", "test_runner"):
    data = parsed_toml.get(AGENT_FILES[efficient_name])
    if data is not None and data.get("model_reasoning_effort") != "low":
        errors.append(f"{efficient_name} must use low reasoning effort")

if total_agent_instruction_bytes > TOTAL_AGENT_INSTRUCTION_MAX_BYTES:
    errors.append(
        "total agent instruction budget exceeded: "
        f"{total_agent_instruction_bytes} > "
        f"{TOTAL_AGENT_INSTRUCTION_MAX_BYTES} bytes"
    )

codex = shutil.which("codex")
if codex:
    rules_path = ROOT / ".codex" / "rules" / "default.rules"
    for command, expected_decision in POLICY_CASES:
        result = subprocess.run(
            [codex, "execpolicy", "check", "--rules", str(rules_path), *command],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        rendered = " ".join(command)
        if result.returncode != 0:
            details = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
            errors.append(f"execpolicy failed for {rendered!r}: {details}")
            continue
        try:
            decision = json.loads(result.stdout).get("decision")
        except (json.JSONDecodeError, AttributeError) as exc:
            errors.append(f"invalid execpolicy output for {rendered!r}: {exc}")
            continue
        if decision != expected_decision:
            errors.append(
                f"execpolicy decision for {rendered!r} was {decision!r}, expected {expected_decision!r}"
            )
elif os.environ.get("CI", "").lower() == "true":
    errors.append("Codex CLI is required in CI for command-policy validation")

if errors:
    print("Guardrails validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Guardrails structure, TOML, role policy, and prompt budgets passed.")
print(
    f"Root instructions: {root_instruction_bytes}/"
    f"{ROOT_INSTRUCTION_MAX_BYTES} bytes"
)
print(
    f"Agent instructions: {total_agent_instruction_bytes}/"
    f"{TOTAL_AGENT_INSTRUCTION_MAX_BYTES} bytes total"
)
if codex:
    print("Command-policy validation passed with Codex CLI.")
else:
    print("Codex CLI not found; skipped optional command-policy validation.")
