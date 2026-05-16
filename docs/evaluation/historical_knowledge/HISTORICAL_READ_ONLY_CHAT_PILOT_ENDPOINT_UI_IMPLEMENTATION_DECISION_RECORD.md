# Historical Read-Only Chat Pilot Endpoint/UI Implementation Decision Record

Version: v0.1

Date: 16 May 2026

## Decision Record

- DecisionId: `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_GATE_2026_05_16_V0_1`
- DecisionStatus: `DRAFTED_FOR_MINIMAL_IMPLEMENTATION_CANDIDATE_CONSIDERATION`
- DecisionDate: `2026-05-16`
- InputsReviewed:
  - `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_DESIGN_PACK.md`
  - `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_CONTRACT_DESIGN.md`
  - `HISTORICAL_READ_ONLY_CHAT_PILOT_UI_SURFACE_DESIGN.md`
  - `HISTORICAL_READ_ONLY_CHAT_PILOT_ACCESS_CONTROL_DESIGN.md`
  - `HISTORICAL_READ_ONLY_CHAT_PILOT_AUDIT_LOGGING_DESIGN.md`
  - `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_ENTRY_CRITERIA.md`
  - `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_GATE.md`
- EndpointUiDesignComplete: Yes
- EndpointContractDesignComplete: Yes
- UiSurfaceDesignComplete: Yes
- AccessControlDesignComplete: Yes
- AuditLoggingDesignComplete: Yes
- MinimalImplementationCandidatePermitted: Gate drafted; future candidate may be considered only if separately approved.
- EndpointCreatedThisSlice: No
- UICreatedThisSlice: No
- ChatExposedThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No
- Blockers: None recorded in this drafted gate; any unresolved blocker in the blocker model prevents candidate implementation.
- DecisionRationale: Existing endpoint/UI design controls are complete enough to permit consideration of a future minimal/internal/read-only/envelope-only implementation candidate. This decision does not itself create endpoint/UI or expose chat.
- ApprovedBy: Not production approval; documentation-control slice only.
- Notes: No live LLM, final answer generation, live retrieval, corpus query, database read/write, corpus mutation, source ingestion, Code Evidence ingestion, schema migration, production deployment, or cross-repo change is approved.

## Minimal Candidate Decision Update

- MinimalEndpointUiCandidateStatus: `IMPLEMENTED_INTERNAL_METADATA_ENVELOPE_ONLY`
- MinimalCandidateControl: `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_IMPLEMENTATION_CANDIDATE.md`
- MinimalCandidateService: `app/services/historical_read_only_chat_pilot_endpoint_ui_candidate_service.py`
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
- DecisionRationale: Existing route registration is global and existing chat route behaviour uses database access, retrieval, LLM answer generation, and audit writes. The safe candidate is therefore an internal unmounted service/contract only.
