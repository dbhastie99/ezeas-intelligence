# Minerva Internal Chat Endpoint Smoke Harness v0.1

## Purpose

The internal chat endpoint smoke harness is local-only developer/test tooling for the Minerva MVP internal chat stub. It exercises the fixture-key backed internal chat service and, optionally, the FastAPI route in process.

The harness confirms that:

- the internal chat stub can build deterministic responses;
- fixture keys resolve through the internal fixture harness;
- roles produce different disclosure levels;
- deterministic draft metadata is returned for valid fixture cases;
- fixture evidence is marked synthetic;
- invalid fixture keys are rejected deterministically;
- no-live-LLM, no-DB, no-runtime-fetch, no-write, and no-final-answer boundaries remain in force.

## How To Run

Default service mode:

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe scripts/smoke_internal_chat_stub.py
```

Write concise JSON output:

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe scripts/smoke_internal_chat_stub.py --output docs/evaluation/minerva_internal_chat_endpoint_smoke_harness_v0_1/SMOKE_HARNESS_SAMPLE_OUTPUT.json
```

Optional route/client mode:

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe scripts/smoke_internal_chat_stub.py --mode route
```

## Modes

Service mode is the default. It instantiates `InternalChatApiStubService` directly, supplies fixture-key requests, and does not require a running server.

Route/client mode uses FastAPI `TestClient` against `POST /api/v1/internal/minerva/chat/stub`. It is still local process only and does not use external network calls.

## Smoke Cases

The harness covers:

- Developer with `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`;
- Payroll Administrator with `ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES`;
- Payroll User with `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`;
- Customer Administrator with `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`;
- Worker with `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`;
- Analytics User with `ANALYTICS_EVIDENCE_DEFERRED`;
- Payroll Manager with `RUNTIME_OBJECT_EVIDENCE_REQUIRED`;
- invalid fixture key `NOT_A_FIXTURE`.

## Pass And Fail Meaning

A case passes when the response status, fixture metadata, draft status, role disclosure, and boundary flags match the expected deterministic result.

The invalid fixture key case is expected to return `INVALID_FIXTURE_KEY`. The harness treats that deterministic rejection as a passing case when no live LLM, DB, runtime fetch, write action, or final answer generation occurs.

The harness exits with status code 0 only when every case passes. Any failed case is included in the JSON with `Pass: false` and a `FailureReason`.

## Boundaries

This is not production chat and is not customer-facing. It does not prove production, customer, tenant, deployed schema, migration, live object, payroll result, payment, or finalisation availability.

The harness preserves these boundaries:

- no live LLM calls;
- no external API calls;
- no DB access;
- no runtime object evidence fetch;
- no chat persistence;
- no UI exposure;
- no payroll calculation;
- no write actions;
- no raw code snippets;
- no final customer-facing answer generation.

Fixture evidence remains synthetic/internal test evidence only.
