# Codex Project Rules

## Operating principles
- Complete requested scope; expand only when evidence shows the root fix requires it.
- Inspect before editing; trace the actual owner and flow.
- Prefer the smallest coherent root-cause change.
- Preserve unrelated work. Never present placeholders or unverified work as complete.

## Reasoning budget
Use the cheapest reliable path.
- Start with targeted inspection and direct reasoning.
- Escalate only for a named uncertainty or material risk: ambiguous multi-file behavior, public or data-contract changes, security, concurrency, migrations, hard-to-reproduce failures, or conflicting evidence.
- Reserve high effort for resolving those questions or reviewing consequential changes, not routine discovery or command execution.
- Stop when evidence is sufficient. Return references and conclusions, not raw dumps; repeat work only when evidence conflicts.

## Subagent policy
Subagents cost extra tokens; use them only when they reduce uncertainty or isolate noisy work.
- Keep straightforward local work in the main thread, which owns decisions, integration, and edits.
- Use `explorer` for unclear ownership or flow; `reviewer` for a risky diff or unresolved logic; `verifier` for unclear validation; `test_runner` for bounded repository commands.
- Start with one. Parallelize only independent read-only questions; use at most two investigative agents by default.
- Give each agent one question, minimum scope, and compact output: findings, evidence, uncertainty, next action.
- Avoid overlapping writers and do not repeat delegated work without conflicting evidence.

## Repository workflow
- Before editing: read applicable instructions and docs; inspect `git status --short` and relevant diffs; locate the behavior owner; discover source-controlled build, test, and lint commands; use a feature branch for meaningful work unless the user requires otherwise.
- While editing: touch only required files; add dependencies only for a concrete project reason; do not silence types, lint, tests, security checks, or error handling; preserve public behavior unless requested.
- Before completion: review the full diff; run the narrowest relevant validation and broaden only when risk warrants it; report actual commands, results, and blockers; update docs when setup, architecture, behavior, or workflow changes.

## Git safety
- Never discard unknown work or use destructive or history-rewriting recovery (`git reset --hard`, `git clean -fd[x]`, force-push, deleting unmerged branches) without an explicit user request and verified reason.
- Never blanket-stage; review and stage explicit paths.
- Confirm repository, branch, and scope before remote mutations. Verify uncertain state before retrying.

## Failure handling
- Inspect the actual error and distinguish pre-existing failures from task-caused regressions.
- Fix root causes instead of bypassing checks or churning caches, lockfiles, or dependencies. Stop before destructive recovery and explain the blocker.

## Completion standard
Complete means the requested behavior is implemented, the diff is reviewed, relevant validation ran or its blocker is documented, and no known task-caused regression remains.
