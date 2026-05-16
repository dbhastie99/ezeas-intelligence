# Historical Read-Only Gated Retrieval Fixture Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines metadata-only fixtures for the Minerva historical read-only gated retrieval skeleton candidate.

The fixtures are in-memory test metadata only. They do not create runtime data, ingest source content, query a corpus, query a database, or activate retrieval.

## Fixture Groups

| Fixture | Expected Decision |
| --- | --- |
| missing answer-use permission | `REFUSED_NOT_ELIGIBLE` |
| missing retrieval eligibility | `REFUSED_NOT_ELIGIBLE` |
| missing provenance | `REFUSED_MISSING_PROVENANCE` |
| conflicted evidence without caveat | `REFUSED_CONFLICTED` |
| superseded evidence requested as current truth | `REFUSED_SUPERSEDED_CURRENT_TRUTH` |
| historical-context-only evidence requested as current truth | `REFUSED_HISTORICAL_CONTEXT_ONLY` |
| approved current-truth metadata | `ELIGIBLE_CURRENT_TRUTH` |
| approved historical-context metadata | `ELIGIBLE_HISTORICAL_CONTEXT` |
| caveat-required metadata | preserves `CaveatRequired: true` |

## Boundary

No live retrieval backend is used. No LLM is called. No chat is exposed. No endpoint/UI exists. No corpus mutation occurs. No DB read/write occurs. Fixture responses are for gate evaluation only.
