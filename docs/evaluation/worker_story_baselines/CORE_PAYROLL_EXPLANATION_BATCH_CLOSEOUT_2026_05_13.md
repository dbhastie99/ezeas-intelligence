# Core Payroll Explanation Batch Close-Out v0.1

Date: 2026-05-13

This close-out records the completed Core Payroll Explanation baseline batch after all four selected domains moved from blocked baseline-required status to checked-in v0.1 baseline packs.

It is a curated comparison-control summary. It is not authorization to rerun benchmarks, weaken benchmark expectations, ingest operational JSON, connect Code Evidence to answers, call a live LLM, mutate corpus records, run migrations, add endpoints, add UI, or modify workforce-platform.

## Ledger State

- `BASELINE_REQUIRED`: 21
- `BASELINE_ALREADY_EXISTS`: 10
- `RUNBOOK_OUTSTANDING`: 0
- Baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net; Annual Leave / Leave Management; Finalisation Readiness; Payroll Output; RateSource / Rate Story; Decision Story.
- No Core Payroll Explanation batch domains remain blocked.
- Domains with runbook outstanding: none.

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

## Checked-In Batch Packs

- `docs/evaluation/worker_story_baselines/finalisation_readiness/v0_1/`
- `docs/evaluation/worker_story_baselines/payroll_output/v0_1/`
- `docs/evaluation/worker_story_baselines/ratesource_rate_story/v0_1/`
- `docs/evaluation/worker_story_baselines/decision_story/v0_1/`

## Batch Outcomes

| Domain | Baseline outcome | Benchmark | Corpus coverage | Answer gap report | Close-out classification |
| --- | --- | --- | --- | --- | --- |
| Finalisation Readiness | Passed baseline with refinement | 12 total / 12 passed / 0 failed | STRONG=11, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 11 KEEP actions; 1 IMPROVE_SYNTHESIS action | Weak group `purpose_and_operator_meaning` needs synthesis refinement. |
| Payroll Output | Captured-with-failures baseline | 7 total / 6 passed / 1 failed | STRONG=10, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 10 KEEP actions; 1 IMPROVE_SYNTHESIS action | Failed case `payroll-output-rich-answer` is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap. Weak group `worker_level_output` needs synthesis refinement. |
| RateSource / Rate Story | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=1, MISSING=0 | NEEDS_REFINEMENT; 10 KEEP actions; 1 IMPROVE_SYNTHESIS action | Failed case `rate-source-rate-story-rich-answer` is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap. Weak group `rate_source_evidence_index` needs synthesis refinement. |
| Decision Story | Captured-with-failures baseline | 7 total / 6 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions | Failed case `decision-story-rich-answer` is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap. |

## Preserved Interpretation

Passed baselines and captured-with-failures baselines are both durable comparison controls, but they are different signals. Finalisation Readiness has a passing benchmark state with a known synthesis refinement. Payroll Output, RateSource / Rate Story, and Decision Story are intentionally captured with benchmark failures so future work can compare against the current known failure signatures.

Payroll Output failure is not corpus gap. RateSource / Rate Story failure is not corpus gap. Decision Story failure is not corpus gap. These failures remain source-evidence or matched-phrase drift signals unless a future evaluated slice proves otherwise.

Finalisation Readiness needs synthesis refinement for `purpose_and_operator_meaning`. Payroll Output needs synthesis refinement for `worker_level_output`. RateSource / Rate Story needs synthesis refinement for `rate_source_evidence_index`.

Generated JSON outputs from benchmark, corpus coverage or answer-gap commands are transient evaluation materials. They are not durable checked-in artefacts unless explicitly versioned as part of a baseline pack. The durable artefacts for this close-out are the curated markdown baseline packs and this close-out summary.

## Guardrails

This close-out did not implement or authorize:

- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- corpus mutation;
- DB or schema migration;
- endpoints or UI;
- workforce-platform changes.

No operational JSON ingestion occurred. No Code Evidence answer integration occurred. No live LLM call occurred. No corpus mutation occurred. No DB or schema migration occurred. No endpoint or UI change occurred. No workforce-platform change occurred.

The recommended next baseline batch should be small. It should not attempt all remaining 21 `BASELINE_REQUIRED` domains at once.
