# PayRun Admin Queue Baseline Summary

Slice name: PayRun Admin Queue Baseline Capture v0.1 - Record READY Baseline Results With Failures

Domain: PayRun Admin Queue

Source runbook: `docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future PayRun Admin Queue evaluation changes. It does not prove runtime implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` before the PayRun Admin Queue baseline commands were run.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none

Generated JSON reports were local/generated under `.\artifacts\eval\` and were not committed. This baseline summarizes those generated outputs into curated markdown only.

## Commands Executed

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| PayRun Admin Queue benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payrun_admin_queue.json` | yes | 8 total, 6 passed, 2 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_payrun_admin_queue_corpus_coverage.py` | yes | PayRun Admin Queue coverage reported 11 STRONG, 0 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_payrun_admin_queue_corpus_coverage.py --json --output .\artifacts\eval\payrun_admin_queue_corpus_coverage.json` | yes | Local generated JSON report created and summarized, not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_payrun_admin_queue_answer_gap_report.py --coverage-report .\artifacts\eval\payrun_admin_queue_corpus_coverage.json` | yes | Overall status GOOD; 11 KEEP actions. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_payrun_admin_queue_answer_gap_report.py --coverage-report .\artifacts\eval\payrun_admin_queue_corpus_coverage.json --json --output .\artifacts\eval\payrun_admin_queue_answer_gap_report.json` | yes | Local generated JSON report created and summarized, not committed. |

## Captured High-Level Findings

- DB readiness result: `READY`.
- Benchmark result: 8 total, 6 passed, 2 failed.
- Audit/chat rows created: false.
- Failed benchmark case IDs: `payrun-admin-queue-rich-answer`; `payrun-admin-queue-cleanliness-assurance`.
- Failure classification: benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap.
- Observed answer framing was directionally PayRun Admin Queue-specific, but source snippet / matched phrase evidence checks failed.
- Corpus coverage result: `STRONG` = 11, `WEAK` = 0, `MISSING` = 0.
- Indexed corpus: 5 active documents, 4583 chunks.
- Answer gap report: `GOOD`.
- Recommended actions: 11 `KEEP`.
- Recommended next action: Keep current PayRun Admin Queue retrieval terms and answer synthesis under benchmark watch.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Generated artefacts committed: no.

## Evidence Groups Covered By The Baseline Shape

The following PayRun Admin Queue evidence groups were reported as `STRONG`:

- `purpose_and_operator_meaning`
- `blockers_warnings_and_ready_actions`
- `worker_attention_and_dirty_contacts`
- `processing_and_reprocessing_actions`
- `finalisation_readiness`
- `assurance_snapshot`
- `review_surfaces_and_navigation`
- `worker_story_connection`
- `payroll_bases_connection`
- `movement_review_connection`
- `outstanding_hardening`

No evidence groups were reported as `WEAK` or `MISSING`.

## Known Gaps

- The benchmark completed with failures, so this is a captured baseline with failures, not a blocked baseline.
- The failures are benchmark/source-evidence check or retrieval/source-matched-phrase drift, not missing formal corpus coverage.
- Generated output files under `.\artifacts\eval\` were created locally and were not committed.
- Movement Review and Gross-to-Net remain blocked v0.1 capture packs.
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

Keep current PayRun Admin Queue retrieval terms and answer synthesis under benchmark watch. Treat the two failing benchmark cases as source-evidence check or retrieval/source-matched-phrase drift unless a later run proves otherwise.
