# Payroll Bases & Totals Baseline Summary

Slice name: Minerva Domain Baseline Capture Batch v0.1 - Blocked Database Capture

Domain: Payroll Bases & Totals

Source runbook: `docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in capture record for a controlled baseline attempt, not proof of runtime implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

The read-only DB readiness gate returned `DATABASE_CONNECTION_FAILED` before the domain baseline commands were run.

- Readiness command: `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py`
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none
- Blocker: SQL Server connection could not be established from this environment.

Because DB readiness did not pass, the benchmark, corpus coverage diagnostic and answer gap report commands were not executed in this slice.

## Commands Identified

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| Payroll Bases & Totals benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_bases_and_totals.json` | no | `BLOCKED_DATABASE_CONNECTION`; no pass/fail counts captured. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py` | no | `BLOCKED_DATABASE_CONNECTION`; no `STRONG` / `WEAK` / `MISSING` counts captured. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py --json --output .\artifacts\eval\payroll_bases_corpus_coverage.json` | no | `BLOCKED_DATABASE_CONNECTION`; generated JSON was not created. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json` | no | `BLOCKED_DATABASE_CONNECTION`; no overall status or action counts captured. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json --json --output .\artifacts\eval\payroll_bases_answer_gap_report.json` | no | `BLOCKED_DATABASE_CONNECTION`; generated JSON was not created. |

## Captured High-Level Findings

- DB readiness result: `DATABASE_CONNECTION_FAILED`.
- Benchmark result: `BLOCKED_DATABASE_CONNECTION`; counts not captured.
- Corpus coverage result: `BLOCKED_DATABASE_CONNECTION`; counts not captured.
- Answer gap report: `BLOCKED_DATABASE_CONNECTION`; actions not captured.
- Audit/chat rows created: not available because the benchmark was not run.
- Command availability: canonical runbook commands and scripts exist.
- Generated artefacts committed: no.

## Evidence Groups In Scope

The canonical coverage plan exists, but group statuses were not captured:

- `purpose_and_operator_meaning`
- `bucket_definition_and_membership`
- `worked_hours_and_quantity`
- `gross_ordinary_superable_taxable_bases`
- `current_effective_truth`
- `readiness_and_rebuild`
- `worker_story_connection`
- `movement_review_connection`
- `outstanding_hardening`

## Known Gaps

- This pack records a blocked baseline capture attempt, not an executed comparison baseline.
- No benchmark pass/fail counts are available for this slice.
- No corpus coverage counts are available for this slice.
- No answer gap status or recommended action counts are available for this slice.
- Annual Leave / Leave Management remains `RUNBOOK_OUTSTANDING` in the completed-domain ledger.

## Guardrails

This baseline pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Restore database connectivity and rerun the Payroll Bases & Totals benchmark, corpus coverage diagnostic and answer gap report commands before treating this domain as `BASELINE_ALREADY_EXISTS`.
