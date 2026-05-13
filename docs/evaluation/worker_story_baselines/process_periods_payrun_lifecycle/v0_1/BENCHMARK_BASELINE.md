# Process Periods / PayRun Lifecycle Benchmark Baseline

This file records intentional benchmark non-execution for the Process Periods / PayRun Lifecycle baseline pack. It is diagnostic-only and not operational truth.

## Command Not Run

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

Attempted baseline capture on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `DATABASE_CONNECTION_FAILED`.

## Scope

The benchmark scope is the Process Periods / PayRun Lifecycle rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

The manifest covers governed payroll-period context, `ProcessPeriod`, `ProcessPeriodGroup`, `PaymentDate`, PayRun creation, worker admission, run type, run purpose, regular, supplementary and retro PayRuns, `PayRunContact`, admission versus processing, current-effective output and connections to Finalisation Readiness, Payment Execution, Worker Story, Admin Queue and Movement Review.

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

- Process Periods and PayRuns provide operational payroll context, not mere date ranges or run lists.
- `PaymentDate` belongs on `ProcessPeriod`.
- Default/payment-date derivation policy belongs on `ProcessPeriodGroup` or equivalent governed policy, not hardcoded logic.
- Payroll calendar and year definitions must be governed and configurable.
- Pay frequency coverage must honestly distinguish supported frequencies from gaps.
- Open or non-finalised PayRuns differ from finalised or protected PayRuns.
- Dirty `PayRunContact` evidence means reprocessing is required before safe use.
- Finalised or protected PayRuns require correction or review pathways rather than ordinary mutation.
- Minerva baseline packs do not prove runtime payroll truth.

## Source References

- Runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json`
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
