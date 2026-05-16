# Historical Answer Synthesis Enforcement Fixture Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines metadata-only fixtures for answer synthesis enforcement skeleton testing.

## Fixtures

| Fixture | RetrievalDecision | Expected AnswerModeDecision | Boundary |
| --- | --- | --- | --- |
| governed current-truth retrieval output | `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL` | `CURRENT_TRUTH_ANSWER_ALLOWED` | in-memory metadata only |
| governed historical-context retrieval output | `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL` | `HISTORICAL_CONTEXT_ANSWER_ALLOWED` | preserves historical label/caveat behaviour |
| governed caveated retrieval output | `ELIGIBLE_CAVEATED_RETRIEVAL` | `CAVEATED_ANSWER_ALLOWED` | preserves `CaveatRequired: true` |
| context-only retrieval output | context-only metadata | `CONTEXT_ONLY_ANSWER_ALLOWED` | not current truth |
| insufficient governed evidence | unknown or unmatched metadata | `REFUSE_INSUFFICIENT_GOVERNED_EVIDENCE` | no answer allowed |
| not answer-approved retrieval output | `REFUSE_MISSING_ANSWER_USE_PERMISSION` or not-answerable evidence | `REFUSE_NOT_ANSWER_APPROVED` | refusal preserved |
| retrieval not eligible output | `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY` | `REFUSE_RETRIEVAL_NOT_ELIGIBLE` | refusal preserved |
| missing provenance output | `REFUSE_MISSING_PROVENANCE` | `REFUSE_MISSING_PROVENANCE` | refusal preserved |
| conflicted evidence output | `REFUSE_CONFLICTED_EVIDENCE` or conflicted metadata | `REFUSE_CONFLICTED_EVIDENCE` | no settled/current-truth answer |
| superseded evidence output | `REFUSE_SUPERSEDED_EVIDENCE` or superseded current-truth metadata | `REFUSE_SUPERSEDED_EVIDENCE` | no current-truth answer |
| citation required but missing | citation-required metadata without citation/provenance | `REFUSE_CITATION_REQUIRED` | pending citation/provenance enforcement |
| runtime required output | `BLOCKED_RUNTIME_NOT_IMPLEMENTED` or runtime-required metadata | `BLOCKED_RUNTIME_NOT_IMPLEMENTED` | no runtime activation |

## Boundary

Fixtures are in-memory and metadata-only. No live retrieval backend is used. No LLM is called. No final answer generation occurs. No chat is exposed. No endpoint/UI exists. No corpus mutation occurs. No DB read/write occurs.

## Citation/Refusal Fixture Handoff

The answer synthesis fixtures feed the metadata-only citation/refusal enforcement fixtures in:

- `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_SKELETON.md`
- `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_RESPONSE_CONTRACT.md`
- `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_FIXTURE_CATALOG.md`
- `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_GUARDRAILS.md`

Those fixtures add SourceId, SourceTitle, SourceDate or UnknownDateMarker, governance ids, conflict status, supersession status, and caveat readiness checks without performing live retrieval, citation rendering, LLM calls, final answer generation, chat exposure, DB read/write, or corpus mutation.
