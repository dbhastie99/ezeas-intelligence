# Historical Read-Only Chat Pilot Minimal Endpoint/UI Response Contract

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the response contract for the internal minimal endpoint/UI candidate service. It is a metadata/status envelope only.

## Response Fields

- `MinimalEndpointUiCandidateImplemented`
- `EndpointCreatedThisSlice`
- `RouteRegisteredGlobally`
- `UICreatedThisSlice`
- `ChatExposedThisSlice`
- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `LiveRetrievalPerformed`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `RequestId`
- `OperatorContext`
- `OrchestratorResponse`
- `PilotResponseStatus`
- `PilotResponseMode`
- `RefusalRequired`
- `RefusalReason`
- `CitationReady`
- `CaveatRequired`
- `RuntimeBoundaryAsserted`
- `Guardrails`
- `NonGoals`
- `Explanation`

## No-Runtime Defaults

- `MinimalEndpointUiCandidateImplemented`: `true`
- `EndpointCreatedThisSlice`: `false`
- `RouteRegisteredGlobally`: `false`
- `UICreatedThisSlice`: `false`
- `ChatExposedThisSlice`: `false`
- `LiveLLMCalled`: `false`
- `FinalAnswerGenerated`: `false`
- `LiveRetrievalPerformed`: `false`
- `CorpusMutationPerformed`: `false`
- `DatabaseReadPerformed`: `false`
- `DatabaseWritePerformed`: `false`
- `RuntimeBoundaryAsserted`: `true`

## Contract Boundary

The contract carries the orchestrator envelope forward. It does not create a final answer, render citations, perform retrieval, call a model, query a database, mutate corpus, expose chat, create endpoint/UI, or register a route.

## Closeout Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md` confirms this response contract remains envelope/status-only. `READY_CURRENT_TRUTH_ENVELOPE`, `READY_HISTORICAL_CONTEXT_ENVELOPE`, `READY_CAVEATED_ENVELOPE`, `REFUSAL_ENVELOPE`, `BLOCKED_NO_RUNTIME_ENVELOPE`, and `BLOCKED_NO_EXPOSURE_ENVELOPE` all keep exposure/runtime fields No/false. No final answer generation, live LLM call, live retrieval, DB read/write, corpus mutation, production chat exposure, public endpoint, tenant/customer endpoint, or global route registration is authorised.
