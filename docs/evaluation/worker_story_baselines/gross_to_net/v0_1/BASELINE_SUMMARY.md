# Gross-to-Net Baseline Summary

Slice name: Minerva Domain Baseline Capture Batch v0.1 - Blocked Database Capture

Domain: Gross-to-Net

Source runbook: `docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md`

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
| Gross-to-Net benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.gross_to_net.json` | no | `BLOCKED_DATABASE_CONNECTION`; no pass/fail counts captured. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_gross_to_net_corpus_coverage.py` | no | `BLOCKED_DATABASE_CONNECTION`; no `STRONG` / `WEAK` / `MISSING` counts captured. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_gross_to_net_corpus_coverage.py --json --output .\artifacts\eval\gross_to_net_corpus_coverage.json` | no | `BLOCKED_DATABASE_CONNECTION`; generated JSON was not created. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json` | no | `BLOCKED_DATABASE_CONNECTION`; no overall status or action counts captured. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json --json --output .\artifacts\eval\gross_to_net_answer_gap_report.json` | no | `BLOCKED_DATABASE_CONNECTION`; generated JSON was not created. |

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

- `gross_to_net_purpose`
- `gross_earnings_and_payroll_output`
- `taxable_basis_and_payg`
- `deductions_and_obligations`
- `negative_net_pay`
- `net_pay_and_payment_allocation`
- `worker_story_relationship`
- `finalisation_and_payment_execution`
- `current_effective_output_truth`
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

Restore database connectivity and rerun the Gross-to-Net benchmark, corpus coverage diagnostic and answer gap report commands before treating this domain as `BASELINE_ALREADY_EXISTS`.
