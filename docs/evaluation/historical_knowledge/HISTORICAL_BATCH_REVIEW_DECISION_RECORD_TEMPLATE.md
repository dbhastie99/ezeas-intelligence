# Historical Batch Review Decision Record Template

Version: v0.1

Date: 16 May 2026

Use this template to create governed decision records for historical batch review candidates.

Decision records are control artefacts only. Creating a decision record does not ingest source content, perform deep review, mutate operational corpus, promote current truth, create Code Evidence, call live LLMs, write databases, or permit answer use.

| Field | Value |
| --- | --- |
| DecisionRecordId |  |
| CandidateSelectionId |  |
| QueueEntryId |  |
| SourceId |  |
| SourceTitle |  |
| RegisteredBatchId |  |
| DecisionStatus | `DECISION_RECORD_PLANNED` |
| DecisionType | `SELECTION_DECISION` |
| ReviewPriority |  |
| ReviewStartPermitted | No |
| ReviewCompleted | No |
| IngestionPermitted | No |
| AnswerUsePermitted | No |
| CurrentTruthPermitted | No |
| CrossChecksRequired |  |
| CrossChecksCompleted |  |
| EvidenceReviewed |  |
| ReviewExecutionPlanLink | `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_PLAN.md` when review start is permitted |
| FindingsRecordLink | Planned; required before review completion |
| BackfillRequired |  |
| OperationalCorpusMutationPermitted | No |
| CodeEvidenceIngestionPermitted | No |
| LiveLLMUsePermitted | No |
| DecisionRationale |  |
| Blockers |  |
| DecidedBy |  |
| DecidedAtUtc |  |
| Notes |  |

Required conservative defaults:

- `ReviewStartPermitted`: No
- `ReviewCompleted`: No
- `IngestionPermitted`: No
- `AnswerUsePermitted`: No
- `CurrentTruthPermitted`: No
- `OperationalCorpusMutationPermitted`: No
- `CodeEvidenceIngestionPermitted`: No
- `LiveLLMUsePermitted`: No
- historical source remains not current truth
- source content has not been ingested
- deep review has not started
- answer use is not permitted
