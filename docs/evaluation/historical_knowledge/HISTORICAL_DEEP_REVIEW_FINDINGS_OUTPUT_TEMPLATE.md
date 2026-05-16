# Historical Deep Review Findings Output Template

Version: v0.1

Date: 16 May 2026

Use this template to capture governed historical deep-review findings. Findings are review outputs only and do not become current truth automatically.

| Field | Value |
| --- | --- |
| FindingsRecordId |  |
| DecisionRecordId |  |
| CandidateSelectionId |  |
| QueueEntryId |  |
| SourceId |  |
| SourceTitle |  |
| SourceDate |  |
| Reviewer |  |
| ReviewDateUtc |  |
| RepositoryContext |  |
| DomainContext |  |
| FindingId |  |
| FindingType |  |
| FindingSummary |  |
| SourceEvidenceReference |  |
| CrossCheckStatus |  |
| CurrentTruthImpactAssessment |  |
| SupersessionAssessment |  |
| ConflictAssessment |  |
| RecommendedNextDecision |  |
| IngestionRecommended | No |
| AnswerUseRecommended | No |
| CurrentTruthPromotionRecommended | No |
| Blockers |  |
| Notes |  |

Required conservative defaults:

- `IngestionRecommended`: No
- `AnswerUseRecommended`: No
- `CurrentTruthPromotionRecommended`: No

Recommended finding types:

- `FACT`
- `DECISION`
- `DOCTRINE`
- `BACKLOG_ITEM`
- `HISTORICAL_NOTE`
- `SUPERSEDED_ITEM`
- `CONFLICT`

Recommended evidence classifications:

- `CANDIDATE_HISTORICAL_EVIDENCE`
- `CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL`
- `SUPERSEDED_EVIDENCE`
- `DUPLICATE_EVIDENCE`
- `CONFLICTING_EVIDENCE`
- `BACKLOG_OR_FOLLOW_UP`
- `NOT_RELEVANT`
- `REQUIRES_REPOSITORY_CROSS_CHECK`
