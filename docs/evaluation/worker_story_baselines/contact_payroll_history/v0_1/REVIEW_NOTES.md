# Contact Payroll History Review Notes

This captured pack preserves the actual Contact Payroll History DB-backed baseline results without inventing or widening command output.

## Review Checklist

- Confirm DB readiness is recorded as `READY`.
- Confirm the benchmark result is 7 total, 5 passed and 2 failed.
- Confirm failed cases are `contact-payroll-history-rich-answer` and `contact-payroll-history-retro-replay-correction`.
- Confirm corpus coverage is `STRONG` = 7, `WEAK` = 3 and `MISSING` = 1.
- Confirm missing group `gross_to_net_history` is recorded.
- Confirm weak groups `current_and_historical_payroll_output`, `retro_replay_and_correction_relationship` and `outstanding_hardening` are recorded.
- Confirm answer gap status is `NEEDS_REFINEMENT` with 7 KEEP, 1 IMPROVE_SYNTHESIS, 2 IMPROVE_RETRIEVAL_TERMS and 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER action.
- Confirm no generated JSON output is required as a committed artefact.
- Confirm the ledger moves Contact Payroll History to `BASELINE_ALREADY_EXISTS`.
- Confirm ObjectTime / Source Truth, Process Periods / PayRun Lifecycle and Imports / Actuals remain blocked `BASELINE_REQUIRED` domains.
- Confirm this pack is diagnostic-only and not operational truth.

## Reviewer Questions

- Are the two benchmark failures accepted as captured baseline failures rather than hidden by expectation changes?
- Is the `gross_to_net_history` corpus gap visible enough to prevent widening Contact Payroll History claims prematurely?
- Are generated JSON files still treated as transient evaluation outputs rather than committed baseline artefacts?

## Guardrails

This review note does not authorize operational JSON ingestion, Code Evidence answer integration, live LLM calls, corpus mutation, DB/schema migration, endpoint/UI changes, workforce-platform changes, or benchmark expectation weakening.
