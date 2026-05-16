# Historical Citation/Refusal Enforcement Fixture Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines metadata-only fixtures for citation/refusal enforcement skeleton testing.

## Fixtures

| Fixture | Input shape | Expected CitationRefusalDecision | Boundary |
| --- | --- | --- | --- |
| complete current-truth citation metadata | `AllowedAnswerMode: CURRENT_TRUTH` with source and governance ids | `CITATION_READY_CURRENT_TRUTH` | prepares citation envelope only |
| complete historical-context citation metadata | `AllowedAnswerMode: HISTORICAL_CONTEXT` with source and governance ids | `CITATION_READY_HISTORICAL_CONTEXT` | preserves historical label/caveat behaviour |
| complete caveated citation metadata | `AllowedAnswerMode: CAVEATED` or `CaveatRequired: true` with ready caveat | `CITATION_READY_CAVEATED` | preserves caveat metadata |
| missing source id | citation-required metadata without `SourceId` | `REFUSE_MISSING_SOURCE_ID` | no citation-ready envelope |
| missing source title | citation-required metadata without `SourceTitle` | `REFUSE_MISSING_SOURCE_TITLE` | no citation-ready envelope |
| missing source date or unknown marker | citation-required metadata without `SourceDate` and `UnknownDateMarker` | `REFUSE_MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER` | refusal or caveat requirement |
| missing governance chain | non-refusal metadata missing answer-use, retrieval-eligibility, or answer-mode ids | `REFUSE_MISSING_GOVERNANCE_CHAIN` | no answer-use activation |
| conflicted evidence without caveat ready | `ConflictStatus: CONFLICTED` or `UNRESOLVED` and `CaveatReady: false` | `REFUSE_CONFLICTED_EVIDENCE` | conflicted evidence blocked |
| superseded current truth | `SupersessionStatus: SUPERSEDED` with current-truth mode | `REFUSE_SUPERSEDED_EVIDENCE` | no current-truth answer |
| not answer approved | missing or refusal-like answer mode metadata | `REFUSE_NOT_ANSWER_APPROVED` | no answer allowed |
| prior gate refusal | `RefusalRequired: true` with `RefusalReason` | `REFUSE_PRIOR_GATE_REFUSAL` | refusal preserved |
| runtime required metadata | runtime, live LLM, chat, endpoint/UI, DB, or retrieval flags requested | `BLOCKED_RUNTIME_NOT_IMPLEMENTED` | no runtime activation |

## Boundary

Fixtures are in-memory and metadata-only. No live retrieval backend is used. No LLM is called. No final answer generation occurs. No final natural-language chat answer is generated. No chat is exposed. No endpoint/UI exists. No corpus mutation occurs. No DB read/write occurs.
