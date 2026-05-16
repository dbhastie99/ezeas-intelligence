# Historical Citation/Refusal Enforcement Response Contract

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the response contract for the Minerva historical citation/refusal enforcement skeleton.

## Required Response Fields

- `CitationRefusalSkeletonImplemented`
- `CitationRefusalDecision`
- `CitationReady`
- `RefusalRequired`
- `RefusalReason`
- `CitationEnvelopePrepared`
- `FinalAnswerGenerated`
- `LiveLLMCalled`
- `ChatExposed`
- `RetrievalRuntimeCalled`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `EndpointUIPresent`
- `RequiredCitationFieldsPresent`
- `MissingCitationFields`
- `CaveatRequired`
- `CaveatReady`
- `RuntimeBoundaryAsserted`
- `Guardrails`
- `NonGoals`
- `Explanation`

## Required Defaults

- `CitationRefusalSkeletonImplemented`: true
- `FinalAnswerGenerated`: false
- `LiveLLMCalled`: false
- `ChatExposed`: false
- `RetrievalRuntimeCalled`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `EndpointUIPresent`: false
- `RuntimeBoundaryAsserted`: true

## Decision Catalog

`CitationRefusalDecision` must be one of:

- `CITATION_READY_CURRENT_TRUTH`
- `CITATION_READY_HISTORICAL_CONTEXT`
- `CITATION_READY_CAVEATED`
- `REFUSE_MISSING_SOURCE_ID`
- `REFUSE_MISSING_SOURCE_TITLE`
- `REFUSE_MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER`
- `REFUSE_MISSING_GOVERNANCE_CHAIN`
- `REFUSE_CONFLICTED_EVIDENCE`
- `REFUSE_SUPERSEDED_EVIDENCE`
- `REFUSE_NOT_ANSWER_APPROVED`
- `REFUSE_PRIOR_GATE_REFUSAL`
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED`

## Contract Boundary

The response is for citation/refusal gate enforcement only. It is not a final answer, not a chat response, not citation rendering, not retrieved evidence, not runtime answer-use permission, and not runtime retrieval activation.

The skeleton is in-memory and metadata-only. No live retrieval backend is used, no LLM is called, no final chat answer is generated, no final answer generation occurs, no chat is exposed, no endpoint/UI exists, no corpus mutation occurs, and no DB read/write occurs.
