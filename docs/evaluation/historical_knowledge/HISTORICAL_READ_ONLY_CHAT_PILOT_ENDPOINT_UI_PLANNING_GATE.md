# Historical Read-Only Chat Pilot Endpoint/UI Planning Gate

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document records the Minerva historical read-only chat pilot endpoint/UI planning gate. The gate decides what must be true before a future endpoint/UI design pack may be considered.

## 2. Scope

Scope is limited to planning-gate documentation, control state, and tests. This slice does not create endpoints, UI, chat routes, live LLM calls, final answer generation, live retrieval, corpus/vector search, corpus query, database access, source ingestion, Code Evidence ingestion, schema migrations, or cross-repo changes.

## 3. Current Status

- EndpointUiPlanningGateStatus: PLANNING_GATE_DRAFTED
- EndpointCreatedThisSlice: No
- UICreatedThisSlice: No
- ChatExposedThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CONTRACT_HARDENING.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_DECISION_CATALOG.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CLOSEOUT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_ENTRY_CRITERIA.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`

## 5. Endpoint/UI Planning Gate Status Model

- `ENDPOINT_UI_PLANNING_GATE_NOT_STARTED`
- `ENDPOINT_UI_PLANNING_GATE_DRAFTED`
- `ENDPOINT_UI_PLANNING_GATE_BLOCKED`
- `ENDPOINT_UI_PLANNING_GATE_DEFERRED`
- `ENDPOINT_UI_PLANNING_GATE_READY_FOR_ENDPOINT_UI_DESIGN_PACK`
- `ENDPOINT_UI_PLANNING_GATE_REQUIRES_ACCESS_CONTROL_REVIEW`
- `ENDPOINT_UI_PLANNING_GATE_REQUIRES_AUDIT_LOGGING_REVIEW`
- `ENDPOINT_UI_PLANNING_GATE_REQUIRES_LLM_POLICY_REVIEW`
- `ENDPOINT_UI_PLANNING_GATE_REJECTED`
- `ENDPOINT_UI_PLANNING_GATE_SUPERSEDED`

## 6. Planning Preconditions

- orchestrator contract hardening complete;
- orchestrator closeout complete;
- response contract complete;
- fixture catalog complete;
- guardrails complete;
- no-runtime assertions complete;
- endpoint/UI scope remains not implemented;
- live LLM remains not approved;
- final answer generation remains not approved;
- live retrieval backend remains not connected;
- DB read/write remains not approved;
- corpus mutation remains prohibited.

## 7. Endpoint Boundary

This slice does not create an endpoint. Future endpoint planning must remain internal/read-only first. A future endpoint must not expose public production chat without separate approval. A future endpoint must preserve no live LLM/no final answer boundaries unless later explicitly approved.

## 8. UI Boundary

This slice does not create UI. Future UI planning must be separate. UI must not imply production chat readiness. UI must surface refusal/gate status rather than hiding blocked evidence.

## 9. Chat Exposure Boundary

This slice does not expose chat. Any future chat exposure requires separate explicit implementation and approval. Pilot access must be internal and controlled.

## 10. Live LLM Boundary

No live LLM is called. LLM use remains unapproved. Any future LLM use requires separate policy/safety gate.

## 11. Final Answer Boundary

No final natural-language answer is generated. The orchestrator remains envelope/status only. Future final answer generation requires separate explicit approval.

## 12. Retrieval / Corpus / DB Boundary

- no live retrieval backend;
- no corpus query;
- no corpus mutation;
- no DB reads;
- no DB writes;
- no Code Evidence ingestion.

## 13. Safety / Access Control Requirements

- internal-only pilot;
- operator/developer-only access initially;
- refusal must remain visible;
- evidence/citation status must remain visible;
- no unapproved current-truth answers;
- blocked gates must be surfaced;
- no silent fallback to historical truth.

## 14. Audit / Logging Planning Requirements

- request id;
- user/operator context where available;
- orchestrator response status;
- refusal reason;
- citation readiness;
- caveat flag;
- no-runtime assertions;
- timestamp;
- no sensitive content leakage.

## 15. Stop Conditions

- endpoint creation required;
- UI creation required;
- chat exposure required;
- live LLM required;
- final answer generation required;
- live retrieval required;
- corpus query required;
- corpus mutation required;
- DB read/write required;
- public access required;
- access control unresolved;
- audit/logging unresolved;
- refusal visibility unresolved.

## 16. What This Gate Authorises

Only a future endpoint/UI design pack may be considered. This gate flows into endpoint/UI design, not endpoint/UI creation. Any future endpoint/UI creation must be separately approved.

## 17. What This Gate Does Not Authorise

- endpoint creation
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

Preferred next Minerva slice should be historical read-only chat pilot endpoint/UI design pack v0.1 if this gate records ready. That future slice should design endpoint/UI shape only and must flow into endpoint/UI design, not endpoint/UI creation. It must still not expose chat unless explicitly approved. If blockers exist, next slice should remediate blockers.

## 19. Progress After This Slice

Minerva has moved from orchestrator closeout into endpoint/UI planning gate. Minerva remains pre-chat-exposure. Endpoint/UI/live LLM/final answer generation remain separate future decisions.

## 20. Developer Handoff

Use this planning gate as a control artefact only. Do not create routes, endpoints, UI, chat exposure, live LLM calls, final natural-language answer generation, live retrieval backend, vector search, corpus query, DB read/write, corpus mutation, source ingestion, Code Evidence ingestion, schema migrations, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes without a separate explicit approval slice.
