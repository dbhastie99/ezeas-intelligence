# Historical Ingestion/Backfill Decision Template

Version: v0.1

Date: 16 May 2026

Use this template to record a governed ingestion/backfill decision-control state after findings classification and outcome decision. This template is conservative by default and does not ingest source content, backfill corpus, promote current truth, or permit answer use.

## Decision Record

| Field | Value |
| --- | --- |
| IngestionBackfillDecisionId |  |
| SourceRegisterId |  |
| SourceId |  |
| SourceTitle |  |
| SourceDate |  |
| FindingId |  |
| FindingReference |  |
| FindingClassification |  |
| FindingClassificationId |  |
| ReviewDecisionRecordReference |  |
| DecisionRecordId |  |
| FindingsRecordId |  |
| RegisteredBatchId |  |
| QueueEntryId |  |
| CandidateSelectionId |  |
| OutcomeDecisionStatus |  |
| DecisionStatus | `INGESTION_BACKFILL_BLOCKED` |
| IngestionDecisionStatus | `INGESTION_DECISION_NOT_STARTED` |
| ProposedIngestionScope | Not defined. |
| ProposedBackfillScope | Not defined. |
| ProposedBackfillTarget |  |
| BackfillTargetBoundary | No target write occurs in this slice. |
| ProposedTruthStatus | Not current truth. |
| ProposedAnswerUseStatus | Answer use not approved. |
| CurrentTruthPermitted | No |
| CurrentTruthPromotionPermitted | No |
| AnswerUsePermitted | No |
| IngestionPermitted | No |
| BackfillPermitted | No |
| BackfillExecutionPermitted | No |
| BackfillDryRunPermitted | No, unless a later explicit dry-run slice approves it |
| CorpusMutationPermitted | No |
| OperationalCorpusMutationPermitted | No |
| CodeEvidenceIngestionPermitted | No |
| DatabaseWritePermitted | No |
| LiveLLMUsePermitted | No |
| ChatExposurePermitted | No |
| CrossCheckStatus |  |
| RepositoryCrossCheckStatus |  |
| ConflictStatus |  |
| ConflictAssessment |  |
| SupersessionStatus |  |
| SupersessionAssessment |  |
| DuplicateStatus |  |
| DuplicateAssessment |  |
| ProvenanceStatus |  |
| RollbackPlanStatus |  |
| BackfillExecutionDesignReference | `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_EXECUTION_DESIGN.md` |
| BackfillDryRunStatus | Not approved. |
| BackfillApplyStatus | Not approved. |
| FormalEvidenceGapStatus |  |
| SensitiveDataAssessment |  |
| Blockers |  |
| RequiredNextAction |  |
| DecisionRationale |  |
| Reviewer |  |
| DecisionDate |  |
| DecidedBy |  |
| DecidedAtUtc |  |
| Notes |  |

## Explicit Non-Goals

- Do not ingest source content.
- Do not mutate operational corpus.
- Do not create Code Evidence.
- Do not write to database.
- Do not call live LLM.
- Do not execute backfill.
- Do not approve a backfill dry-run.
- Do not create or mutate corpus records.
- Do not promote current truth.
- Do not permit answer use.
- Do not expose chat.
- Do not add endpoints.
- Do not add UI.
- Do not modify runtime answer behaviour.
- Do not represent backlog or follow-up findings as implemented behaviour.

Required conservative defaults:

- `CurrentTruthPermitted`: No
- `CurrentTruthPromotionPermitted`: No
- `AnswerUsePermitted`: No
- `IngestionPermitted`: No
- `BackfillPermitted`: No
- `BackfillExecutionPermitted`: No
- `BackfillDryRunPermitted`: No, unless a later explicit dry-run slice approves it
- `CorpusMutationPermitted`: No
- `OperationalCorpusMutationPermitted`: No
- `CodeEvidenceIngestionPermitted`: No
- `DatabaseWritePermitted`: No
- `LiveLLMUsePermitted`: No
- `ChatExposurePermitted`: No

Permitted ingestion/backfill decision statuses are defined in `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`.

Blocker codes are defined in `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_BLOCKER_MODEL.md`.
