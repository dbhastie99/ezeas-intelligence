# Historical Answer-Use Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This blocker model defines the blocker codes and resolution expectations for the historical answer-use permission gate.

Blocker resolution does not itself enable retrieval, expose chat, call a live LLM, or make evidence answerable.

## 2. Blocker Codes

| Blocker code | Resolution expectation |
| --- | --- |
| `MISSING_SOURCE_ID` | Record the governed `SourceId` or reject/defer answer use. |
| `MISSING_DECISION_RECORD` | Link the governing historical review decision record. |
| `MISSING_FINDINGS_RECORD` | Link findings where findings are applicable or document why not applicable. |
| `MISSING_CLASSIFICATION` | Link finding classification where applicable or document why not applicable. |
| `MISSING_INGESTION_BACKFILL_DECISION` | Link ingestion/backfill decision where applicable or document why not applicable. |
| `MISSING_CURRENT_TRUTH_PROMOTION` | Link current-truth promotion when current-truth answer use is requested. |
| `CURRENT_TRUTH_NOT_APPROVED` | Obtain separate current-truth approval before current-truth answer use can be considered. |
| `PROVENANCE_INCOMPLETE` | Complete source provenance including title, date marker, repository/domain context, and notes. |
| `CROSS_CHECK_INCOMPLETE` | Complete or explicitly defer required cross-checks with rationale. |
| `CONFLICT_UNRESOLVED` | Resolve, reject, or explicitly caveat the conflict before reassessment. |
| `SUPERSESSION_UNRESOLVED` | Resolve supersession status before reassessment. |
| `ANSWER_SCOPE_UNDEFINED` | Define answer scope by repository/domain context and answer mode. |
| `CITATION_REQUIREMENT_UNDEFINED` | Define citation/provenance requirements before reassessment. |
| `REVOCATION_PATH_MISSING` | Define removal, revocation, or quarantine path. |
| `RETRIEVAL_GATE_NOT_IMPLEMENTED` | Preserve runtime answer-use activation as No until later retrieval gating exists. |
| `CHAT_CONTRACT_NOT_IMPLEMENTED` | Preserve chat eligibility as No until later answer contract and pilot gate exist. |

## 3. Resolution Boundary

Resolving a blocker only permits the answer-use record to be reassessed.

Blocker resolution does not itself enable retrieval.

Blocker resolution does not itself expose chat.

Blocker resolution does not itself call a live LLM.

Blocker resolution does not itself make evidence answerable.

Blocker resolution does not mutate corpus, ingest source content, promote current truth, write to a database, create endpoint changes, or create UI changes.
