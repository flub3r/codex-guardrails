# Codex Guardrails

A lean, opinionated starter configuration for OpenAI Codex. It is for teams that want disciplined engineering behavior, stronger reasoning on consequential decisions, and a small recurring context cost.

The package keeps prompt overhead intentionally small. The root `AGENTS.md` is the main always-loaded instruction file. Configuration and command policies control runtime behavior, while each focused agent file is added only to the spawned agent that uses it. Longer explanations stay in normal documentation.

## What it enforces

- Inspect the repository before editing and solve the root problem instead of guessing.
- Start with the cheapest reliable path and escalate reasoning only for a named uncertainty or material risk.
- Assess delegation on every non-trivial task and choose roles dynamically from independence, context load, duration, and risk.
- Use efficient workers for discovery and validation, while reserving a stronger high-effort reviewer for consequential changes.
- Prefer targeted reads and distilled evidence over broad scans, raw logs, and duplicated work.
- Keep the main Codex thread responsible for decisions, integration, and edits.
- Tell the user before subagents spawn and summarize each agent's contribution at completion.
- Discover real repository test/build commands, review the final diff, and report validation honestly.
- Preserve unrelated user changes and refuse to call placeholders or skipped validation "done".
- Block common destructive Git and force-push layouts, forbid blanket staging, and require approval for every push.
- Prompt for covered core GitHub mutations while keeping read-only inspection frictionless.

Codex command rules match exact argument prefixes. The policy hard-blocks common force-push layouts and prompts on every other push; `AGENTS.md` supplies the position-independent rule that the agent must refuse any force flag.

## Reasoning allocation

| Agent | Model | Effort | Mode | Purpose |
|---|---|---|---|---|
| `explorer` | `gpt-5.6-terra` | medium | read-only | Resolve unclear ownership, execution flow, and root cause |
| `reviewer` | `gpt-5.6` | high | read-only | Deep review of consequential correctness, security, and regression risk |
| `verifier` | `gpt-5.6-terra` | low | read-only | Find the minimal real validation path and challenge unsupported claims |
| `test_runner` | `gpt-5.6-luna` | low | workspace-write | Run bounded repository-defined checks without editing source |

Unnamed subagents default to `gpt-5.6-terra` at low effort. Four threads is a runaway-work ceiling, not a recommended count: `AGENTS.md` chooses roles and count from the task's actual independent work. The primary Codex model remains a user or team choice.

Agent reasoning summaries are disabled and response verbosity is low. Agents still perform their configured reasoning, but return compact findings rather than extra narration that pollutes the parent context.

See [`docs/REASONING-BUDGET.md`](docs/REASONING-BUDGET.md) for the escalation ladder and tuning method.

## Install into a project

Clone this repository, then run one of the installers from the clone.

### Windows / PowerShell

```powershell
.\scripts\install-project.ps1 -Target "C:\path\to\your-project"
```

### macOS / Linux

```bash
./scripts/install-project.sh /path/to/your-project
```

The installer stops without changing anything if the target already contains `AGENTS.md` or `.codex`. It never deletes or overwrites existing Codex configuration; merge existing project instructions manually.

After installation, review the copied files before committing them to the target project.

## Validate this repository

```bash
python scripts/verify.py
```

CI runs the same structure, TOML, role-policy, prompt-budget, and command-policy checks on pushes and pull requests. The Codex CLI version used for policy validation is pinned in the workflow. The verifier reports byte budgets as a stable proxy for instruction growth; it does not claim exact model token counts.

Locally, command-policy checks run when Codex CLI is installed; CI requires it instead of silently skipping those checks. CI also smoke-tests the non-destructive installers on Windows and Linux.

## Customize without bloating context

See [`docs/CUSTOMIZING.md`](docs/CUSTOMIZING.md). Put global enforceable behavior in `AGENTS.md`, role-specific behavior in agent files, and explanations in normal docs. State each rule once and tune effort from representative tasks rather than intuition.

## Why this structure

Current Codex releases support project configuration, custom project agents, project-local rules, and delegation requested by applicable `AGENTS.md` instructions. OpenAI documents that subagents consume more total tokens, but they can isolate noisy work and route narrow tasks to cheaper models. This starter assesses delegation on every meaningful task, chooses workers from the task rather than a fixed recipe, uses `gpt-5.6-terra` for efficient read-heavy work and `gpt-5.6-luna` for narrow repeatable work, and reserves higher effort for measured quality gains.

Official references:

- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/rules
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/api/docs/guides/latest-model

## License

MIT. See [`LICENSE`](LICENSE).
