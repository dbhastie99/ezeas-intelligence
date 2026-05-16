# Historical Ingestion/Backfill Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines blocker codes and resolution expectations for Minerva historical ingestion/backfill decision control.

Blocker resolution does not itself perform ingestion, permit answer use, or promote current truth.

## 2. Blocker Codes

| Blocker code | Meaning | Resolution expectation |
| --- | --- | --- |
| `MISSING_DECISION_RECORD` | No governed decision record is linked. | Create or link `DecisionRecordId` before reassessment. |
| `MISSING_FINDINGS_RECORD` | No findings record is linked. | Link `FindingsRecordId` from governed deep-review findings output. |
| `MISSING_CLASSIFICATION` | No finding classification is linked. | Complete or link `FindingClassificationId`. |
| `MISSING_OUTCOME_DECISION` | No outcome decision exists. | Record outcome decision status before ingestion/backfill decision control. |
| `MISSING_SOURCE_REFERENCE` | Source id or source evidence reference is missing. | Link `SourceId` and `SourceEvidenceReference`. |
| `UNKNOWN_SOURCE_DATE_UNASSESSED` | Source date/version is unknown without explicit assessment. | Record known date/version or explicit unknown-date marker with rationale. |
| `CROSS_CHECK_INCOMPLETE` | Required repository or cross-repository checks are incomplete. | Complete checks or defer with explicit rationale. |
| `CONFLICT_UNRESOLVED` | Finding conflicts with current truth and conflict is unresolved. | Resolve conflict or keep the decision blocked. |
| `SUPERSESSION_UNRESOLVED` | Supersession status is unknown or disputed. | Record supersession assessment and controlling source. |
| `DUPLICATE_UNRESOLVED` | Duplicate status is unknown or disputed. | Link duplicate evidence or record not-duplicate rationale. |
| `PROVENANCE_INCOMPLETE` | Required provenance fields are missing. | Complete provenance sufficient for traceability and later removal. |
| `ROLLBACK_PLAN_MISSING` | Rollback/removal instructions are missing. | Record rollback/removal plan before any future write planning. |
| `CURRENT_TRUTH_DECISION_MISSING` | Current-truth boundary is absent or ambiguous. | Record that current-truth decision remains separate or link a later explicit decision. |
| `ANSWER_USE_DECISION_MISSING` | Answer-use boundary is absent or ambiguous. | Record that answer-use permission remains separate or link a later explicit decision. |
| `TARGET_STORE_UNDECIDED` | Proposed backfill target is missing or uncontrolled. | Identify whether target is metadata-only, historical corpus, governed evidence corpus, Code Evidence, or another controlled store before planning. |
| `SOURCE_NOT_REVIEWED` | The source has not completed governed historical review. | Complete review or keep ingestion/backfill blocked. |
| `CLASSIFICATION_NOT_ALLOWED_FOR_INGESTION` | The finding classification does not permit ingestion/backfill consideration. | Reject or retain historical-only unless a later governed reclassification occurs. |
| `SUPERSEDED_BY_CURRENT_TRUTH` | Newer repository or formal evidence supersedes the finding. | Do not use as current truth; link to the controlling current evidence. |
| `CONFLICT_REQUIRES_RESOLUTION` | The finding conflicts with current truth or another reviewed finding. | Resolve the conflict before any ingestion/backfill decision can proceed. |
| `DUPLICATE_REQUIRES_LINKING` | The finding duplicates existing evidence. | Link to existing evidence rather than creating duplicate truth. |
| `IMPLEMENTATION_STATE_UNCERTAIN` | It is unclear whether the finding describes planned, implemented, removed, or partial behaviour. | Complete repository and evidence checks before representing implementation state. |
| `REPOSITORY_CROSS_CHECK_REQUIRED` | A repository cross-check is required before decision. | Complete or explicitly defer repository cross-checks with rationale. |
| `FORMAL_EVIDENCE_GAP` | Formal evidence is missing or insufficient for the proposed use. | Capture or link formal evidence, or block/defer the decision. |
| `SENSITIVE_OR_TENANT_DATA_RISK` | The source or finding may contain sensitive, tenant, or unsuitable operational data. | Quarantine or redact under data handling controls before reassessment. |
| `ANSWER_USE_NOT_APPROVED` | Answer-use permission has not been explicitly approved. | Keep `AnswerUsePermitted` No unless a separate answer-use decision approves it. |
| `CURRENT_TRUTH_NOT_APPROVED` | Current-truth promotion has not been explicitly approved. | Keep `CurrentTruthPromotionPermitted` No unless a separate current-truth decision approves it. |
| `INGESTION_SCOPE_NOT_DEFINED` | Proposed ingestion scope is missing or ambiguous. | Define bounded ingestion scope before any planning decision. |
| `BACKFILL_STRATEGY_NOT_DEFINED` | Proposed backfill strategy is missing or ambiguous. | Define backfill target, method, provenance, and rollback strategy before planning. |
| `REVIEW_GATE_NOT_READY` | Required upstream review gate is incomplete or not ready. | Complete the gate or defer with explicit rationale. |
| `SOURCE_AUTHORITY_TOO_LOW` | The source authority is too low for the proposed use. | Restrict to historical context, reject, or require higher-authority evidence. |
| `HISTORICAL_ONLY_CONTEXT` | The finding is valid only as historical context. | Preserve historical-only retention and block current answer/current truth use. |

## 3. Resolution Boundary

Resolving a blocker permits only reassessment of the ingestion/backfill decision-control record.

Blocker resolution does not ingest source content.

Blocker resolution does not backfill corpus.

Blocker resolution does not permit answer use.

Blocker resolution does not promote current truth.

Blocker resolution does not expose chat.

Blocker resolution does not add endpoints.

Blocker resolution does not add UI.

Blocker resolution does not modify runtime answer behaviour.

Blocker resolution does not mutate operational corpus, create Code Evidence, write to a database, call a live LLM, change schemas, change endpoints, change UI, change `workforce-platform`, change `award-configurator-v1`, or change `ezeas-analytics`.
