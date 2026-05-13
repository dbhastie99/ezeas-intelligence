# Process Periods / PayRun Lifecycle Baseline Summary

Slice name: Process Periods / PayRun Lifecycle Baseline Capture v0.1

Domain: Process Periods / PayRun Lifecycle

Source runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This blocked baseline pack is diagnostic-only and not operational truth. It records DB-readiness non-execution for Process Periods / PayRun Lifecycle and does not capture benchmark, corpus coverage or answer gap results.

## Execution Context

Attempted on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `DATABASE_CONNECTION_FAILED`.

- Readiness command: `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py`
- Ready: no.
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none.
- Configuration source reported: `.env:MINERVA_DATABASE_URL`
- Dialect/driver reported: `mssql/pyodbc`
- Selected ODBC driver reported: `ODBC Driver 18 for SQL Server`
- Error class: `pyodbc.OperationalError`
- Result status: `BLOCKED_DATABASE_CONNECTION`

Because readiness was not `READY`, Process Periods / PayRun Lifecycle benchmark, corpus coverage and answer gap commands were not run. No generated JSON reports were produced for this Process Periods / PayRun Lifecycle attempt.

## Commands

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| DB readiness check | `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py` | yes | `DATABASE_CONNECTION_FAILED`; ready: no. |
| Process Periods / PayRun Lifecycle benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json` | no | Blocked by DB readiness. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py` | no | Blocked by DB readiness. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py --json --output .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json` | no | Blocked by DB readiness; generated artefact committed: no. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json` | no | Blocked by DB readiness. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json --json --output .\artifacts\eval\process_period_payrun_lifecycle_answer_gap_report.json` | no | Blocked by DB readiness; generated artefact committed: no. |

## Blocked Finding

- Readiness status: `DATABASE_CONNECTION_FAILED`.
- Result status: `BLOCKED_DATABASE_CONNECTION`.
- Baseline pack created: blocked pack only.
- Benchmark result: not run.
- Corpus coverage result: not run.
- Answer gap report: not run.
- Generated artefact committed: no.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Final ledger status remains `BASELINE_REQUIRED`.
- This blocked pack does not count as `BASELINE_ALREADY_EXISTS`.

## Domain Boundary To Preserve

Process Periods / PayRun Lifecycle provides operational payroll context for pay period membership, payment date context, payroll frequency, PayRun state, worker inclusion, recalculation readiness, finalisation boundaries, payroll evidence snapshots, worker story context, reconciliation context, movement/change comparison context, tax/payment-date context where supported and batch/group period policy context where supported.

It is not merely a date range or run list domain. It is also not runtime ProcessPeriod, PayRun, payment execution or finalisation truth.

The next captured run must preserve these boundaries:

- `PaymentDate` belongs on `ProcessPeriod`.
- Default or derived payment-date policy belongs on `ProcessPeriodGroup` or an equivalent governed policy, not hardcoded logic.
- Payroll calendar and payroll-year definitions must be governed and configurable, not hardcoded.
- Pay frequency support must ultimately include `DAILY`, `WEEKLY`, `FORTNIGHTLY`, `MONTHLY` and `QUARTERLY` where relevant.
- Unsupported frequencies or incomplete provider coverage must be surfaced honestly.
- Dirty contact doctrine means payroll-impacting source or configuration changes make the current `PayRunContact` unsafe until reprocessed.
- Default dirty-contact response is full contact-level PayRun reprocessing unless selective recalculation is explicitly supported, tested and explainable.
- Finalised or protected PayRuns require correction or review pathways rather than ordinary mutation.
- Minerva baseline packs are diagnostic comparison controls, not operational payroll truth.

## Not Implemented

This pack does not implement or claim:

- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- corpus mutation;
- DB or schema migration;
- endpoint or UI changes;
- workforce-platform changes;
- PayRun runtime changes;
- ProcessPeriod runtime changes;
- dirty runtime calls;
- finalised correction intake creation;
- review request creation;
- correction execution;
- retro or replay execution;
- supplementary execution;
- adjustment execution;
- payment or remittance execution;
- finalisation execution.

## Guardrails

This blocked pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime ProcessPeriod or PayRun lifecycle truth;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Fix SQL Server connectivity or credentials so the readiness check returns `READY` before running commands. Then rerun the Process Periods / PayRun Lifecycle benchmark, corpus coverage diagnostic and answer gap report before moving this domain to `BASELINE_ALREADY_EXISTS`.
