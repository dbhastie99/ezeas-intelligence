# Process Periods / PayRun Lifecycle Corpus Coverage Baseline

This file records intentional corpus coverage non-execution for the Process Periods / PayRun Lifecycle baseline pack. It is diagnostic-only and not operational truth.

## Commands Not Run

```powershell
.\.venv\Scripts\python.exe scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py --json --output .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
```

DB readiness returned `DATABASE_CONNECTION_FAILED`, so the coverage diagnostic was not run.

## Scope

The Process Periods / PayRun Lifecycle corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage should preserve evidence for:

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

## Blocked Result Summary

Result status: `BLOCKED_DATABASE_CONNECTION`

- Domain: Process Periods / PayRun Lifecycle
- Plan id: not evaluated
- Evidence groups: not evaluated
- `STRONG`: not evaluated
- `WEAK`: not evaluated
- `MISSING`: not evaluated
- Coverage JSON generated: no
- Generated artefact committed: no
- Indexed corpus: not evaluated
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Corpus coverage result: not run.

Baseline pack created: blocked pack only.

Final ledger status remains `BASELINE_REQUIRED`; this blocked pack does not count as `BASELINE_ALREADY_EXISTS`.

## Source References

- Runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/process_period_payrun_lifecycle_corpus_coverage_service.py`
- Coverage script: `scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Interpretation

No coverage conclusion exists for this slice. The next run must wait for readiness to be `READY` before running commands and must report Process Periods / PayRun Lifecycle evidence gaps from actual diagnostic output.

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
