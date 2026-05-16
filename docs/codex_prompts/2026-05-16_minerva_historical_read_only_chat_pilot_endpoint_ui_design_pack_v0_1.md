# Minerva Historical Read-Only Chat Pilot Endpoint/UI Design Pack v0.1 Prompt

Date: 16 May 2026

## Purpose

This durable prompt/control artefact records the requested slice: Minerva historical read-only chat pilot endpoint/UI design pack v0.1.

## Execution Boundary

Execute documentation/control/test hardening only. Do not create endpoint code, route/controller/API handler code, UI code, live LLM calls, final answer generation, live retrieval backend, DB reads or writes, corpus mutation, source ingestion, Code Evidence ingestion, schema migrations, production deployment, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

## Requested Artefacts

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_DESIGN_PACK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_CONTRACT_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_UI_SURFACE_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ACCESS_CONTROL_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_AUDIT_LOGGING_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_ENTRY_CRITERIA.md`

Update existing endpoint/UI planning gate, entry criteria, blocker model, boundary rules, orchestrator closeout, orchestrator response contract, remaining runtime boundaries, historical knowledge control index, and `tests/test_domain_baseline_capture_batch.py`.

## Required Posture

- Endpoint/UI design only.
- No endpoint creation.
- No route/controller/API handler creation.
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
- No cross-repo changes.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.
