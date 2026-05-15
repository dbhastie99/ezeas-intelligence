# Historical Batch Review Queue Entry Template

Version: v0.1

Date: 16 May 2026

Use this template for future entries in `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE.md`.

Queue entries are control metadata only. They do not ingest source content, review source content, mutate corpus, promote current truth, or permit answer use.

| Field | Value |
| --- | --- |
| QueueEntryId |  |
| SourceId |  |
| SourceTitle |  |
| SourceType |  |
| SourceDate |  |
| RegisteredBatchId |  |
| RepositoryContext |  |
| DomainContext |  |
| QueueStatus |  |
| CandidateSelectionStatus | `NOT_SELECTED` |
| CandidateSelectionLink |  |
| ReviewPriority |  |
| CurrentTruthRisk |  |
| IngestionPermitted | No |
| AnswerUsePermitted | No |
| RequiredCrossChecks |  |
| RequiredReviewOutputs |  |
| Blockers |  |
| Notes |  |
| LastReviewedUtc |  |
| Reviewer |  |
| DecisionRecordLink |  |

Required defaults before governed ingestion/backfill approval:

- `IngestionPermitted`: No
- `AnswerUsePermitted`: No
- historical source remains not current truth
- queue entry remains metadata-only control state
- candidate selection is optional and governed separately through `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION.md`
