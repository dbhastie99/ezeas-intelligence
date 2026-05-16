# Historical Citation/Refusal Enforcement Skeleton

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the first Minerva historical citation/refusal enforcement skeleton.

The skeleton is in-memory and metadata-only. It consumes supplied answer synthesis skeleton output and decides whether the future answer can proceed to a citation-ready response envelope or must refuse because provenance, citation, conflict, supersession, or governance-chain requirements are missing.

The response is for citation/refusal gate enforcement only. It does not render citations and does not generate final natural-language chat answers.

## Scope

The skeleton evaluates fields such as `AnswerModeDecision`, `AllowedAnswerMode`, `RefusalRequired`, `RefusalReason`, `CitationRequired`, `CaveatRequired`, `CaveatReady`, `SourceId`, `SourceTitle`, `SourceDate`, `UnknownDateMarker`, `RepositoryContext`, `DomainContext`, `AnswerUsePermissionId`, `RetrievalEligibilityId`, `AnswerModeId`, `EvidenceScope`, `RetrievalMode`, `ProvenanceStatus`, `ConflictStatus`, `SupersessionStatus`, and `RuntimeBoundaryAsserted`.

## Decision Mapping

- Prior `RefusalRequired: true` metadata maps to `REFUSE_PRIOR_GATE_REFUSAL` and preserves `RefusalReason`.
- Missing `SourceId` where `CitationRequired` is true maps to `REFUSE_MISSING_SOURCE_ID`.
- Missing `SourceTitle` where `CitationRequired` is true maps to `REFUSE_MISSING_SOURCE_TITLE`.
- Missing `SourceDate` without `UnknownDateMarker` where `CitationRequired` is true maps to `REFUSE_MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER`.
- Missing `AnswerUsePermissionId`, `RetrievalEligibilityId`, or `AnswerModeId` for a non-refusal answer maps to `REFUSE_MISSING_GOVERNANCE_CHAIN`.
- `UNRESOLVED` or `CONFLICTED` evidence without a ready caveat maps to `REFUSE_CONFLICTED_EVIDENCE`.
- `SUPERSEDED` evidence requested as current truth maps to `REFUSE_SUPERSEDED_EVIDENCE`.
- Non-refusal metadata without an approved answer mode maps to `REFUSE_NOT_ANSWER_APPROVED`.
- Runtime-required metadata maps to `BLOCKED_RUNTIME_NOT_IMPLEMENTED`.
- Complete current-truth citation metadata maps to `CITATION_READY_CURRENT_TRUTH`.
- Complete historical-context citation metadata maps to `CITATION_READY_HISTORICAL_CONTEXT`.
- Complete caveated citation metadata maps to `CITATION_READY_CAVEATED`.

## Boundary

No live retrieval backend is used. No LLM is called. No final answer generation occurs. No final natural-language chat answer is generated. No chat is exposed. No endpoint/UI exists. No corpus mutation occurs. No DB read/write occurs.

This skeleton does not perform live retrieval, vector search, corpus query, source content ingestion, operational corpus mutation, Code Evidence ingestion, database reads or writes, schema migrations, endpoint changes, UI changes, citation rendering runtime, chat exposure, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, current-truth promotion, runtime answer-use activation, or runtime retrieval activation beyond supplied metadata evaluation.
