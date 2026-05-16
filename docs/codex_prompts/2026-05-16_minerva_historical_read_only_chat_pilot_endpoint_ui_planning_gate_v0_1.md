# Minerva Historical Read-Only Chat Pilot Endpoint/UI Planning Gate v0.1

Date: 16 May 2026

## Purpose

Create and execute the durable control artefact slice for the Minerva historical read-only chat pilot endpoint/UI planning gate v0.1.

## Context

This slice follows the historical read-only chat pilot orchestrator contract hardening and closeout v0.1. The orchestrator candidate is hardened for in-memory metadata-only orchestration. No live retrieval backend, corpus/vector/database store, live LLM, chat endpoint, UI, final natural-language answer generation, DB read/write, or corpus mutation is currently authorised.

## Objective

Create the endpoint/UI planning gate for Minerva historical knowledge. The gate decides what must be true before a future endpoint/UI design pack or implementation candidate may be considered.

## Required Posture

- Endpoint/UI planning gate only.
- Documentation/control/test hardening only.
- No endpoint creation.
- No UI creation.
- No chat exposure.
- No live LLM calls.
- No final natural-language answer generation.
- No live retrieval backend.
- No vector search.
- No corpus query.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No database reads or writes.
- No schema migrations.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.

## Required Artefacts

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_BOUNDARY_RULES.md`

Update:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CLOSEOUT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CONTRACT_HARDENING.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `tests/test_domain_baseline_capture_batch.py`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Suggested Commit Message

`minerva-historical-read-only-chat-pilot-endpoint-ui-planning-gate-v01`
