# Reasoning Budget

This starter optimizes for correct engineering decisions per token, not the most agents or the longest analysis.

## Escalation ladder

1. **Direct work:** The main agent performs targeted inspection and handles straightforward, local changes.
2. **Explore:** Use `explorer` when ownership, execution flow, or root cause remains unclear.
3. **Validate:** Use `verifier` to identify the minimal evidence path and `test_runner` to execute bounded commands.
4. **Deep review:** Use `reviewer` at `gpt-5.6` high only for consequential changes or unresolved logic.

High-reasoning triggers include ambiguous multi-file behavior, public APIs or data contracts, security boundaries, concurrency, migrations, hard-to-reproduce failures, and conflicting evidence. Repository size alone, routine edits, or a desire for extra reassurance are not sufficient triggers.

## Token controls

- Unnamed subagents default to `gpt-5.6-terra` low rather than inheriting an expensive parent setting.
- The configuration caps open subagent threads at four as a runaway-work ceiling; project rules choose the useful count from actual independent work.
- Every delegated task gets one question and a compact output contract.
- `model_verbosity = "low"` and `model_reasoning_summary = "none"` keep returned context focused while preserving configured reasoning effort.
- Exploration stops when evidence is sufficient to decide, and delegated work is not repeated without conflicting evidence.
- Prompt explanations live in docs instead of the always-loaded root instructions.

## Measuring changes

Run representative tasks before and after a configuration change. Track success, missed defects, validation coverage, total tokens, latency, and cost. Change one dimension at a time: prompt text, model, effort, or agent count.

`scripts/verify.py` enforces byte ceilings for root and agent instructions. Bytes are a stable repository budget, not an exact tokenizer estimate. Raise a ceiling only with a reviewed reason and workload evidence.
