# PayRun Admin Queue Corpus Coverage Baseline

This file records the PayRun Admin Queue corpus coverage baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Commands Executed

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payrun_admin_queue_corpus_coverage.py
```

JSON mode with output file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payrun_admin_queue_corpus_coverage.py --json --output .\artifacts\eval\payrun_admin_queue_corpus_coverage.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Evidence Group Coverage Summary

Domain: PayRun Admin Queue

Result status: `COMPLETED`

Indexed corpus: 5 active documents, 4583 chunks.

| Evidence Group | Captured Coverage Status |
|---|---|
| `purpose_and_operator_meaning` | `STRONG` |
| `blockers_warnings_and_ready_actions` | `STRONG` |
| `worker_attention_and_dirty_contacts` | `STRONG` |
| `processing_and_reprocessing_actions` | `STRONG` |
| `finalisation_readiness` | `STRONG` |
| `assurance_snapshot` | `STRONG` |
| `review_surfaces_and_navigation` | `STRONG` |
| `worker_story_connection` | `STRONG` |
| `payroll_bases_connection` | `STRONG` |
| `movement_review_connection` | `STRONG` |
| `outstanding_hardening` | `STRONG` |

## Coverage Counts

- `STRONG`: 11
- `WEAK`: 0
- `MISSING`: 0

Generated artefact committed: no. The JSON output command created `.\artifacts\eval\payrun_admin_queue_corpus_coverage.json` locally for summarization, but the file is not a required committed artefact.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Status Interpretation

- `STRONG`: multiple relevant chunks or documents were found and the group is likely well supported by indexed formal evidence.
- `WEAK`: some relevant formal evidence was found, but coverage is thin or narrow.
- `MISSING`: no useful formal-corpus support was found for the group.

Coverage status is about available indexed formal corpus evidence. It is not operational truth and does not prove whether the platform runtime implements the behavior.

## Diagnostic Interpretation

All 11 PayRun Admin Queue evidence groups were reported as `STRONG`. The benchmark failures are not classified as corpus gaps because the coverage diagnostic reported no `WEAK` or `MISSING` groups.

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
