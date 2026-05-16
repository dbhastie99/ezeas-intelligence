# Historical Read-Only Chat Pilot Remaining Runtime Boundaries

Version: v0.1

Date: 16 May 2026

## Purpose

This document lists remaining runtime boundaries before any real Minerva historical read-only chat pilot can exist.

## Remaining Boundaries Before Any Real Pilot

- endpoint/UI;
- endpoint/UI planning gate as the next controlled boundary;
- endpoint/UI design pack completed as a planned boundary;
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

## Non-Authorisation

This boundary record does not authorise chat exposure, live LLM calls, final answer generation, endpoint/UI creation, live retrieval, database reads, database writes, corpus mutation, source content ingestion, Code Evidence ingestion, schema migrations, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

## Implementation Candidate Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE.md` adds an internal in-memory orchestration candidate only. The remaining runtime boundaries are unchanged: endpoint/UI, live LLM usage, live retrieval backend, database access, citation rendering runtime, audit/logging runtime, pilot access control, production exposure prevention, monitoring/rollback, no corpus mutation, and no DB write remain separate future decisions.

## Endpoint/UI Planning Gate Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_GATE.md` is the next controlled boundary after orchestrator closeout. It may consider whether a future endpoint/UI design pack can be planned, but it does not create endpoint/UI, expose chat, call a live LLM, generate final answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics.

## Endpoint/UI Design Pack Boundary

`HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_DESIGN_PACK.md` completes the endpoint/UI design boundary. It designs request/response envelopes, UI visibility, access-control expectations, audit/logging expectations, and implementation entry criteria only. It does not create endpoint/UI, expose chat, call a live LLM, generate final answers, connect live retrieval, query corpus/vector/database stores, read or write a database, mutate corpus, ingest source content, ingest Code Evidence, migrate schemas, or change workforce-platform, award-configurator-v1, or ezeas-analytics.
