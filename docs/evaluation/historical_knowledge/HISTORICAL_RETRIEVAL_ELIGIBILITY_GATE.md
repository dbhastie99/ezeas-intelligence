# Historical Retrieval Eligibility Gate

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed retrieval eligibility gate for Minerva historical knowledge.

The gate controls whether evidence that has already passed answer-use permission may be considered by future retrieval for current-truth answer mode, historical-context mode, caveated answer mode, backlog/context mode, doctrine/context mode, or excluded/refused modes.

This slice defines the control model only. It does not implement retrieval runtime, change answer synthesis, expose chat, call a live LLM, ingest content, mutate corpus, promote current truth, activate answer use at runtime, or activate retrieval eligibility at runtime.

## 2. Scope

This gate applies after answer-use permission has been recorded and, where current-truth retrieval is requested, after current-truth promotion has explicitly permitted current-truth use.

Historical sources are not answerable current truth by default. Current-truth promotion does not automatically permit answer use. Answer-use permission does not automatically implement retrieval. Retrieval eligibility does not expose chat.

## 3. Retrieval Eligibility Status Model

| Status | Meaning |
| --- | --- |
| `RETRIEVAL_ELIGIBILITY_NOT_REQUESTED` | No retrieval eligibility decision has been requested. |
| `RETRIEVAL_ELIGIBILITY_BLOCKED` | Retrieval eligibility is blocked until recorded blockers are resolved and reassessed. |
| `RETRIEVAL_ELIGIBILITY_DEFERRED` | Retrieval eligibility is intentionally postponed; conservative defaults remain No. |
| `RETRIEVAL_ELIGIBILITY_REJECTED` | Retrieval eligibility is rejected under current controls. |
| `RETRIEVAL_ELIGIBLE_HISTORICAL_CONTEXT_ONLY` | Evidence may be retrieved only for labelled historical-context mode. |
| `RETRIEVAL_ELIGIBLE_CURRENT_TRUTH` | Evidence may be retrieved for current-truth mode only within approved scope. |
| `RETRIEVAL_ELIGIBLE_WITH_CAVEAT` | Evidence may be retrieved only with required caveats preserved. |
| `RETRIEVAL_ELIGIBLE_BACKLOG_CONTEXT_ONLY` | Evidence may be retrieved only for backlog/planning context and not as implemented behaviour. |
| `RETRIEVAL_ELIGIBLE_DOCTRINE_CONTEXT_ONLY` | Evidence may be retrieved only for governed doctrine/hardening context. |
| `RETRIEVAL_EXCLUDED_NOT_ANSWERABLE` | Evidence must not be used for answer retrieval. |
| `RETRIEVAL_EXCLUDED_SUPERSEDED` | Evidence is superseded and excluded from current-truth retrieval. |
| `RETRIEVAL_EXCLUDED_CONFLICTED` | Evidence is conflicted and excluded from settled-answer retrieval. |
| `RETRIEVAL_REVOKED` | Prior retrieval eligibility has been revoked and must not be used. |

## 4. Preconditions Before Retrieval Eligibility Can Be Considered

Retrieval eligibility must not be considered unless all required controls exist or are explicitly blocked/deferred with rationale:

- `SourceId` exists.
- `AnswerUsePermissionId` exists.
- `AnswerUsePermissionStatus` is recorded.
- `EvidenceScope` is recorded.
- `AnswerScope` is recorded.
- `CurrentTruthPromotionId` exists where current-truth retrieval is requested.
- `CurrentTruthPermitted` is Yes where current-truth retrieval is requested.
- `AnswerUsePermitted` is Yes for the requested mode.
- Source provenance exists.
- Cross-check status is recorded.
- Conflict status is resolved or explicitly caveated.
- Supersession status is resolved.
- Citation/provenance requirement is defined.
- Revocation/removal path is defined.
- Retrieval runtime has not yet been enabled in this slice.

## 5. Answer-Use Permission Dependency

Answer-use permission is required before retrieval eligibility can be approved.

Answer-use permission alone does not implement retrieval.

Answer-use permission alone does not expose chat.

