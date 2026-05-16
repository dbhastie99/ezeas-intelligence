# Historical Retrieval Exclusion Rules

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines exclusion rules for future Minerva historical retrieval eligibility decisions.

Excluded evidence must not be used for current-truth answer generation.

This is a control document only. It does not implement retrieval runtime, expose chat, call a live LLM, mutate corpus, ingest source content, write a database, create endpoints, or create UI changes.

## 2. Exclusion Rules

Not-answerable evidence is excluded from answer retrieval.

Superseded evidence is excluded from current-truth retrieval.

Conflicted evidence is excluded from settled-answer retrieval.

Blocked answer-use permission excludes retrieval.

Revoked answer-use permission excludes retrieval.

Missing provenance excludes retrieval.

Unresolved cross-check can block or caveat retrieval depending on approved scope.

Missing citation requirement excludes chat-answer retrieval.

## 3. Required Excluded Statuses

| Evidence condition | Required retrieval status |
| --- | --- |
| `NOT_ANSWERABLE` | `RETRIEVAL_EXCLUDED_NOT_ANSWERABLE` |
| `SUPERSEDED_NOT_ANSWERABLE` | `RETRIEVAL_EXCLUDED_SUPERSEDED` |
| `CONFLICTED_NOT_ANSWERABLE` | `RETRIEVAL_EXCLUDED_CONFLICTED` |
| Blocked answer-use permission | `RETRIEVAL_ELIGIBILITY_BLOCKED` or excluded status |
| Revoked answer-use permission | `RETRIEVAL_REVOKED` |
| Missing provenance | `RETRIEVAL_ELIGIBILITY_BLOCKED` |
| Missing citation requirement | `RETRIEVAL_ELIGIBILITY_BLOCKED` for chat-answer retrieval |

## 4. Current-Truth Boundary

Excluded evidence must not be used for current-truth answer generation.

Superseded evidence must not override newer repository truth.

Conflicted evidence must not be presented as settled truth.

Historical explanation use may be allowed only when separately approved, labelled historical, and not presented as current truth.

## 5. Excluded Evidence to Refusal Answer Modes

Excluded evidence maps to refusal answer modes under `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_CONTRACT.md`.

`RETRIEVAL_EXCLUDED_NOT_ANSWERABLE` maps to `REFUSAL_NOT_ANSWER_APPROVED` or `REFUSAL_INSUFFICIENT_GOVERNED_EVIDENCE`.

`RETRIEVAL_EXCLUDED_SUPERSEDED` maps to `REFUSAL_SUPERSEDED_EVIDENCE` for current-truth answers.

`RETRIEVAL_EXCLUDED_CONFLICTED` maps to `REFUSAL_CONFLICTED_EVIDENCE` for settled answers unless a caveated mode is explicitly approved.

Missing, blocked, revoked, or otherwise not eligible retrieval maps to `REFUSAL_RETRIEVAL_NOT_ELIGIBLE`.

This mapping does not expose chat, implement retrieval runtime, implement answer synthesis runtime, call a live LLM, mutate corpus, or make excluded evidence answerable.
