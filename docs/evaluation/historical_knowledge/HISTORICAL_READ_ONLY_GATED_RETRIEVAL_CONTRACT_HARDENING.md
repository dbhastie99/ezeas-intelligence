# Historical Read-Only Gated Retrieval Contract Hardening

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document hardens the Minerva historical read-only gated retrieval skeleton contract for deterministic in-memory metadata evaluation.

The hardened contract prepares the next safe implementation step: an answer synthesis enforcement skeleton.

## 2. Scope

This hardening covers the skeleton response contract, decision catalogue, behaviour rules, fixture coverage, runtime boundary assertions, and no-side-effect guarantees.

The skeleton evaluates supplied metadata only. It does not perform live retrieval, query a vector store, query corpus stores, read or write a database, call a live LLM, expose chat, synthesize answers, or render citations.

## 3. Current Status

- RetrievalSkeletonContractStatus: `HARDENED_READ_ONLY_METADATA_ONLY`
- LiveRetrievalPerformed: No
- LiveLLMCalled: No
- CorpusMutationPerformed: No
- DatabaseReadPerformed: No
- DatabaseWritePerformed: No
- EndpointUIPresent: No
- ChatExposed: No

## 4. Response Contract Hardening

Every skeleton response must expose:

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

Required defaults remain:

- `RetrievalGateSkeletonImplemented`: true
- `LiveRetrievalPerformed`: false
- `LiveLLMCalled`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `EndpointUIPresent`: false
- `RuntimeBoundaryAsserted`: true

## 5. Decision Catalogue

The hardened decision catalogue is:

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

`RuntimeActionPermitted` remains No for every decision.

## 6. Behaviour Rules

- Missing or blocked answer-use permission must refuse.
- Missing or blocked retrieval eligibility must refuse.
- Missing or incomplete provenance must refuse.
- Conflicted evidence without approved caveat must refuse.
- Superseded evidence must refuse current-truth retrieval.
- Historical-context-only evidence must not become current-truth retrieval.
- Fully approved current-truth metadata may return eligible current-truth retrieval.
- Approved historical-context metadata may return historical-context eligible retrieval.
- Caveat-required metadata must preserve `CaveatRequired: true`.
- Not-answerable evidence must refuse.
- Runtime not implemented conditions must remain explicit.

## 7. Fixture Coverage

Fixture coverage must include missing answer-use permission, missing retrieval eligibility, missing provenance, conflicted evidence without caveat, superseded current-truth request, historical-context-only evidence requested as current truth, approved current-truth metadata, approved historical-context metadata, caveat-required metadata, not-answerable evidence, and runtime-not-implemented requests.

Fixtures are metadata-only and do not create or alter runtime evidence.

## 8. Runtime Boundary Assertions

The skeleton must always assert:

- live retrieval performed: false;
- live LLM called: false;
- corpus mutation performed: false;
- database read performed: false;
- database write performed: false;
- endpoint/UI present: false;
- runtime boundary asserted: true.

## 9. No-Side-Effect Guarantees

This hardening introduces no source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM call, no DB read/write, no schema migration, no endpoint change, no UI change, no live retrieval backend, no answer synthesis runtime, no citation rendering runtime, no chat exposure, no workforce-platform change, no award-configurator-v1 change, no ezeas-analytics change, no current-truth promotion, no runtime answer-use activation, and no runtime retrieval activation beyond in-memory metadata evaluation.

## 10. What This Hardening Does Not Mean

- live retrieval has been implemented;
- answer synthesis has been implemented;
- citation rendering has been implemented;
- chat has been exposed;
- live LLM can be called;
- corpus can be mutated;
- database can be read or written;
- endpoint or UI exists;
- historical evidence has become answerable current truth.

## 11. Recommended Next Slice

The recommended next slice is the historical answer synthesis enforcement skeleton.

That slice must continue to preserve no live retrieval, no live LLM, no chat exposure, no endpoint/UI, no database read/write, no corpus mutation, and no current-truth promotion unless separately authorized.

## 12. Progress After This Slice

Narrow safe internal chat pilot readiness moves from about 91% to about 93%.

Minerva remains pre-runtime and pre-chat. The current phase is read-only gated retrieval skeleton contract hardening readiness for the later answer synthesis enforcement skeleton.

## 13. Developer Handoff

Future developers should treat this hardening as a deterministic metadata-only contract. It may be used by later answer-synthesis enforcement skeleton planning, but it does not authorize retrieval, answer synthesis, citation rendering, chat, endpoint/UI, live LLM, corpus mutation, database access, or current-truth promotion.
