# Historical Runtime Retrieval / Answer Synthesis Gate Plan

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed runtime retrieval / answer synthesis gate plan for Minerva historical knowledge.

The plan maps existing governance controls into future runtime guardrails before any retrieval filtering, answer synthesis gating, citation rendering, or chat pilot can be implemented.

This slice is documentation/control/test hardening only.

## 2. Scope

This plan applies after source registration, review governance, decision records, findings classification, ingestion/backfill decision control, current-truth promotion control where applicable, answer-use permission gating, retrieval eligibility gating, answer-mode contract control, and citation/provenance answer readiness.

Historical sources are not answerable current truth by default. Answer-use permission does not automatically implement retrieval. Retrieval eligibility does not automatically expose chat. Answer-mode contract does not implement answer synthesis runtime. Citation/provenance contract does not render citations at runtime.

Minerva is not exposed for chat in this slice.

## 3. Runtime Gate Planning Status Model

| Status | Meaning |
| --- | --- |
| `RUNTIME_GATE_PLAN_NOT_STARTED` | Runtime gate planning has not started. |
| `RUNTIME_GATE_PLAN_DRAFTED` | Runtime gate planning has been drafted but does not permit implementation. |
| `RUNTIME_GATE_PLAN_BLOCKED` | Runtime gate planning is blocked until recorded blockers are resolved and reassessed. |
| `RUNTIME_GATE_PLAN_DEFERRED` | Runtime gate planning is intentionally postponed. |
| `RUNTIME_GATE_READY_FOR_IMPLEMENTATION_DESIGN` | Runtime gate planning may proceed to implementation design only; runtime implementation remains prohibited. |
| `RUNTIME_GATE_REQUIRES_PILOT_READINESS_REVIEW` | Runtime gate planning requires pilot readiness review before chat work can proceed. |
| `RUNTIME_GATE_REJECTED` | Runtime gate planning is rejected under current controls. |
| `RUNTIME_GATE_SUPERSEDED` | Runtime gate planning has been superseded and must not be used for implementation decisions. |

## 4. Existing Governance Inputs

Future runtime gate design must use these upstream controls:

- `HISTORICAL_ANSWER_USE_PERMISSION_GATE.md`
- `HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md`
- `HISTORICAL_ANSWER_MODE_CONTRACT.md`
- `HISTORICAL_CITATION_PROVENANCE_ANSWER_CONTRACT.md`
- `HISTORICAL_ANSWER_EVIDENCE_CHAIN_REQUIREMENTS.md`
- `HISTORICAL_ANSWER_REFUSAL_POLICY.md`
- `HISTORICAL_RETRIEVAL_EXCLUSION_RULES.md`
- `HISTORICAL_CURRENT_TRUTH_PROMOTION_CONTROL.md`
- `HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`

## 5. Runtime Retrieval Gate Requirements

Runtime retrieval must check retrieval eligibility before exposing evidence to answer synthesis.

Not-answerable, blocked, revoked, superseded, conflicted, missing-provenance, and missing-citation evidence must be excluded from current-truth answer mode.

Historical-context evidence must only be retrievable for historical-context answer mode.

Caveated evidence must carry caveat metadata forward.

Retrieval runtime must preserve `SourceId`, `EvidenceScope`, `RetrievalMode`, `AnswerScope`, provenance status, conflict status, supersession status, and revocation path.

## 6. Runtime Answer-Use Gate Requirements

Answer-use permission must be checked before non-refusal answer modes.

Missing, blocked, rejected, revoked, or superseded answer-use permission must produce refusal or insufficient-governed-evidence behaviour.

Current-truth answer use requires separate current-truth permission and answer-use permission.

Answer-use gate must not override retrieval exclusion rules.

## 7. Runtime Answer-Mode Gate Requirements

Answer mode must be selected from approved answer-mode statuses only.

Answer mode must match retrieval mode and evidence scope.

Historical-context mode must not be rendered as current truth.

Backlog/follow-up context must not be rendered as implemented behaviour.

Doctrine/hardening context must not be rendered as runtime implementation evidence.

Refusal modes must be available when gates fail.

## 8. Runtime Citation / Provenance Gate Requirements

Non-refusal answers must have required citation/provenance fields.

Missing provenance must block chat-answer readiness.

Citation/provenance must include `SourceId`, `SourceTitle`, `SourceDate` or unknown-date marker, `RepositoryContext`, `DomainContext`, `AnswerUsePermissionId`, `RetrievalEligibilityId`, `AnswerModeId`, `EvidenceScope`, `RetrievalMode`, `AnswerMode`, and `RevocationPath`.

Citation rendering is not implemented in this slice.

## 9. Runtime Refusal Gate Requirements

Absent answer-use permission, absent retrieval eligibility, absent answer mode, missing provenance, unresolved conflict, supersession, or missing citation must map to refusal or insufficient governed evidence.

Refusal must not fabricate citations.

Refusal must identify the missing or blocked gate where known.

## 10. Runtime Conflict / Supersession Gate Requirements

Conflicted evidence cannot produce settled/current-truth answers.

Superseded evidence cannot produce current-truth answers.

Caveated answer use requires explicit approval and visible caveat.

Superseded or conflicted material may be historical context only where approved and labelled.

## 11. Chat Pilot Dependency Boundary

This slice does not expose chat.

Chat pilot requires runtime retrieval gate implementation, answer-use gate implementation, answer-mode enforcement, citation/provenance enforcement, refusal behaviour tests, audit/logging plan, and pilot readiness approval.

Chat pilot must be read-only initially.

## 12. Runtime Implementation Stop Conditions

Stop this slice or any implementation derived from it if any of these are required:

- source content ingestion required
- corpus mutation required
- Code Evidence ingestion required
- DB write required
- endpoint/UI required
- live LLM call required
- retrieval runtime change required
- answer synthesis runtime change required
- citation rendering runtime required
- current-truth promotion required
- answer-use runtime activation required
- retrieval eligibility runtime activation required
- unresolved conflict/supersession behaviour
- missing provenance/citation behaviour unresolved

## 13. What This Gate Plan Does Not Mean

Creating this gate plan does not mean runtime retrieval has been implemented.

Creating this gate plan does not mean answer synthesis gating has been implemented.

Creating this gate plan does not mean citation rendering has been implemented.

Creating this gate plan does not mean chat has been exposed.

Creating this gate plan does not mean live LLM can be called.

Creating this gate plan does not mean corpus can be mutated.

Creating this gate plan does not mean evidence has become answerable current truth.

Creating this gate plan does not mean endpoint or UI exists.

## 14. Recommended Next Slice

Preferred next Minerva slice should be historical chat pilot readiness checklist v0.1.

That slice should decide whether the governance chain is ready to move into runtime implementation design.

It must still not expose chat.

## 15. Progress After This Slice

Minerva has moved from citation/provenance answer readiness into runtime retrieval/answer synthesis gate planning.

Minerva remains pre-runtime and pre-chat.

Estimated progress toward narrow safe internal chat pilot is about 77%.

## 16. Developer Handoff

Future developers must treat this plan as a planning/control artefact only. Runtime implementation design must first prove that answer-use permission, retrieval eligibility, answer-mode enforcement, citation/provenance enforcement, refusal behaviour, conflict/supersession behaviour, audit/logging, and pilot readiness approval are all linked.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no answer synthesis runtime changes, no citation rendering runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, no runtime retrieval eligibility activation, and no runtime answer-mode activation are introduced by this plan.
