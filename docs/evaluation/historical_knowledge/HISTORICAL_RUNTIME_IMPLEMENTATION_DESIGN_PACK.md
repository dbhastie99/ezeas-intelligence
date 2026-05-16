# Historical Runtime Implementation Design Pack

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This design pack defines the governed runtime implementation design for a future narrow, read-only Minerva historical chat pilot.

It bridges chat pilot readiness control into future runtime implementation planning before any retrieval runtime, answer synthesis runtime, citation rendering runtime, endpoint/UI, live LLM call, or chat exposure is introduced.

## 2. Scope

This pack covers future retrieval gating, answer-use permission enforcement, answer-mode enforcement, citation/provenance enforcement, refusal behaviour, conflict/supersession handling, and audit/logging.

This pack is documentation/control/test hardening only.

## 3. Runtime Design Status Model

| Status | Meaning |
| --- | --- |
| `RUNTIME_DESIGN_NOT_STARTED` | Runtime implementation design has not started. |
| `RUNTIME_DESIGN_DRAFTED` | Runtime implementation design has been drafted but does not permit runtime code. |
| `RUNTIME_DESIGN_BLOCKED` | Runtime implementation design is blocked until recorded blockers are resolved. |
| `RUNTIME_DESIGN_DEFERRED` | Runtime implementation design is intentionally postponed. |
| `RUNTIME_DESIGN_READY_FOR_TEST_MATRIX` | Design may proceed to a concrete runtime implementation test matrix only. |
| `RUNTIME_DESIGN_READY_FOR_READ_ONLY_SKELETON_CANDIDATE` | Design may later support a read-only skeleton candidate after test matrix approval. |
| `RUNTIME_DESIGN_REJECTED` | Runtime implementation design is rejected under current controls. |
| `RUNTIME_DESIGN_SUPERSEDED` | Runtime implementation design has been superseded and must not drive implementation. |

## 4. Inputs Reviewed

- `HISTORICAL_CHAT_PILOT_READINESS_CHECKLIST.md`
- `HISTORICAL_CHAT_PILOT_GO_NO_GO.md`
- `HISTORICAL_CHAT_PILOT_SCOPE_BOUNDARY.md`
- `HISTORICAL_CHAT_PILOT_IMPLEMENTATION_ENTRY_CRITERIA.md`
- `HISTORICAL_RUNTIME_RETRIEVAL_ANSWER_SYNTHESIS_GATE_PLAN.md`
- `HISTORICAL_RUNTIME_GATE_CHAIN_REQUIREMENTS.md`
- `HISTORICAL_ANSWER_USE_PERMISSION_GATE.md`
- `HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md`
- `HISTORICAL_ANSWER_MODE_CONTRACT.md`
- `HISTORICAL_CITATION_PROVENANCE_ANSWER_CONTRACT.md`
- `HISTORICAL_ANSWER_REFUSAL_POLICY.md`

## 5. Proposed Runtime Gate Architecture

Future chain:

`request/query context -> retrieval gate -> answer-use gate -> answer-mode gate -> citation/provenance gate -> refusal gate -> audit/logging -> answer output or refusal`

The architecture is design only and not implemented.

The future chain must be read-only, deterministic at gate boundaries, and refusal-first when any required gate lacks approved state.

## 6. Retrieval Gate Design Summary

The future retrieval gate must accept request/query context, candidate evidence metadata, retrieval eligibility status, answer-use permission linkage, current-truth status, historical-context status, conflict status, supersession status, and provenance/citation readiness.

It must exclude not-answerable, blocked, revoked, superseded, conflicted, missing-provenance, missing-citation, and out-of-scope evidence from current-truth answer use. It must pass only eligible, scoped, caveated evidence forward to answer-use and answer-mode checks.

## 7. Answer-Use Gate Design Summary

The future answer-use gate must enforce separate answer-use permission before any non-refusal answer mode.

Current-truth answer use requires current-truth promotion, answer-use permission, retrieval eligibility, answer mode, and citation/provenance readiness. Historical-context answer use remains historical and labelled. Missing, blocked, rejected, revoked, or superseded permission must refuse or return insufficient governed evidence.

## 8. Answer-Mode Gate Design Summary

The future answer-mode gate must select only approved answer modes: current-truth, historical-context, caveated, backlog/context, doctrine/context, or refusal.

Historical-context mode must not be rendered as current truth. Backlog/context mode must not be represented as implemented behaviour. Doctrine/context mode must not be represented as runtime implementation evidence.

## 9. Citation / Refusal Gate Design Summary

The future citation/provenance gate must require source and governance identifiers before any non-refusal answer. Missing provenance, missing citation, unresolved conflict, supersession, or not-answerable status must produce refusal or insufficient governed evidence.

Refusal must not fabricate citations and must identify the blocked or missing gate where known.

## 10. Audit / Logging Design Summary

Future audit/logging must record query/request context, retrieval mode, answer mode, evidence ids considered, evidence ids excluded, gate decisions, refusal reason, citation/provenance status, caveat status, and no mutation/no-write pilot status.

The future pilot audit surface must remain read-only and must not write to operational corpus or evidence stores unless a later explicit approval creates a safe audit sink.

## 11. Implementation Boundary

- this slice does not implement retrieval runtime;
- this slice does not implement answer synthesis runtime;
- this slice does not implement citation rendering runtime;
- this slice does not expose chat;
- this slice does not call a live LLM;
- this slice does not create endpoint/UI;
- this slice does not mutate corpus or evidence stores.

## 12. Flow To Test Matrix

This design flows into `HISTORICAL_RUNTIME_IMPLEMENTATION_TEST_MATRIX.md`, not runtime implementation directly.

The test matrix must convert retrieval gating, answer-use enforcement, answer-mode enforcement, citation/provenance enforcement, refusal behaviour, conflict/supersession handling, and audit/logging design into planned scenarios before any read-only skeleton candidate is considered.

Passing through the test matrix does not itself implement retrieval runtime, answer synthesis runtime, citation rendering runtime, endpoint/UI, live LLM calls, database writes, corpus mutation, or chat exposure.

## 13. Stop Conditions

- live LLM call required;
- endpoint/UI required;
- retrieval runtime code required;
- answer synthesis runtime code required;
- citation rendering code required;
- source ingestion required;
- corpus mutation required;
- DB write required;
- unresolved current-truth/answer-use/retrieval eligibility boundary;
- unresolved refusal behaviour;
- unresolved citation/provenance behaviour.

## 14. What This Design Pack Does Not Mean

- runtime retrieval has been implemented;
- answer synthesis gating has been implemented;
- citation rendering has been implemented;
- chat has been exposed;
- live LLM can be called;
- corpus can be mutated;
- evidence has become answerable current truth;
- endpoint or UI exists.

## 15. Recommended Next Slice

Preferred next Minerva slice should be historical runtime implementation test matrix v0.1.

That slice should convert the runtime design into concrete tests before any runtime skeleton is implemented.

If the design reveals blockers, the next slice should remediate blockers instead.

## 16. Progress After This Slice

Minerva has moved from chat pilot readiness control into runtime implementation design.

Minerva remains pre-runtime and pre-chat.

Estimated progress toward narrow safe internal chat pilot is about 85%.

## 17. Developer Handoff

Future developers must treat this design pack as a design/control artefact only. A later implementation test matrix must be approved before a read-only retrieval skeleton or pilot skeleton is considered.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no answer synthesis runtime changes, no citation rendering runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, no runtime retrieval eligibility activation, and no runtime answer-mode activation are introduced by this design pack.
