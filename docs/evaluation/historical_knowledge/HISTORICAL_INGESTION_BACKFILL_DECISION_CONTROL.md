# Historical Ingestion/Backfill Decision Control

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed decision-control model between classified Minerva historical review findings and any future ingestion or backfill work.

It exists so Minerva can distinguish reviewed-but-not-ingested historical evidence from evidence that may be considered for a later governed ingestion/backfill plan. It does not perform ingestion, backfill, current-truth promotion, or answer-use approval.

## 2. Scope

This model applies after findings classification and outcome decision have been recorded through:

- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDINGS_CLASSIFICATION_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_OUTCOME_DECISION_MODEL.md`

This slice is documentation/control/test hardening only. It does not ingest source content, backfill corpus, mutate operational evidence, create Code Evidence, write databases, call live LLMs, change schemas, change endpoints, change UI, change `workforce-platform`, change `award-configurator-v1`, change `ezeas-analytics`, promote current truth, permit answer use, or execute deep review.

## 3. Required Control State Separation

The decision gate separates these states. Moving into one state does not imply
approval for any later state:

| State | Meaning |
| --- | --- |
| `FINDING_CLASSIFIED` | A historical review finding has been classified. A classified finding is not ingestion, current truth, or answer-use permission. |
| `INGESTION_BACKFILL_CANDIDATE` | The classified finding may be assessed for a later ingestion/backfill decision. It is still only a candidate. |
| `INGESTION_BACKFILL_DECISION_DRAFTED` | A decision record has been drafted. Drafting does not approve ingestion, backfill, current truth, or answer use. |
| `INGESTION_BACKFILL_APPROVED` | A future ingestion/backfill plan may be prepared under separate execution controls. Approval here does not automatically mean current truth. |
| `INGESTION_BACKFILL_BLOCKED` | Ingestion/backfill must not proceed until blockers are resolved and the record is reassessed. |
| `INGESTION_BACKFILL_DEFERRED` | Ingestion/backfill is intentionally postponed. Deferral must preserve conservative defaults. |
| `HISTORICAL_ONLY_RETENTION` | The finding may be retained only as historical context and must not be used as a current answer. |
| `CURRENT_TRUTH_PROMOTION_CANDIDATE` | The finding may be considered for a separate current-truth approval. It is not current truth. |
| `ANSWER_USE_CANDIDATE` | The finding may be considered for separate answer-use approval. It is not answer-use permission. |
| `CURRENT_TRUTH_APPROVED` | A separate current-truth approval exists. This does not automatically permit answer use. |
| `ANSWER_USE_APPROVED` | A separate answer-use approval exists. This is required before the finding may support answers. |

`CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL` is still only a candidate.

## 4. Ingestion / Backfill Decision Status Model

| Status | Meaning |
| --- | --- |
| `INGESTION_DECISION_NOT_STARTED` | No ingestion/backfill decision has been opened. |
| `INGESTION_DECISION_BLOCKED` | Required evidence, cross-checks, provenance, rollback planning, or boundary decisions are missing. |
| `INGESTION_DECISION_DEFERRED` | Decision is intentionally postponed pending dependency work or higher-priority review. |
| `INGESTION_DECISION_REJECTED` | Ingestion/backfill is rejected under current controls. |
| `INGESTION_DECISION_APPROVED_FOR_PLANNING_ONLY` | A future ingestion plan may be drafted, but no source content may be ingested. |
| `BACKFILL_DECISION_APPROVED_FOR_PLANNING_ONLY` | A future backfill plan may be drafted, but no target store may be written. |
| `INGESTION_READY_PENDING_BACKFILL_PLAN` | Ingestion planning prerequisites are satisfied, but a governed backfill plan is still required. |
| `BACKFILL_READY_PENDING_EXECUTION_PLAN` | Backfill planning prerequisites are satisfied, but a governed execution plan is still required before any write. |
| `INGESTED_NOT_CURRENT_TRUTH` | A future governed ingestion may have completed, but current-truth promotion remains separate and unapproved. |
| `INGESTED_HISTORICAL_ONLY` | A future governed ingestion may have completed into historical-only scope, not current answer truth. |
| `CURRENT_TRUTH_PROMOTION_REQUIRED_SEPARATELY` | Current-truth promotion requires a separate explicit governed decision. |

## 5. Conservative Permission Defaults

Every ingestion/backfill decision record starts with these values:

| Permission | Default |
| --- | --- |
| `IngestionPermitted` | No |
| `BackfillPermitted` | No |
| `CurrentTruthPromotionPermitted` | No |
| `AnswerUsePermitted` | No |
| `OperationalCorpusMutationPermitted` | No |
| `CodeEvidenceIngestionPermitted` | No |
| `DatabaseWritePermitted` | No |
| `LiveLLMUsePermitted` | No |
| `ChatExposurePermitted` | No |

These defaults remain No unless a later governed decision explicitly changes the
specific permission. No default may be inferred from classification, outcome
decision, ingestion/backfill approval, or current-truth approval.

## 6. Preconditions Before Ingestion / Backfill Can Be Considered

Ingestion/backfill may not be considered unless all required controls below exist or are explicitly blocked/deferred with rationale:

- `DecisionRecordId` exists.
- `FindingsRecordId` exists.
- `FindingClassificationId` exists.
- Outcome decision exists.
- Source id exists.
- Source reference exists.
- Source date/version is known or explicitly marked unknown.
- Repository/domain context exists.
- Required cross-checks are completed or explicitly deferred with rationale.
- Conflicts are resolved or explicitly blocked.
- Supersession status is recorded.
- Duplicate status is recorded.
- Provenance requirement is recorded.
- Rollback/removal requirement is recorded.
- Current-truth decision remains separate.
- Answer-use decision remains separate.

## 7. Classification and Outcome Requirements

Only classified findings may enter ingestion/backfill decision control.

A classified finding is not ingestion.

A classified finding is not current truth.

A classified finding is not answer-use permission.

`CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL` does not mean current truth.

`CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL` is still only a candidate.

`HISTORICAL_ONLY_CONTEXT` may only be considered for historical-labelled ingestion.

Historical-only findings must not be used as current answers.

`SUPERSEDED_BY_CURRENT_REPOSITORY_TRUTH` must not be ingested as current truth.

Superseded findings must not be used as current truth.

`CONFLICTS_WITH_CURRENT_TRUTH` must remain blocked until conflict resolution.

Conflicting findings must be blocked until conflict resolution.

Duplicate findings should link to existing evidence rather than create duplicate truth.

Backlog/follow-up findings may inform planning but must not be represented as implemented behaviour.

`OUTCOME_READY_FOR_INGESTION_DECISION` only means an ingestion/backfill decision may be considered.

`OUTCOME_READY_FOR_ANSWER_USE_DECISION` does not permit answer use by itself.

## 8. Cross-Check Requirements

Required cross-checks must be identified and completed or explicitly deferred with rationale before ingestion/backfill can be considered:

- `workforce-platform` cross-check where source affects workforce/platform/runtime doctrine.
- `award-configurator-v1` cross-check where source affects award build/configuration/parser/interpreter truth.
- `ezeas-analytics` cross-check where source affects analytics/reporting schema/view/readiness truth.
- `ezeas-intelligence` cross-check where source affects Minerva retrieval/evidence/answering doctrine.

Current repository truth and latest committed logs must take priority over unreviewed historical material.

## 9. Provenance Requirements

Every ingestion/backfill decision record must preserve:

- `SourceId`
- `SourceTitle`
- `SourceDate` or unknown-date marker
- `RegisteredBatchId`
- `QueueEntryId`
- `CandidateSelectionId`
- `DecisionRecordId`
- `FindingsRecordId`
- `FindingClassificationId`
- `Reviewer`
- `ReviewDateUtc`
- `CrossCheckStatus`
- `OutcomeDecisionStatus`
- `IngestionDecisionStatus`
- `SourceEvidenceReference`
- `Notes`

## 10. Backfill Target Boundary

This slice does not decide final storage target.

Future backfill planning must identify whether evidence is historical-only, doctrine candidate, hardening candidate, developer-log context, current-truth candidate, or rejected.

Future backfill planning must define whether the target is metadata-only, historical corpus, governed evidence corpus, Code Evidence, or another controlled store.

No target write occurs in this slice.

## 11. Current Truth Boundary

Ingestion/backfill decision control does not promote current truth.

Ingestion/backfill approval does not automatically mean current truth.

Current-truth promotion requires a separate explicit decision.

Current-truth promotion must be visible to retrieval/answer gating before chat exposure.

Historical evidence must not override newer repository truth unless explicitly approved.

## 12. Answer-Use Boundary

Answer use remains No in this slice.

Answer-use permission requires separate explicit approval.

Current-truth approval does not automatically mean answer-use permission.

Answer-use permission must remain a separate decision.

Ingested historical material must not become answerable current truth by default.

Minerva chat exposure must respect answer-use permission and current-truth status.

## 13. Rollback / Removal Requirements

Any future ingestion/backfill plan must include rollback/removal instructions.

Provenance must be sufficient to remove or quarantine ingested evidence.

Superseded or rejected evidence must be quarantineable.

No irreversible ingestion is allowed without rollback planning.

## 14. Blocker Handling

Blocked decisions must record one or more blocker codes and the required resolution path:

- `MISSING_DECISION_RECORD`
- `MISSING_FINDINGS_RECORD`
- `MISSING_CLASSIFICATION`
- `MISSING_OUTCOME_DECISION`
- `MISSING_SOURCE_REFERENCE`
- `UNKNOWN_SOURCE_DATE_UNASSESSED`
- `CROSS_CHECK_INCOMPLETE`
- `CONFLICT_UNRESOLVED`
- `SUPERSESSION_UNRESOLVED`
- `DUPLICATE_UNRESOLVED`
- `PROVENANCE_INCOMPLETE`
- `ROLLBACK_PLAN_MISSING`
- `CURRENT_TRUTH_DECISION_MISSING`
- `ANSWER_USE_DECISION_MISSING`
- `TARGET_STORE_UNDECIDED`
- `SOURCE_NOT_REVIEWED`
- `CLASSIFICATION_NOT_ALLOWED_FOR_INGESTION`
- `SUPERSEDED_BY_CURRENT_TRUTH`
- `CONFLICT_REQUIRES_RESOLUTION`
- `DUPLICATE_REQUIRES_LINKING`
- `IMPLEMENTATION_STATE_UNCERTAIN`
- `REPOSITORY_CROSS_CHECK_REQUIRED`
- `FORMAL_EVIDENCE_GAP`
- `SENSITIVE_OR_TENANT_DATA_RISK`
- `ANSWER_USE_NOT_APPROVED`
- `CURRENT_TRUTH_NOT_APPROVED`
- `INGESTION_SCOPE_NOT_DEFINED`
- `BACKFILL_STRATEGY_NOT_DEFINED`
- `REVIEW_GATE_NOT_READY`
- `SOURCE_AUTHORITY_TOO_LOW`
- `HISTORICAL_ONLY_CONTEXT`

Resolving a blocker only permits the decision record to be reassessed. It does not ingest source content, permit answer use, or promote current truth.

## 15. What Ingestion / Backfill Decision Control Does Not Mean

Creating decision-control docs does not ingest source content.

Decision control does not backfill corpus.

Decision control does not promote current truth.

Decision control does not permit answer use.

Decision control does not mutate operational corpus.

Decision control does not create Code Evidence.

Decision control does not write to a database.

Decision control does not call a live LLM.

Decision control does not expose chat.

Decision control does not add endpoints.

Decision control does not add UI.

Decision control does not modify runtime answer behaviour.

## 16. Developer Handoff

Future developers must use this model after findings classification and outcome decision, and before any ingestion/backfill planning work.

Use `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_TEMPLATE.md` for individual decision records and `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_BLOCKER_MODEL.md` for blocker handling.

Do not ingest source content, backfill corpus, mutate operational evidence, create Code Evidence, call live LLM, write databases, create migrations, change endpoints, change UI, change `workforce-platform`, change `award-configurator-v1`, change `ezeas-analytics`, promote current truth, permit answer use, or execute deep review merely because ingestion/backfill decision control exists.
