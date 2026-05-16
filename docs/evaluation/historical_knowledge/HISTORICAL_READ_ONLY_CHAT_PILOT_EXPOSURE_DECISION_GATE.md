# Historical Read-Only Chat Pilot Exposure Decision Gate

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This gate records what must be true before a future strictly internal Minerva historical read-only chat pilot exposure candidate may be considered.

## 2. Scope

Scope is limited to documentation/control/test hardening for exposure-readiness decisioning. This slice consolidates minimal endpoint/UI candidate closeout, no-production exposure attestation, decision catalog, runtime boundaries, access-control requirements, and remaining blockers. It does not expose chat.

## 3. Current Status

- PilotExposureDecisionGateStatus: DECISION_GATE_DRAFTED
- InternalExposureApprovedThisSlice: No
- ProductionChatExposedThisSlice: No
- PublicAccessEnabledThisSlice: No
- TenantCustomerAccessEnabledThisSlice: No
- GlobalRouteRegisteredThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_STATIC_REVIEW.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_DECISION_CATALOG.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_PILOT_EXPOSURE_DECISION_ENTRY_CRITERIA.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_NO_PRODUCTION_EXPOSURE_ATTESTATION.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_IMPLEMENTATION_CANDIDATE.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_RESPONSE_CONTRACT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`
- `historical_read_only_chat_pilot_endpoint_ui_candidate_service.py`

## 5. Pilot Exposure Decision Status Model

- `PILOT_EXPOSURE_DECISION_NOT_STARTED`
- `PILOT_EXPOSURE_DECISION_DRAFTED`
- `PILOT_EXPOSURE_DECISION_BLOCKED`
- `PILOT_EXPOSURE_DECISION_DEFERRED`
- `PILOT_EXPOSURE_DECISION_READY_FOR_INTERNAL_EXPOSURE_CANDIDATE`
- `PILOT_EXPOSURE_DECISION_REQUIRES_ACCESS_CONTROL_REVIEW`
- `PILOT_EXPOSURE_DECISION_REQUIRES_AUDIT_LOGGING_REVIEW`
- `PILOT_EXPOSURE_DECISION_REQUIRES_LLM_POLICY_REVIEW`
- `PILOT_EXPOSURE_DECISION_REJECTED`
- `PILOT_EXPOSURE_DECISION_SUPERSEDED`

## 6. Exposure Preconditions

- minimal endpoint/UI candidate closeout complete;
- static review complete;
- no-production exposure attestation complete;
- decision catalog complete;
- response contract complete;
- guardrails complete;
- access control decision required;
- audit/logging decision required;
- no live LLM approved;
- no final answer generation approved;
- no live retrieval backend;
- no DB read/write;
- no corpus mutation;
- explicit exposure decision required.

## 7. Internal-Only Boundary

- future exposure candidate may only be internal;
- future exposure candidate must be operator/developer controlled;
- future exposure candidate must remain envelope/status-only unless later approved;
- this slice does not approve exposure.

## 8. Public / Tenant / Customer Boundary

- no public access;
- no tenant/customer access;
- no production customer-facing route;
- no production chat exposure.

## 9. Global Route Registration Boundary

- no global route registration in this slice;
- any future registration must be separately approved;
- internal exposure candidate must remain controlled and reversible.

## 10. Live LLM / Final Answer Boundary

- no live LLM calls;
- no final natural-language answer generation;
- future LLM/final-answer behaviour requires separate policy gate.

## 11. Retrieval / Corpus / DB Boundary

- no live retrieval backend;
- no corpus/vector search;
- no corpus mutation;
- no source ingestion;
- no Code Evidence ingestion;
- no DB reads;
- no DB writes.

## 12. Access Control / Audit Boundary

- access control must be explicitly decided before exposure;
- audit/logging must be explicitly decided before exposure;
- refusal/citation/caveat/no-runtime flags must remain visible;
- exposure must not hide blocked gates.

## 13. Remaining Blockers

- exposure not approved;
- access control decision not complete;
- audit/logging runtime not implemented;
- live LLM not approved;
- final answer generation not approved;
- production/public/tenant access prohibited.

## 14. Stop Conditions

- production chat exposure required;
- public access required;
- tenant/customer access required;
- global route registration required;
- live LLM required;
- final answer generation required;
- live retrieval required;
- corpus query required;
- corpus mutation required;
- DB read/write required;
- access control unresolved;
- audit/logging unresolved;
- refusal visibility unresolved;
- citation visibility unresolved.

## 15. What This Gate Authorises

- a future strictly internal exposure candidate may be considered if gate records ready.
- any future exposure must be separately approved and remain internal unless later expanded.

## 16. What This Gate Does Not Authorise

- production chat exposure
- public endpoint
- tenant/customer endpoint
- global route registration
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
- workforce-platform changes
- award-configurator-v1 changes
- ezeas-analytics changes

## 17. Recommended Next Slice

Preferred next Minerva slice should be historical read-only chat pilot internal exposure candidate v0.1 if this gate records ready and explicit approval is provided.

If explicit exposure approval is not provided, next slice should defer exposure and close out readiness.

That future slice must still not approve live LLM or final natural-language answer generation unless separately gated.

## 18. Progress After This Slice

Minerva has moved from minimal endpoint/UI closeout into pilot exposure decision gate.

Minerva remains pre-production-chat-exposure.

Future internal exposure remains separately gated.

## 19. Developer Handoff

Use this gate only to decide readiness for a future strictly internal exposure candidate. Do not register global routes, create public or tenant/customer endpoints, expose production chat, create production UI, call live LLMs, generate final answers, connect live retrieval, query corpus/vector/database stores, read or write databases, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics without separate explicit approval.
