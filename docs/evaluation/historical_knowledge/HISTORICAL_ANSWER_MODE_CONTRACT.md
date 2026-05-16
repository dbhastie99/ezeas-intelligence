# Historical Answer Mode Contract

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed answer-mode contract for Minerva historical knowledge.

The contract controls how future Minerva answers must distinguish current-truth answers, historical-context answers, caveated answers, backlog/follow-up context answers, doctrine/hardening context answers, developer-log context answers, and refusal or insufficient-evidence responses.

This slice is documentation/control/test hardening only.

## 2. Scope

This contract applies after historical source registration, review governance, decision records, findings classification, ingestion/backfill decision control, current-truth promotion control where applicable, answer-use permission gating, and retrieval eligibility gating.

Historical sources are not answerable current truth by default. Historical-context approval must not be treated as current-truth approval.

Minerva is not exposed for chat in this slice.

## 3. Answer Mode Status Model

| Status | Meaning |
| --- | --- |
| `ANSWER_MODE_NOT_REQUESTED` | No answer-mode decision has been requested. |
| `ANSWER_MODE_BLOCKED` | Answer-mode approval is blocked until recorded blockers are resolved and reassessed. |
| `ANSWER_MODE_DEFERRED` | Answer-mode decision is intentionally postponed; conservative defaults remain in force. |
| `ANSWER_MODE_REJECTED` | Requested answer mode is rejected under current controls. |
| `ANSWER_MODE_APPROVED_CURRENT_TRUTH` | Current-truth answer mode is approved only within recorded scope. |
| `ANSWER_MODE_APPROVED_HISTORICAL_CONTEXT` | Historical-context answer mode is approved only with visible historical labelling. |
| `ANSWER_MODE_APPROVED_WITH_CAVEAT` | Caveated answer mode is approved only with required caveat preserved visibly. |
| `ANSWER_MODE_APPROVED_BACKLOG_CONTEXT` | Backlog or follow-up context answer mode is approved only for planned/deferred context. |
| `ANSWER_MODE_APPROVED_DOCTRINE_CONTEXT` | Doctrine or hardening context answer mode is approved only within recorded governing scope. |
| `ANSWER_MODE_REFUSE_INSUFFICIENT_GOVERNED_EVIDENCE` | Future answer must refuse or state insufficient governed evidence. |
| `ANSWER_MODE_REFUSE_NOT_ANSWER_APPROVED` | Future answer must refuse because evidence is not answer-use approved. |
| `ANSWER_MODE_REFUSE_CONFLICTED` | Future answer must refuse settled truth because evidence remains conflicted. |
| `ANSWER_MODE_REFUSE_SUPERSEDED` | Future answer must refuse current-truth use because evidence is superseded. |
| `ANSWER_MODE_REVOKED` | Prior answer-mode approval has been revoked and must not be used. |

## 4. Answer Modes

| AnswerMode | Required treatment |
| --- | --- |
| `CURRENT_TRUTH_ANSWER` | Use only governed current-truth evidence with answer-use permission, retrieval eligibility, provenance, and citations. |
| `HISTORICAL_CONTEXT_ANSWER` | Label answer as historical context and do not present it as current operating truth. |
| `CAVEATED_CURRENT_TRUTH_ANSWER` | Preserve visible caveat explaining uncertainty, conflict, scope, or historical limitation. |
| `BACKLOG_CONTEXT_ANSWER` | Explain planned, deferred, blocked, or follow-up work only as non-implemented context unless separately supported. |
| `DOCTRINE_CONTEXT_ANSWER` | Explain governing doctrine within approved repository/domain scope. |
| `HARDENING_CONTEXT_ANSWER` | Explain hardening principles or requirements without treating them as runtime implementation evidence. |
| `DEVELOPER_LOG_CONTEXT_ANSWER` | Explain developer-log rationale as historical/log context, not standalone current truth. |
| `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE` | Refuse or state insufficient governed evidence. |
| `REFUSAL_NOT_ANSWER_APPROVED` | Refuse because answer-use permission is missing, blocked, rejected, revoked, or superseded. |
| `REFUSAL_CONFLICTED_EVIDENCE` | Refuse settled answer because evidence is conflicted and no caveated mode is approved. |
| `REFUSAL_SUPERSEDED_EVIDENCE` | Refuse current-truth answer because evidence is superseded. |
| `REFUSAL_RETRIEVAL_NOT_ELIGIBLE` | Refuse because retrieval eligibility is missing, blocked, revoked, superseded, conflicted, or excluded. |

