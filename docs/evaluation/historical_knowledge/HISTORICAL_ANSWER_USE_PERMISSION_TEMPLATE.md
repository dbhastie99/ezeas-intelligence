# Historical Answer-Use Permission Template

Version: v0.1

Date: 16 May 2026

## 1. Template Purpose

Use this template for future historical answer-use permission records.

This template does not expose chat, call a live LLM, change retrieval runtime, mutate corpus, ingest source content, promote current truth, write to a database, create endpoint changes, create UI changes, or activate answer-use permission at runtime.

## 2. Permission Record

| Field | Value |
| --- | --- |
| AnswerUsePermissionId | TBD |
| SourceId | TBD |
| SourceTitle | TBD |
| SourceDate | TBD or unknown-date marker |
| RepositoryContext | TBD |
| DomainContext | TBD |
| DecisionRecordId | TBD |
| FindingsRecordId | TBD or not applicable with rationale |
| FindingClassificationId | TBD or not applicable with rationale |
| IngestionBackfillDecisionId | TBD or not applicable with rationale |
| CurrentTruthPromotionId | TBD or not applicable with rationale |
| AnswerUsePermissionStatus | `ANSWER_USE_NOT_REQUESTED` |
| RetrievalEligibilityLink | TBD or not yet requested |
| EvidenceScope | `NOT_ANSWERABLE` |
| AnswerScope | TBD |
| CurrentTruthPermitted | No |
| HistoricalContextPermitted | No |
| CaveatRequired | Yes |
| CitationRequired | Yes |
| ProvenanceStatus | TBD |
| CrossCheckStatus | TBD |
| ConflictStatus | TBD |
| SupersessionStatus | TBD |
| RetrievalEligible | No |
| ChatEligible | No |
| RevocationPath | TBD |
| Blockers | TBD |
| DecisionRationale | TBD |
| ApprovedBy | TBD |
| ApprovedAtUtc | TBD |
| Notes | TBD |

## 3. Conservative Defaults

| Permission | Default |
| --- | --- |
| CurrentTruthPermitted | No |
| HistoricalContextPermitted | No |
| RetrievalEligible | No |
| ChatEligible | No |
| CaveatRequired | Yes |
| CitationRequired | Yes |

## 4. Decision Notes

`ANSWER_USE_NOT_REQUESTED`, `ANSWER_USE_BLOCKED`, `ANSWER_USE_DEFERRED`, and `ANSWER_USE_REQUIRES_REVIEW` preserve all conservative defaults.

`ANSWER_USE_APPROVED_HISTORICAL_CONTEXT_ONLY` does not permit current-truth answer use.

`ANSWER_USE_APPROVED_CURRENT_TRUTH` requires a valid `CurrentTruthPromotionId`, `CurrentTruthPermitted` Yes, and separate `AnswerUsePermitted` Yes in the governing decision record.

`ANSWER_USE_APPROVED_WITH_CAVEAT` requires caveats to be carried into any future answer contract.

`ANSWER_USE_REVOKED` and `ANSWER_USE_SUPERSEDED` are not answerable states.

## 5. Explicit Non-Goals

- This record does not expose chat.
- This record does not call a live LLM.
- This record does not change retrieval runtime.
- This record does not mutate corpus.
- This record does not ingest source content.
- This record does not promote current truth.
- This record does not write to a database.
- This record does not create endpoint changes.
- This record does not create UI changes.
- This record does not activate runtime answer-use permission.
