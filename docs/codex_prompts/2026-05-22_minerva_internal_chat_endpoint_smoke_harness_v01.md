# Prompt Artefact: Minerva Internal Chat Endpoint Smoke Harness v0.1

Date: 2026-05-22

Repository: `ezeas-intelligence`

## Objective

Implement the next Minerva MVP slice:

Internal Chat Endpoint Smoke Harness v0.1

## Context

The following Minerva internal-chat MVP slices are now committed or expected committed:

1. Role-Scoped Code Evidence Foundation v0.1
2. Code Evidence Answer Support v0.1
3. Internal Chat Orchestrator Envelope v0.1
4. Internal Chat Deterministic Answer Draft v0.1
5. Internal Chat API Stub v0.1
6. Internal Chat Evidence Fixture Harness v0.1
7. Internal Chat Fixture-Key API Support v0.1

Current capability:

- Internal route exists: `POST /api/v1/internal/minerva/chat/stub`
- Request accepts optional `FixtureKey`.
- `FixtureKey` resolves through `InternalChatEvidenceFixtureHarnessService`.
- Response includes orchestrator envelope, evidence support packet, deterministic draft, fixture metadata, role-safe disclosure, required caveats, no-action attestation.
- Live LLM remains disabled.
- Final answer generation remains disabled.
- Runtime evidence is not fetched.
- DB is not accessed.
- No chat persistence exists.
- No UI exists.

## Primary Goal

Create an internal smoke harness that exercises the internal chat stub route/service with fixture keys and roles, and produces deterministic readable sample outputs.

This should let developers/testers run one command and confirm:

- the internal chat stub route/service works;
- fixture keys resolve;
- roles produce different disclosure levels;
- deterministic draft is returned;
- fixture evidence is marked synthetic;
- no-live-LLM/no-DB/no-runtime/no-write boundaries are preserved.

This is still internal/demo/test tooling only.

## Strict Non-Goals

- no live LLM calls;
- no external API calls;
- no DB connection;
- no database migrations;
- no chat persistence;
- no Workforce Platform integration;
- no UI work;
- no operational payroll evidence fetch;
- no live object evidence fetch;
- no vector search / embeddings;
- no code execution beyond running the local smoke harness/test;
- no mutation of external repos;
- no raw code snippets;
- no production/customer availability claims from fixture/code evidence alone;
- no payroll calculation;
- no write actions;
- no final customer-facing answer generation.

## Expected Files

Script/harness:

- `scripts/smoke_internal_chat_stub.py`

Tests:

- `tests/test_internal_chat_endpoint_smoke_harness.py`

Knowledge doc:

- `docs/knowledge/minerva_internal_chat_endpoint_smoke_harness_v0_1.md`

Evaluation baseline:

- `docs/evaluation/minerva_internal_chat_endpoint_smoke_harness_v0_1/SMOKE_HARNESS_BASELINE.md`

Prompt artefact:

- `docs/codex_prompts/2026-05-22_minerva_internal_chat_endpoint_smoke_harness_v01.md`

Optional generated/sample output:

- `docs/evaluation/minerva_internal_chat_endpoint_smoke_harness_v0_1/SMOKE_HARNESS_SAMPLE_OUTPUT.json`

## Implementation Requirements

The script must be deterministic and local-only.

Service mode is default:

- instantiate `InternalChatApiStubService` directly;
- run fixture-key requests;
- do not require a running server;
- do not use network;
- do not call DB or live LLM.

Route/client mode is optional if simple:

- use FastAPI `TestClient` or existing test client to call `POST /api/v1/internal/minerva/chat/stub`;
- still local process only;
- no external network.

Smoke cases:

- Developer with `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`;
- Payroll Administrator with `ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES`;
- Payroll User with `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`;
- Customer Administrator with `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`;
- Worker with `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`;
- Analytics User with `ANALYTICS_EVIDENCE_DEFERRED`;
- Payroll Manager with `RUNTIME_OBJECT_EVIDENCE_REQUIRED`;
- Invalid FixtureKey case.

Each case should include question, role, fixture key, source scopes where useful, and `IncludeDeterministicDraft: true`.

The script should print concise JSON to stdout and optionally support `--output`.

Checks must assert or record:

- `LiveLlmUsed` is false;
- `IsFinalAnswer` is false;
- `FinalAnswerGenerationPermitted` is false;
- `NoActionAttestation` exists;
- `FixtureEvidenceSynthetic` is true for valid fixture cases;
- invalid fixture case is rejected deterministically;
- payroll user does not expose technical file/function/test names;
- worker does not receive code evidence;
- analytics fixture is deferred;
- runtime object evidence fixture requires runtime evidence.

The script must exit nonzero if any case fails.

## Verification Commands

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_internal_chat_endpoint_smoke_harness.py tests/test_internal_chat_api_stub_fixture_key.py tests/test_internal_chat_evidence_fixture_harness_service.py tests/test_internal_chat_api_stub_service.py tests/test_internal_chat_api_stub_route.py tests/test_internal_chat_deterministic_answer_draft_service.py tests/test_internal_chat_orchestrator_service.py tests/test_code_evidence_answer_support_service.py tests/test_code_evidence_inventory_service.py tests/test_code_evidence_answer_policy_service.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe scripts/smoke_internal_chat_stub.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe scripts/smoke_internal_chat_stub.py --output docs/evaluation/minerva_internal_chat_endpoint_smoke_harness_v0_1/SMOKE_HARNESS_SAMPLE_OUTPUT.json
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
python -m json.tool docs/evaluation/minerva_internal_chat_endpoint_smoke_harness_v0_1/SMOKE_HARNESS_SAMPLE_OUTPUT.json
git diff --check
git status --short
```

## Implementation Result

Implemented service mode and route/client mode in `scripts/smoke_internal_chat_stub.py`.

The harness produces concise JSON and treats deterministic invalid fixture rejection as a passing smoke case.

No production/customer availability claims are made from fixture/code evidence alone.
