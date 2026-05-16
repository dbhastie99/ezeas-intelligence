# Minerva Historical Read-Only Chat Pilot Minimal Endpoint/UI Implementation Candidate v0.1

Date: 16 May 2026

## Purpose

Create and execute the durable control artefact for the first minimal internal read-only endpoint/UI implementation candidate for Minerva historical knowledge.

## Execution Control

- Create only a minimal internal candidate if it remains read-only, envelope/status-only, metadata-only, and non-production.
- Prefer an unmounted candidate service if route mounting is unclear.
- Do not globally expose or mount a production route.
- Do not create frontend UI unless an established internal preview pattern exists.
- Candidate code may call only `historical_read_only_chat_pilot_orchestrator_candidate_service`.

## Required Boundaries

- No production chat exposure.
- No public endpoint.
- No tenant/customer endpoint.
- No live LLM calls.
- No final natural-language answer generation.
- No live retrieval backend.
- No vector or corpus search.
- No corpus mutation.
- No source ingestion.
- No Code Evidence ingestion.
- No DB reads or writes.
- No schema migrations.
- No workforce-platform, award-configurator-v1, or ezeas-analytics changes.

## Implementation Decision

Existing FastAPI routers are globally registered from `app/main.py`, and the existing chat route uses DB access, retrieval, LLM answer generation, and audit writes. Therefore this slice creates an internal service candidate only and does not create or register a router or UI.

## Files To Create

- `app/services/historical_read_only_chat_pilot_endpoint_ui_candidate_service.py`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_IMPLEMENTATION_CANDIDATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_RESPONSE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_GUARDRAILS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_FIXTURE_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CLOSEOUT_ENTRY_CRITERIA.md`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
python -m py_compile app/services/historical_read_only_chat_pilot_endpoint_ui_candidate_service.py
git diff --check
```

Remove `.pytest_tmp` if present.
