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
