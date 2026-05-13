# Gross-to-Net Baseline Summary

Slice name: Gross-to-Net Baseline Capture v0.1 - Record READY Baseline Results

Domain: Gross-to-Net

Source runbook: `docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future Gross-to-Net evaluation changes. It does not prove runtime implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` before the Gross-to-Net baseline commands were run.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none

Generated JSON reports were local/generated under `.\artifacts\eval\` and were not committed. This baseline summarizes those generated outputs into curated markdown only.

## Commands Executed

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| Gross-to-Net benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.gross_to_net.json` | yes | 6 total, 5 passed, 1 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_gross_to_net_corpus_coverage.py` | yes | Gross-to-Net coverage reported 10 STRONG, 0 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_gross_to_net_corpus_coverage.py --json --output .\artifacts\eval\gross_to_net_corpus_coverage.json` | yes | Local generated JSON report created and summarized, not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json` | yes | Overall status GOOD; 10 KEEP actions. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json --json --output .\artifacts\eval\gross_to_net_answer_gap_report.json` | yes | Local generated JSON report created and summarized, not committed. |

## Captured High-Level Findings

- DB readiness result: `READY`.
- Benchmark result: 6 total, 5 passed, 1 failed.
- Failed benchmark case: `gross-to-net-current-effective-worker-story`.
- Failure classification: benchmark answer-term expectation drift, not corpus gap; coverage is strong across all planned Gross-to-Net evidence groups.
- Audit/chat rows created: false.
- Corpus coverage result: `STRONG` = 10, `WEAK` = 0, `MISSING` = 0.
- Indexed corpus: 5 active documents, 4583 chunks.
- Answer gap report: `GOOD`.
- Report type: `GROSS_TO_NET_ANSWER_GAP_REPORT`.
- Source coverage plan: `GROSS_TO_NET`.
- Recommended actions: 10 `KEEP`.
- Recommended next action: Keep current Gross-to-Net retrieval terms and answer synthesis under benchmark watch.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Generated artefacts committed: no.

## Evidence Groups Covered By The Baseline Shape

The following Gross-to-Net evidence groups were reported as `STRONG`:

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

No evidence groups were reported as `WEAK` or `MISSING`.

## Known Gaps

- This is a captured baseline with a benchmark failure, not a blocked database capture.
- The failing benchmark case remains recorded for future comparison; expectations were not weakened.
- Generated output files under `.\artifacts\eval\` were created locally and were not committed.
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

Keep current Gross-to-Net retrieval terms and answer synthesis under benchmark watch. Treat `gross-to-net-current-effective-worker-story` as captured benchmark drift against otherwise strong corpus coverage, not as a corpus mutation request.
