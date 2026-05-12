# Worker Story Baseline Summary

Slice name: Worker Story Baseline Capture v0.3 - Record READY Baseline Results

Domain: Worker Story

Source runbook: `docs/WORKER_STORY_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Source DB readiness note: `docs/evaluation/worker_story_baselines/WORKER_STORY_BASELINE_DB_READINESS.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future Worker Story evaluation changes. It does not prove runtime implementation, payroll correctness, corpus completeness or live platform state.

## Execution Context

Captured on 2026-05-12 from `C:\Projects\ezeas-intelligence`.

Worker Story Baseline DB Readiness v0.1 returned `READY` before the baseline commands were rerun.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none

The v0.3 capture replaces the prior blocked database state with READY rerun results. Generated JSON reports were local/generated under `reports/` and were not committed; the baseline policy prefers curated markdown summaries unless generated output is stable, useful and intentionally versioned.

## Commands Executed

| Area | Command | Completed In v0.3 | Captured Result Summary |
|---|---|---:|---|
| Worker Story benchmark | `.\.venv\Scripts\python.exe scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures` | yes | 5 total, 4 passed, 1 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts/scan_worker_story_corpus_coverage.py` | yes | Worker Story / Worker Calculation Story coverage reported 10 STRONG, 0 WEAK, 0 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json` | yes | Local generated JSON report created and summarized, not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json` | yes | Overall status GOOD; all 10 groups STRONG -> KEEP. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json --json --output reports/worker_story_answer_gap_report.json` | yes | Local generated JSON report created and summarized, not committed. |

## Captured High-Level Findings

- DB readiness result: `READY`.
- Benchmark result: 5 total, 4 passed, 1 failed.
- Failed benchmark: `worker-story-evidence-rich-answer`.
- Failed question: "What is Worker Story and what evidence does it show?"
- Failure classification: synthesis/routing/answer-mode drift, not a missing corpus evidence gap.
- Observed issue: the answer drifted into Annual Leave wording for a Worker Story question.
- Corpus coverage result: `STRONG` = 10, `WEAK` = 0, `MISSING` = 0.
- Indexed corpus: 5 active documents, 4583 chunks.
- Answer gap report: `GOOD`; all groups `KEEP`.
- Generated artefacts committed: no.

## Evidence Groups Covered By The Baseline Shape

All Worker Story evidence groups were reported as `STRONG`:

- `worker_story_purpose`
- `source_truth_and_inclusion`
- `interpreted_worked_hours`
- `calculated_payroll_outcome`
- `decision_story_and_rate_story`
- `leave_and_accrual_outcome`
- `payroll_bases_and_totals`
- `movement_review_and_admin_queue`
- `current_effective_truth`
- `outstanding_hardening`

## Known Gaps

- The remaining failed benchmark is an answer synthesis/routing/answer-mode drift target.
- The failed answer omitted expected Worker Story terms and drifted into Annual Leave wording.
- The corpus coverage diagnostic and answer gap report do not identify a formal corpus coverage gap for Worker Story.
- Generated output files under `reports/` were created locally and were not committed.
- Annual Leave / Leave Management remains `RUNBOOK_OUTSTANDING` in the completed-domain ledger.

## Post-Baseline Hardening Note v0.1

This section records the post-baseline result without overwriting the v0.3 baseline history above.

After Worker Story answer synthesis/routing drift hardening, the real DB-backed benchmark was rerun in the same environment after DB readiness returned `READY`.

- DB readiness result: `READY`.
- Worker Story benchmark rerun: 5 total, 5 passed, 0 failed.
- Annual Leave regression benchmark: 1 total, 1 passed, 0 failed.
- Audit/chat rows created: false.
- The v0.3 failed benchmark, `worker-story-evidence-rich-answer`, is considered addressed by synthesis/routing hardening.
- Corpus coverage remains interpreted as sufficient, not the source of the issue.

Completed-domain ledger status is unchanged: Worker Story remains `BASELINE_ALREADY_EXISTS`; counts remain `BASELINE_REQUIRED`: 29, `BASELINE_ALREADY_EXISTS`: 1 and `RUNBOOK_OUTSTANDING`: 1.

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
- does not create v0.5 slices automatically.

## Recommended Next Slice

Run Worker Story answer synthesis/routing drift hardening before scaling baseline capture to the other 29 domains. The first failed benchmark, `worker-story-evidence-rich-answer`, should be the next hardening target unless the drift is formally accepted as an expected baseline limitation.
