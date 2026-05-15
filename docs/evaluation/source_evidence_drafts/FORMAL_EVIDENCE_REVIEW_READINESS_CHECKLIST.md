# Formal Evidence Review Readiness Checklist

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This checklist guides a reviewer through the required checks before updating a formal evidence review decision record beyond `NOT_REVIEWED`.

It is a documentation/control artefact only. Completing this checklist does not itself change review status, permit governed ingestion, mutate corpus, run recapture, promote a baseline, or update the ledger.

## 2. Scope

This checklist applies before a reviewer selects any of these decision statuses in a formal evidence review decision record:

- `NEEDS_REVISION`
- `REVIEWED_READY_FOR_INGESTION`
- `SUPERSEDED`

Source artefacts to use with this checklist:

- `docs/evaluation/source_evidence_drafts/README.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_GATE_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md`
- `docs/evaluation/source_evidence_drafts/tax_payg/TAX_PAYG_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`
- `docs/evaluation/source_evidence_drafts/imports_actuals/IMPORTS_ACTUALS_FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_NOT_REVIEWED_v0_1.md`

The completed-domain ledger state remains:

- `BASELINE_REQUIRED`: 17
- `BASELINE_ALREADY_EXISTS`: 14
- `RUNBOOK_OUTSTANDING`: 0
- `NEEDS_REVIEW`: 0
- Total domains: 31

## 3. Reviewer Preconditions

Before changing a decision status, the reviewer must confirm:

- Correct domain and slug.
- Current baseline status.
- Current review gate status.
- Latest decision record.
- Source-evidence draft under review.
- Formal evidence gap plan.
- Review-gate index entry.
- Decision-record index entry.
- No newer superseding artefact exists.

The reviewer must also confirm that any proposed decision uses the current `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md` structure.

## 4. Source Artefact Checklist

The reviewer must check that every source artefact referenced by the decision record exists, is the intended version, and matches the domain under review.

Required checks:

- Formal source-evidence draft path is present and domain-specific.
- Formal evidence gap plan path is present and domain-specific.
- Formal evidence review gate path is present and domain-specific.
- Review-gate index entry matches the gate status.
- Decision-record index entry points to the latest decision record.
- Existing `NOT_REVIEWED` decision record is considered before any replacement record is created.
- No referenced artefact claims governed ingestion, corpus mutation, recapture, or promotion unless a later governed artefact records that fact.

## 5. Doctrine Review Checklist

The reviewer must check whether the source-evidence draft accurately states the external or formal doctrine needed for the domain.

Required checks:

- Doctrine claims are specific enough to support the evidence gap they are meant to close.
- Doctrine claims do not exceed the cited source material.
- Domain boundaries are explicit.
- Any unresolved doctrine ambiguity is recorded as a blocker or follow-up action.
- If doctrine is not acceptable, the selected decision status must be `NEEDS_REVISION`.

## 6. Implementation-State Review Checklist

The reviewer must check whether the draft accurately describes current implementation state.

Required checks:

- Runtime claims are compared with current repository artefacts where relevant.
- Documentation does not imply runtime behaviour that does not exist.
- No tax, payroll, import, actuals, reconciliation, endpoint, UI, or workforce-platform capability is created by the checklist or decision record.
- Any implementation-state mismatch is recorded as a blocker or follow-up action.
- If implementation-state claims are not acceptable, the selected decision status must be `NEEDS_REVISION`.

## 7. Evidence-Gap Coverage Checklist

The reviewer must check whether the draft covers the formal evidence gap it was created to address.

Required checks:

- Gap terms from the formal evidence gap plan are addressed.
- Existing benchmark, corpus coverage, and answer-gap evidence are not overstated.
- Remaining evidence gaps are named clearly.
- Coverage is sufficient before selecting `REVIEWED_READY_FOR_INGESTION`.
- Partial or ambiguous coverage must be recorded as `NEEDS_REVISION` or as follow-up tied to a more limited decision.

## 8. Non-Overclaiming Checklist

The reviewer must check that the decision record and any Minerva-facing implications remain conservative.

Required checks:

- Draft text is not described as ingested corpus evidence.
- Checklist completion is not described as review approval.
- `REVIEWED_READY_FOR_INGESTION` is not described as ingestion, recapture, promotion, or runtime capability.
- `NEEDS_REVISION` is not described as permission for governed ingestion.
- `SUPERSEDED` artefacts are not used for governed ingestion.
- Minerva must not overstate checklist completion as review approval, ingestion, recapture, or promotion.

