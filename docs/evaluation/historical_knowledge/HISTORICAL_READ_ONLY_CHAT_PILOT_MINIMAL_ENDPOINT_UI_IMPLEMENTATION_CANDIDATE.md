# Historical Read-Only Chat Pilot Minimal Endpoint/UI Implementation Candidate

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document records the first minimal internal read-only endpoint/UI implementation candidate for Minerva historical knowledge.

## 2. Scope

Scope is limited to an internal metadata/envelope candidate service that calls the existing in-memory orchestrator candidate and returns status output. No runtime endpoint, UI, production chat, live retrieval, live LLM, database access, corpus query, corpus mutation, source ingestion, Code Evidence ingestion, schema migration, or cross-repo change is introduced.

## 3. Current Status

- MinimalEndpointUiCandidateStatus: IMPLEMENTED_INTERNAL_METADATA_ENVELOPE_ONLY
- EndpointCreatedThisSlice: No
- RouteRegisteredGlobally: No
- UICreatedThisSlice: No
- ChatExposedThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `app/main.py`
- `app/api/v1/chat.py`
- `app/api/v1/ingest.py`
- `app/services/historical_read_only_chat_pilot_orchestrator_candidate_service.py`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_GATE.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_DECISION_RECORD.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_CONTRACT_DESIGN.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_UI_SURFACE_DESIGN.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`

## 5. Candidate Implementation Status Model

- `MINIMAL_ENDPOINT_UI_CANDIDATE_NOT_STARTED`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_DOCUMENTED`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_IMPLEMENTED_INTERNAL_ONLY`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_BLOCKED`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_READY_FOR_CLOSEOUT`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_REQUIRES_ROUTE_REVIEW`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_REQUIRES_ACCESS_CONTROL_REVIEW`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_REJECTED`
- `MINIMAL_ENDPOINT_UI_CANDIDATE_SUPERSEDED`

## 6. Candidate Surface

The candidate surface is internal-only; metadata/envelope-only; not production chat; not public; not tenant/customer-facing; not final natural-language answer generation.

## 7. Request Envelope

The candidate accepts supplied in-memory metadata with these fields: `RequestId`, `OperatorContext`, `SourceId`, `EvidenceScope`, `AnswerUsePermissionStatus`, `RetrievalEligibilityStatus`, `AnswerMode`, `CitationStatus`, `ProvenanceStatus`, `ConflictStatus`, `SupersessionStatus`, `CurrentTruthPermitted`, `RetrievalEligible`, `ChatEligible`, `CitationRequired`, `CaveatRequired`, `SourceTitle`, `SourceDate`, `UnknownDateMarker`, `RepositoryContext`, `DomainContext`, `AnswerUsePermissionId`, `RetrievalEligibilityId`, `AnswerModeId`, and `Notes`.

## 8. Response Envelope

The response envelope is defined in `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_RESPONSE_CONTRACT.md`. It exposes implementation flags, no-runtime flags, the request id/operator context, the orchestrator response, pilot status/mode, refusal/citation/caveat flags, guardrails, non-goals, and explanation.

## 9. Orchestrator Integration

The candidate calls only `evaluate_historical_read_only_chat_pilot_orchestrator_candidate` from `app/services/historical_read_only_chat_pilot_orchestrator_candidate_service.py`. It does not call retrieval services, LLM clients, database sessions, corpus stores, vector stores, or external services.

## 10. Endpoint / Route Registration Position

- Endpoint module exists: No.
- Candidate service module exists: Yes.
- RouterRegisteredGlobally: No.
- No production app exposure unless later approved.

## 11. UI Position

- No UI created.
- UICreatedThisSlice: No.
- Future UI must visibly display refusal/citation/caveat/runtime flags.

## 12. Runtime Boundary Confirmation

- EndpointCreationPermittedForProduction: No
- RouteGlobalRegistrationPermitted: No
- UICreationPermittedForProduction: No
- ChatExposurePermitted: No
- LiveLLMCallPermitted: No
- FinalAnswerGenerationPermitted: No
- LiveRetrievalPermitted: No
- CorpusMutationPermitted: No
- DatabaseReadPermitted: No
- DatabaseWritePermitted: No
- SchemaMigrationPermitted: No

## 13. No-Exposure / No-Production Boundary

This candidate is not public, not production, not tenant/customer-facing, not mounted, and not a chat route. It does not create production endpoint/UI exposure.

## 14. Stop Conditions

Stop if the slice requires route registration, production exposure, public access, tenant/customer access, live LLM calls, final answer generation, live retrieval, vector/corpus search, DB access, corpus mutation, source ingestion, Code Evidence ingestion, schema migration, or cross-repo changes.

## 15. What This Candidate Authorises

- a future closeout/static review slice may be considered.
- any future production chat exposure requires separate approval.

## 16. What This Candidate Does Not Authorise

- production chat exposure
- public endpoint
- tenant/customer endpoint
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

Preferred next Minerva slice should be historical read-only chat pilot minimal endpoint/UI candidate closeout v0.1. That future slice should review the candidate for no-exposure, no-LLM, no-DB, no-corpus, and envelope-only behaviour. It must still not expose production chat.

## 18. Progress After This Slice

Minerva now has an internal metadata/envelope candidate service for the endpoint/UI boundary. The implementation remains unmounted, no-route, no-UI, no-production, no-live-runtime, and suitable only for a future closeout/static review slice.

## 19. Developer Handoff

Use `app/services/historical_read_only_chat_pilot_endpoint_ui_candidate_service.py` only as an internal metadata-envelope adapter around the orchestrator candidate. Do not register a route, expose UI, call live LLMs, generate final answers, connect retrieval, query corpus/vector/database stores, read or write databases, mutate corpus, ingest sources, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics without a separate explicit approval slice.
