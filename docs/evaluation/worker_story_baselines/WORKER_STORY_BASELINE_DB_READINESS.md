# Worker Story Baseline DB Readiness

Worker Story Baseline-Capture Pilot v0.2 was blocked because the documented benchmark and corpus coverage commands could not connect to the configured SQL Server knowledge database. The captured baseline status was:

- Benchmark: `BLOCKED_DATABASE_CONNECTION`
- Corpus coverage: `BLOCKED_DATABASE_CONNECTION`
- Answer gap report: `BLOCKED_MISSING_COVERAGE_REPORT`

This readiness check exists so Worker Story baseline capture can be rerun only after the intended ezeas-intelligence knowledge store is reachable.

## Command

Run from the repository root:

```powershell
py scripts/check_worker_story_baseline_db_readiness.py
```

JSON output:

```powershell
py scripts/check_worker_story_baseline_db_readiness.py --json
```

The script exits `0` only when readiness status is `READY`. Any other status exits non-zero.

## What It Verifies

The check is intentionally small and read-only. It verifies:

- `MINERVA_DATABASE_URL` is configured in the environment or `.env`;
- the accepted configuration variable name is `MINERVA_DATABASE_URL`;
- which safe configuration source was used, without printing the connection string;
- the redacted SQL Server target, database target, DSN and selected ODBC driver when these can be parsed safely;
- local ODBC driver availability when `pyodbc` can inspect installed drivers;
- a database connection can be opened;
- the required knowledge tables are queryable by metadata inspection:
  - `KnowledgeDocument`
  - `KnowledgeChunk`

These are the minimum tables required by the Worker Story benchmark and corpus coverage diagnostic to read already indexed formal knowledge evidence.

## Statuses

- `READY`: configuration exists, the connection opens, and required knowledge tables are present.
- `MISSING_CONFIGURATION`: `MINERVA_DATABASE_URL` was not found in the environment or `.env`.
- `DATABASE_CONNECTION_FAILED`: configuration exists, but the database connection could not be opened.
- `REQUIRED_TABLES_MISSING`: the connection opened, but one or more required knowledge tables were not found.
- `UNKNOWN_ERROR`: an unexpected readiness-check error occurred.

## Troubleshooting `DATABASE_CONNECTION_FAILED`

Use the readiness output to determine where the failure starts. The diagnostic output is intentionally redacted and must not be edited to print passwords, access tokens or full connection strings.

1. Confirm the active configuration source:

```powershell
Get-ChildItem Env:MINERVA_DATABASE_URL
Select-String -Path .env -Pattern '^MINERVA_DATABASE_URL='
```

Environment variables take precedence over `.env`. If the environment variable is present, that is the active source even when `.env` also contains a value.

Accepted configuration variable:

- `MINERVA_DATABASE_URL`

Do not use `DATABASE_URL` or an unprefixed SQLAlchemy setting for this readiness check. The application settings use the `MINERVA_` prefix, and this diagnostic requires an explicit environment or `.env` value instead of silently relying on a local default.

2. Confirm the expected local SQL Server target for this repo.

The documented local example in `README.md` uses `mssql+pyodbc` with ODBC Driver 18, `Server=localhost`, and `Database=ezeas-intelligence-db`. If your environment uses a named SQL Server instance, a remote host, or a DSN, verify that the active `MINERVA_DATABASE_URL` points to that same intended knowledge store.

3. Confirm ODBC driver availability.

The readiness command reports the selected ODBC driver and, when `pyodbc` can inspect the machine, whether matching SQL Server ODBC drivers are installed. If the selected driver is unavailable, install the expected Microsoft SQL Server ODBC driver or update `MINERVA_DATABASE_URL` to an installed driver.

4. Confirm the required database name and tables.

The intended database must contain the Minerva knowledge tables:

- `KnowledgeDocument`
- `KnowledgeChunk`

Readiness is read-only. Do not run migrations, create tables, ingest corpus, or mutate schema as part of this recovery slice.

5. Rerun readiness before any baseline command:

```powershell
.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py
```

Do not treat `DATABASE_CONNECTION_FAILED` as a corpus coverage gap, benchmark failure or answer gap failure. When readiness is not `READY`, benchmark, corpus coverage and answer gap commands have not proven anything about corpus sufficiency.

## Before Retrying Baseline Capture

Only retry Worker Story baseline capture after this readiness command returns `READY`.

Then rerun the documented Worker Story baseline commands:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures
py scripts/scan_worker_story_corpus_coverage.py
py scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json --json --output reports/worker_story_answer_gap_report.json
```

## Guardrails

The readiness check is diagnostic-only and read-only. It:

- does not mutate corpus;
- does not create the database;
- does not create tables;
- does not run migrations;
- does not ingest documents;
- does not ingest operational JSON;
- does not connect Code Evidence to answers;
- does not call a live LLM;
- does not write chat messages or audit rows;
- does not prove runtime platform truth;
- does not prove payroll correctness.
