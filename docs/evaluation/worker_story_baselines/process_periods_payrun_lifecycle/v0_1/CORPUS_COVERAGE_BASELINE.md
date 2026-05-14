# Process Periods / PayRun Lifecycle Corpus Coverage Baseline

This file records manually captured corpus coverage output for the Process Periods / PayRun Lifecycle promoted baseline. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py
python scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py --json --output .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
```

The generated JSON file `artifacts/eval/process_period_payrun_lifecycle_corpus_coverage.json` was produced as a transient evaluation artefact and must remain untracked.

## Scope

The Process Periods / PayRun Lifecycle corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage preserves evidence for `ProcessPeriod`, `ProcessPeriodGroup`, `PaymentDate`, PayRun creation, PayRun admission, `RunType`, `RunPurpose`, regular PayRun, supplementary PayRun, retro PayRun, termination PayRun, reversal PayRun, adjustment PayRun, `PayRunContact`, current-effective output, payment execution, period close, Worker Story, PayRun Admin Queue, Movement Review and outstanding hardening.

## Captured Result Summary

Result status: `COMPLETED`

- Plan/domain: `PROCESS_PERIOD_PAYRUN_LIFECYCLE` / Process Periods / PayRun Lifecycle
- Evidence groups: 13
- `STRONG`: 13
- `WEAK`: 0
- `MISSING`: 0
- Indexed corpus: 5 active documents, 4583 chunks
- Coverage JSON generated: yes
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Coverage Groups

- `purpose_and_operator_meaning`: STRONG
- `process_period_and_group_context`: STRONG
- `open_not_open_closed_lifecycle`: STRONG
- `close_rolls_forward`: STRONG
- `payment_date_and_calendar_policy`: STRONG
- `payrun_creation_and_admission`: STRONG
- `run_type_and_run_purpose`: STRONG
- `regular_supplementary_retro_distinction`: STRONG
- `payrun_contact_lifecycle`: STRONG
- `current_effective_output_and_finalisation`: STRONG
- `payment_execution_and_period_close`: STRONG
- `worker_story_admin_queue_and_movement_review_connection`: STRONG
- `outstanding_hardening`: STRONG

## Previously Weak Groups

- `purpose_and_operator_meaning`: now STRONG; representative terms include `ProcessPeriod`, Process Period, PayRun, payroll period and payment event.
- `close_rolls_forward`: now STRONG; representative terms include close rolls forward, rolls forward, closed period, next period and implemented.
- `outstanding_hardening`: now STRONG; representative terms include hardening, supplementary, retro, payment execution and not implemented.

## Source References

- Runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/process_period_payrun_lifecycle_corpus_coverage_service.py`
- Coverage script: `scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Diagnostic-Only Guardrails

This corpus coverage baseline:

- does not mutate corpus;
- does not ingest documents;
- does not ingest operational JSON;
- does not change endpoint/UI/runtime behavior;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