## 5. Preconditions Before Answer Mode Can Be Used

Answer mode must not be used unless all required controls exist or the response maps to a refusal/insufficient-evidence mode:

- `RetrievalEligibilityId` exists.
- `RetrievalEligibilityStatus` is recorded.
- `AnswerUsePermissionId` exists.
- `AnswerUsePermissionStatus` is recorded.
- `EvidenceScope` is recorded.
- `AnswerScope` is recorded.
- `RetrievalMode` is recorded.
- Source provenance exists.
- Citation requirement is defined.
- Conflict status is resolved or explicitly caveated.
- Supersession status is resolved.
- `CurrentTruthPermitted` is Yes where current-truth answer is requested.
- `RetrievalEligible` is Yes for non-refusal answer modes.
- `ChatEligible` is not enabled in this slice.

## 6. Retrieval Eligibility Dependency

Answer mode selection depends on retrieval eligibility.

Retrieval eligibility alone does not implement answer synthesis.

Absent, blocked, revoked, superseded, conflicted, or excluded retrieval eligibility must map to refusal or insufficient-evidence answer modes.

## 7. Answer-Use Permission Dependency

Answer-use permission is required before non-refusal answer modes can be approved.

Blocked, revoked, superseded, rejected, or missing answer-use permission must map to refusal.

Historical-context approval must not be treated as current-truth approval.

## 8. Current-Truth Answer Rules

Current-truth answers require current-truth promotion, answer-use permission, retrieval eligibility, provenance, and citation support.

Current-truth answers must not rely on historical-only, superseded, conflicted, or not-answerable evidence.

Current-truth answers must not override newer repository truth.

## 9. Historical-Context Answer Rules

Historical-context answers must be labelled historical.

Historical-context answers must not be presented as current operating truth.

Historical-context answers may explain project history, rationale, or prior decisions only within approved scope.

## 10. Caveated Answer Rules

Caveated answers must carry caveat into the response.

Caveated answers must explain uncertainty, conflict, scope, or historical limitation.

Caveated answers must not present unresolved evidence as settled truth.

## 11. Backlog / Follow-Up Context Rules

Backlog/follow-up evidence may explain planned or deferred work.

Backlog/follow-up evidence must not be represented as implemented behaviour.

Future answer contract must distinguish planned, deferred, blocked, and implemented states.

## 12. Doctrine / Hardening Context Rules

Doctrine/hardening context may be used to explain governing principles where answer-use and retrieval eligibility allow it.

Doctrine/hardening context must not be treated as runtime implementation evidence unless separately supported.

## 13. Refusal / Insufficient Evidence Rules

If answer-use permission is absent, answer mode must refuse or say insufficient governed evidence.

If retrieval eligibility is absent, answer mode must refuse or say insufficient governed evidence.

If evidence is superseded, answer mode must refuse current-truth answer.

If evidence is conflicted, answer mode must refuse settled answer unless a caveated mode is explicitly approved.

If citation/provenance is missing, answer mode must refuse chat-answer readiness.

## 14. Citation / Provenance Requirements

Every answer-mode record must preserve:

- `SourceId`
- `SourceTitle`
- `SourceDate` or unknown-date marker
- `RepositoryContext`
- `DomainContext`
- `AnswerUsePermissionId`
- `RetrievalEligibilityId`
- `AnswerModeId`
- `EvidenceScope`
- `RetrievalMode`
- `AnswerMode`
- `CitationRequired`
- `CaveatRequired`
- `ProvenanceStatus`
- `Reviewer/Approver`
- `ApprovedAtUtc`
- `RevocationPath`
- `Notes`

Answer modes require the citation/provenance answer contract before chat readiness.

The governing citation/provenance answer contract is `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_ANSWER_CONTRACT.md`.

