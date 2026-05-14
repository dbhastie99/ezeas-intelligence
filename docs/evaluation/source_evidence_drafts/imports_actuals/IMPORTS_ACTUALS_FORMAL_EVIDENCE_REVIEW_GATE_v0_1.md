# Imports / Actuals Formal Evidence Review Gate v0.1

Slice: Imports / Actuals Formal Evidence Review Gate v0.1

Domain: Imports / Actuals

Current review status: `NOT_REVIEWED`

Default review status: `NOT_REVIEWED`

This review gate prevents shortcutting from draft text directly into Minerva corpus evidence. The Imports / Actuals formal source-evidence draft is not ready for corpus ingestion until it has been reviewed for doctrine accuracy, implementation-state accuracy and non-overclaiming.

This gate does not ingest the draft, mutate the corpus, mutate the database or promote Imports / Actuals.

## Source Artefacts Under Review

- `docs/evaluation/worker_story_baselines/imports_actuals/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md`
- Imports / Actuals baseline recapture result: 11 total / 8 passed / 3 failed; corpus coverage STRONG=9, WEAK=1, MISSING=2; answer gap `NEEDS_REFINEMENT`; ledger status remains `BASELINE_REQUIRED`.

## Required Review Outcomes

A reviewer must record exactly one explicit status before any governed ingestion slice can use the draft:

- `NOT_REVIEWED`
- `NEEDS_REVISION`
- `REVIEWED_READY_FOR_INGESTION`
- `SUPERSEDED`

This slice records the default and current status as `NOT_REVIEWED`. It does not mark the draft as reviewed or ready for ingestion.

## Doctrine Review Checklist

Before status can move to `REVIEWED_READY_FOR_INGESTION`, the reviewer must confirm that the draft accurately preserves these doctrine boundaries:

- Imports / Actuals is source-evidence and reconciliation context, not merely file upload or CSV parsing.
- Imported actuals are evidence lanes, not calculated payroll truth.
- Source truth, imported actuals, calculated payroll truth and current-effective output remain separate.
- Deterministic payroll calculation remains authoritative for calculated outcomes.
- Mapping ambiguity and unmapped actuals require review/configuration handling.
- Worker Story and Admin Queue surface evidence and review state without hiding mapping issues.
- No runtime behaviour is claimed unless already implemented and evidenced.

## Implementation-State Review Checklist

The reviewer must confirm that the draft does not claim any of these are implemented:

- operational JSON ingestion.
- Code Evidence answer integration.
- live LLM answer integration.
- import runtime changes.
- actuals ingestion runtime changes.
- reconciliation runtime changes.
- PayRun runtime changes.
- automatic correction/review/payment/finalisation execution.
- corpus mutation has occurred.

## Evidence Gap Coverage Checklist

The reviewer must confirm that the draft addresses these gap and coverage terms:

- `purpose_and_operator_meaning`
- `outstanding_hardening`
- `pay_code_and_rate_type_mapping`
- pay code mapping
- RateType mapping
- tenant override mapping
- mapping snapshots
- unmapped actuals review
- configuration issue handling
- imported actuals lane / actuals lane
- primary calculated lane
- comparator calculated lane
- variance
- Worker Story
- Admin Queue
- mapping issues

## Ingestion Preconditions

A future ingestion slice may proceed only in a future explicit ingestion slice after review readiness, and only after all of these are true:

- Status is `REVIEWED_READY_FOR_INGESTION`.
- Reviewer, date and evidence are recorded.
- The ingestion mechanism is identified.
- Corpus mutation is explicitly in scope for that future slice.
- Tests are updated for the ingestion path.
- Generated JSON policy is confirmed.
- Baseline recapture plan is attached.

## Future Recapture Acceptance Criteria

Imports / Actuals may be promoted only after real command results show:

- no MISSING groups, or any remaining missing group has a documented accepted rationale.
- `pay_code_and_rate_type_mapping` becomes STRONG or accepted with rationale.
- benchmark passes 11/11.
- answer gap becomes GOOD or acceptable.
- ledger promotion is performed only after successful recapture.

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
