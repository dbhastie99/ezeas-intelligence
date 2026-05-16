# Minerva Historical Read-Only Chat Pilot Minimal Endpoint/UI Candidate Closeout v0.1

Date: 16 May 2026

## Purpose

Create and execute the durable control artefact for the Minerva historical read-only chat pilot minimal endpoint/UI candidate closeout v0.1.

## Scope

Close out and statically review the existing internal minimal endpoint/UI candidate only. This slice is documentation/control/test hardening only.

## Required Posture

- Candidate closeout/static review only.
- No production endpoint creation.
- No public route/controller/API handler creation.
- No production UI creation.
- No production chat exposure.
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

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_STATIC_REVIEW.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_DECISION_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_PILOT_EXPOSURE_DECISION_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_NO_PRODUCTION_EXPOSURE_ATTESTATION.md`

Update existing minimal endpoint/UI candidate controls, remaining runtime boundaries, the historical knowledge control index, and `tests/test_domain_baseline_capture_batch.py`.

## Verification

Run:

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `python -m py_compile app/services/historical_read_only_chat_pilot_endpoint_ui_candidate_service.py`
- `git diff --check`

Clean `.pytest_tmp` if present.

