# Historical Read-Only Chat Pilot Safety Scenarios

Version: v0.1

Date: 16 May 2026

## Purpose

This document maps required safety scenarios to expected retrieval, synthesis, and citation/refusal behaviour for the Minerva historical in-memory skeleton chain.

## Scenario Matrix

| Scenario | Retrieval expected behaviour | Synthesis expected behaviour | Citation/refusal expected behaviour |
| --- | --- | --- | --- |
| current-truth eligible metadata | `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL`; read-only metadata-only; no live retrieval | `CURRENT_TRUTH_ANSWER_ALLOWED`; no final answer generated | `CITATION_READY_CURRENT_TRUTH`; citation-ready metadata envelope only |
| historical-context metadata | `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL`; historical context only | `HISTORICAL_CONTEXT_ANSWER_ALLOWED`; current truth not allowed | `CITATION_READY_HISTORICAL_CONTEXT` or `CITATION_READY_CAVEATED` when the retrieval gate preserves a required caveat; historical context remains labelled and never becomes current truth |
| caveated metadata | `ELIGIBLE_CAVEATED_RETRIEVAL`; `CaveatRequired` preserved | `CAVEATED_ANSWER_ALLOWED`; caveat requirement preserved | `CITATION_READY_CAVEATED`; caveat readiness required |
| missing answer-use permission | `REFUSE_MISSING_ANSWER_USE_PERMISSION` | `REFUSE_NOT_ANSWER_APPROVED` | prior refusal remains refusal |
| missing retrieval eligibility | `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY` | `REFUSE_RETRIEVAL_NOT_ELIGIBLE` | prior refusal remains refusal |
| missing provenance | `REFUSE_MISSING_PROVENANCE` | `REFUSE_MISSING_PROVENANCE` or citation-required refusal | prior refusal remains refusal |
| missing citation fields | retrieval may be eligible only if provenance metadata is otherwise supplied | `REFUSE_CITATION_REQUIRED` when source/provenance is incomplete | `REFUSE_MISSING_SOURCE_ID`, `REFUSE_MISSING_SOURCE_TITLE`, or `REFUSE_MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER` |
| conflicted evidence | `REFUSE_CONFLICTED_EVIDENCE` unless approved caveat metadata is present | `REFUSE_CONFLICTED_EVIDENCE`; no settled/current-truth answer | `REFUSE_CONFLICTED_EVIDENCE` unless required caveat is ready |
| superseded evidence | `REFUSE_SUPERSEDED_EVIDENCE` for current truth | `REFUSE_SUPERSEDED_EVIDENCE` for current truth | `REFUSE_SUPERSEDED_EVIDENCE` for current truth |
| not-answerable evidence | `REFUSE_NOT_ANSWERABLE` | `REFUSE_NOT_ANSWER_APPROVED` | prior refusal remains refusal |
| prior refusal | refusal response is passed downstream | refusal remains refusal | `REFUSE_PRIOR_GATE_REFUSAL` |
| no-runtime cases | `LiveRetrievalPerformed false`; no DB read/write; no corpus mutation | `LiveLLMCalled false`; `FinalAnswerGenerated false`; `ChatExposed false` | `FinalAnswerGenerated false`; `LiveLLMCalled false`; `EndpointUIPresent false` |
| skeleton chain never calls live LLM | no live LLM call | no live LLM call | no live LLM call |
| skeleton chain never exposes chat | no chat exposure | no chat exposure | no chat exposure |
| skeleton chain never generates final answer | no answer generation | no final answer generated | no final answer generated |
| skeleton chain never queries live retrieval | no live retrieval backend | no retrieval runtime call | no retrieval runtime call |
| skeleton chain never reads or writes DB | no database read/write | no database read/write | no database read/write |
| skeleton chain never mutates corpus | no corpus mutation | no corpus mutation | no corpus mutation |
| skeleton chain never creates endpoint/UI | no endpoint/UI | no endpoint/UI | no endpoint/UI |

## Boundary

These scenarios are metadata-only tests. They do not call a live LLM, generate final natural-language chat answers, perform live retrieval, query a database, expose chat, mutate corpus, ingest source content, create Code Evidence, or activate runtime answer-use/retrieval eligibility beyond in-memory metadata evaluation.
