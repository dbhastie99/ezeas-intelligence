# Historical Retrieval Eligibility Template

Version: v0.1

Date: 16 May 2026

## 1. Template Purpose

Use this template for future historical retrieval eligibility records.

This template does not expose chat, call a live LLM, change retrieval runtime, mutate corpus, ingest source content, promote current truth, write to a database, create endpoint changes, create UI changes, activate answer-use permission at runtime, or activate retrieval eligibility at runtime.

## 2. Eligibility Record

| Field | Value |
| --- | --- |
| RetrievalEligibilityId | TBD |
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
| AnswerUsePermissionStatus | TBD |
| RetrievalEligibilityStatus | `RETRIEVAL_ELIGIBILITY_NOT_REQUESTED` |
| EvidenceScope | `NOT_ANSWERABLE` |
| AnswerScope | TBD |
| RetrievalMode | TBD |
| AnswerModeContractLink | `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_CONTRACT.md` or TBD |
| CurrentTruthPermitted | No |
| HistoricalContextPermitted | No |
| RetrievalEligible | No |
| ChatEligible | No |
| CaveatRequired | Yes |
| CitationRequired | Yes |
| ProvenanceStatus | TBD |
| CrossCheckStatus | TBD |
| ConflictStatus | TBD |
| SupersessionStatus | TBD |
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

`RETRIEVAL_ELIGIBILITY_NOT_REQUESTED`, `RETRIEVAL_ELIGIBILITY_BLOCKED`, `RETRIEVAL_ELIGIBILITY_DEFERRED`, and `RETRIEVAL_ELIGIBILITY_REJECTED` preserve all conservative defaults.

`RETRIEVAL_ELIGIBLE_HISTORICAL_CONTEXT_ONLY` does not permit current-truth retrieval.

`RETRIEVAL_ELIGIBLE_CURRENT_TRUTH` requires valid current-truth approval, `CurrentTruthPermitted` Yes, and answer-use permission for the requested mode.

`RETRIEVAL_ELIGIBLE_WITH_CAVEAT` requires caveats to be carried into any future answer contract.

`RETRIEVAL_EXCLUDED_NOT_ANSWERABLE`, `RETRIEVAL_EXCLUDED_SUPERSEDED`, `RETRIEVAL_EXCLUDED_CONFLICTED`, and `RETRIEVAL_REVOKED` are not answerable retrieval states.
