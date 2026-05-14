# Process Periods / PayRun Lifecycle Corpus Coverage Baseline

This file records the manually captured corpus coverage result for the Process Periods / PayRun Lifecycle baseline pack. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py
python scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py --json --output .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
```

DB readiness was `READY` in normal PowerShell before capture. Codex did not rerun these DB-backed commands.

The generated JSON file `artifacts/eval/process_period_payrun_lifecycle_corpus_coverage.json` was produced as a transient evaluation artefact and must remain untracked.

## Scope

The Process Periods / PayRun Lifecycle corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage preserves evidence for:

- `ProcessPeriod`;
- `ProcessPeriodGroup`;
- `PaymentDate`;
- `PaymentDate` derivation from `ProcessPeriodGroup` policy;
- `PayRun`;
- `PayRunBatch`;
- `PayRunContact`;
- PayRun lifecycle state;
- open and non-finalised PayRuns;
- finalised and protected PayRuns;
- dirty `PayRunContact`;
- reprocessing requirement;
- finalisation lock or protection;
- payroll evidence snapshot;
- period-local context;
- payroll calendar policy;
- pay frequency;
- worker story PayRun context;
- Contact Payroll History dependency;
- reconciliation dependency;
- bucket source date or work date context where relevant;
- source truth impact on PayRun outcomes;
- no runtime mutation guarantee.

## Captured Result Summary

Result status: `COMPLETED_WITH_WEAK_GROUPS`

- Plan/domain: `PROCESS_PERIOD_PAYRUN_LIFECYCLE` / Process Periods / PayRun Lifecycle
- Evidence groups: 13
- `STRONG`: 10
- `WEAK`: 3
- `MISSING`: 0
- Indexed corpus: 5 active documents, 4583 chunks
- Coverage JSON generated: yes
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Final ledger status remains `BASELINE_REQUIRED`; this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

## Coverage Groups

- `purpose_and_operator_meaning`: WEAK
- `process_period_and_group_context`: STRONG
- `open_not_open_closed_lifecycle`: STRONG
- `close_rolls_forward`: WEAK
- `payment_date_and_calendar_policy`: STRONG
- `payrun_creation_and_admission`: STRONG
- `run_type_and_run_purpose`: STRONG
- `regular_supplementary_retro_distinction`: STRONG
- `payrun_contact_lifecycle`: STRONG
- `current_effective_output_and_finalisation`: STRONG
- `payment_execution_and_period_close`: STRONG
- `worker_story_admin_queue_and_movement_review_connection`: STRONG
- `outstanding_hardening`: WEAK

## Representative Weak Groups

- `purpose_and_operator_meaning`: matched 8 chunks across 2 documents; representative term `ProcessPeriod`.
- `close_rolls_forward`: matched 5 chunks across 1 document; representative term `close rolls forward`.
- `outstanding_hardening`: matched 3 chunks across 1 document; representative term `payment execution`.

## Interpretation

There is no corpus absence finding for this recapture. The benchmark and answer-gap failures should be handled as answer-synthesis and retrieval-term refinement work before adding new corpus.

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
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
