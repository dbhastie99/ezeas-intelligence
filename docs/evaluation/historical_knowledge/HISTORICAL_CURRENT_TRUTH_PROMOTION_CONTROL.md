# Historical Current-Truth Promotion Control

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the control model for considering reviewed and backfilled Minerva historical evidence as a future current-truth promotion candidate.

This slice defines the control model only.

It does not promote any historical finding to current truth.

It does not change any answer-use permissions.

It does not mutate corpus.

It does not write to a database.

It does not ingest source content.

It does not call a live LLM.

It does not expose chat.

Current-truth promotion is separate from ingestion/backfill.

Current-truth promotion is separate from answer-use permission.

## 2. Scope

This model applies after historical source registration, historical review, findings classification, ingestion/backfill decision control, future backfill execution, and future backfill validation have created reviewed evidence that may be assessed for current-truth promotion.

Backfilled evidence can remain historical-only.

A current-truth candidate is not current truth until approved by a later explicit promotion slice.

A current-truth approved item is still not answer-use approved unless answer-use permission is separately granted.

This slice is documentation/test/control only. It does not ingest content, mutate corpus, write to a database, promote current truth, permit answer use, expose chat, add endpoints, add UI, modify runtime answer behaviour, or create Code Evidence.

## 3. Required Control State Separation

The current-truth promotion model separates these states. Completion of one state does not imply permission for any later state:

| State | Meaning |
| --- | --- |
| `HISTORICAL_SOURCE_REGISTERED` | A historical source is registered. Registration is not review, ingestion, current truth, or answer-use permission. |
| `HISTORICAL_SOURCE_REVIEWED` | The historical source has a governed review result. Review is not ingestion, current truth, or answer-use permission. |
| `FINDING_CLASSIFIED` | A reviewed finding has been classified. Classification is not current truth. |
| `INGESTION_BACKFILL_DECISION_APPROVED` | A decision may permit later backfill planning or execution under separate controls. Approval here is not current truth. |
| `BACKFILL_EXECUTION_COMPLETED` | A future explicit execution slice has completed a controlled backfill. Completion is not current-truth promotion. |
| `BACKFILLED_EVIDENCE_VALIDATED` | Future post-backfill validation has passed. Validation is not current truth or answer-use permission. |
| `CURRENT_TRUTH_CANDIDATE_IDENTIFIED` | A reviewed/backfilled item may be assessed for promotion. It is still not current truth. |
| `CURRENT_TRUTH_PROMOTION_REVIEW_STARTED` | A governed promotion review has started. Review start is not approval. |
| `CURRENT_TRUTH_PROMOTION_BLOCKED` | Promotion must not proceed until blockers are resolved and reassessed. |
| `CURRENT_TRUTH_PROMOTION_DEFERRED` | Promotion is intentionally postponed; all conservative defaults remain No. |
| `CURRENT_TRUTH_PROMOTION_APPROVED_FUTURE_SLICE` | Approval may occur only in a later explicit promotion slice, not in this slice. |
| `ANSWER_USE_PERMISSION_SEPARATE` | Answer-use permission remains a separate gate even after future current-truth approval. |

## 4. Conservative Permission Defaults

Every current-truth promotion candidate record starts with these values:

| Permission | Default |
| --- | --- |
| `CurrentTruthPromotionPermitted` | No |
| `CurrentTruthPromotionApplied` | No |
| `AnswerUsePermitted` | No |
| `CorpusMutationPermitted` | No |
| `DatabaseWritePermitted` | No |
| `ChatExposurePermitted` | No |
| `LiveLLMUsePermitted` | No |
| `CodeEvidenceIngestionPermitted` | No |

These defaults remain No unless a later governed slice explicitly changes the specific permission. No default may be inferred from source registration, review completion, finding classification, ingestion/backfill approval, backfill execution, backfill validation, or candidate identification.

## 5. Preconditions Before Promotion Review Can Start

Current-truth promotion review must not start unless all required controls exist or are explicitly blocked/deferred with rationale:

