# Historical Read-Only Chat Pilot Remaining Runtime Boundaries

Version: v0.1

Date: 16 May 2026

## Purpose

This document lists remaining runtime boundaries before any real Minerva historical read-only chat pilot can exist.

## Remaining Boundaries Before Any Real Pilot

- endpoint/UI;
- endpoint/UI planning gate as the next controlled boundary;
- endpoint/UI design pack completed as a planned boundary;
- endpoint/UI implementation gate as a controlled boundary;
- pilot exposure decision gate as the current controlled boundary;
- internal exposure deferred closeout as the current boundary after no explicit exposure approval;
- readiness stream closeout as the current boundary after deferred internal exposure;
- live LLM usage;
- live retrieval backend;
- citation rendering runtime;
- audit/logging runtime;
- pilot access control;
- production exposure prevention;
- monitoring/rollback;
- no corpus mutation;
- no DB write.

## Current Boundary State

No endpoint/UI exists. No live LLM approval exists. No live retrieval backend is connected. No production chat route exists. No citation rendering runtime exists beyond metadata envelope validation. No audit/logging runtime exists beyond design documentation. Pilot implementation candidate remains separate.

Internal exposure deferred closeout is the current boundary after the pilot exposure decision gate because explicit exposure approval is not present. It closes/defer readiness and does not approve exposure.

Readiness stream closeout is the current boundary after internal exposure deferred closeout. It records `CLOSED_DEFERRED_PENDING_EXPOSURE_APPROVAL` and does not approve exposure.

## Non-Authorisation

This boundary record does not authorise chat exposure, live LLM calls, final answer generation, endpoint/UI creation, live retrieval, database reads, database writes, corpus mutation, source content ingestion, Code Evidence ingestion, schema migrations, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

## Implementation Candidate Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE.md` adds an internal in-memory orchestration candidate only. The remaining runtime boundaries are unchanged: endpoint/UI, live LLM usage, live retrieval backend, database access, citation rendering runtime, audit/logging runtime, pilot access control, production exposure prevention, monitoring/rollback, no corpus mutation, and no DB write remain separate future decisions.

## Endpoint/UI Planning Gate Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_GATE.md` is the next controlled boundary after orchestrator closeout. It may consider whether a future endpoint/UI design pack can be planned, but it does not create endpoint/UI, expose chat, call a live LLM, generate final answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

## Endpoint/UI Design Pack Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_DESIGN_PACK.md` completes the endpoint/UI design boundary. It designs request/response envelopes, UI visibility, access-control expectations, audit/logging expectations, and implementation entry criteria only. It does not create endpoint/UI, expose chat, call a live LLM, generate final answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

## Endpoint/UI Implementation Gate Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_GATE.md` is a controlled boundary after endpoint/UI design. It may decide whether a future minimal/internal/read-only/envelope-only endpoint/UI implementation candidate can be considered, but it does not create endpoint/UI, expose chat, call a live LLM, generate final answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, deploy production chat, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

## Minimal Endpoint/UI Candidate Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_IMPLEMENTATION_CANDIDATE.md` creates an internal metadata/envelope candidate service only. It does not create endpoint/UI, register a global route, expose chat, call a live LLM, generate final answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, deploy production chat, promote current truth, activate runtime answer-use permission, activate runtime retrieval eligibility, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

RouteRegisteredGlobally: No.

## Minimal Endpoint/UI Candidate Closeout Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md` closes out the candidate as `CLOSEOUT_COMPLETED_INTERNAL_ENVELOPE_ONLY`. It may support only future pilot exposure decision gate consideration. It does not create endpoint/UI, register a global route, expose production chat, enable public access, enable tenant/customer access, call a live LLM, generate final natural-language answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, promote current truth, activate runtime answer-use permission, activate runtime retrieval eligibility, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

## Pilot Exposure Decision Gate Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_GATE.md` is the current controlled boundary after minimal endpoint/UI candidate closeout. It may decide only what must be true before a future strictly internal exposure candidate may be considered. It does not approve exposure, create endpoint/UI, register a global route, expose production chat, enable public access, enable tenant/customer access, call a live LLM, generate final natural-language answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, promote current truth, activate runtime answer-use permission, activate runtime retrieval eligibility, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

## Internal Exposure Deferred Closeout Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_DEFERRED_CLOSEOUT.md` is the current boundary after the exposure decision gate. Status: `DEFERRED_NO_EXPLICIT_EXPOSURE_APPROVAL`. It records that internal exposure is deferred, no exposure evidence is captured, and future exposure may be reconsidered only if explicit approval and resume criteria are supplied. It does not expose chat, register a global route, enable public access, enable tenant/customer access, call a live LLM, generate final natural-language answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, promote current truth, activate runtime answer-use permission, activate runtime retrieval eligibility, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

## Readiness Stream Closeout Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_READINESS_STREAM_CLOSEOUT.md` is the current stream-level boundary after internal exposure deferred closeout. Status: `CLOSED_DEFERRED_PENDING_EXPOSURE_APPROVAL`. It records that the Minerva read-only chat pilot readiness stream is closed/deferred, explicit exposure approval is absent, and no exposure was enabled. It does not expose chat, register a global route, enable public access, enable tenant/customer access, call a live LLM, generate final natural-language answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, promote current truth, activate runtime answer-use permission, activate runtime retrieval eligibility, or change workforce-platform, award-configurator-v1, or ezeas-analytics.
