# Reasoning Budget

This starter optimizes for correct engineering decisions per token, not the most agents or the longest analysis.

## Escalation ladder

1. **Direct work:** The primary agent handles inspection, edits, self-review, and normal validation.
2. **Isolate:** Delegate one bounded question only when noisy context, independent parallel work, or unresolved uncertainty is more expensive in the primary task.
3. **Deep review:** Use `reviewer` at `gpt-5.6` high only for consequential risk or conflicting evidence—not as a routine completion step.

High-reasoning triggers include ambiguous multi-file behavior, public APIs or data contracts, security boundaries, concurrency, migrations, hard-to-reproduce failures, and conflicting evidence. Repository size alone, routine edits, or a desire for extra reassurance are not sufficient triggers.

## Token controls

- Unnamed subagents default to `gpt-5.6-terra` low rather than inheriting an expensive parent setting.
- The configuration caps open subagent threads at three as a runaway-work ceiling; zero helpers is the default.
- Every delegated task gets one question and a compact output contract.
- `model_verbosity = "low"` and `model_reasoning_summary = "none"` keep returned context focused while preserving configured reasoning effort.
- Exploration stops when evidence is sufficient to decide, and delegated work is not repeated without conflicting evidence.
- Prompt explanations live in docs instead of the always-loaded root instructions.

## Pause and resume

Before a likely pause, leave one compact checkpoint in the task: outcome and done criteria, completed work, current repository/external state, next action, validation, and blockers. After resuming, verify status and continue at the next incomplete step. Repeat prior work only when state changed or its evidence is uncertain.

## Measuring changes

Run representative tasks before and after a configuration change. Track success, missed defects, validation coverage, total tokens, latency, and cost. Change one dimension at a time: prompt text, model, effort, or agent count.

`scripts/verify.py` enforces byte ceilings for root and agent instructions. Bytes are a stable repository budget, not an exact tokenizer estimate. Raise a ceiling only with a reviewed reason and workload evidence.
