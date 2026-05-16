# Historical Answer Synthesis Enforcement Response Contract

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the response contract for the Minerva historical answer synthesis enforcement skeleton.

## Required Response Fields

- `AnswerSynthesisSkeletonImplemented`
- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposed`
- `RetrievalRuntimeCalled`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `EndpointUIPresent`
- `AnswerModeDecision`
- `AllowedAnswerMode`
- `RefusalRequired`
- `RefusalReason`
- `CitationRequired`
- `CaveatRequired`
- `RuntimeBoundaryAsserted`
- `Guardrails`
- `NonGoals`
- `Explanation`

## Required Defaults

- `AnswerSynthesisSkeletonImplemented`: true
- `LiveLLMCalled`: false
- `FinalAnswerGenerated`: false
- `ChatExposed`: false
- `RetrievalRuntimeCalled`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `EndpointUIPresent`: false
- `RuntimeBoundaryAsserted`: true

## Decision Catalog

`AnswerModeDecision` must be one of:

- `CURRENT_TRUTH_ANSWER_ALLOWED`
- `HISTORICAL_CONTEXT_ANSWER_ALLOWED`
- `CAVEATED_ANSWER_ALLOWED`
- `CONTEXT_ONLY_ANSWER_ALLOWED`
- `REFUSE_INSUFFICIENT_GOVERNED_EVIDENCE`
- `REFUSE_NOT_ANSWER_APPROVED`
- `REFUSE_RETRIEVAL_NOT_ELIGIBLE`
- `REFUSE_MISSING_PROVENANCE`
- `REFUSE_CONFLICTED_EVIDENCE`
- `REFUSE_SUPERSEDED_EVIDENCE`
- `REFUSE_CITATION_REQUIRED`
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED`

## Contract Boundary

The response is for gate enforcement only. It is not a final answer, not a chat response, not citation rendering, not retrieved evidence, not runtime answer-use permission, and not runtime retrieval activation.

The skeleton is in-memory and metadata-only. No live retrieval backend is used, no LLM is called, no final chat answer is generated, no chat is exposed, no endpoint/UI exists, no corpus mutation occurs, and no DB read/write occurs.
