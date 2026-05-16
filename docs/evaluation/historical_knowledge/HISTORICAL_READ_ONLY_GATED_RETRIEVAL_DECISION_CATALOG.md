# Historical Read-Only Gated Retrieval Decision Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines the hardened decision values for the Minerva historical read-only gated retrieval skeleton.

All decisions are metadata-only gate decisions. `RuntimeActionPermitted` is No for every decision.

## Catalog

| Decision | RetrievalAllowed | CurrentTruthAllowed | HistoricalContextAllowed | CaveatRequired | RefusalRequired | RuntimeActionPermitted | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL` | Yes | Yes | No | As supplied | No | No | Metadata is fully approved for current-truth retrieval gate handoff only. |
| `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL` | Yes | No | Yes | Yes or as supplied | No | No | Metadata is approved for historical-context retrieval gate handoff only and must not become current truth. |
| `ELIGIBLE_CAVEATED_RETRIEVAL` | Yes | As supplied | As supplied | Yes | No | No | Metadata is eligible only with the caveat requirement preserved. |
| `REFUSE_MISSING_ANSWER_USE_PERMISSION` | No | No | No | As supplied | Yes | No | Answer-use permission is missing or blocked. |
| `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY` | No | No | No | As supplied | Yes | No | Retrieval eligibility is missing or blocked. |
| `REFUSE_MISSING_PROVENANCE` | No | No | No | As supplied | Yes | No | Citation or provenance metadata is missing or incomplete. |
| `REFUSE_CONFLICTED_EVIDENCE` | No | No | No | Yes | Yes | No | Conflicted evidence lacks an approved caveat. |
| `REFUSE_SUPERSEDED_EVIDENCE` | No | No | Historical only if separately approved in a future runtime | As supplied | Yes | No | Superseded evidence cannot support current-truth retrieval. |
| `REFUSE_HISTORICAL_CONTEXT_NOT_CURRENT_TRUTH` | No | No | Yes | Yes | Yes | No | Historical-context-only evidence must not become current-truth retrieval. |
| `REFUSE_NOT_ANSWERABLE` | No | No | No | As supplied | Yes | No | Evidence is explicitly not answerable or no approved retrieval path exists. |
| `BLOCKED_RUNTIME_NOT_IMPLEMENTED` | No | No | No | As supplied | Yes | No | Runtime retrieval/backend/LLM/DB/endpoint behaviour is not implemented. |

## Boundary

This decision catalog does not implement live retrieval, vector search, corpus query, database reads or writes, live LLM calls, endpoint/UI, chat, answer synthesis runtime, citation rendering runtime, corpus mutation, Code Evidence ingestion, source ingestion, or current-truth promotion.

## Answer Synthesis Enforcement Handoff

The answer synthesis enforcement skeleton consumes these decisions as supplied metadata only:

- `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL` -> `CURRENT_TRUTH_ANSWER_ALLOWED`
- `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL` -> `HISTORICAL_CONTEXT_ANSWER_ALLOWED`
- `ELIGIBLE_CAVEATED_RETRIEVAL` -> `CAVEATED_ANSWER_ALLOWED`
- `REFUSE_MISSING_ANSWER_USE_PERMISSION` -> `REFUSE_NOT_ANSWER_APPROVED`
- `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY` -> `REFUSE_RETRIEVAL_NOT_ELIGIBLE`
- `REFUSE_MISSING_PROVENANCE` -> `REFUSE_MISSING_PROVENANCE`
- `REFUSE_CONFLICTED_EVIDENCE` -> `REFUSE_CONFLICTED_EVIDENCE`
- `REFUSE_SUPERSEDED_EVIDENCE` -> `REFUSE_SUPERSEDED_EVIDENCE`
- `REFUSE_NOT_ANSWERABLE` -> `REFUSE_NOT_ANSWER_APPROVED`
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED` -> `BLOCKED_RUNTIME_NOT_IMPLEMENTED`

The handoff is not final answer generation, not chat, not citation rendering, and not runtime activation.