- Source is registered.
- Source is reviewed.
- Finding is classified.
- Finding classification supports promotable assessment.
- Ingestion/backfill decision exists where required.
- Backfill execution is completed where required.
- Backfill validation is completed where required.
- Current repository truth is cross-checked.
- Supersession status is recorded.
- Conflict status is recorded.
- Duplicate status is recorded.
- Source authority is confirmed.
- Formal evidence gaps are checked.
- Implementation state is assessed.
- Sensitive data and tenant-data risk are checked.
- Proposed current-truth scope is documented.
- Reviewer approval requirement is documented.
- Answer-use permission remains separate.

## 6. Promotion Decision Status Model

| Status | Meaning |
| --- | --- |
| `PROMOTION_REVIEW_NOT_STARTED` | No promotion review has begun. |
| `PROMOTION_CANDIDATE_IDENTIFIED` | A candidate exists for later review. It is not current truth. |
| `PROMOTION_REVIEW_STARTED` | Review has begun under this control model. It is not approval. |
| `PROMOTION_BLOCKED` | Promotion is blocked by one or more blocker codes. |
| `PROMOTION_DEFERRED` | Promotion is deferred with rationale; conservative defaults remain No. |
| `PROMOTION_REJECTED` | Promotion is rejected under current controls. |
| `PROMOTION_APPROVED_IN_FUTURE_EXPLICIT_SLICE` | A later explicit slice may approve promotion. This status is not applied by this slice. |
| `ANSWER_USE_REQUIRES_SEPARATE_APPROVAL` | Current-truth approval, if later granted, still does not grant answer-use permission. |

## 7. Required Assessments

Promotion review must assess:

- Source authority against current repository truth.
- Whether the historical finding is superseded by current repository truth.
- Whether the finding conflicts with current repository truth or other reviewed evidence.
- Whether the finding duplicates existing governed evidence and should be linked instead.
- Whether current code, tests, schema, docs, and committed logs support the proposed truth statement.
- Whether formal source evidence is missing.
- Whether implementation state is implemented, planned, partial, removed, or uncertain.
- Whether sensitive or tenant-specific data creates a promotion risk.
- Whether proposed truth scope is narrow enough to avoid over-promotion.
- Whether answer-use remains separately blocked.

## 8. Required Artefacts

Use these artefacts together:

- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_REVIEW_CHECKLIST.md`

Future promotion records must be created from the template or an approved successor.

## 9. Answer-Use Permission Gate Handoff

Current-truth promotion does not automatically permit answer use and must flow into the answer-use permission gate when current-truth answers are requested.

The answer-use permission gate is governed by `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_PERMISSION_GATE.md`.

Future current-truth answer use requires both `CurrentTruthPermitted` Yes and separate `AnswerUsePermitted` Yes.

A current-truth promotion record may link a future answer-use permission record, but that link does not activate retrieval, expose chat, call a live LLM, or make evidence answerable unless a later runtime gate explicitly implements it.

## 10. Retrieval Eligibility and Future Chat Handoff

Current-truth promotion requires answer-use permission and retrieval eligibility before future chat use.

Future current-truth chat use requires `CurrentTruthPermitted` Yes, answer-use permission for the requested answer scope, and retrieval eligibility for the requested retrieval mode.

Retrieval eligibility is governed by `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md`.

Current-truth promotion must not be treated as retrieval eligibility, chat exposure, answer synthesis permission, or runtime activation.

## 11. Explicit Non-Goals

- Do not ingest source content.
- Do not mutate operational corpus.
- Do not create Code Evidence.
- Do not write to database.
- Do not call live LLM.
- Do not promote current truth.
- Do not permit answer use.
- Do not expose chat.
- Do not add endpoints.
- Do not add UI.
- Do not modify runtime answer behaviour.
- Do not fabricate benchmark, coverage, answer gap, or DB-backed results.

## 12. Developer Handoff

Future developers must treat this control as the handoff point after future backfilled evidence validation and before any later explicit promotion slice.

Creating a current-truth promotion candidate does not promote current truth.

Starting promotion review does not promote current truth.

Resolving a blocker does not promote current truth.

Approving current truth in a future explicit slice would still not permit answer use unless answer-use permission is separately granted.