Retrieval eligibility must respect `EvidenceScope` and `AnswerScope` from the answer-use permission record.

Absent, blocked, revoked, superseded, or rejected answer-use permission must block retrieval eligibility.

## 6. Current-Truth Dependency

Current-truth retrieval requires `CurrentTruthPermitted` Yes.

Historical-context retrieval does not become current-truth retrieval.

Current-truth retrieval must not override newer repository truth.

Current-truth retrieval must be revocable.

## 7. Evidence Scope to Retrieval Mode Mapping

| EvidenceScope | RetrievalEligibilityStatus |
| --- | --- |
| `HISTORICAL_CONTEXT_ONLY` | `RETRIEVAL_ELIGIBLE_HISTORICAL_CONTEXT_ONLY` |
| `CURRENT_TRUTH` | `RETRIEVAL_ELIGIBLE_CURRENT_TRUTH` |
| `CURRENT_TRUTH_WITH_CAVEAT` | `RETRIEVAL_ELIGIBLE_WITH_CAVEAT` |
| `BACKLOG_CONTEXT_ONLY` | `RETRIEVAL_ELIGIBLE_BACKLOG_CONTEXT_ONLY` |
| `PLATFORM_DOCTRINE_CONTEXT` | `RETRIEVAL_ELIGIBLE_DOCTRINE_CONTEXT_ONLY` |
| `HARDENING_REQUIREMENT_CONTEXT` | `RETRIEVAL_ELIGIBLE_DOCTRINE_CONTEXT_ONLY` or equivalent governed context mode |
| `DEVELOPER_LOG_CONTEXT` | `RETRIEVAL_ELIGIBLE_HISTORICAL_CONTEXT_ONLY` unless separately promoted |
| `NOT_ANSWERABLE` | `RETRIEVAL_EXCLUDED_NOT_ANSWERABLE` |
| `SUPERSEDED_NOT_ANSWERABLE` | `RETRIEVAL_EXCLUDED_SUPERSEDED` |
| `CONFLICTED_NOT_ANSWERABLE` | `RETRIEVAL_EXCLUDED_CONFLICTED` |

## 8. Retrieval Mode Rules

Current-truth mode may only retrieve current-truth eligible evidence.

Historical-context mode may retrieve historical-context evidence but must not present it as current truth.

Caveated mode must carry caveat into future answer contract.

Backlog/context mode must not present backlog items as implemented behaviour.

Doctrine/context mode must preserve source and review status.

Excluded modes must not be used for answer generation.

## 9. Exclusion Rules

Not-answerable evidence is excluded from answer retrieval.

Superseded evidence is excluded from current-truth retrieval.

Conflicted evidence is excluded from settled-answer retrieval.

Blocked or revoked answer-use permission excludes retrieval.

Missing provenance excludes retrieval.

Unresolved cross-check can block or caveat retrieval depending on approved scope.

Missing citation requirement excludes chat-answer retrieval.

## 10. Conflict / Supersession Handling

Conflicted evidence defaults to excluded from current-truth and settled-answer modes.

Superseded evidence defaults to excluded from current-truth mode.

Historical explanation use may be allowed only if labelled historical and not current truth.

Caveats must be preserved for future answer synthesis.

## 11. Citation / Provenance Requirements

Every retrieval eligibility record must preserve:

- `SourceId`
- `SourceTitle`
- `SourceDate` or unknown-date marker
- `RepositoryContext`
- `DomainContext`
- `AnswerUsePermissionId`
- `RetrievalEligibilityId`
- `EvidenceScope`
- `RetrievalMode`
- `CitationRequired`
- `CaveatRequired`
- `Reviewer/Approver`
- `ApprovedAtUtc`
- `RevocationPath`
- `Notes`

## 12. Insufficient Evidence / Refusal Boundary

If retrieval eligibility is absent, future Minerva answer logic must refuse or state insufficient governed evidence.

If retrieval eligibility is blocked, future Minerva answer logic must refuse or state evidence is not retrieval-approved.

If only historical-context evidence exists, future Minerva answer logic must not answer as current truth.

If evidence is conflicted, future Minerva answer logic must not answer as settled truth.

## 13. Chat Exposure Boundary

