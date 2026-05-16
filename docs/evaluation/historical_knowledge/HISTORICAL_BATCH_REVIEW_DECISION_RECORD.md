# Historical Batch Review Decision Record

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed decision-record model for Minerva historical batch review.

A historical batch review decision record is the control artefact that must exist before, during, and after any future deep review. It records whether review may start, whether review is complete, whether ingestion is permitted, whether answer use is permitted, whether current-truth promotion is permitted, what cross-check evidence is required, what evidence was reviewed, and what blockers remain.

## 2. Scope

This model applies after metadata-only batch registration, review queueing, and candidate selection.

It covers decision-record status, decision types, required fields, pre-review permissions, review-completion boundaries, ingestion boundaries, answer-use boundaries, current-truth boundaries, cross-check evidence, blockers, deferrals, and developer handoff.

It does not ingest source content, perform deep review, mutate operational corpus, create Code Evidence, write databases, call live LLMs, change runtime behaviour, promote current truth, or permit answer use.

## 3. Decision Record Status Model

| Decision status | Meaning |
| --- | --- |
| `DECISION_RECORD_PLANNED` | A decision record is expected but has not yet been opened. |
| `DECISION_RECORD_OPEN` | A decision record exists and is available to capture review-start, review-completion, ingestion, answer-use, and current-truth decisions. |
| `DECISION_RECORD_BLOCKED` | The decision cannot advance because required evidence, source references, cross-check targets, or controls are missing. |
| `DECISION_RECORD_DEFERRED` | The decision is intentionally postponed behind dependency work or higher-priority review. |
| `DECISION_RECORD_REVIEW_COMPLETE_NOT_INGESTED` | Review completion has been recorded, but ingestion, answer use, and current-truth promotion remain unapproved. |
| `DECISION_RECORD_INGESTION_APPROVED_PENDING_BACKFILL` | A separate explicit ingestion decision approved future ingestion work, but governed backfill has not completed. |
| `DECISION_RECORD_INGESTED_NOT_CURRENT_TRUTH` | A governed ingestion/backfill path completed, but current-truth promotion has not been approved. |
| `DECISION_RECORD_CURRENT_TRUTH_APPROVED` | Current-truth promotion has been explicitly approved after completed cross-checks and required governance. |
| `DECISION_RECORD_REJECTED` | The source or decision path is rejected under current controls. |
| `DECISION_RECORD_SUPERSEDED` | The decision record is replaced by a newer, broader, or more authoritative decision record or source. |

## 4. Decision Types

| Decision type | Meaning |
| --- | --- |
| `SELECTION_DECISION` | Records how candidate selection maps into the decision-record path. |
| `REVIEW_START_DECISION` | Records whether deep review may explicitly start. |
| `REVIEW_COMPLETION_DECISION` | Records whether a deep review has completed and what findings link supports completion. |
| `INGESTION_DECISION` | Records whether a separate governed ingestion path is approved. |
| `ANSWER_USE_DECISION` | Records whether Minerva may use the reviewed source for answer generation under governed constraints. |
| `CURRENT_TRUTH_DECISION` | Records whether the source may be promoted to current truth. |
| `SUPERSESSION_DECISION` | Records whether the source or decision record is superseded by another source or decision. |
| `REJECTION_DECISION` | Records that the source should not proceed under current controls. |

## 5. Required Decision Fields

Every historical batch review decision record must include these fields:

| Field | Requirement |
| --- | --- |
| DecisionRecordId | Stable decision record identifier. |
| CandidateSelectionId | Candidate-selection record identifier or explicit reason if not applicable. |
| QueueEntryId | Historical batch review queue entry identifier. |
| SourceId | Registered source identifier. |
| SourceTitle | Source title from the source or batch register. |
| RegisteredBatchId | Registered batch identifier. |
| DecisionStatus | One status from the decision record status model. |
| DecisionType | One decision type from the decision types model. |
| ReviewPriority | Review priority inherited from queue/candidate controls or explicitly set. |
| ReviewStartPermitted | Yes/No decision for deep-review start. |
| ReviewCompleted | Yes/No review-completion state. |
| IngestionPermitted | Yes/No ingestion permission. |
| AnswerUsePermitted | Yes/No answer-use permission. |
| CurrentTruthPermitted | Yes/No current-truth permission. |
| CrossChecksRequired | Required cross-check evidence surfaces. |
| CrossChecksCompleted | Completed cross-check evidence surfaces. |
| EvidenceReviewed | Evidence reviewed by the governed review process. |
| ReviewExecutionPlanLink | Link to `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_PLAN.md` or successor governed execution plan. |
| FindingsRecordLink | Link to separate findings record. |
| BackfillRequired | Yes/No or details for required backfill before ingestion or current-truth use. |
| OperationalCorpusMutationPermitted | Yes/No operational corpus mutation permission. |
| CodeEvidenceIngestionPermitted | Yes/No Code Evidence ingestion permission. |
| LiveLLMUsePermitted | Yes/No live LLM use permission. |
| DecisionRationale | Rationale for the recorded decision. |
| Blockers | Remaining blockers or `None`. |
| DecidedBy | Reviewer or automation identity recording the decision. |
| DecidedAtUtc | UTC decision timestamp. |
| Notes | Additional control notes. |

## 6. Pre-Review Decision Requirements

Before any future deep review begins:

