# Movement Review Benchmark Baseline

This file records the Movement Review benchmark baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Command Executed

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

Result status: `COMPLETED`

Pass/fail summary:

- Total: 8
- Passed: 8
- Failed: 0
- Audit/chat rows created: false

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

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
