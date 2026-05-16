# Codex Prompt - Minerva Historical Read-Only Chat Pilot Endpoint/UI Implementation Gate v0.1

Create and execute the Minerva historical read-only chat pilot endpoint/UI implementation gate v0.1.

## Objective

Create a documentation/control/test gate that decides whether a future minimal endpoint/UI implementation candidate may be considered. This slice moves Minerva from endpoint/UI design into endpoint/UI implementation gate only.

## Required Posture

- Endpoint/UI implementation gate only.
- Documentation/control/test hardening only.
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
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.

## Required Durable Artefacts

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_DECISION_RECORD.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_NO_EXPOSURE_ATTESTATION.md`

## Existing Controls To Update

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_DESIGN_PACK.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_CONTRACT_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_UI_SURFACE_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ACCESS_CONTROL_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_AUDIT_LOGGING_DESIGN.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_IMPLEMENTATION_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_REMAINING_RUNTIME_BOUNDARIES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `tests/test_domain_baseline_capture_batch.py`

## Gate Content Requirements

The implementation gate must include purpose, scope, current status, inputs reviewed, status model, implementation preconditions, endpoint boundary, UI boundary, chat exposure boundary, live LLM boundary, final answer boundary, retrieval/corpus/DB boundary, access-control readiness, audit/logging readiness, stop conditions, authorisations, non-authorisations, recommended next slice, progress after this slice, and developer handoff.

Current status must record `EndpointUiImplementationGateStatus: IMPLEMENTATION_GATE_DRAFTED` and conservative `No` values for endpoint, route, API handler, UI, chat exposure, live LLM, final answer generation, live retrieval, corpus mutation, database read, and database write.

Inputs reviewed must include the endpoint/UI design pack, endpoint contract design, UI surface design, access-control design, audit/logging design, implementation entry criteria, endpoint/UI boundary rules, remaining runtime boundaries, and orchestrator response contract.

The status model must include not-started, drafted, blocked, deferred, ready-for-minimal-implementation-candidate, access-control review, audit-logging review, LLM policy review, rejected, and superseded states.

Preconditions must require completed endpoint/UI design, endpoint contract, UI surface, access-control, audit/logging, implementation entry criteria, refusal/citation visibility rules, orchestrator response contract, and continued absence of endpoint, UI, live LLM approval, final answer approval, live retrieval backend, DB read/write, and corpus mutation.

Boundaries must state that this slice does not create endpoint, route, controller, API handler, UI, chat exposure, live LLM calls, final natural-language answers, live retrieval, corpus query, corpus mutation, DB reads, DB writes, or Code Evidence ingestion. Future endpoint/UI candidate consideration must remain minimal/internal/read-only/envelope-only unless separately approved.

Access-control readiness must keep future access internal/operator-developer first with no public or production tenant/customer approval. Audit/logging readiness must preserve request id, operator context, response status, refusal reason, citation readiness, caveat flag, runtime boundary, and timestamp where available, while confirming this slice does not implement runtime logging.

The gate may authorise only future consideration of a separately approved minimal endpoint/UI implementation candidate. It must not authorise endpoint creation, route/controller/API handler creation, UI creation, chat exposure, live LLM calls, final natural-language answer generation, live retrieval backend, corpus/vector search, corpus mutation, source ingestion, Code Evidence ingestion, DB reads, DB writes, schema migrations, production deployment, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

## Companion Artefact Requirements

The decision record must define the required decision fields and use conservative `No` defaults for endpoint/UI/chat/LLM/final-answer/live-retrieval/corpus/DB fields.

The minimal endpoint/UI candidate entry criteria must require implementation gate completion, design completion, contract completion, UI surface completion, access-control completion, audit/logging completion, orchestrator response contract completion, decision record completion, minimal/internal/read-only scope, envelope/status-only response, and continued absence of live LLM approval, final answer approval, live retrieval backend, DB read/write, and corpus mutation.

The blocker model must define the required blocker codes and state that blocker resolution does not itself create endpoint/UI or expose chat.

The no-exposure attestation must attest no endpoint, route/controller/API handler, UI, chat exposure, live LLM, final answer, live retrieval, DB read/write, corpus mutation, or cross-repo changes.

## Verification

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `git diff --check`
- remove `.pytest_tmp` if present

## Report

Report files changed, tests run and result, `git diff --check` result, `.pytest_tmp` status, progress after this slice, and confirmation that no source content ingestion, operational corpus mutation, Code Evidence ingestion, live LLM call, DB read/write, schema migration, endpoint change, UI change, live retrieval backend, final answer generation runtime, chat exposure, workforce-platform change, award-configurator-v1 change, ezeas-analytics change, current-truth promotion, runtime answer-use activation, or runtime retrieval activation beyond in-memory metadata evaluation was introduced.

Suggested commit message: `minerva-historical-read-only-chat-pilot-endpoint-ui-implementation-gate-v01`
