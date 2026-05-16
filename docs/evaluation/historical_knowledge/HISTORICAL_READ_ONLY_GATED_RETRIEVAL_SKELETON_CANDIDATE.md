# Historical Read-Only Gated Retrieval Skeleton Candidate

Version: v0.1

Date: 16 May 2026

## Purpose

This document defines the first Minerva historical read-only gated retrieval skeleton candidate.

The skeleton is an in-memory and metadata-only gate evaluator. It accepts supplied metadata and returns a deterministic gate decision for answer-use permission, retrieval eligibility, answer mode, citation/provenance, conflict, supersession, current-truth, historical-context, caveat, and refusal handling.

## Scope

The skeleton service is `app/services/historical_read_only_gated_retrieval_skeleton_service.py`.

It does not retrieve evidence. It evaluates metadata already supplied by a caller.

## Decisions

The candidate supports these deterministic decisions:

- `REFUSED_NOT_ELIGIBLE`
- `REFUSED_MISSING_PROVENANCE`
- `REFUSED_CONFLICTED`
- `REFUSED_SUPERSEDED_CURRENT_TRUTH`
- `REFUSED_HISTORICAL_CONTEXT_ONLY`
- `ELIGIBLE_CURRENT_TRUTH`
- `ELIGIBLE_HISTORICAL_CONTEXT`

Historical sources are not answerable current truth by default. Historical-context-only metadata remains historical-context-only and must not become current truth.

## Runtime Boundary

This skeleton is in-memory and metadata-only. No live retrieval backend is used. No vector search is used. No corpus query is performed. No LLM is called. No chat is exposed. No endpoint/UI exists. No corpus mutation occurs. No DB read/write occurs. The response is for gate evaluation only.

No source content ingestion, no operational corpus mutation, no Code Evidence ingestion, no live LLM calls, no database reads, no database writes, no schema migrations, no endpoint changes, no UI changes, no live retrieval backend, no answer synthesis runtime, no citation rendering runtime, no chat exposure, no workforce-platform changes, no award-configurator-v1 changes, no ezeas-analytics changes, no current-truth promotion, no runtime answer-use permission activation, and no runtime retrieval eligibility activation beyond in-memory metadata evaluation are introduced.
