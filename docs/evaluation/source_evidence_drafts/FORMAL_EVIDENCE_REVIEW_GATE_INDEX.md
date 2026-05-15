# Formal Evidence Review Gate Index

Slice: Minerva Review Gate Index / Ingestion Guard Register v0.1

Date: 15 May 2026

## Purpose

This register is the central ingestion guard for Minerva baseline domains that have formal source-evidence drafts and review gates.

It records whether a domain is draft-only, has a review gate that has not been reviewed, needs revision, is reviewed and ready for a future governed ingestion slice, is superseded, is blocked from ingestion, is eligible for recapture, or remains `BASELINE_REQUIRED`.

## Scope

This register currently covers formal evidence draft and review-gate controls for:

- Imports / Actuals
- Tax / PAYG

It is a documentation/control artefact only. It does not ingest evidence, mutate the corpus, mutate the database, run benchmark recapture, promote ledgers, change endpoints, change runtime behaviour, or create generated artefacts.

The completed-domain ledger state remains:

- `BASELINE_REQUIRED`: 17
- `BASELINE_ALREADY_EXISTS`: 14
- `RUNBOOK_OUTSTANDING`: 0
- `NEEDS_REVIEW`: 0
- Total domains: 31

## Status Definitions

- `DRAFT_ONLY`: a formal source-evidence draft exists, but no review gate has been created. Governed ingestion is blocked.
- `NOT_REVIEWED`: a review gate exists, but no reviewer has approved it. Governed ingestion is blocked.
- `NEEDS_REVISION`: a reviewer has found issues that must be corrected. Governed ingestion is blocked.
- `REVIEWED_READY_FOR_INGESTION`: a reviewer has recorded readiness, reviewer identity, review date and evidence. This can permit a future governed ingestion slice, subject to the ingestion decision rules below.
- `SUPERSEDED`: the referenced draft or gate has been replaced and must not be used for ingestion.
- `BLOCKED_FROM_INGESTION`: a domain is explicitly not eligible for governed ingestion until a named blocker is resolved.
- `ELIGIBLE_FOR_RECAPTURE`: a domain may be recaptured only after governed ingestion has occurred or an explicit evidence update changes the source-evidence basis.
- `BASELINE_REQUIRED`: the domain is not promoted in the completed-domain ledger.

## Ingestion Decision Rules

1. A formal source-evidence draft alone does not permit governed ingestion.
2. A review gate with `NOT_REVIEWED` blocks governed ingestion.
3. A review gate with `NEEDS_REVISION` blocks governed ingestion.
4. Only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice.
5. `SUPERSEDED` means the referenced draft/gate must not be used for ingestion.
6. Baseline promotion requires real benchmark, corpus coverage, and answer-gap evidence.
7. No domain is promoted merely because source-evidence documents exist.
8. Generated JSON artefacts remain transient unless repo convention changes.
9. Minerva must not overstate review, ingestion, runtime, or promotion state.

`REVIEWED_READY_FOR_INGESTION` is not itself ingestion. Any ingestion must be a later governed slice where corpus mutation is explicitly in scope, the ingestion mechanism is identified, tests are updated for that ingestion path, generated JSON policy is confirmed, and a baseline recapture plan is attached.

## Current Domain Gate Table

| Domain | Baseline status | Evidence gap plan | Formal source-evidence draft | Review gate | Current review status | Governed ingestion permitted | Promotion permitted | Recapture permitted |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Imports / Actuals | `BASELINE_REQUIRED` | present: `docs/evaluation/worker_story_baselines/imports_actuals/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md` | present: `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md` | present: `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md` | `NOT_REVIEWED` | No. `NOT_REVIEWED` blocks governed ingestion; only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice. | No. Imports / Actuals is not promoted and remains `BASELINE_REQUIRED`. | Only after governed ingestion or an explicit evidence update. |
| Tax / PAYG | `BASELINE_REQUIRED` | present: `docs/evaluation/worker_story_baselines/tax_payg/v0_1/FORMAL_EVIDENCE_GAP_PLAN.md` | present: `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_SOURCE_EVIDENCE_DRAFT_v0_1.md` | present: `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_GATE_v0_1.md` | `NOT_REVIEWED` | No. `NOT_REVIEWED` blocks governed ingestion; only `REVIEWED_READY_FOR_INGESTION` can permit a future governed ingestion slice. | No. Tax / PAYG is not promoted and remains `BASELINE_REQUIRED`. | Only after governed ingestion or an explicit evidence update. |

## Non-Goals

This register does not implement:

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

It does not change completed-domain ledger counts and does not mark Tax / PAYG or Imports / Actuals as `BASELINE_ALREADY_EXISTS`.

## Minerva Usage Guidance

Minerva may use this register as a control signal for what must not be overstated. It may say that formal source-evidence drafts and review gates exist for Imports / Actuals and Tax / PAYG. It must also say that both current gates are `NOT_REVIEWED`, governed ingestion is blocked, neither domain has been promoted, and both domains remain `BASELINE_REQUIRED`.

Minerva must not describe a source-evidence draft as ingested corpus evidence. It must not claim review approval, runtime behaviour, corpus mutation, benchmark recapture, promotion, or ledger movement unless a later governed artefact records those facts.
