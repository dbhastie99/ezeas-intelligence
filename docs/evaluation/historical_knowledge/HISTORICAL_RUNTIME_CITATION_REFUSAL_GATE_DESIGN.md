# Historical Runtime Citation / Refusal Gate Design

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the future citation/refusal gate design for a narrow, read-only Minerva historical chat pilot.

No citation rendering runtime is implemented.

## 2. Required Provenance Fields

- `SourceId`;
- `SourceTitle`;
- `SourceDate` or unknown-date marker;
- `RepositoryContext`;
- `DomainContext`;
- `AnswerUsePermissionId`;
- `RetrievalEligibilityId`;
- `AnswerModeId`;
- `EvidenceScope`;
- `RetrievalMode`;
- `AnswerMode`;
- `RevocationPath`;
- evidence ids used;
- evidence ids excluded.

## 3. Citation Readiness Checks

Non-refusal answers must have complete citation/provenance readiness for every used evidence id.

Missing citation/provenance readiness blocks answer output.

No fabricated citations are allowed.

## 4. Caveat Readiness Checks

Required caveats must be present before caveated or historical-context answers can be rendered.

Historical-context caveats must state that the material is historical/contextual and not current truth unless separately promoted and approved.

## 5. Refusal Triggers

- missing answer-use permission;
- missing retrieval eligibility;
- missing answer mode;
- missing citation/provenance;
- missing required caveat;
- conflicted evidence;
- superseded evidence;
- not-answerable evidence;
- insufficient governed evidence;
- out-of-scope request.

## 6. Missing Evidence Behaviour

When evidence is missing, incomplete, blocked, not-answerable, conflicted, or superseded, the future gate must refuse or return insufficient governed evidence.

The refusal must identify the missing or blocked gate where known and must not invent source support.

## 7. Output Shape For Future Answer Renderer

The future citation/refusal gate should output:

- `RequestId`;
- `RenderableAnswerPermitted`;
- `AnswerMode`;
- `CitationBlocks`;
- `ProvenanceStatus`;
- `CaveatStatus`;
- `RefusalRequired`;
- `RefusalReason`;
- `RendererPayload` or `RefusalPayload`;
- `AuditSummary`.

## 8. Boundary

This document is design only. It does not implement citation rendering runtime, answer synthesis runtime, retrieval runtime, endpoint/UI, live LLM calls, database writes, corpus mutation, or chat exposure.
