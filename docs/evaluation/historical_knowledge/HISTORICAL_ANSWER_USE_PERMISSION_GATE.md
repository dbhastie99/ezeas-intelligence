# Historical Answer-Use Permission Gate

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed answer-use permission gate for Minerva historical knowledge.

The gate controls whether reviewed, classified, ingested/backfilled, and current-truth-promoted historical evidence may be used by Minerva in future answers.

This slice defines the control model only. It does not expose chat, alter retrieval behaviour, call a live LLM, ingest content, mutate corpus, promote current truth, or permit answer use at runtime.

## 2. Scope

This gate applies only after the relevant prior historical controls exist: source registration, review decision record, findings record, finding classification, ingestion/backfill decision where applicable, backfill execution/validation where applicable, and current-truth promotion where current-truth answer use is requested.

Historical sources are not answerable current truth by default. Registration, queueing, candidate selection, decision records, deep-review planning, findings classification, ingestion/backfill decision control, backfill execution design, and current-truth promotion do not permit answer use by themselves.

## 3. Answer-Use Permission Status Model

| Status | Meaning |
| --- | --- |
| `ANSWER_USE_NOT_REQUESTED` | No answer-use decision has been requested. |
| `ANSWER_USE_BLOCKED` | Answer use is blocked until recorded blockers are resolved and reassessed. |
| `ANSWER_USE_DEFERRED` | Answer-use decision is intentionally postponed; conservative defaults remain No. |
| `ANSWER_USE_REJECTED` | Answer use is rejected under current controls. |
| `ANSWER_USE_APPROVED_HISTORICAL_CONTEXT_ONLY` | Evidence may support labelled historical-context answers only, not current truth. |
| `ANSWER_USE_APPROVED_CURRENT_TRUTH` | Evidence may support current-truth answers only when current-truth approval also exists. |
| `ANSWER_USE_APPROVED_WITH_CAVEAT` | Evidence may support answers only with recorded caveats preserved. |
| `ANSWER_USE_REQUIRES_REVIEW` | Answer use cannot be decided until further review is completed. |
| `ANSWER_USE_REVOKED` | Prior answer-use permission has been revoked and must not be used. |
| `ANSWER_USE_SUPERSEDED` | Prior answer-use permission has been superseded by newer controlling evidence. |

## 4. Preconditions Before Answer Use Can Be Considered

Answer use must not be considered unless all required controls exist or are explicitly blocked/deferred with rationale:

- `SourceId` exists.
- `DecisionRecordId` exists.
- `FindingsRecordId` exists where applicable.
- `FindingClassificationId` exists where applicable.
- `IngestionBackfillDecisionId` exists where applicable.
- `CurrentTruthPromotionId` exists where current truth answer use is requested.
- Source provenance exists.
- Cross-check status is recorded.
- Conflict status is resolved or explicitly caveated.
- Supersession status is resolved.
- Answer scope is defined.
- Citation/provenance requirement is defined.
- Revocation/removal path is defined.
- Retrieval gating has not yet been enabled in this slice.

## 5. Current-Truth Dependency

Current-truth promotion does not automatically permit answer use.

Answer-use approval for current truth requires `CurrentTruthPermitted` Yes and separate `AnswerUsePermitted` Yes.

Historical context answer use may be permitted separately from current-truth answer use.

An answer-use decision must not override newer repository truth.

## 6. Ingestion / Backfill Dependency

Ingested/backfilled evidence does not automatically permit answer use.

Metadata-only historical records are not answerable unless explicitly approved for historical context.

Answer-use permission must record whether the evidence is historical context, current truth, caveated answer material, or not answerable.

## 7. Evidence Scope Rules

| EvidenceScope | Meaning |
| --- | --- |
| `HISTORICAL_CONTEXT_ONLY` | May be used only to explain historical context when separately approved. |
| `CURRENT_TRUTH` | May be used as current truth only with current-truth approval and answer-use approval. |
| `CURRENT_TRUTH_WITH_CAVEAT` | May be used as current truth only with required caveats preserved. |
| `BACKLOG_CONTEXT_ONLY` | May explain backlog or planned work only, not implemented current state. |
| `PLATFORM_DOCTRINE_CONTEXT` | May explain platform doctrine only within approved repository/domain scope. |
| `HARDENING_REQUIREMENT_CONTEXT` | May explain hardening requirements only within approved scope. |
| `DEVELOPER_LOG_CONTEXT` | May explain developer-log rationale only as historical/log context. |
| `NOT_ANSWERABLE` | Must not be used in answers. |
| `SUPERSEDED_NOT_ANSWERABLE` | Must not answer current-state questions. |
| `CONFLICTED_NOT_ANSWERABLE` | Must not answer as settled truth. |

