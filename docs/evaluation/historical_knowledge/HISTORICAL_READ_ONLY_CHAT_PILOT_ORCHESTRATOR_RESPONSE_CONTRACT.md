# Historical Read-Only Chat Pilot Orchestrator Response Contract

Version: v0.1

Date: 16 May 2026

## Purpose

This contract defines the deterministic response envelope returned by the internal in-memory read-only chat pilot orchestrator candidate.

## Required Fields

- `ChatPilotOrchestratorCandidateImplemented`
- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposed`
- `EndpointUIPresent`
- `LiveRetrievalPerformed`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `RetrievalGateResult`
- `AnswerSynthesisGateResult`
- `CitationRefusalGateResult`
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

## Required Defaults

- `ChatPilotOrchestratorCandidateImplemented`: true
- `LiveLLMCalled`: false
- `FinalAnswerGenerated`: false
- `ChatExposed`: false
- `EndpointUIPresent`: false
- `LiveRetrievalPerformed`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `RuntimeBoundaryAsserted`: true

## Allowed Envelope Modes

- `READY_CURRENT_TRUTH_ENVELOPE`
- `READY_HISTORICAL_CONTEXT_ENVELOPE`
- `READY_CAVEATED_ENVELOPE`
- `REFUSAL_ENVELOPE`
- `BLOCKED_NO_RUNTIME_ENVELOPE`

## Boundary

The response is an orchestration envelope only. No endpoint/UI exists. No live LLM is called. No final answer is generated. No live retrieval backend is used. No DB read/write occurs. No corpus mutation occurs. This is not production chat exposure.
