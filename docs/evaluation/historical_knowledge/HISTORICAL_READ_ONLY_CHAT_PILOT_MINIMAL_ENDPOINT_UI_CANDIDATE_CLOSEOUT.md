# Historical Read-Only Chat Pilot Minimal Endpoint/UI Candidate Closeout

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document closes out the minimal internal endpoint/UI candidate for Minerva historical knowledge as an internal envelope/status-only candidate.

## 2. Scope

Scope is limited to static review and closeout of the existing candidate service and its control documents. This closeout does not expand exposure, register routes, create production UI, connect runtime retrieval, call a live LLM, generate final answers, query databases, mutate corpus, ingest sources, ingest Code Evidence, or change other repositories.

## 3. Current Status

- MinimalEndpointUiCandidateCloseoutStatus: CLOSEOUT_COMPLETED_INTERNAL_ENVELOPE_ONLY
- EndpointCreatedForProduction: No
- RouteRegisteredGlobally: No
- UICreatedForProduction: No
- ChatExposedToUsers: No
- PublicAccessEnabled: No
- TenantCustomerAccessEnabled: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_IMPLEMENTATION_CANDIDATE.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_RESPONSE_CONTRACT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_GUARDRAILS.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_FIXTURE_CATALOG.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CLOSEOUT_ENTRY_CRITERIA.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_GATE.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_NO_EXPOSURE_ATTESTATION.md`
- `historical_read_only_chat_pilot_endpoint_ui_candidate_service.py`

## 5. Candidate Closeout Status Model

- `MINIMAL_ENDPOINT_UI_CLOSEOUT_NOT_STARTED`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_COMPLETED_INTERNAL_ENVELOPE_ONLY`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_BLOCKED`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_REQUIRES_EXPOSURE_REVIEW`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_REQUIRES_LLM_POLICY_REVIEW`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_REQUIRES_ACCESS_CONTROL_REVIEW`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_READY_FOR_PILOT_EXPOSURE_DECISION_GATE`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_REJECTED`
- `MINIMAL_ENDPOINT_UI_CLOSEOUT_SUPERSEDED`

## 6. Candidate Implementation Review

- The candidate service exists.
- The candidate consumes supplied metadata only.
- The candidate calls/reuses the in-memory orchestrator only.
- The candidate returns envelope/status output.
- The candidate does not register a production route.
- The candidate does not expose public chat.

## 7. Envelope / Status Output Review

- The current-truth fixture returns ready envelope without final answer generation.
- The historical-context fixture returns historical envelope.
- The caveated fixture preserves caveat.
- The refusal fixture remains refusal.
- The no-runtime flags remain false.

## 8. Refusal / Citation / Caveat Visibility Review

- Refusal remains visible.
- Citation readiness remains visible.
- Caveat requirement remains visible.
- Blocked gates remain visible.
- Historical-context is not silently converted to current truth.

## 9. Runtime Boundary Review

- No live LLM.
- No final answer generation.
- No live retrieval.
- No corpus mutation.
- No DB read/write.
- No Code Evidence ingestion.

## 10. Exposure Boundary Review

- No production chat exposure.
- No public access.
- No tenant/customer access.
- No global route registration.
- Any future exposure requires separate decision gate.

## 11. Static Review Findings

The static review finds the candidate suitable for internal closeout as an envelope/status-only service. It remains unmounted, internal, metadata-only, no-route, no-UI, no-live-runtime, no-DB, no-corpus, and no-final-answer.

## 12. What This Closeout Authorises

- a future pilot exposure decision gate may be considered.
- any future exposure must be separately approved.

## 13. What This Closeout Does Not Authorise

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

## 14. Recommended Next Slice

Preferred next Minerva slice should be historical read-only chat pilot exposure decision gate v0.1.

That future slice should decide whether a strictly internal pilot exposure can be considered.

That future slice must still not approve live LLM or final natural-language answer generation unless separately gated.

## 15. Progress After This Slice

Minerva has a closed-out minimal internal endpoint/UI candidate for future decision-gate consideration only. The candidate remains in-memory, metadata-only, envelope/status-only, no-route, no-production, no-public-access, no-tenant/customer-access, no-live-LLM, no-final-answer, no-live-retrieval, no-DB, and no-corpus.

## 16. Developer Handoff

Use the candidate service only as an internal metadata-envelope adapter around the in-memory orchestrator candidate. A future pilot exposure decision gate is required before any internal exposure discussion. Do not register a route, expose UI, call live LLMs, generate final answers, connect retrieval, query corpus/vector/database stores, read or write databases, mutate corpus, ingest sources, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics without separate explicit approval.