## 8. Answer Scope Rules

Answer use must be scoped by repository/domain context.

Answer use must distinguish historical explanation from current operating truth.

Answer use must preserve caveats where required.

Answer use must not silently mix historical and current truth.

Answer use must not allow superseded evidence to answer current-state questions.

Answer use must not allow conflicting evidence to answer current-state questions unless explicitly caveated and approved.

## 9. Citation / Provenance Requirements

Every answer-use permission record must preserve:

- `SourceId`
- `SourceTitle`
- `SourceDate` or unknown-date marker
- `RepositoryContext`
- `DomainContext`
- `DecisionRecordId`
- `CurrentTruthPromotionId` where applicable
- `AnswerUsePermissionId`
- `EvidenceScope`
- `AnswerScope`
- `Reviewer/Approver`
- `ApprovedAtUtc`
- `RevocationPath`
- `Notes`

## 10. Conflict / Supersession Handling

Conflicted evidence defaults to not answerable.

Superseded evidence defaults to not answerable for current-state questions.

Historical explanation use may be allowed only if labelled historical and not current truth.

Conflict or supersession caveats must be carried into any future answer contract.

## 11. Refusal / Insufficient Evidence Boundary

If answer-use permission is absent, Minerva must refuse or state insufficient governed evidence.

If answer-use permission is blocked, Minerva must refuse or state that evidence is not answer-approved.

If evidence is historical-only, Minerva must not present it as current truth.

If evidence is conflicted, Minerva must not answer as settled truth.

## 12. Retrieval Boundary

This slice does not implement retrieval filtering.

Future retrieval gating must consume answer-use permission status.

Future retrieval gating must exclude not-answerable, blocked, superseded, and conflicted evidence from current-truth answer mode.

Future retrieval gating must preserve historical-context-only evidence for historical-context answer mode only.

Answer-use permission flows into retrieval eligibility and does not itself implement retrieval.

Answer-use permission does not make evidence retrieval eligible until a separate retrieval eligibility gate approves the requested retrieval mode.

Future retrieval eligibility is governed by `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md`.

## 13. Chat Exposure Boundary

This slice does not expose Minerva chat.

This slice does not change answer synthesis.

This slice does not call a live LLM.

Chat exposure requires a later chat answer contract and pilot-readiness gate.

## 14. Blocker Handling

Blocked decisions must record one or more blocker codes and the required resolution path:

- `MISSING_SOURCE_ID`
- `MISSING_DECISION_RECORD`
- `MISSING_FINDINGS_RECORD`
- `MISSING_CLASSIFICATION`
- `MISSING_INGESTION_BACKFILL_DECISION`
- `MISSING_CURRENT_TRUTH_PROMOTION`
- `CURRENT_TRUTH_NOT_APPROVED`
- `PROVENANCE_INCOMPLETE`
- `CROSS_CHECK_INCOMPLETE`
- `CONFLICT_UNRESOLVED`
- `SUPERSESSION_UNRESOLVED`
- `ANSWER_SCOPE_UNDEFINED`
- `CITATION_REQUIREMENT_UNDEFINED`
- `REVOCATION_PATH_MISSING`
- `RETRIEVAL_GATE_NOT_IMPLEMENTED`
- `CHAT_CONTRACT_NOT_IMPLEMENTED`

Resolving a blocker only permits reassessment of the answer-use decision. It does not enable retrieval, expose chat, call a live LLM, or make evidence answerable.

## 15. What Answer-Use Permission Gate Does Not Mean

Creating answer-use permission docs does not expose chat.

Answer-use gate does not expose chat.

Answer-use gate does not call a live LLM.

Answer-use gate does not change retrieval runtime.

Answer-use gate does not mutate corpus.

Answer-use gate does not ingest source content.

Answer-use gate does not promote current truth.

Answer-use gate does not write to a database.

Answer-use gate does not create endpoint or UI changes.

## 16. Developer Handoff

Future developers must use this gate after current-truth promotion control when current-truth answer use is requested, or after historical review/ingestion controls when historical-context answer use is requested.

Use `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_PERMISSION_TEMPLATE.md` for individual permission records, `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_BLOCKER_MODEL.md` for blockers, and `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_SCOPE_RULES.md` for evidence and answer scope interpretation.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no answer-use permission activation, and no runtime answer-use permission activation are introduced by this gate.
