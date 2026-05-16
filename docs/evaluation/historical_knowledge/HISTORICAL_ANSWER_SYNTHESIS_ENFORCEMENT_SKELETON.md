# Historical Answer Synthesis Enforcement Skeleton

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the first Minerva historical answer synthesis enforcement skeleton.

The skeleton is in-memory and metadata-only. It consumes supplied retrieval gate output and decides which answer mode is allowed or whether refusal is required. It does not generate final natural-language chat answers.

## Scope

The skeleton evaluates fields such as `RetrievalDecision`, `RetrievalMode`, `ExpectedAnswerMode`, `RefusalReason`, `CitationRequired`, `CaveatRequired`, `RuntimeBoundaryAsserted`, `SourceId`, `EvidenceScope`, `AnswerUsePermissionStatus`, `RetrievalEligibilityStatus`, `AnswerMode`, `ProvenanceStatus`, `ConflictStatus`, and `SupersessionStatus`.

The response is for gate enforcement only.

## Decision Mapping

- `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL` maps to `CURRENT_TRUTH_ANSWER_ALLOWED`.
- `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL` maps to `HISTORICAL_CONTEXT_ANSWER_ALLOWED` and preserves historical label/caveat behaviour.
- `ELIGIBLE_CAVEATED_RETRIEVAL` maps to `CAVEATED_ANSWER_ALLOWED` and preserves `CaveatRequired: true`.
- `REFUSE_*` retrieval decisions preserve refusal and refusal reason.
- Missing citation/provenance where `CitationRequired` is true maps to `REFUSE_CITATION_REQUIRED`.
- Conflicted evidence maps to `REFUSE_CONFLICTED_EVIDENCE`.
- Superseded evidence must not produce a current-truth answer and maps to `REFUSE_SUPERSEDED_EVIDENCE` when current-truth answering is requested.
- Not-answerable evidence maps to `REFUSE_NOT_ANSWER_APPROVED`.
- Runtime not implemented conditions map to `BLOCKED_RUNTIME_NOT_IMPLEMENTED`.

## Boundary

No live retrieval backend is used. No LLM is called. No final answer generation occurs. No chat is exposed. No endpoint/UI exists. No corpus mutation occurs. No DB read/write occurs.

This skeleton does not perform live retrieval, vector search, corpus query, source content ingestion, operational corpus mutation, Code Evidence ingestion, database reads or writes, schema migrations, endpoint changes, UI changes, citation rendering runtime, chat exposure, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, current-truth promotion, runtime answer-use activation, or runtime retrieval activation beyond supplied metadata evaluation.
