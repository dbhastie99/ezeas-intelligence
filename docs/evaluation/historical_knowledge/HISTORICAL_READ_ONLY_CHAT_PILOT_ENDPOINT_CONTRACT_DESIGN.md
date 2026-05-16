# Historical Read-Only Chat Pilot Endpoint Contract Design

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the future Minerva historical read-only chat pilot endpoint contract as design only. No endpoint, route, controller, or API handler is created.

## Future Endpoint Posture

- internal-only;
- read-only;
- metadata/envelope input only at first;
- in-memory orchestrator candidate only unless later approved;
- no live LLM unless later explicitly approved;
- no DB connection or live retrieval backend unless later explicitly approved.

## Request Envelope Fields

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

## Response Envelope Fields

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

## Non-Creation Statement

This contract design creates no endpoint, no route, no controller, and no API handler. It does not expose chat, call a live LLM, generate a final natural-language answer, connect live retrieval, query corpus/vector/database stores, mutate corpus, ingest source content, ingest Code Evidence, read or write a database, migrate schemas, or change runtime behaviour.