The required source-to-answer evidence chain is `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_EVIDENCE_CHAIN_REQUIREMENTS.md`.

An approved answer mode does not by itself make an answer chat-ready. Future chat readiness requires governed citation/provenance, refusal handling, retrieval enforcement, and pilot-readiness approval.

## 15. Conflict / Supersession Handling

Conflicted evidence defaults to refusal for settled/current-truth answers.

Superseded evidence defaults to refusal for current-truth answers.

Caveated answer use requires explicit approval and visible caveat.

Historical explanation use must label superseded/conflicted evidence appropriately.

## 16. Runtime Boundary

This slice does not implement answer synthesis runtime.

This slice does not implement retrieval filtering.

This slice does not activate answer modes at runtime.

This slice does not mutate corpus or evidence stores.

This slice does not call a live LLM.

## 17. Chat Exposure Boundary

This slice does not expose Minerva chat.

Chat exposure requires later pilot readiness gate.

Chat exposure requires runtime retrieval gating, answer-mode enforcement, citation/provenance enforcement, and refusal behaviour tests.

Answer modes must be runtime-enforced before chat exposure.

Approved answer-mode controls are planning inputs only until a later runtime gate implementation design and pilot readiness approval exist.

## 18. Chat Pilot Readiness Prerequisite

Answer modes are prerequisite to chat pilot readiness.

Chat pilot readiness must not be approved unless current-truth, historical-context, caveated, backlog/context, doctrine/context, and refusal answer treatments are governed and linked to citation/provenance requirements.

This prerequisite does not implement answer synthesis runtime, retrieval runtime, live LLM calls, endpoint/UI, or chat exposure.

## 19. Blocker Handling

Blocked decisions must record one or more blocker codes and the required resolution path:

- `MISSING_RETRIEVAL_ELIGIBILITY`
- `RETRIEVAL_NOT_ELIGIBLE`
- `MISSING_ANSWER_USE_PERMISSION`
- `ANSWER_USE_NOT_APPROVED`
- `MISSING_CURRENT_TRUTH_PROMOTION`
- `CURRENT_TRUTH_NOT_APPROVED`
- `PROVENANCE_INCOMPLETE`
- `CITATION_REQUIREMENT_UNDEFINED`
- `CONFLICT_UNRESOLVED`
- `SUPERSESSION_UNRESOLVED`
- `CAVEAT_REQUIRED_NOT_DEFINED`
- `ANSWER_SCOPE_UNDEFINED`
- `ANSWER_MODE_UNDEFINED`
- `CHAT_ELIGIBILITY_NOT_APPROVED`
- `RUNTIME_RETRIEVAL_NOT_IMPLEMENTED`
- `ANSWER_SYNTHESIS_GATE_NOT_IMPLEMENTED`
- `CHAT_CONTRACT_NOT_IMPLEMENTED`

Resolving a blocker only permits reassessment of the answer-mode decision. It does not enable retrieval runtime, answer synthesis runtime, chat, live LLM calls, or answerability.

## 20. What Answer Mode Contract Does Not Mean

Creating answer-mode docs does not expose chat.

Answer-mode contract does not call a live LLM.

Answer-mode contract does not change retrieval runtime.

Answer-mode contract does not change answer synthesis runtime.

Answer-mode contract does not mutate corpus.

Answer-mode contract does not ingest source content.

Answer-mode contract does not promote current truth.

Answer-mode contract does not activate answer use at runtime.

Answer-mode contract does not write to a database.

Answer-mode contract does not create endpoint or UI changes.

Answer-mode contract does not create endpoint changes.

Answer-mode contract does not create UI changes.

## 21. Developer Handoff

Future developers must use this contract after answer-use permission and retrieval eligibility are recorded and before any answer synthesis runtime, citation/provenance answer contract, refusal policy hardening, pilot-readiness gate, or chat exposure.

Use `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_TEMPLATE.md` for individual answer-mode records, `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_REFUSAL_POLICY.md` for refusal behaviour, `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_BLOCKER_MODEL.md` for blockers, and `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_CITATION_REQUIREMENTS.md` for citation/provenance requirements.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no answer synthesis runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, and no runtime retrieval eligibility activation are introduced by this contract.
