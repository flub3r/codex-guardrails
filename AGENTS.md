# Codex Project Rules

## Operating principles
- Complete scope; expand only when evidence shows the root fix requires it.
- Inspect before editing; trace the actual owner and flow.
- Prefer the smallest coherent root-cause change and preserve unrelated work.
- Never present placeholders or unverified work as complete.

## Reasoning budget
Use the cheapest reliable path.
- Start targeted. Escalate for named risk: ambiguous multi-file behavior, public/data contracts, security, concurrency, migrations, hard-to-reproduce failures, or conflicting evidence.
- Reserve high effort for those questions or consequential review, not routine discovery or commands.
- Stop when evidence is sufficient. Return conclusions and references, not raw dumps; repeat work only when evidence conflicts.

## Subagent policy
For every non-trivial task, assess delegation before editing. Use subagents when cheaper model routing, context isolation, parallelism, or independent review outweighs their extra total tokens.

Delegate a bounded assignment when:
- `explorer`: ownership or flow is unclear or spans multiple areas.
- `reviewer`: a meaningful or high-risk diff needs an independent correctness or security check.
- `verifier` or `test_runner`: validation is uncertain, noisy, or long-running.
- A focused worker: implementation streams have disjoint ownership and low integration risk.

Isolate large searches, logs, generated output, or documentation research that would pollute the primary context. When a trigger exists, delegate unless coordination overhead erases the benefit.

Choose roles and count from independence, context savings, risk, and concurrency—not a quota. Parallelize independent work; avoid duplication; favor read-only agents; keep coupled tasks primary. The main agent owns integration and edits.

Before spawning, tell the user the roles, assignments, and benefit. In the final response, list each subagent and its contribution; never expose private chain-of-thought.

## Repository workflow
- Before editing: read applicable instructions; inspect status and diffs; locate the behavior owner; discover repository validation commands. Create a branch only when work is not isolated and the current branch is default or shared.
- While editing: touch only required files; justify dependencies; never silence checks or error handling; preserve public behavior unless requested.
- Before completion: review the full diff; validate narrowly, broadening when risk warrants; summarize commands, results, and blockers; update affected docs.

## Git safety
- Never discard work or use destructive recovery (`git reset --hard`, destructive `git clean`, force-push). Policy blocks common forms and prompts every push; refuse force flags. Users handle exceptions.
- Never blanket-stage; review and stage explicit paths.
- Confirm repository, branch, and scope before remote mutations. Verify uncertain state before retrying.

## Failure handling
- Inspect the error and distinguish pre-existing failures from task-caused regressions.
- Fix root causes instead of bypassing checks or churning caches, lockfiles, or dependencies. Stop before destructive recovery.

## Completion standard
Complete means requested behavior is implemented, the diff is reviewed, relevant validation ran or its blocker is documented, and no known task-caused regression remains.
