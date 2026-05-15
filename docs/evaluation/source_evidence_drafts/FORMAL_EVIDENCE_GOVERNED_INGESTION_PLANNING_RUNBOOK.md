# Formal Evidence Governed Ingestion Planning Runbook

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This runbook controls planning for a future governed corpus-ingestion slice after a domain is explicitly marked `REVIEWED_READY_FOR_INGESTION`.

It is a documentation/control artefact only. It does not approve review, perform governed ingestion, mutate corpus, run recapture, promote a baseline, change runtime behaviour, change endpoints, change UI, call a live LLM, write to the database, or change completed-domain ledger counts.

## 2. Required Control Artefacts

Use this runbook with these durable repository controls:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_READINESS_CHECKLIST.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_STATUS_TRANSITION_RUNBOOK.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

These artefacts, not chat-only agreement, control review status, ingestion planning, recapture eligibility, and promotion blocking.

## 3. Planning Scope

Governed ingestion planning is the written preparation for a later slice that may mutate corpus only if corpus mutation is explicitly in scope for that later slice.

Ingestion planning alone does not mutate corpus.

Ingestion planning alone does not run recapture.

Ingestion planning alone does not promote a baseline.

Ingestion planning alone does not change runtime behaviour.

Ingestion planning alone does not change ledger counts.

Ingestion planning alone does not permit Minerva to answer as if ingestion has happened.

Governed ingestion must be a separate explicit slice after planning and review readiness.

## 4. Future Planning Preconditions

A future governed ingestion planning slice may proceed only when all of these preconditions are documented:

- Latest decision record selected status is `REVIEWED_READY_FOR_INGESTION`.
- Reviewer identity present.
- Reviewer date present.
- Reviewer rationale present.
- Reviewed source artefacts identified.
- Ingestion scope documented.
- Target corpus location documented.
- Mutation risk documented.
- Rollback/restore plan documented.
- Generated artefact policy documented.
- Recapture plan documented.
- Tests planned before corpus mutation.

If any precondition is absent, governed ingestion planning remains blocked and corpus mutation remains out of scope.

## 5. Planning Procedure

1. Select the latest filled decision record from `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`.
2. Confirm its selected decision status is exactly `REVIEWED_READY_FOR_INGESTION`.
3. Confirm reviewer identity, reviewer date, and reviewer rationale are present in the decision record.
4. Identify the reviewed source artefacts that may be considered for ingestion.
5. Document ingestion scope, target corpus location, mutation risk, rollback/restore plan, generated artefact policy, recapture plan, and tests planned before corpus mutation.
6. Record that planning alone does not authorize corpus mutation, recapture, promotion, runtime changes, ledger-count changes, or Minerva answers claiming ingestion has happened.
7. Schedule a separate explicit governed-ingestion slice only after planning review confirms the preconditions remain satisfied.

## 6. Current Domain State

Current Tax / PAYG and Imports / Actuals records are `NOT_REVIEWED`, so governed ingestion is currently not permitted for either domain.

| Domain | Baseline status | Latest decision record | Current decision status | Governed ingestion permitted | Recapture permitted | Promotion permitted |
| --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md` | `NOT_REVIEWED` | No | No | No |

Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Governed ingestion permitted: No.

Recapture permitted: No.

Promotion permitted: No.

## 7. Domain-Specific Answering Constraints

For Tax / PAYG, Minerva may explain Tax / PAYG doctrine, source evidence, implementation state, and known gaps, but must not calculate PAYG withholding.

For Imports / Actuals, Minerva must preserve that Imports / Actuals is not merely file upload or CSV parsing. Imports / Actuals includes evidence-bearing import batches, rows, validation, errors, warnings, provenance, mapping, comparison, and remediation context.

Minerva must preserve that both domains remain `BASELINE_REQUIRED` and `NOT_REVIEWED` while the current decision records remain latest.

## 8. Non-Goals

This runbook does not implement:

- DB writes
- migrations
- corpus mutation
- operational JSON ingestion
- Code Evidence integration
- live LLM calls
- benchmark recapture
- baseline promotion
- ledger promotion
- endpoint changes
- UI changes
- workforce-platform changes
- award-configurator-v1 changes
- payroll runtime changes
- tax runtime changes
- import runtime changes
- actuals ingestion runtime changes
- reconciliation runtime changes
- review approval
- governed ingestion
- generated artefact creation

It does not change completed-domain ledger counts. It does not mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`. It does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.

## 9. Prompt Preservation

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_governed_ingestion_planning_runbook_v0_1.md`.
