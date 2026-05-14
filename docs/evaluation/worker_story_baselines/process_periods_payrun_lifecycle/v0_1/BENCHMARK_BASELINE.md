# Process Periods / PayRun Lifecycle Benchmark Baseline

This file records the manually captured benchmark result for the Process Periods / PayRun Lifecycle baseline pack. It is diagnostic-only and not operational truth.

## Command

```powershell
python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

Recaptured on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness was `READY` in normal PowerShell before capture. Codex did not rerun this DB-backed command.

## Scope

The benchmark scope is the Process Periods / PayRun Lifecycle rich-answer manifest:

```text
samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

The manifest covers governed payroll-period context, `ProcessPeriod`, `ProcessPeriodGroup`, `PaymentDate`, PayRun creation, worker admission, run type, run purpose, regular, supplementary, retro, termination, reversal and adjustment PayRuns, `PayRunContact`, admission versus processing, current-effective output and connections to Finalisation Readiness, Payment Execution, Worker Story, Admin Queue and Movement Review.

## Captured Result Summary

Result status: `COMPLETED_WITH_FAILURES`

Pass/fail summary:

- Total: 13
- Passed: 7
- Failed: 6
- Audit/chat rows created: false

Baseline promotion: withheld.

Final ledger status remains `BASELINE_REQUIRED`; this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

## Failed Cases

### `process-period-payrun-lifecycle-rich-answer`

Question: How should Process Periods and PayRun Lifecycle work in Ezeas?

Missing expected terms include:

- `Process Periods / PayRun Lifecycle`
- `ProcessPeriod`
- `ProcessPeriodGroup`
- governed payroll-period
- payment-event lifecycle evidence
- not payroll calculation truth
- not a generic date range
- open
- not-open
- closed
- closed dominates open
- close rolls forward
- `PaymentDate`
- payment date
- tax/PAYG
- governed
- not hardcoded
- PayRun creation
- PayRun admission
- admission is not processing
- `RunType`
- `RunPurpose`
- regular PayRun
- supplementary PayRun
- retro PayRun
- termination PayRun
- reversal PayRun
- adjustment PayRun
- `PayRunContact`
- worker participation
- operational state layer
- current-effective output
- current-effective payroll output
- stale
- superseded
- current truth
- finalisation readiness
- payment execution
- period close
- downstream governed outcomes
- Worker Story
- PayRun Admin Queue
- Movement Review
- readiness
- review implications
- outstanding hardening

### `process-period-closed-dominates-open`

Question: Why does closed dominate open in ProcessPeriod governance?

Missing expected terms: closed, dominates open, closed dominates open, `ProcessPeriod`, period lifecycle and closed-period truth.

### `process-period-close-rolls-forward`

Question: What does close rolls forward mean?

Missing expected terms: close rolls forward, roll forward, period close, open next period, create next period and implemented.

### `process-period-paymentdate`

Question: Why does PaymentDate matter in Process Periods and PayRun Lifecycle?

Missing expected terms: `PaymentDate`, payment date, tax/PAYG, payment context, calendar policy, governed, derived and not hardcoded.

### `process-period-payrun-creation-admission`

Question: How do PayRun creation and worker admission work inside a ProcessPeriod?

Missing expected terms: PayRun creation, PayRun admission, `ProcessPeriod`, process-period context, worker inclusion, payment event and admission is not processing.

No source snippet or matched phrase contained expected terms PayRun creation, PayRun admission or admission is not processing.

### `process-period-admission-not-processing`

Question: Why is admission not the same as processing?

Missing expected terms: admission, processing, admission is not processing, worker inclusion, `PayRunContact` and processing state.

## Interpretation

The benchmark failures are answer-synthesis and retrieval-term issues, not corpus absence issues. Corpus coverage for the same recapture is 10 STRONG, 3 WEAK and 0 MISSING.

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
