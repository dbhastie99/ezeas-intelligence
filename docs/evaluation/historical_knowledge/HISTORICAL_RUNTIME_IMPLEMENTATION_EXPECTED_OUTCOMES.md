# Historical Runtime Implementation Expected Outcomes

Version: v0.1

Date: 16 May 2026

## Purpose

This document maps runtime implementation test-matrix scenarios to expected outcomes for a future narrow, read-only Minerva historical chat pilot.

It is documentation/test-planning only and does not implement runtime behaviour.

## Outcome Map

| Outcome | Scenario Mapping | Required Behaviour |
| --- | --- | --- |
| allowed current-truth answer | governed current-truth evidence with promotion, answer-use permission, retrieval eligibility, answer mode, citation/provenance, no conflict, no supersession | future runtime may answer in current-truth mode only after every gate passes |
| allowed historical-context answer | historical-context evidence approved for historical context | answer must carry historical label and must not become current truth |
| allowed caveated answer | caveated current-truth answer with approved caveat | answer must include approved caveat |
| context-only answer | backlog/follow-up context or doctrine/hardening context where approved | answer must remain planned/deferred/follow-up context or doctrine/context only |
| refusal insufficient governed evidence | insufficient governed evidence | refuse rather than infer or fabricate |
| refusal not answer-approved | not answer-approved or answer-use permission missing | refuse before non-refusal answer synthesis |
| refusal retrieval not eligible | retrieval not eligible or retrieval eligibility missing | refuse before exposing evidence to answer synthesis |
| refusal missing provenance | missing citation/provenance, SourceId missing, SourceDate missing without unknown marker, RevocationPath missing, or citation not verified | refuse or require explicit caveat/unknown-date marker; citation must not be fabricated |
| refusal conflicted | conflicted evidence requested for settled/current-truth answer | refuse settled/current-truth answer |
| refusal superseded | superseded evidence requested for current-truth answer | refuse current-truth answer; historical explanation may remain historical only if approved |

## Non-Runtime Boundary

These expected outcomes do not implement runtime retrieval, answer synthesis runtime, citation rendering runtime, chat, endpoint/UI, live LLM calls, database writes, source ingestion, corpus mutation, Code Evidence ingestion, current-truth promotion, runtime answer-use activation, or runtime retrieval activation.

## Read-Only Skeleton Decision Link

The read-only gated retrieval skeleton candidate is `HISTORICAL_READ_ONLY_GATED_RETRIEVAL_SKELETON_CANDIDATE.md`.

Its metadata-only decisions map to these expected outcomes:

- `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL` maps to allowed current-truth answer gate handoff only.
- `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL` maps to allowed historical-context answer gate handoff only.
- `ELIGIBLE_CAVEATED_RETRIEVAL` maps to allowed caveated answer gate handoff only.
- `REFUSE_MISSING_ANSWER_USE_PERMISSION` maps to refusal not answer-approved.
- `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY` maps to refusal retrieval not eligible.
- `REFUSE_MISSING_PROVENANCE` maps to refusal missing provenance.
- `REFUSE_CONFLICTED_EVIDENCE` maps to refusal conflicted.
- `REFUSE_SUPERSEDED_EVIDENCE` maps to refusal superseded.
- `REFUSE_HISTORICAL_CONTEXT_NOT_CURRENT_TRUTH` maps to refusal where historical-context-only evidence is requested as current truth.
- `REFUSE_NOT_ANSWERABLE` maps to refusal not answerable.
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED` maps to explicit runtime-not-implemented blocking.

These are gate decisions only. They do not synthesize answers, render citations, perform retrieval, or expose chat.

## Answer Synthesis Enforcement Skeleton Outcomes

The answer synthesis enforcement skeleton is `HISTORICAL_ANSWER_SYNTHESIS_ENFORCEMENT_SKELETON.md`.

Its metadata-only outcomes map as follows:

- `CURRENT_TRUTH_ANSWER_ALLOWED` maps to allowed current-truth answer mode gate handoff only.
- `HISTORICAL_CONTEXT_ANSWER_ALLOWED` maps to allowed historical-context answer mode gate handoff only and preserves historical label/caveat behaviour.
- `CAVEATED_ANSWER_ALLOWED` maps to allowed caveated answer mode gate handoff only and preserves `CaveatRequired: true`.
- `CONTEXT_ONLY_ANSWER_ALLOWED` maps to context-only answer mode gate handoff only.
- `REFUSE_INSUFFICIENT_GOVERNED_EVIDENCE` maps to refusal insufficient governed evidence.
- `REFUSE_NOT_ANSWER_APPROVED` maps to refusal not answer-approved.
- `REFUSE_RETRIEVAL_NOT_ELIGIBLE` maps to refusal retrieval not eligible.
- `REFUSE_MISSING_PROVENANCE` maps to refusal missing provenance.
- `REFUSE_CONFLICTED_EVIDENCE` maps to refusal conflicted evidence.
- `REFUSE_SUPERSEDED_EVIDENCE` maps to refusal superseded evidence for current-truth answering.
- `REFUSE_CITATION_REQUIRED` maps to refusal pending citation/provenance enforcement.
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED` maps to explicit runtime-not-implemented blocking.

These are gate enforcement decisions only. They do not generate final answers, call a live LLM, perform live retrieval, render citations, expose chat, mutate corpus, or perform DB read/write.

## Citation/Refusal Enforcement Skeleton Outcomes

The citation/refusal enforcement skeleton is `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_SKELETON.md`.

Supporting controls are `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_RESPONSE_CONTRACT.md`, `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_FIXTURE_CATALOG.md`, and `HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_GUARDRAILS.md`.

Its metadata-only outcomes map as follows:

- `CITATION_READY_CURRENT_TRUTH` maps to current-truth citation envelope readiness only.
- `CITATION_READY_HISTORICAL_CONTEXT` maps to historical-context citation envelope readiness only.
- `CITATION_READY_CAVEATED` maps to caveated citation envelope readiness only.
- `REFUSE_MISSING_SOURCE_ID` maps to refusal missing provenance.
- `REFUSE_MISSING_SOURCE_TITLE` maps to refusal missing provenance.
- `REFUSE_MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER` maps to refusal missing provenance or missing unknown-date caveat marker.
- `REFUSE_MISSING_GOVERNANCE_CHAIN` maps to refusal not answer-approved.
- `REFUSE_CONFLICTED_EVIDENCE` maps to refusal conflicted evidence.
- `REFUSE_SUPERSEDED_EVIDENCE` maps to refusal superseded evidence for current-truth answering.
- `REFUSE_NOT_ANSWER_APPROVED` maps to refusal not answer-approved.
- `REFUSE_PRIOR_GATE_REFUSAL` maps to preserved upstream refusal.
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED` maps to explicit runtime-not-implemented blocking.

These are citation/refusal gate enforcement decisions only. They do not generate final answers, call a live LLM, perform live retrieval, render citations, expose chat, mutate corpus, or perform DB read/write.
