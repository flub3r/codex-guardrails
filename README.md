# Codex Guardrails

A lean, opinionated starter configuration for OpenAI Codex. It is designed for people who want Codex to behave like a disciplined engineering agent without loading a giant prompt into every session.

The package keeps the always-loaded surface intentionally small: one root `AGENTS.md`, one project `.codex/config.toml`, four focused subagents, and one command-policy file. Longer explanations stay outside the automatic instruction path.

## What it enforces

- Inspect the repository before editing and solve the root problem instead of guessing.
- Use subagents when they reduce context pollution or parallelize genuinely independent work.
- Bias parallelism toward exploration, review, and validation; avoid overlapping write-heavy agents.
- Keep the main Codex thread responsible for decisions and integration.
- Discover real repository test/build commands instead of inventing them.
- Review the final diff and report validation honestly.
- Preserve unrelated user changes.
- Block destructive Git recovery commands and blanket staging.
- Require intentional review of remote Git/GitHub mutations.
- Refuse to call placeholders, skipped validation, or speculative code "done".

## Included agents

| Agent | Model | Mode | Purpose |
|---|---|---|---|
| `explorer` | `gpt-5.6-terra` medium | read-only | Map ownership, execution flow, dependencies, root cause |
| `reviewer` | `gpt-5.6-terra` high | read-only | Independent correctness/security/regression review |
| `verifier` | `gpt-5.6-terra` medium | read-only | Find the real validation path and challenge completion claims |
| `test_runner` | `gpt-5.6-luna` low | workspace-write | Run bounded repository-defined checks without editing source |

The six-thread limit is a ceiling, not a target. The primary Codex model is intentionally not pinned.

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

CI runs the same dependency-free structure/TOML check on pushes and pull requests.

If Codex CLI is installed, command policies can also be inspected with `codex execpolicy check` against `.codex/rules/default.rules`.

## Customize without bloating context

See [`docs/CUSTOMIZING.md`](docs/CUSTOMIZING.md). The short version: put global enforceable behavior in `AGENTS.md`, role-specific behavior in agent files, and explanations in normal docs. Avoid repeating the same rule in several places.

## Why this structure

Current OpenAI Codex releases support project configuration in `.codex/config.toml`, custom project agents under `.codex/agents/`, project-local rules under `.codex/rules/`, and delegation requested by applicable `AGENTS.md` instructions. OpenAI's guidance recommends faster models such as `gpt-5.6-terra` for exploration/read-heavy parallel workers and `gpt-5.6-luna` for narrow repeatable work, while keeping higher-effort reasoning for harder review tasks.

Official references:

- https://developers.openai.com/codex/subagents
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/rules
- https://developers.openai.com/codex/guides/agents-md

## License

MIT. See [`LICENSE`](LICENSE).
