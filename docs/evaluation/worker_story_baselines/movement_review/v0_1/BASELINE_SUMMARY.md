# Movement Review Baseline Summary

Slice name: Movement Review Baseline Capture v0.1 - Record READY Baseline Results

Domain: Movement Review

Source runbook: `docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future Movement Review evaluation changes. It does not prove runtime implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` before the Movement Review baseline commands were run.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none

Generated JSON reports were local/generated under `.\artifacts\eval\` and were not committed. This baseline summarizes those generated outputs into curated markdown only.

## Commands Executed

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| Movement Review benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.movement_review.json` | yes | 8 total, 8 passed, 0 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_movement_review_corpus_coverage.py` | yes | Movement Review coverage reported 11 STRONG, 0 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_movement_review_corpus_coverage.py --json --output .\artifacts\eval\movement_review_corpus_coverage.json` | yes | Local generated JSON report created and summarized, not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_movement_review_answer_gap_report.py --coverage-report .\artifacts\eval\movement_review_corpus_coverage.json` | yes | Overall status GOOD; 11 KEEP actions. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_movement_review_answer_gap_report.py --coverage-report .\artifacts\eval\movement_review_corpus_coverage.json --json --output .\artifacts\eval\movement_review_answer_gap_report.json` | yes | Local generated JSON report created and summarized, not committed. |

## Captured High-Level Findings

- DB readiness result: `READY`.
- Benchmark result: 8 total, 8 passed, 0 failed.
- Audit/chat rows created: false.
- Corpus coverage result: `STRONG` = 11, `WEAK` = 0, `MISSING` = 0.
- Indexed corpus: 5 active documents, 4583 chunks.
- Answer gap report: `GOOD`.
- Report type: `MOVEMENT_REVIEW_ANSWER_GAP_REPORT`.
- Source coverage plan: `MOVEMENT_REVIEW`.
- Recommended actions: 11 `KEEP`.
- Recommended next action: Keep current Movement Review retrieval terms and answer synthesis under benchmark watch.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Generated artefacts committed: no.

## Evidence Groups Covered By The Baseline Shape

The following Movement Review evidence groups were reported as `STRONG`:

- `purpose_and_operator_meaning`
- `reasonableness_not_error`
- `worker_and_organisation_lenses`
- `variance_and_comparable_periods`
- `payroll_bases_connection`
- `worker_story_connection`
- `admin_queue_connection`
- `current_effective_truth`
- `trend_only_and_threshold_treatment`
- `filters_and_return_context`
- `outstanding_hardening`

No evidence groups were reported as `WEAK` or `MISSING`.

## Known Gaps

- This is a captured baseline with a full benchmark pass, not a blocked database capture.
- Generated output files under `.\artifacts\eval\` were created locally and were not committed.
- Gross-to-Net remains a blocked v0.1 capture pack.
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

Keep current Movement Review retrieval terms and answer synthesis under benchmark watch. Do not update Gross-to-Net to captured state until its own DB-backed commands are captured.
