# PayRun Admin Queue Benchmark Baseline

This file records the PayRun Admin Queue benchmark baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Command Executed

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payrun_admin_queue.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Scope

The benchmark scope is the PayRun Admin Queue rich-answer manifest:

```text
samples/eval/rich_answer_benchmark.payrun_admin_queue.json
```

The benchmark checks deterministic retrieval and answer-contract behavior for PayRun Admin Queue questions. It is not a live LLM review and does not prove runtime payroll correctness.

## Captured Result Summary

Result status: `COMPLETED_WITH_FAILURES`

Pass/fail summary:

- Total: 8
- Passed: 6
- Failed: 2
- Audit/chat rows created: false

Failed cases:

- `payrun-admin-queue-rich-answer`
  - Question: What is the PayRun Admin Queue and what does it show?
  - Failure: Source snippets/matched phrases did not contain all expected terms: PayRun Admin Queue, Assurance Snapshot, Worker Attention.
- `payrun-admin-queue-cleanliness-assurance`
  - Question: Why does queue cleanliness not prove PayRun assurance?
  - Failure: No source snippet/matched phrase contained expected terms: queue cleanliness, Assurance Snapshot, reasonableness.

Observed answer framing was directionally PayRun Admin Queue-specific, but source snippet / matched phrase evidence checks failed. Failure classification: benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Source References

- Runbook: `docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md`
- Manifest: `samples/eval/rich_answer_benchmark.payrun_admin_queue.json`
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
