# Minerva Historical Chat Pilot Readiness Checklist v0.1

Date: 16 May 2026

Objective: create and execute the governed historical chat pilot readiness checklist slice for Minerva.

This slice moves Minerva from runtime retrieval / answer synthesis gate planning into chat pilot readiness control for a narrow, read-only internal chat pilot. It must create readiness/go-no-go documentation, checklist, blocker model, pilot scope boundary, implementation entry criteria, and tests.

Allowed work:

- Create `docs/evaluation/historical_knowledge/HISTORICAL_CHAT_PILOT_READINESS_CHECKLIST.md`.
- Create `docs/evaluation/historical_knowledge/HISTORICAL_CHAT_PILOT_GO_NO_GO.md`.
- Create `docs/evaluation/historical_knowledge/HISTORICAL_CHAT_PILOT_SCOPE_BOUNDARY.md`.
- Create `docs/evaluation/historical_knowledge/HISTORICAL_CHAT_PILOT_BLOCKER_MODEL.md`.
- Create `docs/evaluation/historical_knowledge/HISTORICAL_CHAT_PILOT_IMPLEMENTATION_ENTRY_CRITERIA.md`.
- Update the historical knowledge control index, runtime gate plan, runtime gate chain requirements, runtime gate implementation readiness template, chat pilot dependency map, citation/provenance contract, answer-mode contract, and `tests/test_domain_baseline_capture_batch.py`.

Required posture:

- Documentation/control/test hardening only.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No live LLM calls.
- No database writes.
- No schema migrations.
- No endpoint changes.
- No UI changes.
- No retrieval runtime changes.
- No answer synthesis runtime changes.
- No citation rendering runtime changes.
- No chat exposure.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.
- No current-truth promotion.
- No runtime answer-use permission activation.
- No runtime retrieval eligibility activation.
- No runtime answer-mode activation.
- No historical source may become answerable current truth in this slice.

Verification:

- Run `python -m pytest tests/test_domain_baseline_capture_batch.py -q`.
- Run `git diff --check`.
- Remove `.pytest_tmp` if present.

Suggested commit message: `minerva-historical-chat-pilot-readiness-checklist-v01`
