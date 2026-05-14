# Imports / Actuals Baseline Summary

Slice name: Imports / Actuals Baseline Recapture Result Update v0.1

Domain: Imports / Actuals

Source runbook: `docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This recaptured baseline result pack is diagnostic-only and not operational truth. It records manually captured PowerShell command outputs after DB readiness returned `READY`. Imports / Actuals remains `BASELINE_REQUIRED` because the benchmark failed 3 of 11 cases and the answer gap report is `NEEDS_REFINEMENT` with formal corpus gaps.

This is not a successful captured/promoted baseline. It is a recaptured baseline result requiring refinement and formal source evidence.

## Execution Context

Recaptured on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` in normal PowerShell before capture.

- Readiness command: `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py`
- Ready: yes.
- Configuration source: `.env:MINERVA_DATABASE_URL`
- Selected ODBC driver: `ODBC Driver 17 for SQL Server`
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none.
- Read-only guardrails remained in place.

## Commands

| Area | Command | Completed | Captured Result Summary |
|---|---|---:|---|
| Imports / Actuals benchmark | `python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.imports_actuals.json` | yes | 11 total / 8 passed / 3 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `python scripts\scan_imports_actuals_corpus_coverage.py` | yes | 12 evidence groups; STRONG=9, WEAK=1, MISSING=2; indexed corpus 5 active documents, 4583 chunks. |
| Corpus coverage JSON | `python scripts\scan_imports_actuals_corpus_coverage.py --json --output .\artifacts\eval\imports_actuals_corpus_coverage.json` | yes | Generated transient JSON; committed: no. |
| Answer gap report | `python scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json` | yes | `NEEDS_REFINEMENT`; 9 LOW / KEEP groups, 1 MEDIUM / IMPROVE_SYNTHESIS group, 2 ADD_FORMAL_SOURCE_EVIDENCE_LATER groups. |
| Answer gap report JSON | `python scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json --json --output .\artifacts\eval\imports_actuals_answer_gap_report.json` | yes | Generated transient JSON; committed: no. |

## Captured Finding

- DB readiness result: `READY`.
- Result status: `RECAPTURED_BASELINE_REQUIRES_REFINEMENT`.
- Baseline pack state: recaptured result, not promoted.
- Benchmark result: 11 total, 8 passed, 3 failed.
- Failed benchmark cases: `imports-actuals-pay-code-ratetype-mapping`, `imports-actuals-comparison-remediation-connection`, `imports-actuals-worker-story-admin-queue`.
- Corpus coverage result: STRONG=9, WEAK=1, MISSING=2.
- Weak coverage group: `pay_code_and_rate_type_mapping`.
- Missing coverage groups: `purpose_and_operator_meaning`, `outstanding_hardening`.
- Answer gap report: `NEEDS_REFINEMENT`.
- Answer gap actions: 9 KEEP, 1 IMPROVE_SYNTHESIS, 2 ADD_FORMAL_SOURCE_EVIDENCE_LATER.
- Indexed corpus: 5 active documents, 4583 chunks.
- Generated artefact committed: no.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Final ledger status remains `BASELINE_REQUIRED`.
- This recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

Unlike ObjectTime / Source Truth and Process Periods / PayRun Lifecycle, Imports / Actuals has real formal-corpus gaps, not only synthesis or retrieval drift. Promotion cannot happen solely through synthesis hardening unless the missing formal source evidence is addressed or the coverage plan is legitimately revised with justification.

## Domain Boundary To Preserve

Imports / Actuals provides source-evidence and reconciliation context for payroll truth. It is not merely file upload or CSV parsing, and it is not calculated payroll truth.

The next refinement slice must preserve evidence for:

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
- no promotion while benchmark failures and formal corpus gaps remain.

Current doctrine to preserve:

- Award-specific imports must use templates with validation and an error-resolution workflow.
- Claims include boolean Claimable and Claimable Hourly today, with future Claim Amount support for piece work, expense and mileage.
- Pay code mapping to RateTypes must support tenant overrides and mapping snapshots.
- Imported actuals are evidence for reconciliation; they are not the same as calculated payroll truth.
- Source truth, actuals and calculated payroll outcomes must remain explainable as separate evidence chapters.
- Minerva baseline packs do not mutate operational payroll data.

## Not Implemented

This pack does not implement or claim:

- no DB writes;
- no migrations;
- no corpus mutation;
- no operational JSON ingestion;
- no Code Evidence answer integration;
- no live LLM calls;
- no endpoint/UI/workforce-platform/runtime changes;
- no import runtime changes;
- no reconciliation runtime changes;
- no PayRun runtime changes;
- no actuals ingestion runtime;
- no dirty runtime calls;
- no correction/review/payment/finalisation execution;
- finalised correction intake creation;
- review request creation;
- correction execution;
- payment or remittance execution;
- finalisation execution.

## Guardrails

This recaptured baseline result pack:

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

Add formal source evidence later for `purpose_and_operator_meaning` and `outstanding_hardening` before widening answer claims. Tighten Imports / Actuals answer synthesis for `pay_code_and_rate_type_mapping` while keeping status caveats, then rerun benchmark, corpus coverage and answer gap diagnostics before considering promotion.
