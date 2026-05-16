# Historical Citation / Provenance Template

Version: v0.1

Date: 16 May 2026

## 1. Template Purpose

Use this template for future historical citation/provenance records.

This template does not expose chat, call a live LLM, render citations at runtime, change retrieval runtime, change answer synthesis runtime, mutate corpus, ingest source content, promote current truth, write to a database, create endpoint changes, create UI changes, activate answer-use permission at runtime, or activate retrieval eligibility at runtime.

## 2. Citation / Provenance Record

| Field | Value |
| --- | --- |
| CitationProvenanceId | TBD |
| AnswerModeId | TBD |
| RetrievalEligibilityId | TBD |
| AnswerUsePermissionId | TBD |
| SourceId | TBD |
| SourceTitle | TBD |
| SourceDate | TBD or use UnknownDateMarker |
| UnknownDateMarker | `UNKNOWN_DATE` when source date is unavailable |
| RepositoryContext | TBD |
| DomainContext | TBD |
| DecisionRecordId | TBD where applicable |
| FindingsRecordId | TBD where applicable |
| FindingClassificationId | TBD where applicable |
| IngestionBackfillDecisionId | TBD where applicable |
| CurrentTruthPromotionId | TBD where applicable |
| EvidenceScope | `NOT_ANSWERABLE` |
| AnswerScope | TBD |
| RetrievalMode | TBD |
| AnswerMode | `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE` |
| CitationStatus | `CITATION_NOT_REQUESTED` |
| CitationRequired | Yes |
| CaveatRequired | Yes |
| CaveatText | TBD |
| ProvenanceStatus | `NOT_RUNTIME_ENFORCED` |
| ConflictStatus | TBD |
| SupersessionStatus | TBD |
| RefusalReason | TBD |
| RevocationPath | TBD |
| Blockers | TBD |
| ChatEligible | No |
| ApprovedBy | TBD |
| ApprovedAtUtc | TBD |
| Notes | TBD |

## 3. Conservative Defaults

| Field | Default |
| --- | --- |
| CitationRequired | Yes |
| CaveatRequired | Yes |
| ProvenanceStatus | `NOT_RUNTIME_ENFORCED` |
| ChatEligible | No |

## 4. Decision Notes

`CITATION_NOT_REQUESTED`, `CITATION_BLOCKED`, and `CITATION_DEFERRED` preserve conservative defaults.

Missing or incomplete citation/provenance maps to refusal or insufficient governed evidence.

`ChatEligible` remains No in this slice.
