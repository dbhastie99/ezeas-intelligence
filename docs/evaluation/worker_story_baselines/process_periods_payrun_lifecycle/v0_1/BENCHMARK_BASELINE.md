# Process Periods / PayRun Lifecycle Benchmark Baseline

This file records manually captured benchmark output for the Process Periods / PayRun Lifecycle promoted baseline. It is diagnostic-only and not operational truth.

## Command

```powershell
python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

Recaptured on 2026-05-14 from `C:\Projects\ezeas-intelligence` after DB readiness returned `READY`.

## Scope

The benchmark scope is the Process Periods / PayRun Lifecycle rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

The manifest covers governed payroll-period context, `ProcessPeriod`, `ProcessPeriodGroup`, `PaymentDate`, PayRun creation, worker admission, run type, run purpose, regular, supplementary, retro, termination, reversal and adjustment PayRuns, `PayRunContact`, admission versus processing, current-effective output and connections to Finalisation Readiness, Payment Execution, Worker Story, Admin Queue and Movement Review.

## Captured Result Summary

Result status: `PROMOTED_BASELINE_CAPTURED`

- Golden questions: Process Periods / PayRun Lifecycle rich-answer benchmark
- Total: 13
- Passed: 13
- Failed: 0
- Audit/chat rows created: false

Benchmark result: completed with full pass.

Baseline pack state: captured evidence and promoted.

Generated artefact committed: no.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

Code Evidence answer integration: no.

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Boundary Expectations

The benchmark did not weaken expectations that:

- ProcessPeriod is governed payroll-period context, payment-event lifecycle evidence, not payroll calculation truth and not a generic date range.
- ProcessPeriodGroup carries recurring calendar and payment policy context where supported.
- Open, not-open and closed are distinct lifecycle states, and closed dominates open to protect closed-period truth.
- Close rolls forward may open next period or create next period only where implemented.
- PaymentDate matters for tax/PAYG, payment context and governed derived calendar policy; it must not be hardcoded.
- PayRun creation and PayRun admission are not payroll processing, and admission is not processing.
- PayRunContact represents worker participation, admission and processing state.
- Current-effective output and current-effective payroll output must not treat stale or superseded rows as current truth.
- Finalisation readiness, payment execution, period close, Worker Story, PayRun Admin Queue and Movement Review are downstream evidence/review consumers, not Minerva mutation authority.

## Source References

- Runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`
- Manifest: `samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json`
- Runner: `scripts/run_golden_questions.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Diagnostic-Only Guardrails

This benchmark baseline:

- does not mutate corpus;
- does not change endpoint/UI/runtime behavior;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth;
- does not change workforce-platform.
