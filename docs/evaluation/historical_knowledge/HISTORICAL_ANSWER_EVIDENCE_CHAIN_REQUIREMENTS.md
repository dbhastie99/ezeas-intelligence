# Historical Answer Evidence Chain Requirements

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the complete required evidence chain from source registration through answer mode and citation/provenance.

The chain is control documentation only and does not implement runtime behaviour.

## 2. Required Source-To-Answer Chain

Future non-refusal historical answers must be traceable through this source-to-answer-mode-to-citation chain:

1. Source registration establishes `SourceId`, `SourceTitle`, source date or unknown-date marker, source class, repository context, and domain context.
2. Review governance records decision control through `DecisionRecordId` where applicable.
3. Findings records capture review outputs through `FindingsRecordId` where applicable.
4. Findings classification records `FindingClassificationId` where applicable.
5. Ingestion/backfill decision control records `IngestionBackfillDecisionId` where applicable, without implying ingestion.
6. Current-truth promotion control records `CurrentTruthPromotionId` where applicable, without implying answer use.
7. Answer-use permission records `AnswerUsePermissionId`.
8. Retrieval eligibility records `RetrievalEligibilityId`.
9. Answer-mode control records `AnswerModeId`.
10. Citation/provenance control records `CitationProvenanceId`.
11. Runtime gate planning records that the runtime gate and chat pilot readiness steps remain pre-runtime unless separately approved.
12. Chat pilot readiness records pilot approval status before any chat exposure.

## 3. Required Evidence Chain Fields

Every citation/provenance-ready answer chain must preserve:

- `SourceId`
- `SourceTitle`
- `SourceDate` or unknown-date marker
- `RepositoryContext`
- `DomainContext`
- `DecisionRecordId` where applicable
- `FindingsRecordId` where applicable
- `FindingClassificationId` where applicable
- `IngestionBackfillDecisionId` where applicable
- `CurrentTruthPromotionId` where applicable
- `AnswerUsePermissionId`
- `RetrievalEligibilityId`
- `AnswerModeId`
- `CitationProvenanceId`
- `EvidenceScope`
- `AnswerScope`
- `RetrievalMode`
- `AnswerMode`
- `CitationRequired`
- `CaveatRequired`
- `ProvenanceStatus`
- `ConflictStatus`
- `SupersessionStatus`
- `Reviewer/Approver`
- `ApprovedAtUtc`
- `RevocationPath`
- `Notes`

## 4. Chain Rules

Source registration does not make a source current truth.

Review decisions do not ingest source content.

Ingestion/backfill decision control does not mutate corpus.

Current-truth promotion control does not activate answer use.

Answer-use permission does not implement retrieval.

Retrieval eligibility does not expose chat.

Answer-mode control does not implement answer synthesis runtime.

Citation/provenance control does not render citations at runtime.

Runtime gate planning does not implement retrieval runtime, answer synthesis runtime, citation rendering runtime, or chat.

Chat pilot readiness is required before chat exposure and is not approved by this evidence chain.

Missing or incomplete links in the chain map to refusal or insufficient governed evidence.

## 5. Runtime Boundary

This chain is control documentation only and does not implement runtime behaviour.

It does not expose chat, call a live LLM, change retrieval runtime, change answer synthesis runtime, render citations at runtime, mutate corpus, ingest source content, promote current truth, write to a database, create endpoint changes, create UI changes, activate answer use at runtime, or activate retrieval eligibility at runtime.
