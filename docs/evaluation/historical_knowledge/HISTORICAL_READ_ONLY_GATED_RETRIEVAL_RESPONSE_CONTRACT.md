# Historical Read-Only Gated Retrieval Response Contract

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the hardened response contract for the Minerva historical read-only gated retrieval skeleton candidate.

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

## Decision Catalog

`RetrievalDecision` must be one of:

- `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL`
- `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL`
- `ELIGIBLE_CAVEATED_RETRIEVAL`
- `REFUSE_MISSING_ANSWER_USE_PERMISSION`
- `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY`
- `REFUSE_MISSING_PROVENANCE`
- `REFUSE_CONFLICTED_EVIDENCE`
- `REFUSE_SUPERSEDED_EVIDENCE`
- `REFUSE_HISTORICAL_CONTEXT_NOT_CURRENT_TRUTH`
- `REFUSE_NOT_ANSWERABLE`
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED`

`RuntimeActionPermitted` is not exposed as a runtime action flag because runtime action is never permitted by this skeleton. The response instead preserves explicit false no-runtime fields and `RuntimeBoundaryAsserted: true`.
