# Historical Read-Only Gated Retrieval Response Contract

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the response contract for the Minerva historical read-only gated retrieval skeleton candidate.

## Required Response Fields

- `RetrievalGateSkeletonImplemented`
- `LiveRetrievalPerformed`
- `LiveLLMCalled`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `EndpointUIPresent`
- `RetrievalDecision`
- `RetrievalMode`
- `ExpectedAnswerMode`
- `RefusalReason`
- `CitationRequired`
- `CaveatRequired`
- `RuntimeBoundaryAsserted`
- `Guardrails`
- `NonGoals`
- `Explanation`

## Required Defaults

- `RetrievalGateSkeletonImplemented`: true
- `LiveRetrievalPerformed`: false
- `LiveLLMCalled`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `EndpointUIPresent`: false
- `RuntimeBoundaryAsserted`: true

## Contract Boundary

The response is for gate evaluation only. It is not an answer, not a citation rendering payload, not retrieved evidence, not synthesized text, not chat output, and not a runtime activation signal.

The contract confirms that no live retrieval backend is used, no LLM is called, no chat is exposed, no endpoint/UI exists, no corpus mutation occurs, and no DB read/write occurs.