## 9. Decision Status Guidance

### NOT_REVIEWED

Use when no formal review has occurred.

`NOT_REVIEWED` blocks governed ingestion, recapture, and promotion.

### NEEDS_REVISION

Use when the draft has been reviewed and is not safe for governed ingestion.

`NEEDS_REVISION` blocks governed ingestion, recapture, and promotion until a later corrected artefact is reviewed.

### REVIEWED_READY_FOR_INGESTION

Use only when doctrine review, implementation-state review, evidence-gap coverage review, and non-overclaiming review are all acceptable.

`REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only.

### SUPERSEDED

Use when the draft/gate/decision record has been replaced and must not be used for governed ingestion.

`SUPERSEDED` records remain useful as history, but they do not permit governed ingestion, recapture, or promotion.

## 10. Ingestion Readiness Gate

Gate rules:

1. A checklist alone does not change review status.
2. A checklist alone does not permit governed ingestion.
3. A checklist alone does not mutate corpus.
4. A checklist alone does not run recapture.
5. A checklist alone does not promote a baseline.
6. `REVIEWED_READY_FOR_INGESTION` permits planning a future governed ingestion slice only.
7. Governed ingestion must be a separate explicit slice.

Governed ingestion must identify the ingestion mechanism, mutation scope, tests, generated artefact policy, and rollback or correction path in that later slice.

## 11. Recapture Readiness Gate

Recapture must happen only after governed ingestion.

The checklist does not run benchmark recapture, corpus coverage scans, answer-gap reports, or any live LLM call.

Before recapture is permitted, the reviewer or future operator must confirm that governed ingestion has completed in a separate explicit slice or that another explicitly documented evidence update authorises recapture.

## 12. Promotion Readiness Gate

Promotion requires benchmark, corpus coverage, answer-gap evidence, and ledger update.

The checklist does not promote a baseline and does not promote the ledger.

Promotion can be considered only after reviewed evidence, governed ingestion where needed, recapture, and durable evidence showing that the domain satisfies promotion criteria.

## 13. Domain-Specific Notes

Current domain status table:

| Domain | Baseline status | Current decision record status | Governed ingestion permitted | Recapture permitted | Promotion permitted |
| --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No |

### Tax / PAYG

- Tax / PAYG remains `BASELINE_REQUIRED`.
- Minerva may explain Tax / PAYG but must not calculate PAYG withholding.
- Deterministic services, tax providers, and governed rule packs own PAYG withholding calculation.
- Current decision record is `NOT_REVIEWED`.
- Governed ingestion permitted: No.
- Recapture permitted: No.
- Promotion permitted: No.

### Imports / Actuals

- Imports / Actuals remains `BASELINE_REQUIRED`.
- Imports / Actuals is not merely file upload or CSV parsing.
- Imported actuals are not the same as calculated payroll truth.
- Pay code and RateType mapping must remain evidence-bearing and reviewable.
- Current decision record is `NOT_REVIEWED`.
- Governed ingestion permitted: No.
- Recapture permitted: No.
- Promotion permitted: No.

## 14. Minerva Answering Guidance

Minerva may say that this readiness checklist exists and can guide a reviewer before a future decision record changes status.

Minerva must preserve the current status of Tax / PAYG and Imports / Actuals as `BASELINE_REQUIRED` while their latest decision records remain `NOT_REVIEWED`.

Minerva must not claim review approval, governed ingestion, corpus mutation, recapture, benchmark success, answer-gap closure, runtime capability, baseline promotion, or ledger promotion from checklist completion.

## 15. Non-Goals

This checklist does not implement:

- DB writes
- migrations
- corpus mutation
- operational JSON ingestion
- generated artefact commits
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

It does not change completed-domain ledger counts, mark Tax / PAYG or Imports / Actuals as `REVIEWED_READY_FOR_INGESTION`, or mark either domain as promoted.

## 16. Follow-Up Actions

- Assign a reviewer before replacing a `NOT_REVIEWED` decision record.
- Use `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_TEMPLATE.md` for any future decision record.
- Update `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_REVIEW_DECISION_RECORD_INDEX.md` only after a filled replacement decision record exists.
- If the selected status is `REVIEWED_READY_FOR_INGESTION`, plan governed ingestion as a separate explicit slice.
- Keep recapture and promotion blocked until later durable artefacts satisfy their gates.
