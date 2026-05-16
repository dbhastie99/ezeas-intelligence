# Historical Current-Truth Promotion Template

Version: v0.1

Date: 16 May 2026

## 1. Template Purpose

Use this template for future historical current-truth promotion candidate records.

This template does not promote current truth, permit answer use, ingest source content, mutate corpus, write to a database, call a live LLM, expose chat, create Code Evidence, add endpoints, add UI, or modify runtime answer behaviour.

## 2. Candidate Metadata

| Field | Value |
| --- | --- |
| PromotionCandidateId or planned identifier | TBD |
| SourceRegisterId | TBD |
| FindingReference | TBD |
| FindingClassification | TBD |
| BackfillExecutionReference | TBD or not required with rationale |
| BackfillValidationReference | TBD or not required with rationale |
| ProposedCurrentTruthStatement | TBD |
| ProposedTruthScope | TBD |
| RepositoryContext | TBD |
| SourceAuthoritySummary | TBD |
| SupersessionAssessment | TBD |
| ConflictAssessment | TBD |
| DuplicateAssessment | TBD |
| RepositoryCrossCheckStatus | TBD |
| FormalEvidenceGapStatus | TBD |
| ImplementationStateAssessment | TBD |
| SensitiveDataAssessment | TBD |
| PromotionDecisionStatus | `PROMOTION_REVIEW_NOT_STARTED` |
| Blockers | TBD |
| Reviewer | TBD |
| DecisionDate | TBD |
| RequiredNextAction | TBD |
| AnswerUsePermissionStatus | `ANSWER_USE_NOT_APPROVED` |
| AnswerUsePermissionLink | TBD optional planned link to `HISTORICAL_ANSWER_USE_PERMISSION_TEMPLATE.md` record |
| Notes | TBD |
| Explicit non-goals | See section 5. |

## 3. Conservative Permission Defaults

| Permission | Default |
| --- | --- |
| CurrentTruthPromotionPermitted | No |
| CurrentTruthPromotionApplied | No |
| AnswerUsePermitted | No |
| CorpusMutationPermitted | No |
| DatabaseWritePermitted | No |
| ChatExposurePermitted | No |
| LiveLLMUsePermitted | No |
| CodeEvidenceIngestionPermitted | No |

## 4. Decision Notes

`PROMOTION_CANDIDATE_IDENTIFIED` is not current truth.

`PROMOTION_REVIEW_STARTED` is not current truth.

`PROMOTION_BLOCKED` preserves all conservative defaults.

`PROMOTION_DEFERRED` preserves all conservative defaults.

`PROMOTION_APPROVED_IN_FUTURE_EXPLICIT_SLICE` is not available in this slice.

A current-truth approved item is still not answer-use approved unless answer-use permission is separately granted.

## 5. Explicit Non-Goals

- This record does not ingest source content.
- This record does not mutate operational corpus.
- This record does not create Code Evidence.
- This record does not write to database.
- This record does not call live LLM.
- This record does not promote current truth in this slice.
- This record does not permit answer use.
- This record does not expose chat.
- This record does not add endpoints.
- This record does not add UI.
- This record does not modify runtime answer behaviour.