This slice does not expose Minerva chat.

This slice does not change answer synthesis.

This slice does not call a live LLM.

Chat exposure requires later answer-mode contract, refusal policy, citation/provenance answer contract, and pilot-readiness gate.

## 14. Answer-Mode Contract Dependency

Retrieval eligibility flows into the answer-mode contract at `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_CONTRACT.md`.

Retrieval eligibility helps determine which answer modes may be considered, but it does not itself select answer mode at runtime.

Retrieval eligibility alone does not implement answer synthesis, answer-mode enforcement, citation/provenance enforcement, refusal behaviour, or chat exposure.

Absent, blocked, revoked, superseded, conflicted, or excluded retrieval eligibility must map to refusal or insufficient-evidence answer modes under the answer-mode contract.

## 14a. Citation / Provenance Dependency

Retrieval eligibility must flow into answer mode and citation/provenance before chat use.

Retrieval eligibility must be traceable in `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_ANSWER_CONTRACT.md` and `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_EVIDENCE_CHAIN_REQUIREMENTS.md`.

Retrieval eligibility alone does not render citations, satisfy provenance, implement answer synthesis, or expose chat.

## 14b. Runtime Enforcement Before Chat

Retrieval eligibility must be runtime-enforced before chat exposure.

Retrieval eligibility records are planning inputs only until a later runtime gate implementation design and pilot readiness approval exist.

## 15. Runtime Boundary

This slice does not implement retrieval filtering.

This slice does not modify retrieval code.

This slice does not activate answer-use permission at runtime.

This slice does not activate retrieval eligibility at runtime.

This slice does not mutate corpus or evidence stores.

## 16. Blocker Handling

Blocked decisions must record one or more blocker codes and the required resolution path:

- `MISSING_SOURCE_ID`
- `MISSING_ANSWER_USE_PERMISSION`
- `ANSWER_USE_NOT_APPROVED`
- `ANSWER_USE_REVOKED`
- `ANSWER_USE_SUPERSEDED`
- `MISSING_CURRENT_TRUTH_PROMOTION`
- `CURRENT_TRUTH_NOT_APPROVED`
- `PROVENANCE_INCOMPLETE`
- `CROSS_CHECK_INCOMPLETE`
- `CONFLICT_UNRESOLVED`
- `SUPERSESSION_UNRESOLVED`
- `EVIDENCE_SCOPE_UNDEFINED`
- `ANSWER_SCOPE_UNDEFINED`
- `RETRIEVAL_MODE_UNDEFINED`
- `CITATION_REQUIREMENT_UNDEFINED`
- `REVOCATION_PATH_MISSING`
- `RETRIEVAL_RUNTIME_NOT_IMPLEMENTED`
- `CHAT_CONTRACT_NOT_IMPLEMENTED`

Resolving a blocker only permits reassessment of the retrieval eligibility decision. It does not enable retrieval runtime, expose chat, call a live LLM, or make evidence answerable.

## 17. What Retrieval Eligibility Gate Does Not Mean

Creating retrieval eligibility docs does not expose chat.

Retrieval eligibility gate does not call a live LLM.

Retrieval eligibility gate does not change retrieval runtime.

Retrieval eligibility gate does not mutate corpus.

Retrieval eligibility gate does not ingest source content.

Retrieval eligibility gate does not promote current truth.

Retrieval eligibility gate does not activate answer use at runtime.

Retrieval eligibility gate does not write to a database.

Retrieval eligibility gate does not create endpoint or UI changes.

## 18. Developer Handoff

Future developers must use this gate after answer-use permission and before any runtime retrieval filtering, answer-mode contract, citation/provenance answer contract, refusal policy, pilot-readiness gate, or chat exposure.

Use `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_TEMPLATE.md` for individual eligibility records, `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_BLOCKER_MODEL.md` for blockers, `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ANSWER_MODE_MAPPING.md` for retrieval-mode interpretation, and `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_EXCLUSION_RULES.md` for exclusion policy.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database writes, no schema migrations, no endpoint changes, no UI changes, no retrieval runtime changes, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, and no runtime retrieval eligibility activation are introduced by this gate.
