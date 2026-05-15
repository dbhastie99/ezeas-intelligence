# Historical Batch Review Queue

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This queue is the governed review-control surface for metadata-registered Minerva historical sources.

It records whether a batch-registered historical source is eligible for future deep review, blocked from review, already under review, complete but not ingested, or archival-only. It does not perform review, ingestion, backfill, corpus mutation, current-truth promotion, or answer synthesis changes.

## 2. Scope

This queue covers historical sources that have already been registered through the historical batch registration model.

Queue entries are control metadata only. They may reference registered source IDs, batch IDs, source locations, review plans, decision records, and blockers. They must not extract or ingest source content.

The queue is separate from operational corpus content, live evidence stores, Code Evidence, database state, runtime endpoints, UI, workforce-platform, award-configurator-v1, and ezeas-analytics.

## 3. Queue Status Model

| Queue status | Meaning |
| --- | --- |
| `REGISTERED_NOT_TRIAGED` | Source metadata exists, but queue triage has not been completed. |
| `TRIAGED_NOT_READY_FOR_REVIEW` | Source has queue triage, but required readiness evidence or controls are incomplete. |
| `READY_FOR_DEEP_REVIEW` | Source has sufficient metadata and controls to start a future deep review. This does not ingest the source and does not make it current truth. |
| `REVIEW_IN_PROGRESS` | A future governed review has started under an explicit review slice. This queue status alone does not authorize ingestion or answer use. |
| `REVIEW_COMPLETE_NOT_INGESTED` | Review has completed, but no separate governed ingestion/backfill decision has approved corpus use or answer use. |
| `BLOCKED_NEEDS_SOURCE_FILES` | The registered source cannot be reviewed until source files or controlled attachment references are available. |
| `BLOCKED_NEEDS_REPOSITORY_CROSS_CHECK` | The source cannot safely proceed until required repository, code, test, schema, commit, or doctrine cross-check targets are identified or available. |
| `BLOCKED_SUPERSEDED_OR_DUPLICATE` | The source appears superseded, duplicated, or covered by another source and requires resolution before review. |
| `DO_NOT_REVIEW_ARCHIVAL_ONLY` | The source is retained for historical trace only and is not intended for review or current-truth use. |

## 4. Current Queue Entries

| QueueEntryId | SourceId | SourceTitle | SourceType | SourceDate | RegisteredBatchId | RepositoryContext | DomainContext | QueueStatus | ReviewPriority | CurrentTruthRisk | IngestionPermitted | AnswerUsePermitted | RequiredCrossChecks | RequiredReviewOutputs | Blockers | Notes | LastReviewedUtc | Reviewer | DecisionRecordLink |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HBQ-2026-05-16-001 | HIST-ANALYTICS-2025-12-06-20 | Developer Log - Analytics Engine | `DEVELOPER_LOG` | 6 December 2025 to 20 December 2025 | HIST-DEVLOG-BATCH-2026-05-15 | Historical analytics server / workforce analytics context | Analytics; Workforce Analytics DB; Golden Slice; ObjectTime; ProcessedRule; CalcInterpreterLine Replatform Review; Power BI; Reconciliation Reporting | `TRIAGED_NOT_READY_FOR_REVIEW` | High | High: historical analytics material may affect current-answer assumptions and includes supersession risk from `ProcessedRule`-era analytics to `CalcInterpreterLine` target modelling. | No | No | Current ezeas-intelligence code/tests/schema where relevant; current analytics implementation evidence; existing code cross-check plan; repository separation from workforce-platform, award-configurator-v1, and ezeas-analytics. | Review-readiness confirmation; completed deep-review pack if a future review starts; cross-check findings; review decision gate update; final decision record. | Future review must confirm source file or controlled attachment availability and complete repository cross-check before any review completion or ingestion decision. | Existing batch-registered Analytics Engine developer log remains historical, `NOT_REVIEWED`, not current truth, not ingested, and not answerable. Queueing this source only records future review control state. |  |  | `docs/evaluation/historical_knowledge/review_decision_records/HIST_ANALYTICS_2025_12_06_20_DECISION_RECORD_NOT_REVIEWED.md` |

## 5. Review Eligibility Rules

A source may move to `READY_FOR_DEEP_REVIEW` only when the readiness rules in `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_READINESS_RULES.md` are satisfied.

