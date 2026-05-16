# Historical Chat Pilot Readiness Checklist

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This checklist determines whether the Minerva historical knowledge governance chain is complete enough to move into a later runtime implementation design phase for a narrow, read-only internal chat pilot.

It is a readiness/control artefact only.

## 2. Scope

This checklist applies after source registration, review governance, decision records, deep-review execution planning, findings classification, ingestion/backfill decision control, current-truth promotion control, answer-use permission gating, retrieval eligibility gating, answer-mode contract control, citation/provenance answer readiness, runtime gate chain requirements, and runtime retrieval / answer synthesis gate planning.

This slice does not implement chat, endpoint/UI, retrieval runtime, answer synthesis runtime, citation rendering runtime, live LLM calls, source ingestion, corpus mutation, current-truth promotion, runtime answer-use activation, runtime retrieval activation, or runtime answer-mode activation.

## 3. Current Status

Minerva historical knowledge is in chat pilot readiness control.

Historical sources are not answerable current truth by default.

Answer-use permission does not automatically implement retrieval.

Retrieval eligibility does not automatically expose chat.

Answer-mode contract does not implement answer synthesis runtime.

Citation/provenance contract does not render citations at runtime.

Runtime gate plan does not implement runtime retrieval, answer synthesis, citation rendering, or chat.

Minerva is not exposed for chat yet.

## 4. Readiness Status Model

| Status | Meaning |
| --- | --- |
| `CHAT_PILOT_READINESS_NOT_STARTED` | Chat pilot readiness review has not started. |
| `CHAT_PILOT_READINESS_IN_PROGRESS` | Readiness review is underway but not decided. |
| `CHAT_PILOT_READINESS_BLOCKED` | Readiness review is blocked until recorded blockers are resolved and reassessed. |
| `CHAT_PILOT_READINESS_DEFERRED` | Readiness review is intentionally postponed. |
| `CHAT_PILOT_READY_FOR_IMPLEMENTATION_DESIGN` | Governance is ready to consider a later runtime implementation design slice only. |
| `CHAT_PILOT_READY_FOR_READ_ONLY_PILOT_CANDIDATE` | A later read-only pilot candidate may be considered after implementation design and separate approval. |
| `CHAT_PILOT_NOT_READY_RUNTIME_GATES_MISSING` | Runtime gate design or enforcement requirements are incomplete. |
| `CHAT_PILOT_NOT_READY_ANSWER_SAFETY_GAPS` | Answer safety, refusal, conflict, supersession, or provenance controls are incomplete. |
| `CHAT_PILOT_REJECTED` | Chat pilot readiness is rejected under current controls. |
| `CHAT_PILOT_SUPERSEDED` | This readiness decision has been superseded and must not drive implementation decisions. |

## 5. Governance Chain Readiness Checklist

- source registration model exists;
- review queue exists;
- candidate selection exists;
- decision record exists;
- deep-review execution plan exists;
- findings classification exists;
- ingestion/backfill decision control exists;
- current-truth promotion control exists;
- answer-use permission gate exists;
- retrieval eligibility gate exists;
- answer-mode contract exists;
- citation/provenance answer contract exists;
- runtime retrieval / answer synthesis gate plan exists;
- runtime gate chain requirements exist.

## 6. Runtime Gate Readiness Checklist

- retrieval runtime design is not implemented yet;
- answer synthesis runtime design is not implemented yet;
- citation rendering runtime design is not implemented yet;
- chat endpoint/UI is not implemented yet;
- live LLM usage is not approved;
- implementation design may be considered only after go/no-go decision.

## 7. Answer Safety Checklist

- current-truth answers require current-truth promotion, answer-use permission, retrieval eligibility, answer mode, and citation/provenance;
- historical-context answers must be labelled historical;
- caveated answers must carry caveat;
- backlog/context answers must not be represented as implemented behaviour;
- doctrine/context answers must not be represented as runtime implementation evidence;
- refusal modes exist for insufficient governed evidence, missing gates, conflict, supersession, and missing provenance.

## 8. Citation / Provenance Checklist

- `SourceId` required;
- `SourceTitle` required;
- `SourceDate` or unknown-date marker required;
- `RepositoryContext` required;
- `DomainContext` required;
- `AnswerUsePermissionId` required;
- `RetrievalEligibilityId` required;
- `AnswerModeId` required;
- `EvidenceScope` required;
- `RetrievalMode` required;
- `AnswerMode` required;
- `RevocationPath` required.

## 9. Refusal Behaviour Checklist

- missing answer-use permission refuses;
- missing retrieval eligibility refuses;
- missing answer mode refuses;
- missing citation/provenance refuses;
- conflicted evidence refuses settled/current-truth answer;
- superseded evidence refuses current-truth answer;
- not-answerable evidence refuses;
- refusal must not fabricate citations.

## 10. Conflict / Supersession Checklist

- conflicted evidence must not produce settled/current-truth answers;
- superseded evidence must not produce current-truth answers;
- caveated answer use requires explicit caveat approval;
- historical-context use of conflicted or superseded material must be labelled historical and must remain within approved scope.

## 11. Pilot Scope Checklist

- pilot is internal only;
- pilot is read-only;
- pilot cannot mutate corpus;
- pilot cannot ingest source content;
- pilot cannot create Code Evidence;
- pilot cannot write DB;
- pilot cannot change workforce-platform, award-configurator-v1, or ezeas-analytics;
- pilot cannot answer from unapproved historical evidence;
- pilot must support refusal where governance gates are missing.

## 12. Implementation Entry Criteria

- all governance docs exist;
- runtime gate plan exists;
- answer safety checklist exists;
- citation/provenance checklist exists;
- refusal checklist exists;
- blocker model exists;
- go/no-go decision recorded;
- runtime implementation design is separately approved;
- endpoint/UI remains prohibited until later.

## 13. Stop Conditions

- live LLM call required;
- endpoint/UI required;
- retrieval runtime implementation required;
- answer synthesis runtime implementation required;
- citation rendering runtime required;
- source content ingestion required;
- corpus mutation required;
- Code Evidence ingestion required;
- DB write required;
- unapproved historical answer use required;
- conflict/supersession behaviour unresolved;
- citation/provenance behaviour unresolved;
- refusal behaviour unresolved.

## 14. What This Checklist Does Not Mean

- chat pilot is implemented;
- chat endpoint exists;
- UI exists;
- live LLM can be called;
- retrieval runtime exists;
- answer synthesis runtime exists;
- citation rendering exists;
- historical evidence is answerable by default;
- Minerva is exposed for chat.

## 15. Recommended Next Slice

If go/no-go permits, preferred next Minerva slice should be historical runtime implementation design pack v0.1.

That next slice should design runtime retrieval/answer/citation enforcement but still not expose chat.

If no-go, next slice should remediate blocker(s).

## 16. Progress After This Slice

Minerva has moved from runtime gate planning into chat pilot readiness control.

Minerva remains pre-runtime and pre-chat.

Estimated progress toward narrow safe internal chat pilot is about 81%.

## 17. Developer Handoff

Future developers must treat this checklist as a readiness control only. A `GO_FOR_RUNTIME_IMPLEMENTATION_DESIGN` decision permits only a future implementation design slice unless another explicit approval states otherwise.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no answer synthesis runtime changes, no citation rendering runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, no runtime retrieval eligibility activation, and no runtime answer-mode activation are introduced by this checklist.
