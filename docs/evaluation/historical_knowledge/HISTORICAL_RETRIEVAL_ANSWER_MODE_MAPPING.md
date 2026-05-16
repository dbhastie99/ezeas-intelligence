# Historical Retrieval Answer Mode Mapping

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines future retrieval modes and maps evidence scopes to retrieval eligibility statuses.

This is a control document only and does not implement retrieval runtime or chat behaviour.

## 2. Retrieval Modes

| RetrievalMode | Meaning |
| --- | --- |
| `CURRENT_TRUTH_MODE` | Future mode for current-truth answers using only current-truth eligible evidence. |
| `HISTORICAL_CONTEXT_MODE` | Future mode for labelled historical explanation that must not present evidence as current truth. |
| `CAVEATED_ANSWER_MODE` | Future mode where caveats must be preserved in answer synthesis. |
| `BACKLOG_CONTEXT_MODE` | Future mode for backlog/planning context that must not be presented as implemented behaviour. |
| `DOCTRINE_CONTEXT_MODE` | Future mode for governed doctrine or hardening context with source and review status preserved. |
| `EXCLUDED_MODE` | Evidence must not be used for answer generation. |

## 3. Evidence Scope Mapping

| EvidenceScope | RetrievalMode | RetrievalEligibilityStatus |
| --- | --- | --- |
| `HISTORICAL_CONTEXT_ONLY` | `HISTORICAL_CONTEXT_MODE` | `RETRIEVAL_ELIGIBLE_HISTORICAL_CONTEXT_ONLY` |
| `CURRENT_TRUTH` | `CURRENT_TRUTH_MODE` | `RETRIEVAL_ELIGIBLE_CURRENT_TRUTH` |
| `CURRENT_TRUTH_WITH_CAVEAT` | `CAVEATED_ANSWER_MODE` | `RETRIEVAL_ELIGIBLE_WITH_CAVEAT` |
| `BACKLOG_CONTEXT_ONLY` | `BACKLOG_CONTEXT_MODE` | `RETRIEVAL_ELIGIBLE_BACKLOG_CONTEXT_ONLY` |
| `PLATFORM_DOCTRINE_CONTEXT` | `DOCTRINE_CONTEXT_MODE` | `RETRIEVAL_ELIGIBLE_DOCTRINE_CONTEXT_ONLY` |
| `HARDENING_REQUIREMENT_CONTEXT` | `DOCTRINE_CONTEXT_MODE` | `RETRIEVAL_ELIGIBLE_DOCTRINE_CONTEXT_ONLY` or equivalent governed context mode |
| `DEVELOPER_LOG_CONTEXT` | `HISTORICAL_CONTEXT_MODE` | `RETRIEVAL_ELIGIBLE_HISTORICAL_CONTEXT_ONLY` unless separately promoted |
| `NOT_ANSWERABLE` | `EXCLUDED_MODE` | `RETRIEVAL_EXCLUDED_NOT_ANSWERABLE` |
| `SUPERSEDED_NOT_ANSWERABLE` | `EXCLUDED_MODE` | `RETRIEVAL_EXCLUDED_SUPERSEDED` |
| `CONFLICTED_NOT_ANSWERABLE` | `EXCLUDED_MODE` | `RETRIEVAL_EXCLUDED_CONFLICTED` |

## 4. Mode Rules

Current-truth mode may only retrieve current-truth eligible evidence.

Historical-context mode may retrieve historical-context evidence but must not present it as current truth.

Caveated answer mode must carry caveat into future answer contract.

Backlog/context mode must not present backlog items as implemented behaviour.

Doctrine/context mode must preserve source and review status.

Excluded mode must not be used for answer generation.

## 5. Retrieval Modes to Answer Modes

Retrieval modes link to future answer modes through `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_CONTRACT.md`.

| RetrievalMode | Candidate AnswerMode |
| --- | --- |
| `CURRENT_TRUTH_MODE` | `CURRENT_TRUTH_ANSWER` only when current-truth promotion, answer-use permission, retrieval eligibility, provenance, and citation support exist. |
| `HISTORICAL_CONTEXT_MODE` | `HISTORICAL_CONTEXT_ANSWER` with visible historical labelling. |
| `CAVEATED_ANSWER_MODE` | `CAVEATED_CURRENT_TRUTH_ANSWER` only when caveat text or caveat pointer is visible. |
| `BACKLOG_CONTEXT_MODE` | `BACKLOG_CONTEXT_ANSWER` and never implemented behaviour unless separately supported. |
| `DOCTRINE_CONTEXT_MODE` | `DOCTRINE_CONTEXT_ANSWER` or `HARDENING_CONTEXT_ANSWER` within approved scope. |
| `EXCLUDED_MODE` | `REFUSAL_RETRIEVAL_NOT_ELIGIBLE`, `REFUSAL_NOT_ANSWER_APPROVED`, `REFUSAL_CONFLICTED_EVIDENCE`, `REFUSAL_SUPERSEDED_EVIDENCE`, or `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE`. |

This mapping does not implement retrieval runtime, answer synthesis runtime, chat exposure, or runtime answer-mode selection.
