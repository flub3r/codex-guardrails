# Codex Project Rules

## Operating principles
- Solve the requested problem completely; do not expand scope without a concrete reason.
- Inspect the repository before editing. Find the real owner of behavior instead of guessing from filenames.
- Prefer the smallest coherent change that fixes the root cause.
- Preserve user work. Never overwrite, discard, or reformat unrelated changes.
- Do not present placeholders, TODO-only stubs, skipped validation, or speculative code as finished work.

## Subagent policy
Use subagents when they reduce context load or parallelize independent work. Do not spawn agents just to satisfy a quota.

For non-trivial work, consider parallel read-heavy delegation first:
- `explorer`: locate ownership, execution flow, dependencies, and likely root cause.
- `reviewer`: independently review a proposed or completed diff for correctness, regressions, security, and maintainability.
- `verifier`: determine the correct validation commands and verify claimed behavior.
- `test_runner`: run bounded test/lint/build commands and report failures precisely.

Rules:
- Spawn independent read-only investigations together when useful.
- Keep the main agent responsible for decisions, integration, and final edits.
- Avoid parallel write-heavy agents touching overlapping files.
- Parallel implementation is allowed only when file ownership is clearly disjoint and integration risk is low.
- Give every subagent a narrow objective and require distilled findings, not raw dumps.
- Do not repeat work already delegated unless verifying a material uncertainty.

## Repository workflow
Before changing code:
1. Read applicable `AGENTS.md` files and repo docs.
2. Inspect `git status --short` and relevant diffs.
3. Discover actual build/test/lint commands from repository files; never invent them.
4. For meaningful work, use a feature branch unless the user explicitly requires otherwise.

While editing:
- Touch only files required for the task.
- Do not add dependencies unless justified and consistent with the project.
- Do not silence types, lint, tests, security checks, or error handling to make validation pass.
- Keep public behavior backward-compatible unless the task explicitly changes it.

Before completion:
1. Review the complete diff.
2. Run the narrowest relevant validation first, then broader checks when justified.
3. Report every validation command actually run and its result.
4. If validation cannot run, state exactly why; never imply it passed.
5. Update docs when behavior, setup, architecture, or user-facing workflow changed.

## Git safety
Never run or recommend destructive commands merely to recover convenience.

Forbidden without an explicit user request and a verified reason:
- `git reset --hard`
- `git clean -fd` / `git clean -fdx`
- `git push --force` / `git push -f`
- deleting branches with unmerged work
- rewriting shared history
- discarding unknown local changes

Never use blanket staging (`git add .`, `git add -A`, `git add --all`). Stage explicit paths only after reviewing status/diff.

Remote mutations must be intentional. Before push/PR/merge/release actions, confirm the target repo, branch, and intended scope. Do not retry uncertain remote mutations blindly; verify current state first.

## Failure handling
- Treat failing tests as information, not obstacles to bypass.
- Distinguish pre-existing failures from regressions caused by the change.
- If a command fails, inspect the actual error before changing code.
- Prefer root-cause fixes over retries, cache deletion, lockfile churn, or environment resets.
- Stop before destructive recovery actions and explain the blocker.

## Completion standard
A task is complete only when the requested behavior is implemented, the diff is reviewed, relevant validation is run or its blocker is documented, and no known task-caused regression remains.