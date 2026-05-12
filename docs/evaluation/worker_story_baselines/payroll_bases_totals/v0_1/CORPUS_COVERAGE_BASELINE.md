# Payroll Bases & Totals Corpus Coverage Baseline

This file records the Payroll Bases & Totals corpus coverage baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Commands Executed

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py
```

JSON mode with output file:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py --json --output .\artifacts\eval\payroll_bases_corpus_coverage.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Evidence Group Coverage Summary

Domain: Payroll Bases & Totals

Result status: `COMPLETED`

Indexed corpus: 5 active documents, 4583 chunks

| Evidence Group | Captured Coverage Status |
|---|---|
| `purpose_and_operator_meaning` | STRONG |
| `bucket_definition_and_membership` | STRONG |
| `worked_hours_and_quantity` | STRONG |
| `gross_ordinary_superable_taxable_bases` | STRONG |
| `current_effective_truth` | STRONG |
| `readiness_and_rebuild` | STRONG |
| `worker_story_connection` | STRONG |
| `movement_review_connection` | STRONG |
| `outstanding_hardening` | WEAK |

## Coverage Counts

- `STRONG`: 8
- `WEAK`: 1
- `MISSING`: 0

Generated artefact committed: no. `.\artifacts\eval\payroll_bases_corpus_coverage.json` was generated locally and summarized in this curated markdown baseline.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Status Interpretation

- `STRONG`: multiple relevant chunks or documents were found and the group is likely well supported by indexed formal evidence.
- `WEAK`: some relevant formal evidence was found, but coverage is thin or narrow.
- `MISSING`: no useful formal-corpus support was found for the group.

Coverage status is about available indexed formal corpus evidence. It is not operational truth and does not prove whether the platform runtime implements the behavior.

## Diagnostic Interpretation

Payroll Bases & Totals has strong indexed corpus support for eight of nine planned evidence groups. `outstanding_hardening` has weak support and should be refined through retrieval terms before adding new corpus.

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
