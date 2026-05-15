# Historical Batch Review Candidate Selection Template

Version: v0.1

Date: 16 May 2026

Use this template to record candidate-selection decisions for entries in `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE.md`.

Candidate-selection records are metadata/control only. They do not ingest source content, perform deep review, mutate operational corpus, promote current truth, create Code Evidence, call live LLMs, write databases, or permit answer use.

| Field | Value |
| --- | --- |
| CandidateSelectionId |  |
| QueueEntryId |  |
| SourceId |  |
| SourceTitle |  |
| RegisteredBatchId |  |
| CandidateStatus | `NOT_SELECTED` |
| ReviewPriority |  |
| SelectionRationale |  |
| CurrentTruthRisk |  |
| DuplicateOrSupersessionRisk |  |
| RequiredCrossChecks |  |
| RequiredReviewOutputs |  |
| IngestionPermitted | No |
| AnswerUsePermitted | No |
| Blockers |  |
| SelectedBy |  |
| SelectedAtUtc |  |
| DecisionRecordLink | Planned before any future deep review starts |
| Notes |  |

Required defaults:

- `CandidateStatus`: `NOT_SELECTED` until a governed candidate-selection decision is recorded
- `IngestionPermitted`: No
- `AnswerUsePermitted`: No
- historical source remains not current truth
- candidate selection remains metadata-only control state
- deep review has not started
- `DecisionRecordLink` is required or planned before any future deep review starts