At minimum, the source must have a source ID, source location or attachment reference, source type, repository/domain relevance, date or approximate date, current-truth risk assessment, duplicate/supersession risk assessment, required cross-check repositories, expected review outputs, ingestion `No`, and answerability `No`.

## 6. Queue Membership and Candidate Selection

Queue membership does not itself select a source for review.

Candidate selection is a separate governed control stage recorded through `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION.md` and, where needed, the candidate-selection template at `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION_TEMPLATE.md`.

A queue entry can become eligible for candidate selection only after readiness controls are satisfied, but candidate selection still does not start deep review, ingest source content, promote current truth, permit answer use, mutate operational corpus, create Code Evidence, write databases, call live LLM, or change runtime behaviour.

## 7. Decision Record Handoff Before Review Execution

Queue entries and candidate selections flow into decision records before review execution.

The governed decision-record model is `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD.md`, with reusable records shaped by `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD_TEMPLATE.md`.

Queue status and candidate-selection status do not authorize review execution until a decision record explicitly permits review start. The decision record must preserve ingestion `No`, answer use `No`, current truth `No`, operational corpus mutation `No`, Code Evidence ingestion `No`, and live LLM use `No` unless a future governed decision explicitly changes the relevant permission.

## 8. Blocker Categories

Use these blocker categories consistently:

- `MISSING_SOURCE_ID`
- `MISSING_SOURCE_LOCATION_OR_ATTACHMENT`
- `UNKNOWN_SOURCE_TYPE`
- `UNKNOWN_REPOSITORY_OR_DOMAIN_RELEVANCE`
- `MISSING_DATE_OR_APPROXIMATE_DATE`
- `CURRENT_TRUTH_RISK_NOT_ASSESSED`
- `DUPLICATE_OR_SUPERSESSION_RISK_NOT_ASSESSED`
- `CROSS_CHECK_REPOSITORIES_NOT_IDENTIFIED`
- `EXPECTED_REVIEW_OUTPUTS_NOT_IDENTIFIED`
- `INGESTION_OR_ANSWERABILITY_BOUNDARY_UNCLEAR`
- `SOURCE_FILES_UNAVAILABLE`
- `REPOSITORY_CROSS_CHECK_UNAVAILABLE`
- `SUPERSEDED_OR_DUPLICATE_REQUIRES_RESOLUTION`
- `ARCHIVAL_ONLY_NO_REVIEW_INTENT`

## 9. Evidence Required Before Review Starts

Before a future deep review starts, the queue entry must identify:

- registered source ID and batch ID
- controlled source location or attachment reference
- source type and date or approximate date
- repository context and domain context
- current-truth risk and duplicate/supersession risk
- required cross-check repositories or evidence surfaces
- required review outputs and decision record target
- linked or planned decision record
- explicit `IngestionPermitted: No`
- explicit `AnswerUsePermitted: No`

## 10. What Review Queue Status Does Not Mean

Review queue status does not mean source content has been ingested.

Review queue status does not mean source content has been parsed, extracted, or summarized.

Review queue status does not mean source claims are current truth.

Review queue status does not permit Minerva to answer from historical material.

Review queue status does not approve governed ingestion, historical backfill, corpus mutation, Code Evidence ingestion, live LLM calls, database writes, schema migrations, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

## 11. Current Truth Boundary

Historical sources are not current truth unless reviewed, cross-checked, backfilled, and governed through a separate explicit decision.

The current Analytics Engine developer log queue entry remains not current truth. It remains `NOT_REVIEWED` in its decision record and batch register. This queue does not change that status.

## 12. Ingestion Boundary

Ingestion remains `No` for all queue entries unless a future governed ingestion slice explicitly changes it.

`READY_FOR_DEEP_REVIEW`, `REVIEW_IN_PROGRESS`, and `REVIEW_COMPLETE_NOT_INGESTED` do not authorize ingestion. `REVIEW_COMPLETE_NOT_INGESTED` still does not permit answer use until a separate governed ingestion/backfill decision exists.

## 13. Developer Handoff

Future developers should use this queue to find controlled review candidates and blockers after metadata-only batch registration is complete.

Before starting any review, read the batch register, source register, readiness rules, queue entry, existing review-readiness artefacts, cross-check plans, decision gates, and NOT_REVIEWED decision records.

Do not ingest, backfill, mutate corpus, connect Code Evidence, call live LLM, write databases, create migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, promote current truth, or permit answer use from this queue.
