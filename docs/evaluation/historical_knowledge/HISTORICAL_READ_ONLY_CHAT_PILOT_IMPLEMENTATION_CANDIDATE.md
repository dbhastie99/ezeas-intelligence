# Historical Read-Only Chat Pilot Implementation Candidate

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document records the first Minerva historical read-only chat pilot implementation candidate. The candidate is an internal deterministic orchestration helper only. It chains existing in-memory skeleton services and returns an orchestration envelope, not a final chat answer.

## 2. Scope

Scope is limited to supplied in-memory metadata evaluation for a narrow pilot orchestration candidate. The candidate reuses the read-only gated retrieval skeleton, answer synthesis enforcement skeleton, and citation/refusal enforcement skeleton.

## 3. Current Status

- ChatPilotImplementationCandidateStatus: IMPLEMENTED_IN_MEMORY_ORCHESTRATOR_ONLY
- ChatExposedThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- EndpointUICreatedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `HISTORICAL_READ_ONLY_CHAT_PILOT_GO_NO_GO_CLOSEOUT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE_ENTRY_CRITERIA.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_CLOSEOUT_DECISION_RECORD.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_TEST_PACK.md`
- `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_CONTRACT_CLOSEOUT.md`
- `HISTORICAL_ANSWER_SYNTHESIS_ENFORCEMENT_SKELETON.md`
- `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_SKELETON.md`

## 5. Orchestrator Candidate Status Model

- `CHAT_PILOT_ORCHESTRATOR_NOT_STARTED`
- `CHAT_PILOT_ORCHESTRATOR_IMPLEMENTED_IN_MEMORY_ONLY`
- `CHAT_PILOT_ORCHESTRATOR_BLOCKED`
- `CHAT_PILOT_ORCHESTRATOR_READY_FOR_CLOSEOUT`
- `CHAT_PILOT_ORCHESTRATOR_REQUIRES_SAFETY_REMEDIATION`
- `CHAT_PILOT_ORCHESTRATOR_REJECTED`
- `CHAT_PILOT_ORCHESTRATOR_SUPERSEDED`

## 6. Skeleton Chain Used

The orchestrator candidate calls:

- `historical_read_only_gated_retrieval_skeleton_service.py`
- `historical_answer_synthesis_enforcement_skeleton_service.py`
- `historical_citation_refusal_enforcement_skeleton_service.py`

Each helper evaluates supplied in-memory metadata only. No live retrieval backend is used. No LLM is called. No DB read/write occurs. No corpus mutation occurs.

## 7. Input Metadata Contract

Accepted supplied metadata fields are `SourceId`, `EvidenceScope`, `AnswerUsePermissionStatus`, `RetrievalEligibilityStatus`, `AnswerMode`, `CitationStatus`, `ProvenanceStatus`, `ConflictStatus`, `SupersessionStatus`, `CurrentTruthPermitted`, `RetrievalEligible`, `ChatEligible`, `CitationRequired`, `CaveatRequired`, `SourceTitle`, `SourceDate`, `UnknownDateMarker`, `RepositoryContext`, `DomainContext`, `AnswerUsePermissionId`, `RetrievalEligibilityId`, and `AnswerModeId`.

## 8. Orchestration Response Contract

The response contract is detailed in `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`. It is an orchestration envelope only and contains no final natural-language chat answer.

## 9. Allowed Envelope Modes

- `READY_CURRENT_TRUTH_ENVELOPE`
- `READY_HISTORICAL_CONTEXT_ENVELOPE`
- `READY_CAVEATED_ENVELOPE`
- `REFUSAL_ENVELOPE`
- `BLOCKED_NO_RUNTIME_ENVELOPE`

## 10. Refusal Preservation

Prior refusal from any skeleton remains refusal through the orchestration response. Missing answer-use permission, missing retrieval eligibility, missing provenance/citation, conflicted evidence without approved caveat readiness, superseded current-truth evidence, not-answerable evidence, and runtime-required metadata must not become a ready current-truth envelope.

## 11. Runtime Boundary Assertions

The orchestrator asserts `LiveLLMCalled: false`, `FinalAnswerGenerated: false`, `ChatExposed: false`, `EndpointUIPresent: false`, `LiveRetrievalPerformed: false`, `CorpusMutationPerformed: false`, `DatabaseReadPerformed: false`, `DatabaseWritePerformed: false`, and `RuntimeBoundaryAsserted: true`.

## 12. No-Side-Effect Guarantees

The candidate does not expose chat, does not create endpoint/UI, does not call a live LLM, does not generate a final chat answer, does not use a live retrieval backend, does not query vector/corpus/database stores, does not read/write a database, does not mutate corpus, does not ingest source content, and does not create Code Evidence.

## 13. What This Candidate Does Not Authorise

- chat exposure;
- public/internal endpoint creation;
- UI creation;
- live LLM calls;
- final natural-language answer generation;
- live retrieval backend;
- vector/corpus search;
- source content ingestion;
- corpus mutation;
- Code Evidence ingestion;
- database reads;
- database writes;
- schema migrations;
- production deployment.

## 14. Recommended Next Slice

Preferred next Minerva slice should be historical read-only chat pilot orchestrator closeout v0.1.

That future slice should decide whether the in-memory orchestrator candidate is complete enough to move toward endpoint/UI planning.

That future slice must still not expose chat unless explicitly approved.

## 15. Progress After This Slice

Minerva has moved from read-only chat pilot go/no-go closeout into in-memory implementation candidate.

Minerva remains pre-chat-exposure.

Narrow safe internal chat pilot readiness remains 100% for governance/skeleton-readiness and now has an initial implementation candidate.

Endpoint/UI/live LLM remain separate future decisions.

## 16. Developer Handoff

Use this candidate only as an internal in-memory orchestration control. Future endpoint/UI planning, live LLM usage, live retrieval, database access, audit/logging runtime, citation rendering runtime, and production exposure require separate explicit approval.

## 17. Contract Hardening Closeout Link

The implementation candidate is now hardened by `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CONTRACT_HARDENING.md`, `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_DECISION_CATALOG.md`, `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CLOSEOUT.md`, and `HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_ENTRY_CRITERIA.md`.

Hardening status: `HARDENED_IN_MEMORY_ONLY`.

No endpoint/UI exists. No live LLM is called. No final answer is generated. No live retrieval backend is used. No DB read/write occurs. No corpus mutation occurs. This is not production chat exposure.
