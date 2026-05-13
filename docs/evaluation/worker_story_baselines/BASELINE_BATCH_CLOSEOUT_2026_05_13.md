# Minerva Four-Domain Baseline Batch Close-Out v0.1

Date: 2026-05-13

This close-out records the completed small baseline capture batch for Payroll Bases & Totals, PayRun Admin Queue, Movement Review and Gross-to-Net.

It is a curated comparison-control summary. It is not authorization to rerun benchmarks, weaken benchmark expectations, ingest operational JSON, connect Code Evidence to answers, call a live LLM, mutate corpus records, run migrations, add endpoints, add UI, or modify workforce-platform.

## Ledger State

- `BASELINE_REQUIRED`: 25
- `BASELINE_ALREADY_EXISTS`: 5
- `RUNBOOK_OUTSTANDING`: 1
- Baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net.
- Annual Leave / Leave Management remains `RUNBOOK_OUTSTANDING`.

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

## Batch Outcomes

| Domain | Baseline outcome | Benchmark | Corpus coverage | Answer gap report | Close-out classification |
| --- | --- | --- | --- | --- | --- |
| Payroll Bases & Totals | Passed baseline | 6 total / 6 passed / 0 failed | STRONG=8, WEAK=1, MISSING=0 | NEEDS_REFINEMENT | Weak `outstanding_hardening` coverage requires retrieval-term hardening: `outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`. This is not a corpus gap. |
| PayRun Admin Queue | Captured-with-failures baseline | 8 total / 6 passed / 2 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions | Failed cases are `payrun-admin-queue-rich-answer` and `payrun-admin-queue-cleanliness-assurance`. Failure classification is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap. Do not weaken benchmark expectations. |
| Movement Review | Passed baseline | 8 total / 8 passed / 0 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions | Clean pass and GOOD answer gap report. |
| Gross-to-Net | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions | Failed case is `gross-to-net-current-effective-worker-story`. Failure classification is benchmark answer-term expectation drift, not corpus gap. Do not weaken benchmark expectations. |

## Preserved Interpretation

Payroll Bases & Totals is a passed baseline, but it is not a fully clean answer-gap close-out because `outstanding_hardening` is weak and maps to `IMPROVE_RETRIEVAL_TERMS`.

PayRun Admin Queue and Gross-to-Net are valid captured-with-failures baselines. Their failures remain benchmark expectation or source-evidence/retrieval drift signals, not corpus gaps.

Movement Review is the clean baseline in this batch: benchmark passed, corpus coverage is all STRONG, and answer gap status is GOOD.

Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials. They are not durable checked-in artefacts unless explicitly versioned as part of a baseline pack.

## Explicitly Not Implemented

This close-out did not implement or authorize:

- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- corpus mutation;
- DB or schema migration;
- endpoints or UI;
- workforce-platform changes.

No generated JSON output is made durable by this document unless a future slice explicitly versions that output as a baseline artefact.
