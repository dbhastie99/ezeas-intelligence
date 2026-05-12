# Movement Review Benchmark Baseline

This file records the Movement Review benchmark baseline capture attempt for comparison control. It is diagnostic-only and not operational truth.

## Command Identified

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.movement_review.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Scope

The benchmark scope is the Movement Review rich-answer manifest:

```text
samples/eval/rich_answer_benchmark.movement_review.json
```

The benchmark checks deterministic retrieval and answer-contract behavior for Movement Review questions. It is not a live LLM review and does not prove runtime payroll correctness.

## Captured Result Summary

Result status: `BLOCKED_DATABASE_CONNECTION`

Pass/fail summary:

- Total: not captured
- Passed: not captured
- Failed: not captured
- Audit/chat rows created: not available because the benchmark was not run

The read-only DB readiness gate failed before this command was run. No benchmark result is inferred from this blocked state.

Generated artefact committed: no.

## Source References

- Runbook: `docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md`
- Manifest: `samples/eval/rich_answer_benchmark.movement_review.json`
- Runner: `scripts/run_golden_questions.py`

## Diagnostic-Only Guardrails

This benchmark baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.
