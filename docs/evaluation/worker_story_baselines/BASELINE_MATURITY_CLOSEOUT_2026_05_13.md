# Minerva Baseline Maturity Close-Out v0.1

Date: 2026-05-13

This close-out records the first six-domain Minerva baseline maturity sequence after Annual Leave / Leave Management moved from `RUNBOOK_OUTSTANDING` to `BASELINE_ALREADY_EXISTS`.

It is a curated comparison-control summary. It is not authorization to rerun benchmarks, weaken benchmark expectations, ingest operational JSON, connect Code Evidence to answers, call a live LLM, mutate corpus records, run migrations, add endpoints, add UI, or modify workforce-platform.

## Ledger State

- `BASELINE_REQUIRED`: 25
- `BASELINE_ALREADY_EXISTS`: 6
- `RUNBOOK_OUTSTANDING`: 0
- Baseline already existing: Worker Story; Payroll Bases & Totals; PayRun Admin Queue; Movement Review; Gross-to-Net; Annual Leave / Leave Management.
- Annual Leave / Leave Management is no longer `RUNBOOK_OUTSTANDING`; it is now `BASELINE_ALREADY_EXISTS`.
- Domains with runbook outstanding: none.

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

## Checked-In Baseline Packs

- `docs/evaluation/worker_story_baselines/worker_story/v0_1/`
- `docs/evaluation/worker_story_baselines/payroll_bases_totals/v0_1/`
- `docs/evaluation/worker_story_baselines/payrun_admin_queue/v0_1/`
- `docs/evaluation/worker_story_baselines/movement_review/v0_1/`
- `docs/evaluation/worker_story_baselines/gross_to_net/v0_1/`
- `docs/evaluation/worker_story_baselines/annual_leave/v0_1/`

## Maturity Outcomes

| Domain | Baseline outcome | Benchmark | Corpus coverage | Answer gap report | Close-out classification |
| --- | --- | --- | --- | --- | --- |
| Worker Story | Historical captured baseline with later post-hardening pass | Original v0.3 history records 5 total / 4 passed / 1 failed; later rerun records 5 total / 5 passed / 0 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD | Preserve the original failure history. Do not overwrite it with the later pass. |
| Payroll Bases & Totals | Passed baseline with refinement | 6 total / 6 passed / 0 failed | STRONG=8, WEAK=1, MISSING=0 | NEEDS_REFINEMENT | Weak `outstanding_hardening` coverage requires retrieval-term hardening: `outstanding_hardening` -> `IMPROVE_RETRIEVAL_TERMS`. This is not a corpus gap. |
| PayRun Admin Queue | Captured-with-failures baseline | 8 total / 6 passed / 2 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions | Failed cases are `payrun-admin-queue-rich-answer` and `payrun-admin-queue-cleanliness-assurance`. Failure classification is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap. Do not weaken benchmark expectations. |
| Movement Review | Passed baseline | 8 total / 8 passed / 0 failed | STRONG=11, WEAK=0, MISSING=0 | GOOD; 11 KEEP actions | Clean pass and GOOD answer gap report. |
| Gross-to-Net | Captured-with-failures baseline | 6 total / 5 passed / 1 failed | STRONG=10, WEAK=0, MISSING=0 | GOOD; 10 KEEP actions | Failed case is `gross-to-net-current-effective-worker-story`. Failure classification is benchmark answer-term expectation drift, not corpus gap. Do not weaken benchmark expectations. |
| Annual Leave / Leave Management | Passed baseline | 1 total / 1 passed / 0 failed | STRONG=7, WEAK=0, MISSING=0 | GOOD; 7 KEEP actions | Annual Leave now has a checked-in v0.1 baseline pack and no benchmark failures. |

## Preserved Interpretation

Passed baselines and captured-with-failures baselines are both durable comparison controls, but they are not equivalent signal types. Worker Story, Payroll Bases & Totals, Movement Review, and Annual Leave / Leave Management have passing benchmark states recorded. PayRun Admin Queue and Gross-to-Net are intentionally captured with benchmark failures so future work can compare against the current known failure signatures.

Payroll Bases & Totals remains `NEEDS_REFINEMENT` because weak `outstanding_hardening` coverage maps to `IMPROVE_RETRIEVAL_TERMS`; that refinement should be handled as retrieval-term hardening before any corpus expansion.

PayRun Admin Queue failures are not corpus gaps. Gross-to-Net failure is not a corpus gap. The recorded failure classifications must remain benchmark/source-evidence or answer-term expectation signals unless a future evaluated slice proves otherwise.

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

The recommended next baseline batch should be small. It should not attempt all remaining 25 `BASELINE_REQUIRED` domains at once.
