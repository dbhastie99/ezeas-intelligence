# Movement Review Corpus Coverage Baseline

This file records the Movement Review corpus coverage baseline capture attempt for comparison control. It is diagnostic-only and not operational truth.

## Commands Identified

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_movement_review_corpus_coverage.py
```

JSON mode with output file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_movement_review_corpus_coverage.py --json --output .\artifacts\eval\movement_review_corpus_coverage.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Evidence Group Coverage Summary

Domain: Movement Review

Result status: `BLOCKED_DATABASE_CONNECTION`

| Evidence Group | Captured Coverage Status |
|---|---|
| `purpose_and_operator_meaning` | not captured |
| `reasonableness_not_error` | not captured |
| `worker_and_organisation_lenses` | not captured |
| `variance_and_comparable_periods` | not captured |
| `payroll_bases_connection` | not captured |
| `worker_story_connection` | not captured |
| `admin_queue_connection` | not captured |
| `current_effective_truth` | not captured |
| `trend_only_and_threshold_treatment` | not captured |
| `filters_and_return_context` | not captured |
| `outstanding_hardening` | not captured |

## Coverage Counts

- `STRONG`: not captured
- `WEAK`: not captured
- `MISSING`: not captured

Generated artefact committed: no. The JSON output command was not run and `.\artifacts\eval\movement_review_corpus_coverage.json` was not created by this slice.

Live LLM calls: no.

Corpus mutation: no.

## Status Interpretation

- `STRONG`: multiple relevant chunks or documents were found and the group is likely well supported by indexed formal evidence.
- `WEAK`: some relevant formal evidence was found, but coverage is thin or narrow.
- `MISSING`: no useful formal-corpus support was found for the group.

Coverage status is about available indexed formal corpus evidence. It is not operational truth and does not prove whether the platform runtime implements the behavior.

## Diagnostic Interpretation

No coverage interpretation is made for Movement Review in this slice because the DB readiness gate failed.

## Diagnostic-Only Guardrails

This corpus coverage baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.
