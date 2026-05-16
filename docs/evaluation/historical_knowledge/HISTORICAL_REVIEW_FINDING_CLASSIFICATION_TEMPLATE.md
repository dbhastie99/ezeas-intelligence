# Historical Review Finding Classification Template

Version: v0.1

Date: 16 May 2026

Use this template to classify individual findings after governed historical deep-review findings have been captured. Classification records are control artefacts only and do not ingest source content, mutate corpus, promote current truth, or permit answer use.

| Field | Value |
| --- | --- |
| FindingClassificationId |  |
| FindingsRecordId |  |
| DecisionRecordId |  |
| SourceId |  |
| SourceTitle |  |
| FindingId |  |
| FindingSummary |  |
| ClassificationStatus | `CLASSIFICATION_NOT_STARTED` |
| FindingClassificationType |  |
| RepositoryContext |  |
| DomainContext |  |
| CrossCheckRequired |  |
| CrossCheckStatus |  |
| ConflictsWithCurrentTruth |  |
| SupersededBy |  |
| DuplicateOf |  |
| RecommendedOutcomeDecision |  |
| IngestionPermitted | No |
| AnswerUsePermitted | No |
| CurrentTruthPermitted | No |
| Reviewer |  |
| ClassifiedAtUtc |  |
| DecisionRecordLink |  |
| IngestionBackfillDecisionLink | Planned/optional |
| Notes |  |

Required conservative defaults:

- `IngestionPermitted`: No
- `AnswerUsePermitted`: No
- `CurrentTruthPermitted`: No

Permitted classification statuses are defined in `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDINGS_CLASSIFICATION_MODEL.md`.

Permitted outcome decision statuses are defined in `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_OUTCOME_DECISION_MODEL.md`.
