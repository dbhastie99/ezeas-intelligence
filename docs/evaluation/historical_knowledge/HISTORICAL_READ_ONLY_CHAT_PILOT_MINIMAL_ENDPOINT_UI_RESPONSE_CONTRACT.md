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
