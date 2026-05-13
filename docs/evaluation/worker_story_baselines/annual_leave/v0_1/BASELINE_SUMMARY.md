# Annual Leave / Leave Management Baseline Summary

Slice name: Annual Leave Baseline Capture v0.1 - Record READY Baseline Results

Domain: Annual Leave / Leave Management

Source runbook: `docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future Annual Leave / Leave Management evaluation changes. It does not prove runtime implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` before the Annual Leave / Leave Management baseline commands were run.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none

Generated JSON reports were local/generated under `.\artifacts\eval\` and were not committed. This baseline summarizes those generated outputs into curated markdown only.

## Commands Executed

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| Annual Leave benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.annual_leave.json` | yes | 1 total, 1 passed, 0 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_annual_leave_corpus_coverage.py` | yes | Annual Leave / Leave Management coverage reported 7 STRONG, 0 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_annual_leave_corpus_coverage.py --json --output .\artifacts\eval\annual_leave_corpus_coverage.json` | yes | Local generated JSON report created and summarized, not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_annual_leave_answer_gap_report.py --coverage-report .\artifacts\eval\annual_leave_corpus_coverage.json` | yes | Overall status GOOD; 7 KEEP actions. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_annual_leave_answer_gap_report.py --coverage-report .\artifacts\eval\annual_leave_corpus_coverage.json --json --output .\artifacts\eval\annual_leave_answer_gap_report.json` | yes | Local generated JSON report created and summarized, not committed. |

## Captured High-Level Findings

- DB readiness result: `READY`.
- Benchmark result: 1 total, 1 passed, 0 failed.
- Audit/chat rows created: false.
- Corpus coverage result: `STRONG` = 7, `WEAK` = 0, `MISSING` = 0.
- Indexed corpus: 5 active documents, 4583 chunks.
- Answer gap report: `GOOD`.
- Report type: `ANNUAL_LEAVE_MANAGEMENT_ANSWER_GAP_REPORT`.
- Source coverage plan: `ANNUAL_LEAVE_MANAGEMENT`.
- Recommended actions: 7 `KEEP`.
- Recommended next action: Keep current Annual Leave / Leave Management retrieval terms and answer synthesis under benchmark watch.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Generated artefacts committed: no.

## Evidence Groups Covered By The Baseline Shape

The following Annual Leave / Leave Management evidence groups were reported as `STRONG`:

- `configuration`
- `accrual`
- `taken`
- `valuation`
- `payrun`
- `worker_story`
- `outstanding`

No evidence groups were reported as `WEAK` or `MISSING`.

## Known Gaps

- This is a captured baseline, not a runtime implementation claim.
- Generated output files under `.\artifacts\eval\` were created locally and were not committed.
- The generated JSON files `.\artifacts\eval\annual_leave_corpus_coverage.json` and `.\artifacts\eval\annual_leave_answer_gap_report.json` are not required committed artefacts.

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

Keep current Annual Leave / Leave Management retrieval terms and answer synthesis under benchmark watch.
