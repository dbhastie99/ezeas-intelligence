# Payroll Evidence Context Baseline Batch v0.1

Date: 2026-05-13

This batch inspected four selected `BASELINE_REQUIRED` Payroll Evidence Context domains and stopped at DB readiness because the shared read-only readiness check returned `DATABASE_CONNECTION_FAILED`.

This is a blocked baseline-capture slice, not a captured baseline slice. It is diagnostic-only and not operational truth.

## Domains In Scope

- Contact Payroll History
- ObjectTime / Source Truth
- Process Periods / PayRun Lifecycle
- Imports / Actuals

No other baseline-required domains were attempted.

## Readiness Result

Command run from `C:\Projects\ezeas-intelligence`:

```powershell
.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py
```

Readiness status: `DATABASE_CONNECTION_FAILED`

Ready: no

Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`

Missing tables: none

The readiness output reported configured `.env:MINERVA_DATABASE_URL`, selected `mssql/pyodbc` with ODBC Driver 18 for SQL Server, and a SQL Server connection failure to the configured localhost target. The connection string value was intentionally not printed.

Because readiness was not `READY`, benchmark, corpus coverage and answer gap commands were not run for this batch.

## Ledger State After Slice

- `BASELINE_REQUIRED`: 21
- `BASELINE_ALREADY_EXISTS`: 10
- `RUNBOOK_OUTSTANDING`: 0

The four selected domains remain `BASELINE_REQUIRED`. They have v0.4 runbooks and required tooling, but no captured command summaries because DB readiness blocked execution.

## Domain Outcomes

| Domain | Readiness status | Baseline pack created | Benchmark result | Corpus coverage result | Answer gap result | Ledger status |
| --- | --- | --- | --- | --- | --- | --- |
| Contact Payroll History | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |
| ObjectTime / Source Truth | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |
| Process Periods / PayRun Lifecycle | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |
| Imports / Actuals | `DATABASE_CONNECTION_FAILED` | blocked pack only | not run | not run | not run | `BASELINE_REQUIRED` |

## Generated Artefact Status

No benchmark, corpus coverage or answer gap JSON reports were generated for this batch. Generated JSON outputs under `.\artifacts\eval\` remain transient evaluation materials and are not required committed baseline artefacts.

## Guardrails

This blocked slice did not implement or authorize:

- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- corpus mutation;
- DB or schema migration;
- endpoints or UI;
- workforce-platform changes.

No operational JSON ingestion occurred. No Code Evidence answer integration occurred. No live LLM call occurred. No corpus mutation occurred. No DB or schema migration occurred. No endpoint or UI change occurred. No workforce-platform change occurred.

The recommended next baseline batch should remain small and should retry these four domains only after readiness returns `READY`.
