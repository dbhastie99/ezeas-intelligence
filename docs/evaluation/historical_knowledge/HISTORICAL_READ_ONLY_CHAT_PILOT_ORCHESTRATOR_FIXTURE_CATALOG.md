# Historical Read-Only Chat Pilot Orchestrator Fixture Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines metadata-only fixtures for testing the in-memory orchestrator candidate.

## Fixtures

| FixtureId | Scenario | Expected envelope |
| --- | --- | --- |
| HROC-CT-001 | Fully governed current-truth metadata with citation/provenance and governance identifiers | `READY_CURRENT_TRUTH_ENVELOPE` with `FinalAnswerGenerated: false` |
| HROC-HC-001 | Historical-context metadata with current-truth permission false | `READY_HISTORICAL_CONTEXT_ENVELOPE`; not current truth |
| HROC-CAV-001 | Caveated governed metadata | `READY_CAVEATED_ENVELOPE` with `CaveatRequired: true` |
| HROC-AUP-001 | Missing answer-use permission | `REFUSAL_ENVELOPE` |
| HROC-RET-001 | Missing retrieval eligibility | `REFUSAL_ENVELOPE` |
| HROC-CIT-001 | Missing provenance/citation | `REFUSAL_ENVELOPE` |
| HROC-CON-001 | Conflicted settled/current-truth metadata without approved caveat readiness | `REFUSAL_ENVELOPE` |
| HROC-CON-002 | Conflicted metadata with approved caveat readiness | `READY_CAVEATED_ENVELOPE` |
| HROC-SUP-001 | Superseded current-truth metadata | `REFUSAL_ENVELOPE` |
| HROC-REF-001 | Prior skeleton refusal | `REFUSAL_ENVELOPE` |

## Boundary

Fixtures are supplied metadata only. They do not ingest source content, query corpus/vector/database stores, call a live LLM, generate final answers, expose chat, create endpoint/UI, mutate corpus, or write/read a database.

## Hardened Coverage Closeout

This catalog supports `HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CONTRACT_HARDENING.md` and proves fixture coverage for current-truth readiness, historical-context readiness, caveated readiness, missing answer-use permission, missing retrieval eligibility, missing provenance/citation, conflicted evidence, superseded evidence, prior refusal, and no-runtime blocking.

No endpoint/UI exists. No live LLM is called. No final answer is generated. No live retrieval backend is used. No DB read/write occurs. No corpus mutation occurs. This is not production chat exposure.
