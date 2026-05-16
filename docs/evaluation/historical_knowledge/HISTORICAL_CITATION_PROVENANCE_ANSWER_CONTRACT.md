# Historical Citation / Provenance Answer Contract

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed citation/provenance answer contract for Minerva historical knowledge.

The contract controls what provenance must be attached to future Minerva answers before any chat exposure can be considered.

This slice is documentation/control/test hardening only.

## 2. Scope

This contract applies after source registration, review governance, decision records, findings classification, ingestion/backfill decision control where applicable, current-truth promotion control where applicable, answer-use permission gating, retrieval eligibility gating, and answer-mode contract control.

Historical sources are not answerable current truth by default. Answer-use permission does not automatically implement retrieval. Retrieval eligibility does not automatically expose chat. Answer-mode contract does not implement answer synthesis runtime.

Minerva is not exposed for chat in this slice.

## 3. Citation / Provenance Status Model

| Status | Meaning |
| --- | --- |
| `CITATION_NOT_REQUESTED` | No citation/provenance decision has been requested. |
| `CITATION_BLOCKED` | Citation/provenance approval is blocked until recorded blockers are resolved and reassessed. |
| `CITATION_DEFERRED` | Citation/provenance decision is intentionally postponed; conservative defaults remain in force. |
| `CITATION_REQUIRED` | Citation/provenance is required before non-refusal answer readiness. |
| `CITATION_READY_CURRENT_TRUTH` | Citation/provenance is ready for current-truth answers within approved scope. |
| `CITATION_READY_HISTORICAL_CONTEXT` | Citation/provenance is ready for labelled historical-context answers. |
| `CITATION_READY_WITH_CAVEAT` | Citation/provenance is ready only with visible caveat preserved. |
| `CITATION_READY_BACKLOG_CONTEXT` | Citation/provenance is ready only for backlog or follow-up context. |
| `CITATION_READY_DOCTRINE_CONTEXT` | Citation/provenance is ready only for doctrine or hardening context. |
| `CITATION_MISSING_REFUSE` | Missing citation/provenance requires refusal or insufficient governed evidence. |
| `CITATION_INCOMPLETE_REFUSE` | Incomplete citation/provenance requires refusal or insufficient governed evidence. |
| `CITATION_REVOKED` | Prior citation/provenance readiness has been revoked and must not be used. |
| `CITATION_SUPERSEDED` | Prior citation/provenance readiness has been superseded and must not support current truth. |

## 4. Provenance Requirements by Answer Mode

| AnswerMode | Required provenance |
| --- | --- |
| `CURRENT_TRUTH_ANSWER` | Requires current-truth promotion id, answer-use permission id, retrieval eligibility id, answer mode id, source id, source title, source date or unknown marker, repository context, domain context, citation, provenance status, and revocation path. |
| `HISTORICAL_CONTEXT_ANSWER` | Requires historical label, source provenance, answer-use permission id, retrieval eligibility id, answer mode id, evidence scope, and caveat where applicable. |
| `CAVEATED_CURRENT_TRUTH_ANSWER` | Requires visible caveat, caveat rationale, source provenance, and answer-use/retrieval eligibility references. |
| `BACKLOG_CONTEXT_ANSWER` | Requires backlog/follow-up label and must not present planned work as implemented. |
| `DOCTRINE_CONTEXT_ANSWER` | Requires doctrine source references and must not present doctrine as runtime implementation evidence. |
| `HARDENING_CONTEXT_ANSWER` | Requires hardening source references and must not present hardening doctrine as runtime implementation evidence. |
| `DEVELOPER_LOG_CONTEXT_ANSWER` | Requires developer-log source references and historical/log labelling. |
| Refusal modes | Require refusal reason and missing/blocked provenance explanation where applicable. |

## 5. Evidence Chain Requirements

Every citation/provenance record must preserve the complete evidence chain:

- `SourceId`
- `SourceTitle`
- `SourceDate` or unknown-date marker
- `RepositoryContext`
- `DomainContext`
- `DecisionRecordId` where applicable
- `FindingsRecordId` where applicable
- `FindingClassificationId` where applicable
- `IngestionBackfillDecisionId` where applicable
- `CurrentTruthPromotionId` where applicable
- `AnswerUsePermissionId`
- `RetrievalEligibilityId`
- `AnswerModeId`
- `EvidenceScope`
- `AnswerScope`
- `RetrievalMode`
- `AnswerMode`
- `CitationRequired`
- `CaveatRequired`
- `ProvenanceStatus`
- `ConflictStatus`
- `SupersessionStatus`
- `Reviewer/Approver`
- `ApprovedAtUtc`
- `RevocationPath`
- `Notes`

## 6. Current-Truth Citation Rules

Current-truth answers must cite current-truth-approved evidence.

Current-truth answers must not cite historical-only evidence as current truth.

Current-truth answers must not cite superseded/conflicted evidence as settled truth.

Current-truth citation must preserve repository/domain context.

## 7. Historical-Context Citation Rules

Historical-context answers must identify evidence as historical.

Historical-context citation must not imply current operating truth.

