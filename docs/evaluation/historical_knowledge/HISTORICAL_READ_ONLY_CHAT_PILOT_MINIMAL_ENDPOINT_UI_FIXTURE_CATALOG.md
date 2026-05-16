# Historical Read-Only Chat Pilot Minimal Endpoint/UI Fixture Catalog

Version: v0.1

Date: 16 May 2026

## Purpose

This catalog defines metadata-only fixtures for the internal candidate service. Fixtures must remain supplied in-memory metadata and must not query corpus, vector, database, retrieval, or external services.

## Fixtures

- Current-truth envelope: eligible metadata with current-truth permission, retrieval eligibility, chat eligibility, citation readiness, provenance readiness, no conflict, no supersession, and no final answer.
- Historical envelope: eligible metadata with `AnswerMode` set to `HISTORICAL_CONTEXT`, preserving historical status and no final answer.
- Caveated envelope: eligible metadata that requires caveat visibility and returns a caveated status envelope without final answer.
- Refusal envelope: metadata with answer use, retrieval, chat, citation, or provenance blockers that returns refusal status.
- Missing gate refusal: metadata missing a required gate or readiness condition that returns refusal or blocked envelope.
- Conflicted refusal: metadata with unresolved conflict that returns refusal unless an approved caveat envelope is supplied.
- Superseded refusal: metadata marked superseded that returns refusal and does not promote current truth.

## Fixture Boundary

Fixtures are test inputs only. They do not ingest source content, perform operational corpus mutation, create Code Evidence, call live LLMs, read or write a database, register routes, create UI, expose production chat, or activate runtime retrieval/answer-use permissions.

## Closeout Fixture Review

`HISTORICAL_READ_ONLY_CHAT_PILOT_MINIMAL_ENDPOINT_UI_CANDIDATE_CLOSEOUT.md` reviews these fixtures for closeout. The current-truth fixture returns ready envelope without final answer generation. The historical-context fixture returns historical envelope and is not silently converted to current truth. The caveated fixture preserves caveat. The refusal fixture remains refusal. The no-runtime flags remain false.
