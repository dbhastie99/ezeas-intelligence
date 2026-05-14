# Imports / Actuals Formal Evidence Gap Plan

Slice name: Imports / Actuals Formal Evidence Gap Plan v0.1

Domain: Imports / Actuals

This plan records why Imports / Actuals cannot be promoted solely through answer-synthesis hardening. The recaptured baseline found formal source evidence gaps in the corpus, so promotion must wait for governed source evidence to be added later and for real command results to support the ledger change.

## Current Baseline Status

Imports / Actuals remains `BASELINE_REQUIRED`.

Recapture was attempted after DB readiness returned `READY`; DB readiness was not the blocker. Promotion was withheld because the benchmark still failed and the answer gap report remained `NEEDS_REFINEMENT`.

This document does not promote Imports / Actuals and does not update the completed-domain baseline ledger.

## Current Measured Results

- Benchmark: 11 total / 8 passed / 3 failed.
- Corpus coverage: 12 evidence groups; STRONG=9, WEAK=1, MISSING=2.
- Answer gap: `NEEDS_REFINEMENT`.
- Answer gap actions: 9 KEEP, 1 IMPROVE_SYNTHESIS, 2 ADD_FORMAL_SOURCE_EVIDENCE_LATER.

Failed benchmark cases:

- `imports-actuals-pay-code-ratetype-mapping`
- `imports-actuals-comparison-remediation-connection`
- `imports-actuals-worker-story-admin-queue`

## Formal Evidence Gaps

Missing formal source evidence groups:

- `purpose_and_operator_meaning`
- `outstanding_hardening`

Weak formal source evidence group:

- `pay_code_and_rate_type_mapping`

## Why The Gaps Matter

`purpose_and_operator_meaning` matters because the corpus must contain formal evidence defining Imports / Actuals as a domain, not merely scattered import features. It should define imports and actuals as source-evidence and reconciliation context, not just file upload or CSV parsing.

`outstanding_hardening` matters because the corpus must preserve known non-implemented or future-hardening boundaries. Future evidence must explicitly prevent runtime mutation claims, operational JSON ingestion claims, Code Evidence integration claims, live LLM answer claims and actuals ingestion runtime overclaiming.

`pay_code_and_rate_type_mapping` has some support, but not enough. It needs formal source evidence for deterministic pay code / RateType mapping, tenant override mapping, mapping snapshots, unmapped actuals review and configuration issue handling.

## Required Source Evidence To Add Later

Do not add this evidence in this slice. Future governed evidence should cover:

- Imports / Actuals domain purpose.
- Import batch and import row evidence.
- Import validation, warnings, errors and remediation.
- Award-specific import templates.
- Timesheet import and payroll actuals import as evidence lanes.
- Imported actuals vs calculated payroll truth.
- Comparison / Remediation relationship.
- Primary calculated lane.
- Comparator calculated lane.
- Imported actuals lane / actuals lane.
- Variance explanation.
- Pay code mapping.
- RateType mapping.
- Tenant override mapping.
- Mapping snapshots.
- Unmapped actuals review.
- Configuration issue handling.
- Worker Story surfacing.
- Admin Queue surfacing.
- Mapping issues in review queues.
- Evidence provenance and audit.
- Explicit non-goals / outstanding hardening.

## Proposed Source Locations

Likely future source locations, without creating or ingesting anything in this slice:

- platform doctrine / hardening doctrine source docs
- import design notes
- reconciliation design notes
- worker story / admin queue design notes
- future formal Imports / Actuals domain source document
- future Code Evidence source packs, only when Code Evidence integration is intentionally implemented

## Future Promotion Acceptance Criteria

Before any future promotion attempt:

- Formal source evidence is added to the corpus through the governed ingestion process.
- Coverage improves to no MISSING groups.
- `pay_code_and_rate_type_mapping` becomes STRONG or is otherwise accepted with documented rationale.
- Benchmark passes 11/11.
- Answer gap becomes GOOD or acceptable under a documented baseline policy.
- Generated JSON remains uncommitted unless repo convention changes.
- Ledger is promoted only after real command results support it.

## Explicit Non-Goals For This Slice

This slice preserves:

- no DB writes
- no migrations
- no corpus mutation
- no operational JSON ingestion
- no Code Evidence answer integration
- no live LLM calls
- no endpoint/UI/workforce-platform/runtime changes
- no import runtime changes
- no reconciliation runtime changes
- no PayRun runtime changes
- no actuals ingestion runtime
- no dirty runtime calls
- no correction/review/payment/finalisation execution
- no ledger promotion
