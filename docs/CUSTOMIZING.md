# Customizing Codex Guardrails

Keep the always-loaded instructions small. Add project-specific rules to the root `AGENTS.md` only when they apply broadly and materially change how work should be done.

## What to customize

- Replace generic validation guidance with real project commands once they are known.
- Add nested `AGENTS.md` files only for directories that genuinely need different rules.
- Add specialized agents only when a recurring task has a clear boundary; avoid one agent per technology or folder.
- Change subagent models/effort when the task mix or account availability requires it.
- Extend `.codex/rules/default.rules` for commands that are dangerous in your environment.

## What not to customize casually

- Do not raise the concurrency limit merely to create more activity. Six is a ceiling, not a target.
- Do not make every subagent writable. Parallel read-heavy agents are easier to coordinate and less likely to conflict.
- Do not duplicate the same policy across `AGENTS.md`, agent files, and docs. Put enforceable global behavior in `AGENTS.md`; role-specific behavior in the relevant agent file; explanations here or in the README.
- Do not pin the main Codex model in this starter unless a team deliberately wants that policy. The main model should remain a user/team choice.

## Existing projects

The installers refuse to overwrite an existing `AGENTS.md` or `.codex` directory by default. Prefer merging existing instructions manually. Use `-Force` / `--force` only when replacement is intentional and reviewed.

## Verify

Run:

```bash
python scripts/verify.py
```

For command-rule behavior, current Codex releases provide `codex execpolicy check`; use it against `.codex/rules/default.rules` when Codex CLI is installed.
