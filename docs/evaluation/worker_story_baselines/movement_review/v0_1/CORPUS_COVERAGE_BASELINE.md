# Movement Review Corpus Coverage Baseline

This file records the Movement Review corpus coverage baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Commands Executed

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

Result status: `COMPLETED`

Indexed corpus: 5 active documents, 4583 chunks.

| Evidence Group | Captured Coverage Status |
|---|---|
| `purpose_and_operator_meaning` | `STRONG` |
| `reasonableness_not_error` | `STRONG` |
| `worker_and_organisation_lenses` | `STRONG` |
| `variance_and_comparable_periods` | `STRONG` |
| `payroll_bases_connection` | `STRONG` |
| `worker_story_connection` | `STRONG` |
| `admin_queue_connection` | `STRONG` |
| `current_effective_truth` | `STRONG` |
| `trend_only_and_threshold_treatment` | `STRONG` |
| `filters_and_return_context` | `STRONG` |
| `outstanding_hardening` | `STRONG` |

## Coverage Counts

- `STRONG`: 11
- `WEAK`: 0
- `MISSING`: 0

Generated artefact committed: no. The JSON output command created `.\artifacts\eval\movement_review_corpus_coverage.json` locally for summarization, but the file is not a required committed artefact.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Status Interpretation

- `STRONG`: multiple relevant chunks or documents were found and the group is likely well supported by indexed formal evidence.
- `WEAK`: some relevant formal evidence was found, but coverage is thin or narrow.
- `MISSING`: no useful formal-corpus support was found for the group.

Coverage status is about available indexed formal corpus evidence. It is not operational truth and does not prove whether the platform runtime implements the behavior.

## Diagnostic Interpretation

All 11 Movement Review evidence groups were reported as `STRONG`.

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
