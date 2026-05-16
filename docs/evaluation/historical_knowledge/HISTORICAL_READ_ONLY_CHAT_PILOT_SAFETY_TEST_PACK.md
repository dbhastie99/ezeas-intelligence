# Historical Read-Only Chat Pilot Safety Test Pack

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the Minerva historical read-only chat pilot safety test pack. It proves, through documentation and tests, that the current in-memory skeleton chain preserves critical refusal, citation/provenance, caveat, and runtime-boundary behaviours before a future read-only chat pilot go/no-go closeout can be considered.

## 2. Scope

This pack covers safety scenarios for supplied metadata flowing through the read-only gated retrieval skeleton, answer synthesis enforcement skeleton, and citation/refusal enforcement skeleton.

The scope is safety test pack only. It is in-memory metadata evaluation only and does not ingest source content, mutate operational corpus content, query a corpus, call a live LLM, query a database, expose chat, create endpoint/UI, or generate final natural-language chat answers.

## 3. Current Status

Status: `PILOT_SAFETY_TEST_PACK_READY_FOR_CLOSEOUT`.

The current Minerva historical knowledge model includes the governance chain, runtime implementation design, runtime implementation test matrix, read-only gated retrieval skeleton, retrieval skeleton contract hardening, answer synthesis enforcement skeleton, and citation/refusal enforcement skeleton.

Historical sources are not answerable current truth by default. The skeleton chain evaluates supplied in-memory metadata only. No live retrieval backend is used. No corpus/vector/database stores are queried. No live LLM is called. No chat is exposed. No final natural-language chat answer is generated. No endpoint/UI exists.

## 4. Safety Test Pack Status Model

- `PILOT_SAFETY_TEST_PACK_NOT_STARTED`: safety test pack has not been drafted.
- `PILOT_SAFETY_TEST_PACK_DRAFTED`: safety docs exist but are not yet proven by tests.
- `PILOT_SAFETY_TEST_PACK_BLOCKED`: required safety coverage is incomplete or blocked.
- `PILOT_SAFETY_TEST_PACK_READY_FOR_CLOSEOUT`: required docs and tests exist for future go/no-go closeout consideration.
- `PILOT_SAFETY_TEST_PACK_REQUIRES_REMEDIATION`: safety tests or docs reveal a gap requiring correction.
- `PILOT_SAFETY_TEST_PACK_REJECTED`: safety pack is rejected and cannot support closeout.
- `PILOT_SAFETY_TEST_PACK_SUPERSEDED`: safety pack has been replaced by a later governed version.

## 5. Skeleton Chain Under Test

- `historical_read_only_gated_retrieval_skeleton_service.py`
- `historical_answer_synthesis_enforcement_skeleton_service.py`
- `historical_citation_refusal_enforcement_skeleton_service.py`

## 6. Safety Scenario Groups

- Current-truth eligible metadata flows through retrieval, answer synthesis, and citation/refusal as citation-ready without generating final answer.
- Historical-context metadata remains historical context and does not become current truth.
- Caveated metadata preserves caveat requirement.
- Missing answer-use permission refuses.
- Missing retrieval eligibility refuses.
- Missing provenance refuses.
- Missing citation fields refuse.
- Conflicted evidence refuses settled/current-truth answer.
- Superseded evidence refuses current-truth answer.
- Not-answerable evidence refuses.
- Prior refusal remains refusal through downstream gates.
- Skeleton chain never calls live LLM.
- Skeleton chain never exposes chat.
- Skeleton chain never generates final answer.
- Skeleton chain never queries live retrieval.
- Skeleton chain never reads or writes DB.
- Skeleton chain never mutates corpus.
- Skeleton chain never creates endpoint/UI.

## 7. No-Runtime Assertions

- `LiveRetrievalPerformed`: false
- `LiveLLMCalled`: false
- `FinalAnswerGenerated`: false
- `ChatExposed`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `EndpointUIPresent`: false
- `RuntimeBoundaryAsserted`: true

## 8. Refusal Preservation Requirements

Any upstream refusal must remain a refusal downstream. Missing answer-use permission, missing retrieval eligibility, missing provenance, missing citation fields, conflicted evidence, superseded evidence, not-answerable evidence, runtime-required metadata, and prior refusal states must not be converted into answerable current truth.

## 9. Citation / Provenance Preservation Requirements

Citation-ready means metadata-envelope readiness only. Required citation/provenance fields must be present before a non-refusal envelope can be prepared. Citation rendering runtime is not implemented. Missing `SourceId`, `SourceTitle`, or both `SourceDate` and `UnknownDateMarker` must refuse when citation is required.

## 10. Chat Pilot Boundary

This slice does not expose chat. This slice does not approve endpoint/UI. This slice does not approve live LLM use. Final pilot go/no-go remains separate.

## 11. Stop Conditions

Stop if any change would introduce live retrieval, vector search, corpus query, source content ingestion, operational corpus mutation, Code Evidence ingestion, database read/write, schema migration, endpoint/UI, chat exposure, live LLM call, final answer generation runtime, current-truth promotion, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

## 12. What This Safety Test Pack Does Not Mean

This safety test pack does not mean:

- chat pilot is approved;
- chat is exposed;
- live LLM can be called;
- endpoint/UI exists;
- final answers are generated;
- live retrieval exists;
- corpus can be mutated;
- database can be read or written.

## 13. Recommended Next Slice

Preferred next Minerva slice should be historical read-only chat pilot go/no-go closeout v0.1. That future slice should decide whether the skeleton chain is ready for a pilot implementation candidate. It must still not expose chat unless explicitly approved later.

## 14. Flow Into Go/No-Go Closeout

This safety test pack flows into `HISTORICAL_READ_ONLY_CHAT_PILOT_GO_NO_GO_CLOSEOUT.md`, not chat exposure.

The safety pack can support a closeout decision about whether a future implementation candidate may be considered. It does not itself approve chat, endpoint/UI, live LLM use, live retrieval, database access, corpus mutation, final answer generation, or production exposure.

## 15. Progress After This Slice

Minerva has moved from citation/refusal enforcement skeleton into pilot safety test pack readiness. Estimated progress toward narrow safe internal chat pilot is about 99%.

## 16. Developer Handoff

Use this pack with `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_SCENARIOS.md`, `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_EXPECTED_OUTCOMES.md`, `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_BLOCKER_MODEL.md`, and `HISTORICAL_READ_ONLY_CHAT_PILOT_SAFETY_CLOSEOUT_ENTRY_CRITERIA.md`.

The future closeout may evaluate readiness for a pilot implementation candidate, but this pack itself does not implement chat, endpoint/UI, live retrieval, live LLM use, database access, corpus mutation, source ingestion, current-truth promotion, runtime answer-use activation, or runtime retrieval activation.
