# Customizing Codex Guardrails

Keep the always-loaded instructions small. Add a root `AGENTS.md` rule only when it applies broadly, changes behavior materially, and is not already expressed elsewhere.

## Reasoning and model allocation

- Keep unnamed subagents on an efficient default. Raise effort or model capability only for a recurring role with a measured quality gap.
- Reserve the high-reasoning reviewer for ambiguity, public or data-contract changes, security, concurrency, migrations, hard-to-reproduce failures, or conflicting evidence.
- Keep discovery and command execution on cheaper models unless representative tasks show that a higher tier changes outcomes.
- Keep `model_verbosity = "low"` and `model_reasoning_summary = "none"` when a subagent's compact final findings are sufficient.
- Do not increase agent count and reasoning effort at the same time during tuning; change one variable and compare the same tasks.

## What to customize

- Replace generic validation guidance with real project commands once known.
- Add nested `AGENTS.md` files only for directories that genuinely need different rules.
- Add a specialized agent only when a recurring task has a clear boundary and output contract.
- Change subagent models or effort when account availability or measured task performance requires it.
- Extend `.codex/rules/default.rules` for commands that are dangerous in your environment.
- Adjust the byte ceilings in `scripts/verify.py` only when deliberate instruction growth is justified and reviewed.

## What not to customize casually

- Do not raise concurrency to create activity. Four is a ceiling, not a target, and the default workflow starts with one worker.
- Do not make every subagent writable. Read-heavy agents are easier to coordinate and less likely to conflict.
- Do not duplicate policy across `AGENTS.md`, agent files, and docs. Put enforceable global behavior in `AGENTS.md`; role-specific behavior in the relevant agent file; explanations here or in the README.
- Do not pin the main Codex model unless a team deliberately wants that policy. The main model should remain a user or team choice.

## Evaluate changes

Use a small set of representative repository tasks. Compare task success, correctness findings, final-answer completeness, validation coverage, total tokens, latency, and cost. A cheaper run is not better if it misses required behavior; a higher-effort run is not better if its extra work does not change the decision.

## Existing projects

The installers refuse to overwrite an existing `AGENTS.md` or `.codex` directory by default. Prefer merging existing instructions manually. Use `-Force` or `--force` only when replacement is intentional and reviewed.

## Verify

```bash
python scripts/verify.py
```

For command-rule behavior, use `codex execpolicy check` against `.codex/rules/default.rules` when Codex CLI is installed.
