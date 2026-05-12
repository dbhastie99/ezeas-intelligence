# Payroll Bases & Totals Answer Gap Report Baseline

This file records the Payroll Bases & Totals answer gap report baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Commands Executed

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json
```

JSON mode with output file:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json --json --output .\artifacts\eval\payroll_bases_answer_gap_report.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Captured Result Summary

Result status: `COMPLETED`

Report type: `PAYROLL_BASES_ANSWER_GAP_REPORT`

Source coverage plan: `PAYROLL_BASES_AND_TOTALS`

Overall status: `NEEDS_REFINEMENT`

Recommended action counts:

- `KEEP`: 8
- `IMPROVE_RETRIEVAL_TERMS`: 1
- `IMPROVE_SYNTHESIS`: 0
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 0

The following eight evidence groups were reported as `STRONG` -> `KEEP`:

- `purpose_and_operator_meaning`
- `bucket_definition_and_membership`
- `worked_hours_and_quantity`
- `gross_ordinary_superable_taxable_bases`
- `current_effective_truth`
- `readiness_and_rebuild`
- `worker_story_connection`
- `movement_review_connection`

The following weak/refinement group was reported as `WEAK` -> `IMPROVE_RETRIEVAL_TERMS`:

- `outstanding_hardening`

Recommended next action: Refine Payroll Bases & Totals retrieval terms for weak supporting groups before adding new corpus.

Generated artefact committed: no. `.\artifacts\eval\payroll_bases_answer_gap_report.json` was generated locally and summarized in this curated markdown baseline.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Status Interpretation

- `GOOD`: core evidence is strong enough for the current answer path.
- `NEEDS_REFINEMENT`: evidence exists, but retrieval terms or synthesis may need refinement.
- `INSUFFICIENT_CORPUS`: important evidence is missing from the indexed formal corpus.

Answer gap status is an evaluation signal. It is not operational truth and does not prove runtime implementation.

## Recommended Actions

The Payroll Bases & Totals answer gap report can recommend:

- `KEEP`: leave the current retrieval and synthesis behavior unchanged for the group.
- `IMPROVE_RETRIEVAL_TERMS`: refine deterministic search terms or group targeting so existing corpus evidence is found more reliably.
- `IMPROVE_SYNTHESIS`: adjust answer synthesis so retrieved evidence is explained more clearly and completely.
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: defer code changes and add or author formal source evidence in a later corpus slice.

## Diagnostic Interpretation

The answer gap report says `KEEP` for eight groups and `IMPROVE_RETRIEVAL_TERMS` for `outstanding_hardening`. This is a retrieval-term refinement target, not authorization to ingest operational JSON, connect Code Evidence to answers, call a live LLM or mutate corpus.

## Diagnostic-Only Guardrails

This answer gap report baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.
