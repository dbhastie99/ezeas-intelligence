# Worker Story Baseline Summary

Slice name: Worker Story Baseline-Capture Pilot v0.1

Domain: Worker Story

Source runbook: `docs/WORKER_STORY_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This baseline pack is diagnostic-only and not operational truth. It is a checked-in comparison control for future Worker Story evaluation changes. It does not prove runtime implementation, payroll correctness, corpus completeness or live platform state.

## Commands Used Or Intended

| Area | Command | Completed In This Slice | Output Handling |
|---|---|---:|---|
| Worker Story benchmark | `py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures` | no | Command is documented from the runbook. This pilot defines the checked-in baseline shape; future reruns may populate command-specific result details. |
| Corpus coverage diagnostic | `py scripts/scan_worker_story_corpus_coverage.py` | no | Command is documented from the runbook. No generated corpus coverage output is embedded in this pack. |
| Corpus coverage diagnostic JSON | `py scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json` | no | Intended output path is documented. Generated JSON remains outside this curated baseline unless a future slice intentionally checks it in. |
| Answer gap report | `py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json` | no | Command is documented from the runbook. No generated gap report output is embedded in this pack. |
| Answer gap report JSON | `py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json --json --output reports/worker_story_answer_gap_report.json` | no | Intended output path is documented. Generated JSON remains outside this curated baseline unless a future slice intentionally checks it in. |

The command output is manually summarized as a baseline-control shape because this slice is documentation/evaluation-control only. It does not run benchmark capture, ingest corpus, call a live LLM or connect Code Evidence to answers.

## High-Level Baseline Finding

Worker Story has enough repo artefacts to justify a checked-in baseline pack: a v0.4 runbook, rich-answer benchmark manifest, corpus coverage diagnostic script, answer gap report script and documentation tests. This v0.1 pack establishes the reusable baseline artefact shape and records that Worker Story now has a checked-in baseline control pack.

The pack does not claim current benchmark pass/fail, live corpus coverage, answer gap status or runtime payroll truth.

## Evidence Groups Covered

The Worker Story evaluation runbook and retrieval plan cover:

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

- Generated benchmark output is not checked into this v0.1 pack.
- Generated corpus coverage JSON is not checked into this v0.1 pack.
- Generated answer gap report JSON is not checked into this v0.1 pack.
- This pack records the comparison-control structure, not live corpus readiness.
- Annual Leave / Leave Management remains `RUNBOOK_OUTSTANDING` in the completed-domain ledger.

## Guardrails

This baseline pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not prove runtime platform truth;
- does not create payroll/runtime truth;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Run a Worker Story baseline-capture v0.2 slice that decides whether to check in generated benchmark, coverage and answer-gap outputs or continue using curated markdown summaries only. That slice should keep the same non-mutation guardrails and should not expand to other domains until the Worker Story policy is proven.
