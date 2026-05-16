# Minerva Historical Read-Only Chat Pilot Exposure Decision Gate v0.1

Date: 16 May 2026

## Objective

Create and execute the documentation/control/test slice for the Minerva historical read-only chat pilot exposure decision gate v0.1.

## Required Posture

- Pilot exposure decision gate only.
- Documentation/control/test hardening only.
- Do not expose chat.
- Do not register routes globally.
- Do not create public endpoints.
- Do not create tenant/customer access.
- Do not create production UI.
- Do not call live LLMs.
- Do not generate final natural-language answers.
- Do not connect live retrieval.
- Do not read/write DB.
- Do not mutate corpus.
- Do not ingest source content.
- Do not create Code Evidence.
- Do not make cross-repo changes.

## Execution Scope

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_DECISION_RECORD.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_INTERNAL_EXPOSURE_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_EXPOSURE_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_NO_PRODUCTION_EXPOSURE_CLOSEOUT_ATTESTATION.md`

Update:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_STATIC_REVIEW.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_DECISION_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_PILOT_EXPOSURE_DECISION_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_NO_PRODUCTION_EXPOSURE_ATTESTATION.md`
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

## Result Contract

Report changed files, tests, `git diff --check`, `.pytest_tmp` status, progress after this slice, and explicit confirmation that no runtime exposure, ingestion, DB, LLM, retrieval, final-answer, production chat, schema, current-truth promotion, answer-use activation, retrieval activation, or cross-repo changes were introduced.

Suggested commit message: `minerva-historical-read-only-chat-pilot-exposure-decision-gate-v01`
