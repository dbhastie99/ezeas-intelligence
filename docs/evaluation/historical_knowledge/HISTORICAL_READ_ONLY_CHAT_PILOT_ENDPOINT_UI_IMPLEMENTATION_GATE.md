# Historical Read-Only Chat Pilot Endpoint/UI Implementation Gate

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the Minerva historical read-only chat pilot endpoint/UI implementation gate. It decides whether a future minimal endpoint/UI implementation candidate may be considered, based on endpoint/UI design, endpoint contract design, UI surface design, access-control design, audit/logging design, implementation entry criteria, and runtime boundaries.

## 2. Scope

Scope is limited to implementation readiness control. This slice creates documentation and tests only. It does not create endpoint, route, controller, API handler, frontend component, chat exposure, live LLM integration, final answer generation, live retrieval backend, database access, corpus mutation, source ingestion, Code Evidence ingestion, schema migration, production deployment, or cross-repo change.

## 3. Current Status

- EndpointUiImplementationGateStatus: IMPLEMENTATION_GATE_DRAFTED
- EndpointCreatedThisSlice: No
- RouteCreatedThisSlice: No
- APIHandlerCreatedThisSlice: No
- UICreatedThisSlice: No
- ChatExposedThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_DESIGN_PACK.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_CONTRACT_DESIGN.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_UI_SURFACE_DESIGN.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ACCESS_CONTROL_DESIGN.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_AUDIT_LOGGING_DESIGN.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_ENTRY_CRITERIA.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_BOUNDARY_RULES.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`

## 5. Endpoint/UI Implementation Gate Status Model

- `ENDPOINT_UI_IMPLEMENTATION_GATE_NOT_STARTED`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_DRAFTED`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_BLOCKED`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_DEFERRED`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_READY_FOR_MINIMAL_IMPLEMENTATION_CANDIDATE`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_REQUIRES_ACCESS_CONTROL_REVIEW`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_REQUIRES_AUDIT_LOGGING_REVIEW`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_REQUIRES_LLM_POLICY_REVIEW`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_REJECTED`
- `ENDPOINT_UI_IMPLEMENTATION_GATE_SUPERSEDED`

## 6. Implementation Preconditions

- endpoint/UI design pack complete;
- endpoint contract design complete;
- UI surface design complete;
- access-control design complete;
- audit/logging design complete;
- implementation entry criteria complete;
- refusal/citation visibility rules complete;
- orchestrator response contract complete;
- no endpoint exists yet;
- no UI exists yet;
- no live LLM approved;
- no final answer generation approved;
- no live retrieval backend;
- no DB read/write;
- no corpus mutation.

## 7. Endpoint Implementation Boundary

- this slice does not create an endpoint;
- this slice does not create a route/controller/API handler;
- future implementation candidate may only be minimal/internal/read-only if separately approved;
- endpoint must consume orchestrator envelope only unless later approved.

## 8. UI Implementation Boundary

- this slice does not create UI;
- future UI candidate may only display status/envelope output unless later approved;
- UI must visibly surface refusal, citation readiness, caveat, blocked gates, and no-runtime flags.

## 9. Chat Exposure Boundary

- this slice does not expose chat;
- future implementation candidate does not equal production chat;
- public/customer access remains prohibited unless separately approved.

## 10. Live LLM Boundary

- no live LLM is called;
- future endpoint/UI candidate must not call LLM unless separate LLM policy gate approves it.

## 11. Final Answer Boundary

- no final natural-language answer is generated;
- future implementation candidate remains envelope/status-first unless separately approved.

## 12. Retrieval / Corpus / DB Boundary

- no live retrieval backend;
- no corpus query;
- no corpus mutation;
- no DB reads;
- no DB writes;
- no Code Evidence ingestion.

## 13. Access Control Readiness

- access control design exists;
- future candidate must be internal-only/operator-developer first;
- no public or production tenant/customer access is approved.

## 14. Audit / Logging Readiness

- audit/logging design exists;
- future implementation must preserve request id, operator context, response status, refusal reason, citation readiness, caveat flag, runtime boundary, and timestamp where available;
- this slice does not implement runtime logging.

## 15. Stop Conditions

- endpoint creation required in this slice;
- route/controller/API handler creation required in this slice;
- UI creation required in this slice;
- chat exposure required in this slice;
- live LLM call required;
- final answer generation required;
- live retrieval required;
- corpus query required;
- corpus mutation required;
- DB read/write required;
- public/customer access required;
- access control unresolved;
- audit/logging unresolved;
- refusal visibility unresolved;
- citation visibility unresolved.

## 16. What This Gate Authorises

- a future minimal endpoint/UI implementation candidate may be considered if gate records ready.
- any future endpoint/UI creation must be separately approved and remain internal/read-only unless later expanded.

## 17. What This Gate Does Not Authorise

- endpoint creation
- route/controller/API handler creation
- UI creation
- chat exposure
- live LLM calls
- final natural-language answer generation
- live retrieval backend
- corpus/vector search
- corpus mutation
- source ingestion
- Code Evidence ingestion
- DB reads
- DB writes
- schema migrations
- production deployment
- workforce-platform changes
- award-configurator-v1 changes
- ezeas-analytics changes

## 18. Recommended Next Slice

Preferred next Minerva slice should be historical read-only chat pilot minimal endpoint/UI implementation candidate v0.1 if this gate records ready. That future slice should be minimal/internal/read-only/envelope-only. That future slice must still not call live LLM or generate final natural-language answers unless explicitly approved. If blockers exist, next slice should remediate blockers.

## 19. Progress After This Slice

Minerva has moved from endpoint/UI design into endpoint/UI implementation gate. Minerva remains pre-chat-exposure. Endpoint/UI/live LLM/final answer generation remain separate future decisions.

## 19A. Minimal Candidate Follow-On

`HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_IMPLEMENTATION_CANDIDATE.md` records the approved follow-on candidate implementation slice. That slice creates an internal metadata/envelope candidate service only. EndpointCreatedThisSlice: No. RouteRegisteredGlobally: No. UICreatedThisSlice: No. ChatExposedThisSlice: No. The candidate remains no live LLM, no final answer generation, no live retrieval, no DB read/write, no corpus mutation, no source ingestion, and no production chat/public/tenant/customer exposure.

## 20. Developer Handoff

Use this gate as a control artefact only. Do not create routes, endpoints, controllers, API handlers, UI, chat exposure, live LLM calls, final natural-language answer generation, live retrieval backend, vector search, corpus query, DB read/write, corpus mutation, source ingestion, Code Evidence ingestion, schema migrations, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes without a separate explicit approval slice.

No source content ingestion. No operational corpus mutation. No Code Evidence ingestion. No live LLM calls. No database reads. No database writes. No schema migrations. No endpoint/UI creation. No live retrieval backend. No final natural-language answer generation. No chat exposure. No workforce-platform changes. No award-configurator-v1 changes. No ezeas-analytics changes. No current-truth promotion. No runtime answer-use permission activation. No runtime retrieval eligibility activation.
