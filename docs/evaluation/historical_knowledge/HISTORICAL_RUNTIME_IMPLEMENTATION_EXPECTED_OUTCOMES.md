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

- `ELIGIBLE_CURRENT_TRUTH` maps to allowed current-truth answer gate handoff only.
- `ELIGIBLE_HISTORICAL_CONTEXT` maps to allowed historical-context answer gate handoff only.
- `REFUSED_NOT_ELIGIBLE` maps to refusal not answer-approved or retrieval not eligible.
- `REFUSED_MISSING_PROVENANCE` maps to refusal missing provenance.
- `REFUSED_CONFLICTED` maps to refusal conflicted.
- `REFUSED_SUPERSEDED_CURRENT_TRUTH` maps to refusal superseded.
- `REFUSED_HISTORICAL_CONTEXT_ONLY` maps to refusal where historical-context-only evidence is requested as current truth.

These are gate decisions only. They do not synthesize answers, render citations, perform retrieval, or expose chat.
