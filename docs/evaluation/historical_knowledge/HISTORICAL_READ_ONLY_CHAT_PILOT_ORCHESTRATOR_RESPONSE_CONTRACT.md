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

The response contract may inform `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_GATE.md`, but it does not authorise endpoint/UI creation, chat exposure, live LLM use, final natural-language answer generation, live retrieval, corpus query, database access, or corpus mutation.

Endpoint/UI design consumes the orchestrator envelope only and does not create endpoint/UI. Future UI display must surface the envelope status, refusal reason, citation readiness, caveat requirement, and no-runtime flags without converting the envelope into production chat.

## Hardened Decision Coverage

The response contract is hardened by `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_DECISION_CATALOG.md`.

Required decision coverage includes `READY_CURRENT_TRUTH_ENVELOPE`, `READY_HISTORICAL_CONTEXT_ENVELOPE`, `READY_CAVEATED_ENVELOPE`, `REFUSAL_ENVELOPE`, `BLOCKED_NO_RUNTIME_ENVELOPE`, `REFUSE_MISSING_ANSWER_USE`, `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY`, `REFUSE_MISSING_PROVENANCE`, `REFUSE_MISSING_CITATION`, `REFUSE_CONFLICTED`, `REFUSE_SUPERSEDED`, and `REFUSE_NOT_ANSWERABLE`.

All decision outcomes keep `FinalAnswerGenerated`, `LiveLLMCalled`, `ChatExposed`, `EndpointUIPresent`, `LiveRetrievalPerformed`, `CorpusMutationPerformed`, `DatabaseReadPerformed`, and `DatabaseWritePerformed` false.