Historical context must include source date or unknown-date marker.

## 8. Caveated Answer Citation Rules

Caveated answers must cite the caveat basis.

Caveated answers must expose conflict, limitation, uncertainty, or scope boundary.

Caveat must be visible in future answer contract.

## 9. Backlog / Follow-Up Citation Rules

Backlog/follow-up answers must cite backlog/follow-up provenance.

Backlog/follow-up citation must not present planned work as implemented.

Backlog/follow-up citation must preserve whether work is planned, deferred, blocked, or not yet verified.

## 10. Doctrine / Hardening Citation Rules

Doctrine/context answers must cite doctrine source references.

Hardening/context answers must cite hardening source references.

Doctrine and hardening citations must not present doctrine as runtime implementation evidence.

## 11. Refusal Citation Rules

Refusal may cite absence of governed evidence, missing answer-use permission, missing retrieval eligibility, missing provenance, conflict, or supersession.

Refusal must not fabricate citations.

Refusal should explain which gate is missing where known.

## 12. Missing / Incomplete Provenance Handling

Missing `SourceId` blocks non-refusal answers.

Missing citation requirement blocks chat-answer readiness.

Incomplete provenance maps to refusal or insufficient governed evidence.

Unknown source date must be visibly marked and may require caveat or refusal depending on answer mode.

## 13. Conflict / Supersession Handling

Superseded evidence must not support current-truth answers.

Conflicted evidence must not support settled answers.

Caveated answer use requires explicit caveat and answer-use/retrieval eligibility approval.

## 14. Runtime Boundary

This slice does not implement citation rendering.

This slice does not implement answer synthesis runtime.

This slice does not implement retrieval filtering.

This slice does not activate answer modes at runtime.

This slice does not mutate corpus or evidence stores.

This slice does not call a live LLM.

## 15. Chat Exposure Boundary

This slice does not expose Minerva chat.

Chat exposure requires later pilot readiness gate.

Chat exposure requires runtime enforcement of citation/provenance, answer-mode, refusal, and retrieval gates.

## 16. Runtime Gate Plan Flow

Citation/provenance must flow into the runtime gate plan before chat readiness.

The governing runtime gate plan is `docs/evaluation/historical_knowledge/HISTORICAL_RUNTIME_RETRIEVAL_ANSWER_SYNTHESIS_GATE_PLAN.md`.

Citation/provenance readiness is an input to runtime retrieval and answer synthesis gate planning only. It does not render citations at runtime, implement retrieval filtering, implement answer synthesis, permit live LLM calls, or expose chat.

## 17. Blocker Handling

Blocked decisions must record one or more blocker codes and the required resolution path:

- `MISSING_SOURCE_ID`
- `MISSING_SOURCE_TITLE`
- `MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER`
- `MISSING_REPOSITORY_CONTEXT`
- `MISSING_DOMAIN_CONTEXT`
- `MISSING_ANSWER_USE_PERMISSION`
- `MISSING_RETRIEVAL_ELIGIBILITY`
- `MISSING_ANSWER_MODE`
- `MISSING_CURRENT_TRUTH_PROMOTION`
- `PROVENANCE_INCOMPLETE`
- `CITATION_REQUIREMENT_UNDEFINED`
- `CAVEAT_REQUIRED_NOT_DEFINED`
- `CONFLICT_UNRESOLVED`
- `SUPERSESSION_UNRESOLVED`
- `REVOCATION_PATH_MISSING`
- `CITATION_RENDERING_NOT_IMPLEMENTED`
- `CHAT_CONTRACT_NOT_IMPLEMENTED`

Resolving a blocker only permits reassessment of citation/provenance readiness. It does not enable retrieval runtime, citation rendering, answer synthesis runtime, chat, live LLM calls, or answerability.

## 18. What Citation / Provenance Contract Does Not Mean

Creating citation/provenance docs does not expose chat.

Citation/provenance contract does not call a live LLM.

Citation/provenance contract does not change retrieval runtime.

Citation/provenance contract does not change answer synthesis runtime.

Citation/provenance contract does not render citations at runtime.

Citation/provenance contract does not mutate corpus.

Citation/provenance contract does not ingest source content.

Citation/provenance contract does not promote current truth.

Citation/provenance contract does not activate answer use at runtime.

Citation/provenance contract does not write to a database.

Citation/provenance contract does not create endpoint or UI changes.

Citation/provenance contract does not create endpoint changes.

Citation/provenance contract does not create UI changes.

## 19. Developer Handoff

Future developers must use this contract after answer-use permission, retrieval eligibility, and answer mode are recorded and before any answer synthesis runtime, citation rendering runtime, pilot-readiness gate, or chat exposure.

Use `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_TEMPLATE.md` for individual citation/provenance records, `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_BLOCKER_MODEL.md` for blockers, `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_REFUSAL_RULES.md` for refusal behaviour, and `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_EVIDENCE_CHAIN_REQUIREMENTS.md` for source-to-answer evidence chain requirements.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no answer synthesis runtime changes, no citation rendering runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, and no runtime retrieval eligibility activation are introduced by this contract.
