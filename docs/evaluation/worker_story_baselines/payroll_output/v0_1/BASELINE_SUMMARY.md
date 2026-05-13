# Payroll Output Baseline Summary

Slice name: Payroll Output Baseline Capture v0.1 - Record READY Baseline Results

Domain: Payroll Output

Source runbook: `docs/PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future Payroll Output evaluation changes. It does not prove runtime Payroll Output implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` before the Payroll Output baseline commands were run.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none

Generated JSON reports were local/generated under `.\artifacts\eval\` and were not committed. This baseline summarizes those generated outputs into curated markdown only.

## Commands Executed

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| Payroll Output benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_output.json` | yes | 7 total, 6 passed, 1 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_payroll_output_corpus_coverage.py` | yes | Payroll Output coverage reported 10 STRONG, 1 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_payroll_output_corpus_coverage.py --json --output .\artifacts\eval\payroll_output_corpus_coverage.json` | yes | Local generated JSON report created and summarized, not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_payroll_output_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_output_corpus_coverage.json` | yes | Overall status NEEDS_REFINEMENT; 10 KEEP actions; 1 IMPROVE_SYNTHESIS action. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_payroll_output_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_output_corpus_coverage.json --json --output .\artifacts\eval\payroll_output_answer_gap_report.json` | yes | Local generated JSON report created and summarized, not committed. |

## Captured High-Level Findings

- DB readiness result: `READY`.
- Benchmark result: 7 total, 6 passed, 1 failed.
- Failed benchmark case: `payroll-output-rich-answer`.
- Failure classification: benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap.
- Audit/chat rows created: false.
- Corpus coverage result: `STRONG` = 10, `WEAK` = 1, `MISSING` = 0.
- Indexed corpus: 5 active documents, 4583 chunks.
- Answer gap report: `NEEDS_REFINEMENT`.
- Report type: `PAYROLL_OUTPUT_ANSWER_GAP_REPORT`.
- Source coverage plan: `PAYROLL_OUTPUT`.
- Recommended actions: 10 `KEEP`, 1 `IMPROVE_SYNTHESIS`.
- Refinement group: `worker_level_output` -> `IMPROVE_SYNTHESIS`.
- Recommended next action: Tighten Payroll Output answer synthesis for weak core groups while keeping status caveats.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Generated artefacts committed: no.

## Evidence Groups Covered By The Baseline Shape

The Payroll Output corpus coverage diagnostic reported 11 evidence groups:

- 10 groups reported as `STRONG`.
- `worker_level_output` reported as `WEAK`.
- No groups reported as `MISSING`.

## Known Gaps

- `worker_level_output` needs answer synthesis refinement while preserving Payroll Output status caveats.
- The benchmark failure for `payroll-output-rich-answer` is classified as benchmark/source-evidence check or retrieval/source-matched-phrase drift, not a corpus gap.
- Source snippets/matched phrases did not contain all expected terms: Payroll Output, current-effective payroll output truth, Run Output, Process Period Output.
- The observed answer was directionally Payroll Output-specific.
- This is a captured baseline, not a runtime implementation claim.
- Generated output files under `.\artifacts\eval\` were created locally and were not committed.
- The generated JSON files `.\artifacts\eval\payroll_output_corpus_coverage.json` and `.\artifacts\eval\payroll_output_answer_gap_report.json` are not required committed artefacts.

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

Tighten Payroll Output answer synthesis for weak core groups while keeping status caveats.
