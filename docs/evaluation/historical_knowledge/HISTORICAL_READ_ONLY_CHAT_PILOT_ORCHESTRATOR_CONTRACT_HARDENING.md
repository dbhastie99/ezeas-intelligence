# Historical Read-Only Chat Pilot Orchestrator Contract Hardening

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document records contract hardening for the Minerva historical read-only chat pilot orchestrator candidate. The hardening confirms the response envelope, fixture coverage, guardrails, refusal propagation, citation readiness propagation, caveat propagation, and no-runtime boundaries for future endpoint/UI planning consideration.

## 2. Scope

Scope is limited to the existing in-memory metadata-only orchestrator candidate and its documentation/tests. The orchestrator chains supplied metadata through existing skeleton helpers and returns an envelope only.

## 3. Current Status

- OrchestratorContractStatus: HARDENED_IN_MEMORY_ONLY
- ChatExposedThisSlice: No
- LiveLLMCalledThisSlice: No
- FinalAnswerGeneratedThisSlice: No
- EndpointUICreatedThisSlice: No
- LiveRetrievalPerformedThisSlice: No
- CorpusMutationPerformedThisSlice: No
- DatabaseReadPerformedThisSlice: No
- DatabaseWritePerformedThisSlice: No

## 4. Inputs Reviewed

- `HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_FIXTURE_CATALOG.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_GUARDRAILS.md`
- `HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE_CLOSEOUT_ENTRY_CRITERIA.md`
- `historical_read_only_chat_pilot_orchestrator_candidate_service.py`

## 5. Response Contract Hardening

The orchestrator response contract is hardened around these required fields:

- `ChatPilotOrchestratorCandidateImplemented`
- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposed`
- `EndpointUIPresent`
- `LiveRetrievalPerformed`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `RetrievalGateResult`
- `AnswerSynthesisGateResult`
- `CitationRefusalGateResult`
- `PilotResponseStatus`
- `PilotResponseMode`
- `RefusalRequired`
- `RefusalReason`
- `CitationReady`
- `CaveatRequired`
- `RuntimeBoundaryAsserted`
- `Guardrails`
- `NonGoals`
- `Explanation`

Required no-runtime defaults remain:

- `ChatPilotOrchestratorCandidateImplemented`: true
- `LiveLLMCalled`: false
- `FinalAnswerGenerated`: false
- `ChatExposed`: false
- `EndpointUIPresent`: false
- `LiveRetrievalPerformed`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `RuntimeBoundaryAsserted`: true

## 6. Decision Catalogue

The decision catalogue is defined in `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_DECISION_CATALOG.md` and includes ready envelopes, refusal envelopes, no-runtime blocked envelopes, and refusal reasons for missing answer-use permission, missing retrieval eligibility, missing provenance, missing citation, conflict, supersession, and not-answerable metadata.

## 7. Fixture Coverage

Fixture coverage proves:

- fully governed current-truth metadata returns `READY_CURRENT_TRUTH_ENVELOPE` without final answer generation;
- historical-context metadata returns `READY_HISTORICAL_CONTEXT_ENVELOPE` and not current truth;
- caveated metadata preserves `CaveatRequired`;
- missing answer-use permission refuses;
- missing retrieval eligibility refuses;
- missing provenance/citation refuses;
- conflicted settled/current-truth evidence refuses unless caveat-ready;
- superseded current-truth evidence refuses;
- prior refusal remains refusal.

## 8. Refusal Propagation

Refusals from retrieval, answer synthesis, and citation/refusal skeleton helpers propagate to `REFUSAL_ENVELOPE`. The orchestrator does not convert prior refusals into ready current-truth envelopes.

## 9. Citation / Caveat Propagation

Citation readiness propagates from the citation/refusal skeleton to `CitationReady`. Caveat requirements propagate to `CaveatRequired`. Caveated-ready conflict metadata can return `READY_CAVEATED_ENVELOPE`; non-caveat-ready conflict metadata refuses.

## 10. Runtime Boundary Assertions

The hardened contract asserts no runtime activity:

- No endpoint/UI exists.
- No live LLM is called.
- No final answer is generated.
- No live retrieval backend is used.
- No DB read/write occurs.
- No corpus mutation occurs.
- This is not production chat exposure.

## 11. No-Side-Effect Guarantees

- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No live LLM calls.
- No database reads.
- No database writes.
- No schema migrations.
- No endpoint/UI.
- No live retrieval backend.
- No final natural-language answer generation.
- No chat exposure.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.
- No current-truth promotion.
- No runtime answer-use permission activation.
- No runtime retrieval eligibility activation.

## 12. What This Hardening Does Not Mean

- chat is exposed;
- endpoint/UI exists;
- live LLM can be called;
- final answers are generated;
- live retrieval backend exists;
- corpus can be queried or mutated;
- database can be read or written;
- historical evidence is answerable current truth by default.

## 13. Recommended Next Slice

The recommended next slice is endpoint/UI planning gate preparation. That future slice may plan endpoint/UI shape only if it preserves all no-runtime approvals and still does not expose chat.

## 14. Progress After This Slice

Progress after this slice: the orchestrator candidate is hardened for in-memory metadata orchestration only and can be used as an input to a future endpoint/UI planning gate. Endpoint/UI scope is still not approved.

## 15. Developer Handoff

Use this hardened contract as a planning artefact and internal service contract only. Any endpoint/UI, live LLM, final answer generation, live retrieval backend, DB read/write, corpus mutation, source ingestion, Code Evidence ingestion, current-truth promotion, runtime answer-use activation, or runtime retrieval activation requires separate explicit approval.
