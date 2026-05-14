# Imports / Actuals Baseline Summary

Slice name: Imports / Actuals Baseline Capture v0.1

Domain: Imports / Actuals

Source runbook: `docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This blocked baseline pack is diagnostic-only and not operational truth. It records DB-readiness non-execution for Imports / Actuals and does not capture benchmark, corpus coverage or answer gap results.

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

Because readiness was not `READY`, Imports / Actuals benchmark, corpus coverage and answer gap commands were not run. No generated JSON reports were produced for this Imports / Actuals attempt.

## Commands

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| DB readiness check | `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py` | yes | `DATABASE_CONNECTION_FAILED`; ready: no. |
| Imports / Actuals benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.imports_actuals.json` | no | Blocked by DB readiness. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_imports_actuals_corpus_coverage.py` | no | Blocked by DB readiness. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_imports_actuals_corpus_coverage.py --json --output .\artifacts\eval\imports_actuals_corpus_coverage.json` | no | Blocked by DB readiness; generated artefact committed: no. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json` | no | Blocked by DB readiness. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json --json --output .\artifacts\eval\imports_actuals_answer_gap_report.json` | no | Blocked by DB readiness; generated artefact committed: no. |

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

Imports / Actuals provides source-evidence and reconciliation context for payroll truth. It is not merely file upload or CSV parsing, and it is not calculated payroll truth.

The next captured run must preserve evidence for:

- import batch;
- import row;
- import validation;
- import error;
- import warning;
- import template;
- award-specific CSV template;
- timesheet import;
- payroll actuals import;
- external actuals;
- calculated versus actual;
- reconciliation;
- variance;
- pay code mapping;
- RateType mapping;
- tenant override mapping;
- mapping snapshot;
- shift assessment import;
- shift attribute import;
- claim import;
- Claimable;
- Claimable Hourly;
- Claim Amount;
- piece work / expense / mileage amount import context;
- source truth provenance;
- evidence preservation;
- worker story explanation context;
- source truth impact on PayRun outcomes;
- no runtime mutation guarantee;
- no benchmark promotion when DB readiness is blocked.

Current doctrine to preserve:

- Award-specific imports must use templates with validation and an error-resolution workflow.
- Claims include boolean Claimable and Claimable Hourly today, with future Claim Amount support for piece work, expense and mileage.
- Pay code mapping to RateTypes must support tenant overrides and mapping snapshots.
- Imported actuals are evidence for reconciliation; they are not the same as calculated payroll truth.
- Source truth, actuals and calculated payroll outcomes must remain explainable as separate evidence chapters.
- Minerva baseline packs do not mutate operational payroll data.

## Not Implemented

This pack does not implement or claim:

- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- corpus mutation;
- DB or schema migration;
- endpoint or UI changes;
- workforce-platform changes;
- import runtime changes;
- reconciliation runtime changes;
- PayRun runtime changes;
- actuals ingestion runtime;
- dirty runtime calls;
- finalised correction intake creation;
- review request creation;
- correction execution;
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
- does not prove runtime import/actuals truth;
- does not prove imported actuals are calculated interpreter truth;
- does not prove imported source data is automatically correct;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Fix SQL Server connectivity or credentials so the readiness check returns `READY` before running commands. Then rerun the Imports / Actuals benchmark, corpus coverage diagnostic and answer gap report before moving this domain to `BASELINE_ALREADY_EXISTS`.
