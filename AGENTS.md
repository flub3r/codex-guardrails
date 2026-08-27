# Codex Project Rules

## Reasoning budget
- Finish the requested scope. Inspect the real owner before editing; make the smallest coherent fix; preserve unrelated work.
- Start targeted with the cheapest reliable reasoning. Escalate only for named risk or conflicting evidence; stop when evidence is sufficient.
- Never call placeholders or unverified work complete.

## Subagent policy
Default to single-agent work: subagents add model and tool tokens. Delegate a bounded task only for material context isolation, independent parallel speed, or consequential uncertainty.

Do not delegate routine inspection, edits, validation, or review. Self-review first; do not auto-spawn `reviewer` for reassurance.

Concrete triggers: `explorer` for unresolved ownership after targeted reads; `test_runner` for long/noisy checks beside useful work; `verifier` for unclear validation or claims; `reviewer` for consequential security, data, API, concurrency, migration risk, or conflicting evidence; a worker for disjoint low-coupling implementation.

Use the smallest useful count; the limit is a ceiling. Parallelize only independent work. Give one question and a compact output contract. Keep decisions, coupled edits, and integration primary; avoid duplicate work.

Before spawning, tell the user the role, task, and cost benefit. At completion, list each subagent's contribution. Never expose private reasoning.

## Continuity
- Before a likely pause or usage limit, leave a thread checkpoint: outcome/done criteria; completed work; current files, branch, external state; next action; validation/blockers.
- On resume after pause, compaction, or restart, inspect the checkpoint and status/diff. Continue at the next incomplete step; repeat only stale or uncertain work.
- If no checkpoint survived, reconstruct minimal state from status, diff, recent history, and task artifacts; state material uncertainty.

## Workflow
- Before editing: read instructions; inspect status/diffs; locate ownership; discover validation commands.
- While editing: touch required files only; justify dependencies; never silence checks; preserve public behavior unless requested.
- Before completion: review the diff; run the narrowest sufficient validation; report results/blockers; update affected docs.

## Git safety
- Never discard work or use destructive recovery (`git reset --hard`, destructive `git clean`, force-push). Refuse force flags.
- Never blanket-stage; review and stage explicit paths.
- Confirm repository, branch, and scope before remote mutations; verify uncertain state before retrying.

## Completion
Complete means requested behavior is implemented, the diff is reviewed, validation ran or its blocker is documented, and no known task-caused regression remains.