- candidate selection must exist;
- queue entry must exist;
- source id must exist;
- review start must be explicitly permitted before deep review begins;
- ingestion must remain No;
- answer use must remain No;
- current truth must remain No;
- operational corpus mutation must remain No;
- Code Evidence ingestion must remain No;
- live LLM use must remain No.

If any requirement is missing, the decision record must remain `DECISION_RECORD_PLANNED`, `DECISION_RECORD_OPEN`, `DECISION_RECORD_BLOCKED`, or `DECISION_RECORD_DEFERRED` until the missing control is resolved.

## 7. Review-Completion Decision Requirements

Review completion does not automatically permit ingestion.

Review completion does not automatically permit answer use.

Review completion does not automatically promote current truth.

Findings must be captured separately.

Cross-check evidence must be recorded before any ingestion/current-truth decision.

### Review Execution Plan Boundary

Decision records can permit review start by setting `ReviewStartPermitted: Yes`, but review execution must follow `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_PLAN.md`.

In short, decision records can permit review start, but review execution remains governed by the deep-review execution plan.

The linked execution plan, checklist, and findings output template govern review steps, cross-checks, findings capture, stop conditions, and completion criteria.

Permitting review start still does not permit ingestion, answer use, or current-truth promotion. `IngestionPermitted`, `AnswerUsePermitted`, and `CurrentTruthPermitted` remain No unless a separate future governed decision explicitly changes them.

### Findings Classification And Outcome Boundary

Decision records must not advance to ingestion/current-truth/answer-use decisions until findings classification and outcome decision are completed.

Completed findings must first be classified through `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDINGS_CLASSIFICATION_MODEL.md` and the reusable `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDING_CLASSIFICATION_TEMPLATE.md`.

Classified findings must then flow through `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_OUTCOME_DECISION_MODEL.md` before any later ingestion/backfill/current-truth/answer-use decision can be considered.

Findings classification and outcome decision still do not permit ingestion, answer use, or current-truth promotion unless separate future governed decisions explicitly approve those steps.

### Ingestion / Backfill Decision Control Boundary

Decision records must not advance to ingestion/backfill without ingestion/backfill decision control.

After classified findings and outcome decision exist, any `OUTCOME_READY_FOR_INGESTION_DECISION` path must flow through `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md` before ingestion or backfill planning may be considered.

Ingestion/backfill decision control still does not ingest source content, backfill corpus, promote current truth, or permit answer use.

## 8. Ingestion Decision Boundary

Ingestion requires a separate explicit decision.

Ingestion approval is not created by queueing, candidate selection, or review completion.

Ingestion approval still does not automatically mean current truth.

Any ingestion approval must remain linked to the decision record, backfill requirements, findings, and cross-check evidence.

## 9. Answer-Use Decision Boundary

Answer-use permission requires explicit approval.

Answer-use permission must be linked to ingestion/backfill and current-truth decision status.

No `NOT_REVIEWED`, candidate-only, queued-only, or review-complete-not-ingested source may be used as current answer truth.

Answer-use permission remains No unless a future governed ingestion/backfill/current-truth decision explicitly changes it.

## 10. Current-Truth Decision Boundary

Current-truth promotion requires explicit decision.

Current-truth promotion requires completed cross-checks.

Historical material must not override newer repository/source truth unless the decision record explains why.

Current-truth status must be visible to Minerva retrieval/answer logic before any future answer-use integration.

## 11. Cross-Check Evidence Requirements

Decision records must identify required and completed cross-check evidence before any ingestion or current-truth decision can be approved.

Cross-check evidence may include current repository docs, tests, code, schemas, commits, decision gates, review-readiness records, findings records, source registers, batch registers, queue entries, candidate-selection records, and known supersession evidence.

Cross-check requirements must preserve repository separation from `workforce-platform`, `award-configurator-v1`, and `ezeas-analytics`.

Identifying cross-check requirements does not perform those cross-checks.

## 12. Blocker and Deferral Handling

Blocked or deferred decision records must record:

- blocker or deferral reason;
- missing evidence or missing control;
- action needed before review start, review completion, ingestion, answer use, or current-truth decision can advance;
- whether a supersession or rejection decision should be considered.

Resolving a blocker does not itself approve review start, ingestion, answer use, current-truth promotion, corpus mutation, Code Evidence ingestion, database writes, live LLM use, endpoint changes, UI changes, schema migrations, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

## 13. What a Decision Record Does Not Mean

Creating a decision record does not ingest source content.

Creating a decision record does not perform deep review.

Creating a decision record does not promote current truth.

Creating a decision record does not permit answer use.

Creating a decision record does not mutate operational corpus.

Creating a decision record does not create Code Evidence.

Creating a decision record does not write to a database.

Creating a decision record does not call a live LLM.

Creating a decision record does not create schema migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, or change runtime behaviour.

## 14. Developer Handoff

Future developers must create or update a historical batch review decision record before any governed deep-review execution begins.

Use the decision record to preserve the chain from queue entry to candidate selection to review start to findings to review completion to any later ingestion/backfill/current-truth decision.

When review start is permitted, link `ReviewExecutionPlanLink` to `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_EXECUTION_PLAN.md` and link `FindingsRecordLink` to the future findings record created from `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_FINDINGS_OUTPUT_TEMPLATE.md`.

Do not ingest source content, mutate operational corpus, create Code Evidence, call live LLM, write databases, create migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, promote current truth, permit answer use, or execute deep review merely because a decision record exists.
