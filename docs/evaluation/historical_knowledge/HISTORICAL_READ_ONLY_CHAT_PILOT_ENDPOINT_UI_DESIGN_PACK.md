# Historical Read-Only Chat Pilot Endpoint/UI Design Pack

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the Minerva historical read-only chat pilot endpoint/UI design pack. It describes a future internal-only, read-only pilot endpoint/UI shape without creating endpoint, route, controller, API handler, UI, chat exposure, live LLM, final answer generation, live retrieval, DB, corpus, ingestion, or cross-repo runtime code.

## 2. Scope

Scope is limited to endpoint/UI design documentation, control state, and static tests. The design covers request/response envelopes, operator-facing status display, refusal/citation visibility, access-control expectations, audit/logging expectations, and remaining runtime boundaries.

## 3. Current Status

- EndpointUiDesignStatus: DESIGN_DRAFTED_NOT_IMPLEMENTED
- EndpointCreatedThisSlice: No
- RouteCreatedThisSlice: No
- UICreatedThisSlice: No
- ChatExposedThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_GATE.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_ENTRY_CRITERIA.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_BOUNDARY_RULES.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CLOSEOUT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE.md`

## 5. Endpoint/UI Design Status Model

- `ENDPOINT_UI_DESIGN_NOT_STARTED`
- `ENDPOINT_UI_DESIGN_DRAFTED`
- `ENDPOINT_UI_DESIGN_BLOCKED`
- `ENDPOINT_UI_DESIGN_DEFERRED`
- `ENDPOINT_UI_DESIGN_READY_FOR_IMPLEMENTATION_GATE`
- `ENDPOINT_UI_DESIGN_REQUIRES_ACCESS_CONTROL_REVIEW`
- `ENDPOINT_UI_DESIGN_REQUIRES_AUDIT_LOGGING_REVIEW`
- `ENDPOINT_UI_DESIGN_REQUIRES_LLM_POLICY_REVIEW`
- `ENDPOINT_UI_DESIGN_REJECTED`
- `ENDPOINT_UI_DESIGN_SUPERSEDED`

## 6. Proposed Endpoint Design Summary

- future endpoint must be internal-only;
- future endpoint must be read-only;
- future endpoint must accept metadata/envelope input only at first;
- future endpoint must call the in-memory orchestrator candidate only unless later approved;
- future endpoint must not call live LLM unless later explicitly approved;
- future endpoint must not connect to DB or live retrieval backend unless later explicitly approved.

## 7. Proposed UI Surface Design Summary

- future UI must display envelope/status output, not pretend to be production chat;
- future UI must show refusal reason visibly;
- future UI must show citation readiness visibly;
- future UI must show caveat requirement visibly;
- future UI must show blocked gate status visibly;
- future UI must not silently convert historical evidence into current truth.

## 8. Request Envelope Design

- `RequestId`
- `OperatorContext`
- `SourceId`
- `EvidenceScope`
- `AnswerUsePermissionStatus`
- `RetrievalEligibilityStatus`
- `AnswerMode`
- `CitationStatus`
- `ProvenanceStatus`
- `ConflictStatus`
- `SupersessionStatus`
- `CurrentTruthPermitted`
- `RetrievalEligible`
- `ChatEligible`
- `CitationRequired`
- `CaveatRequired`
- `Notes`

## 9. Response Envelope Design

- `RequestId`
- `PilotResponseStatus`
- `PilotResponseMode`
- `RefusalRequired`
- `RefusalReason`
- `CitationReady`
- `CaveatRequired`
- `Guardrails`
- `NonGoals`
- `Explanation`
- `RuntimeBoundaryAsserted`
- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposed`
- `EndpointUIPresent`
- `LiveRetrievalPerformed`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`

## 10. Refusal / Citation Visibility Requirements

- refusal must never be hidden;
- missing answer-use permission must be visible;
- missing retrieval eligibility must be visible;
- missing citation/provenance must be visible;
- conflict/supersession blockers must be visible;
- citation readiness must be visible;
- caveat requirement must be visible.

## 11. Access Control Requirements

- internal-only pilot;
- operator/developer-only initially;
- no public access;
- no tenant/customer production access;
- access control decision before implementation;
- audit context captured where available.

## 12. Audit / Logging Requirements

- `RequestId`
- `OperatorContext`
- `Timestamp`
- `PilotResponseStatus`
- `PilotResponseMode`
- `RefusalReason`
- `CitationReady`
- `CaveatRequired`
- `RuntimeBoundaryAsserted`
- no-runtime flags
- `Notes`

## 13. Runtime Boundary Confirmation

- EndpointCreationPermitted: No
- RouteCreationPermitted: No
- UICreationPermitted: No
- ChatExposurePermitted: No
- LiveLLMCallPermitted: No
- FinalAnswerGenerationPermitted: No
- LiveRetrievalPermitted: No
- CorpusMutationPermitted: No
- DatabaseReadPermitted: No
- DatabaseWritePermitted: No
- SchemaMigrationPermitted: No

## 14. Stop Conditions

- endpoint creation required;
- route/controller/API handler required;
- UI creation required;
- chat exposure required;
- live LLM call required;
- final answer generation required;
- live retrieval required;
- corpus query required;
- corpus mutation required;
- DB read/write required;
- public access required;
- access control unresolved;
- audit/logging unresolved;
- refusal visibility unresolved;
- citation visibility unresolved.

## 15. What This Design Pack Authorises

- a future endpoint/UI implementation gate may be considered.
- any future endpoint/UI creation must be separately approved.

## 16. What This Design Pack Does Not Authorise

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

## 17. Recommended Next Slice

Preferred next Minerva slice should be historical read-only chat pilot endpoint/UI implementation gate v0.1. That future slice should decide whether a minimal endpoint/UI implementation candidate may be considered. That future slice must still not create endpoint/UI unless explicitly approved.

## 18. Progress After This Slice

Minerva has moved from endpoint/UI planning gate into endpoint/UI design. Minerva remains pre-chat-exposure. Endpoint/UI/live LLM/final answer generation remain separate future decisions.

## 19. Developer Handoff

Use this design pack as a control artefact only. Do not create routes, endpoints, UI, chat exposure, live LLM calls, final natural-language answer generation, live retrieval backend, vector search, corpus query, DB read/write, corpus mutation, source ingestion, Code Evidence ingestion, schema migrations, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes without a separate explicit approval slice.
