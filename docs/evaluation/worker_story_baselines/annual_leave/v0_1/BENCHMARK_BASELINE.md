# Annual Leave / Leave Management Benchmark Baseline

This file records the Annual Leave / Leave Management benchmark baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Command Executed

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.annual_leave.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Scope

The benchmark scope is the Annual Leave / Leave Management rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.annual_leave.json
```

The benchmark checks deterministic retrieval and answer-contract behavior for Annual Leave / Leave Management questions. It is not a live LLM review and does not prove runtime payroll or leave-management correctness.

## Captured Result Summary

Result status: `COMPLETED`

Pass/fail summary:

- Total: 1
- Passed: 1
- Failed: 0
- Audit/chat rows created: false

Failed cases: none.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Source References

- Runbook: `docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.annual_leave.json`
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
