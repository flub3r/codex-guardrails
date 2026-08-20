# Codex Guardrails

A lean, opinionated starter configuration for OpenAI Codex. It is for teams that want disciplined engineering behavior, stronger reasoning on consequential decisions, and a small recurring context cost.

The always-loaded surface stays intentionally small: one root `AGENTS.md`, one project `.codex/config.toml`, four focused subagents, and one command-policy file. Longer explanations and tuning guidance stay outside the automatic instruction path.

## What it enforces

- Inspect the repository before editing and solve the root problem instead of guessing.
- Start with the cheapest reliable path and escalate reasoning only for a named uncertainty or material risk.
- Keep straightforward work in the main thread; start with one subagent when delegation is justified.
- Use efficient workers for discovery and validation, while reserving a stronger high-effort reviewer for consequential changes.
- Prefer targeted reads and distilled evidence over broad scans, raw logs, and duplicated work.
- Keep the main Codex thread responsible for decisions, integration, and edits.
- Discover real repository test/build commands, review the final diff, and report validation honestly.
- Preserve unrelated user changes and refuse to call placeholders or skipped validation "done".
- Block destructive Git recovery commands and blanket staging.
- Require intentional review of remote Git/GitHub mutations.

## Reasoning allocation

| Agent | Model | Effort | Mode | Purpose |
|---|---|---|---|---|
| `explorer` | `gpt-5.6-terra` | medium | read-only | Resolve unclear ownership, execution flow, and root cause |
| `reviewer` | `gpt-5.6` | high | read-only | Deep review of consequential correctness, security, and regression risk |
| `verifier` | `gpt-5.6-terra` | low | read-only | Find the minimal real validation path and challenge unsupported claims |
| `test_runner` | `gpt-5.6-luna` | low | workspace-write | Run bounded repository-defined checks without editing source |

Unnamed subagents default to `gpt-5.6-terra` at low effort. The four-thread limit is a safety ceiling, while `AGENTS.md` asks the main agent to start with one worker and use no more than two investigative workers by default. The primary Codex model remains a user or team choice.

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

The installer stops if the target already contains `AGENTS.md` or `.codex`. Merge existing project instructions manually when possible. `-Force` / `--force` exists only for deliberate replacement.

After installation, review the copied files before committing them to the target project.

## Validate this repository

```bash
python scripts/verify.py
```

CI runs the same dependency-free structure, TOML, role-policy, and prompt-budget checks on pushes and pull requests. The verifier reports byte budgets as a stable proxy for instruction growth; it does not claim exact model token counts.

If Codex CLI is installed, command policies can also be inspected with `codex execpolicy check` against `.codex/rules/default.rules`.

## Customize without bloating context

See [`docs/CUSTOMIZING.md`](docs/CUSTOMIZING.md). Put global enforceable behavior in `AGENTS.md`, role-specific behavior in agent files, and explanations in normal docs. State each rule once and tune effort from representative tasks rather than intuition.

## Why this structure

Current Codex releases support project configuration in `.codex/config.toml`, custom project agents under `.codex/agents/`, project-local rules under `.codex/rules/`, and delegation requested by applicable `AGENTS.md` instructions. OpenAI documents that subagents consume more tokens than comparable single-agent runs, recommends `gpt-5.6-terra` for efficient read-heavy work and `gpt-5.6-luna` for narrow repeatable work, and recommends higher effort only where it produces a measured quality gain. OpenAI also reports directional quality and cost gains from leaner system prompts; validate those gains on your own workload.

Official references:

- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/rules
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/api/docs/guides/latest-model

## License

MIT. See [`LICENSE`](LICENSE).
