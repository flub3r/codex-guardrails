# Customizing Codex Guardrails

Keep the always-loaded instructions small. Add a root `AGENTS.md` rule only when it applies broadly, changes behavior materially, and is not already expressed elsewhere.

## Reasoning and model allocation

- Keep unnamed subagents on an efficient default. Raise effort or model capability only for a recurring role with a measured quality gap.
- Reserve the high-reasoning reviewer for ambiguity, public or data-contract changes, security, concurrency, migrations, hard-to-reproduce failures, or conflicting evidence.
- Keep discovery and command execution on cheaper models unless representative tasks show that a higher tier changes outcomes.
- Do not make reviewer delegation a default completion step; require a named risk that self-review cannot cover efficiently.
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

- Treat concurrency as a runaway-work ceiling, not a target. Start with no helper and add only independently useful work.
- Do not make every subagent writable. Read-heavy agents are easier to coordinate and less likely to conflict.
- Do not duplicate policy across `AGENTS.md`, agent files, and docs. Put global behavior in `AGENTS.md`, role behavior in agent files, and explanations here.
- Do not pin the main model unless a team deliberately wants that policy.

## Evaluate changes

Use a small set of representative repository tasks. Compare task success, correctness findings, final-answer completeness, validation coverage, total tokens, latency, and cost. A cheaper run is not better if it misses required behavior; a higher-effort run is not better if its extra work does not change the decision.

## Existing projects

The installers never overwrite an existing `AGENTS.md` or `.codex` directory. Merge existing instructions manually so project-specific configuration is not lost.

## Verify

```bash
python scripts/verify.py
```

When Codex CLI is available, the verifier automatically uses `codex execpolicy check` for representative forbidden, prompted, and read-only commands.
