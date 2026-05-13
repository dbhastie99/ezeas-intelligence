# ObjectTime / Source Truth Benchmark Baseline

This file records intentional benchmark non-execution for the ObjectTime / Source Truth baseline pack. It is diagnostic-only and not operational truth.

## Command Not Run

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.objecttime_source_truth.json
```

Attempted baseline capture on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `DATABASE_CONNECTION_FAILED`.

## Scope

The benchmark scope is the ObjectTime / Source Truth rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.objecttime_source_truth.json
```

The manifest covers ObjectTime / Source Truth, governed source evidence, PayRun inclusion context, SourceTruth versus WorkedHours, raw span hours, interpreted worked hours boundaries, imported and generated source rows, current-effective payroll output, Worker Story, Payroll Bases, Leave Accrual, Comparison / Remediation, Movement Review, Retro / Replay, corrections, dirty contacts, reprocessing, provenance and audit.

## Blocked Result Summary

Result status: `BLOCKED_DATABASE_CONNECTION`

Pass/fail summary:

- Total: not run
- Passed: not run
- Failed: not run
- Audit/chat rows created: false

Benchmark result: not run.

Baseline pack created: blocked pack only.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

Code Evidence answer integration: no.

Final ledger status remains `BASELINE_REQUIRED`; this blocked pack does not count as `BASELINE_ALREADY_EXISTS`.

## Boundary Expectations

When DB readiness returns `READY`, the benchmark must not weaken expectations that:

- ObjectTime is source evidence and PayRun inclusion context, not payroll calculation truth.
- SourceTruth and WorkedHours are separate concepts.
- Raw span hours are not user-facing payroll worked hours.
- Worked hours must come from interpreted payroll truth or governed payroll bucket results where supported.
- ObjectTime can support the journey of why a source row did or did not calculate, but diagnostics do not prove runtime calculation.
- ObjectTime source changes can affect payroll causality, dirty state, finalised correction review and evidence preservation.

## Source References

- Runbook: `docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.objecttime_source_truth.json`
- Runner: `scripts/run_golden_questions.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

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
- does not prove payroll/runtime truth;
- does not change workforce-platform.
