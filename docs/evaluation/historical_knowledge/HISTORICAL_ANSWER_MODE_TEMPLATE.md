# Historical Answer Mode Template

Version: v0.1

Date: 16 May 2026

## 1. Template Purpose

Use this template for future historical answer-mode records.

This template does not expose chat, call a live LLM, change retrieval runtime, change answer synthesis runtime, mutate corpus, ingest source content, promote current truth, write to a database, create endpoint changes, create UI changes, activate answer-use permission at runtime, or activate retrieval eligibility at runtime.

## 2. Answer Mode Record

| Field | Value |
| --- | --- |
| AnswerModeId | TBD |
| RetrievalEligibilityId | TBD |
| AnswerUsePermissionId | TBD |
| SourceId | TBD |
| SourceTitle | TBD |
| SourceDate | TBD or unknown-date marker |
| RepositoryContext | TBD |
| DomainContext | TBD |
| EvidenceScope | `NOT_ANSWERABLE` |
| AnswerScope | TBD |
| RetrievalMode | TBD |
| AnswerModeStatus | `ANSWER_MODE_NOT_REQUESTED` |
| AnswerMode | `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE` |
| CurrentTruthPermitted | No |
| HistoricalContextPermitted | No |
| RetrievalEligible | No |
| ChatEligible | No |
| CaveatRequired | Yes |
| CitationRequired | Yes |
| ProvenanceStatus | TBD |
| ConflictStatus | TBD |
| SupersessionStatus | TBD |
| RefusalReason | TBD |
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

`ANSWER_MODE_NOT_REQUESTED`, `ANSWER_MODE_BLOCKED`, `ANSWER_MODE_DEFERRED`, and `ANSWER_MODE_REJECTED` preserve conservative defaults.

`ANSWER_MODE_APPROVED_CURRENT_TRUTH` requires current-truth promotion, answer-use permission, retrieval eligibility, provenance, and citation support.

`ANSWER_MODE_APPROVED_HISTORICAL_CONTEXT` does not permit current-truth answers.

`ANSWER_MODE_APPROVED_WITH_CAVEAT` requires caveats to be carried visibly into any future response.

Refusal modes are valid outcomes when governed evidence, answer-use permission, retrieval eligibility, citation/provenance, conflict resolution, supersession resolution, runtime retrieval, or chat contract controls are missing.
