# Imports / Actuals Benchmark Baseline

This file records intentional benchmark non-execution for the Imports / Actuals baseline pack. It is diagnostic-only and not operational truth.

## Command Not Run

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.imports_actuals.json
```

Attempted baseline capture on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `DATABASE_CONNECTION_FAILED`.

## Scope

The benchmark scope is the Imports / Actuals rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.imports_actuals.json
```

The manifest covers Imports / Actuals, governed imported evidence, imported timesheet source truth, imported payroll actuals, external actuals, source-system mapping, validation, pay code / RateType mapping, position/classification mapping, ObjectTime/source truth, Comparison / Remediation, reconciliation, Movement Review, Worker Story, Admin Queue, evidence provenance and audit.

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

- Imports / Actuals is source-evidence and reconciliation context, not merely file upload or CSV parsing.
- Imported timesheet truth and imported payroll actuals are separate evidence lanes.
- Imported actuals are evidence for reconciliation and variance explanation; they are not calculated payroll truth.
- Source truth, actuals and calculated payroll outcomes remain explainable as separate evidence chapters.
- Award-specific imports use templates with validation and error-resolution workflow.
- Pay code mapping to RateTypes supports tenant overrides and mapping snapshots.
- Claim imports preserve Claimable, Claimable Hourly and future Claim Amount context for piece work, expense and mileage.
- Minerva baseline packs do not mutate operational payroll data.

## Source References

- Runbook: `docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.imports_actuals.json`
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
