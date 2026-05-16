# Historical Answer Mode Citation Requirements

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines citation and provenance requirements for future Minerva historical answer-mode decisions.

Missing citation/provenance blocks chat-answer readiness.

The governing citation/provenance answer contract is `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_ANSWER_CONTRACT.md`.

The source-to-answer evidence chain requirements are `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_EVIDENCE_CHAIN_REQUIREMENTS.md`.

## 2. Required Citation / Provenance Fields

Every answer-mode record must preserve:

- `SourceId`
- `SourceTitle`
- `SourceDate` or unknown-date marker
- `RepositoryContext`
- `DomainContext`
- `AnswerUsePermissionId`
- `RetrievalEligibilityId`
- `AnswerModeId`
- `EvidenceScope`
- `RetrievalMode`
- `AnswerMode`
- `CitationRequired`
- `CaveatRequired`
- `ProvenanceStatus`
- `Reviewer/Approver`
- `ApprovedAtUtc`
- `RevocationPath`
- `Notes`

## 3. Readiness Rules

Citation/provenance is required before any non-refusal answer mode can be approved.

Missing `SourceId`, source title, repository/domain context, answer-use permission id, retrieval eligibility id, answer-mode id, evidence scope, retrieval mode, answer mode, citation requirement, caveat requirement, provenance status, reviewer/approver, approval timestamp, revocation path, or notes blocks chat-answer readiness.

Unknown source dates must be marked with an explicit unknown-date marker rather than omitted.

Citation requirements do not implement retrieval runtime, answer synthesis runtime, chat exposure, live LLM calls, corpus mutation, source ingestion, database writes, endpoint changes, or UI changes.

Citation requirements also do not render citations at runtime. Runtime citation rendering requires a later explicit implementation slice.
