# Payroll Bases & Totals Baseline Summary

Slice name: Payroll Bases & Totals Baseline Capture v0.1 - Record READY Baseline Results

Domain: Payroll Bases & Totals

Source runbook: `docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future Payroll Bases & Totals evaluation changes. It does not prove runtime implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` after `MINERVA_DATABASE_URL` was switched to direct localhost before the Payroll Bases & Totals baseline commands were run.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none

Generated JSON reports were local/generated under `.\artifacts\eval\` and were not committed. This baseline summarizes those generated outputs into curated markdown only.

## Commands Executed

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| Payroll Bases & Totals benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_bases_and_totals.json` | yes | 6 total, 6 passed, 0 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py` | yes | Payroll Bases & Totals coverage reported 8 STRONG, 1 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py --json --output .\artifacts\eval\payroll_bases_corpus_coverage.json` | yes | Local generated JSON report created and summarized, not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json` | yes | Overall status NEEDS_REFINEMENT; 8 KEEP and 1 IMPROVE_RETRIEVAL_TERMS. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json --json --output .\artifacts\eval\payroll_bases_answer_gap_report.json` | yes | Local generated JSON report created and summarized, not committed. |

## Captured High-Level Findings

- DB readiness result: `READY`.
- Benchmark result: 6 total, 6 passed, 0 failed.
- Audit/chat rows created: false.
- Corpus coverage result: `STRONG` = 8, `WEAK` = 1, `MISSING` = 0.
- Indexed corpus: 5 active documents, 4583 chunks.
- Answer gap report: `NEEDS_REFINEMENT`.
- Recommended actions: 8 `KEEP`, 1 `IMPROVE_RETRIEVAL_TERMS`.
- Weak/refinement group: `outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`.
- Recommended next action: Refine Payroll Bases & Totals retrieval terms for weak supporting groups before adding new corpus.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Generated artefacts committed: no.

## Evidence Groups Covered By The Baseline Shape

The following Payroll Bases & Totals evidence groups were reported as `STRONG`:

- `purpose_and_operator_meaning`
- `bucket_definition_and_membership`
- `worked_hours_and_quantity`
- `gross_ordinary_superable_taxable_bases`
- `current_effective_truth`
- `readiness_and_rebuild`
- `worker_story_connection`
- `movement_review_connection`

The following evidence group was reported as `WEAK`:

- `outstanding_hardening`

No evidence groups were reported as `MISSING`.

## Known Gaps

- The answer gap report needs refinement for `outstanding_hardening`.
- The recommended action is retrieval-term refinement, not new corpus ingestion.
- Generated output files under `.\artifacts\eval\` were created locally and were not committed.
- PayRun Admin Queue, Movement Review and Gross-to-Net remain blocked v0.1 capture packs.
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

Refine Payroll Bases & Totals retrieval terms for `outstanding_hardening` before adding new corpus. Keep PayRun Admin Queue, Movement Review and Gross-to-Net in blocked baseline status until their own DB-backed commands are captured.
