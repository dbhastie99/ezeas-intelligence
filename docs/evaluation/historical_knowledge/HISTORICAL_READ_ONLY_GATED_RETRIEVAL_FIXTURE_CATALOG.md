# Historical Read-Only Gated Retrieval Fixture Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines metadata-only fixtures for the Minerva historical read-only gated retrieval skeleton candidate.

The fixtures are in-memory test metadata only. They do not create runtime data, ingest source content, query a corpus, query a database, or activate retrieval.

## Fixture Groups

| Fixture | Expected Decision |
| --- | --- |
| missing answer-use permission | `REFUSE_MISSING_ANSWER_USE_PERMISSION` |
| missing retrieval eligibility | `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY` |
| missing provenance | `REFUSE_MISSING_PROVENANCE` |
| conflicted evidence without caveat | `REFUSE_CONFLICTED_EVIDENCE` |
| superseded evidence requested as current truth | `REFUSE_SUPERSEDED_EVIDENCE` |
| historical-context-only evidence requested as current truth | `REFUSE_HISTORICAL_CONTEXT_NOT_CURRENT_TRUTH` |
| approved current-truth metadata | `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL` |
| approved historical-context metadata | `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL` |
| caveat-required metadata | `ELIGIBLE_CAVEATED_RETRIEVAL`, preserves `CaveatRequired: true` |
| not-answerable evidence | `REFUSE_NOT_ANSWERABLE` |
| runtime requested or required | `BLOCKED_RUNTIME_NOT_IMPLEMENTED` |

## Boundary

No live retrieval backend is used. No LLM is called. No chat is exposed. No endpoint/UI exists. No corpus mutation occurs. No DB read/write occurs. Fixture responses are for gate evaluation only.
