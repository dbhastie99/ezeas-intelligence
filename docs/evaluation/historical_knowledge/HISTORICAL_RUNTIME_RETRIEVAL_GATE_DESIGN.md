# Historical Runtime Retrieval Gate Design

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the future retrieval gate design for a narrow, read-only Minerva historical chat pilot.

No retrieval runtime is implemented.

## 2. Required Inputs

- request/query context;
- requested retrieval mode;
- requested answer scope;
- candidate evidence ids;
- source ids and source metadata;
- review status;
- current-truth promotion status;
- answer-use permission status and `AnswerUsePermissionId`;
- retrieval eligibility status and `RetrievalEligibilityId`;
- evidence scope;
- provenance/citation readiness;
- caveat requirements;
- conflict status;
- supersession status;
- revocation path.

## 3. Required Answer-Use Permission Dependency

The retrieval gate must depend on answer-use permission. Evidence without approved answer-use permission for the requested scope must not be exposed for non-refusal answer synthesis.

Answer-use permission does not implement retrieval and does not expose chat.

## 4. Retrieval Eligibility Dependency

The retrieval gate must depend on retrieval eligibility. Missing, blocked, rejected, revoked, superseded, or out-of-scope retrieval eligibility must block retrieval and hand off to refusal behaviour.

Retrieval eligibility does not activate runtime retrieval in this slice.

## 5. Current-Truth Versus Historical-Context Filtering

Current-truth answer candidates require current-truth promotion, answer-use permission, retrieval eligibility, approved answer mode, and citation/provenance readiness.

Historical-context evidence may only be returned for approved historical-context answer modes and must carry historical labels and caveats forward.

Historical sources are not answerable current truth by default.

## 6. Exclusion Rules

The future gate must exclude:

- not-answerable evidence;
- missing answer-use permission;
- missing retrieval eligibility;
- blocked, rejected, revoked, or superseded permissions;
- missing citation/provenance readiness;
- out-of-scope evidence;
- evidence requiring unresolved caveats;
- source material not approved for the requested answer mode.

## 7. Conflict / Supersession Filtering

Conflicted evidence must not produce settled/current-truth answers.

Superseded evidence must not produce current-truth answers.

Conflicted or superseded evidence may be returned as historical context only where explicitly approved, labelled, and caveated.

## 8. Output Shape To Answer Synthesis Gate

The future retrieval gate should output:

- `RequestId`;
- `RetrievalMode`;
- `RequestedAnswerMode`;
- `EligibleEvidenceIds`;
- `ExcludedEvidenceIds`;
- `ExclusionReasons`;
- `AnswerUsePermissionIds`;
- `RetrievalEligibilityIds`;
- `EvidenceScopes`;
- `CurrentTruthStatuses`;
- `ConflictStatuses`;
- `SupersessionStatuses`;
- `CaveatRequirements`;
- `CitationProvenanceStatuses`;
- `RefusalRequired`;
- `RefusalReason`.

## 9. Refusal Handoff When Retrieval Is Blocked

If retrieval is blocked, the gate must hand off refusal context instead of evidence content. The refusal handoff must identify the missing or blocked gate where known and must not fabricate citations.

## 10. Link To Test Matrix Scenarios

Retrieval gate design must be tested through `HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX.md`.

The matrix scenarios must cover current-truth retrieval eligibility, historical-context retrieval eligibility, backlog/context retrieval constraints, doctrine/context retrieval constraints, missing retrieval eligibility refusal, conflict filtering, supersession filtering, missing provenance filtering, and not-answerable evidence exclusion.

The test matrix link does not implement runtime retrieval or activate runtime retrieval eligibility.

The first read-only gated retrieval skeleton candidate is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_SKELETON_CANDIDATE.md`. It evaluates supplied metadata in-memory only and does not use live retrieval, vector search, corpus query, database read/write, live LLM, endpoint/UI, chat, answer synthesis runtime, or citation rendering runtime.

The hardened contract is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_CONTRACT_HARDENING.md`. The hardened decision catalog is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_DECISION_CATALOG.md`; all decisions preserve RuntimeActionPermitted No. The contract closeout is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_CONTRACT_CLOSEOUT.md`.

## 11. Boundary

This document is design only. It does not implement runtime retrieval, retrieval filtering, endpoint/UI, live LLM calls, corpus mutation, database writes, or chat exposure.
