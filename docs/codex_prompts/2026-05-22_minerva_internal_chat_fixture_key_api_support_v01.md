# Prompt Artefact: Minerva Internal Chat Fixture-Key API Support v0.1

Date: 2026-05-22

Repository: `ezeas-intelligence`

Objective: implement the next Minerva MVP slice, `Internal Chat Fixture-Key API Support v0.1`.

## Original Request Preserved

Implement optional `FixtureKey` support for the internal Minerva chat API stub.

The prior internal-chat MVP slices are:

1. Role-Scoped Code Evidence Foundation v0.1
2. Code Evidence Answer Support v0.1
3. Internal Chat Orchestrator Envelope v0.1
4. Internal Chat Deterministic Answer Draft v0.1
5. Internal Chat API Stub v0.1
6. Internal Chat Evidence Fixture Harness v0.1

The fixture harness added:

- `app/services/internal_chat_evidence_fixture_harness_service.py`
- fixture keys:
  - `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`
  - `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`
  - `POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY`
  - `ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES`
  - `ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED`
  - `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`
  - `ANALYTICS_EVIDENCE_DEFERRED`
  - `RUNTIME_OBJECT_EVIDENCE_REQUIRED`
- candidate evidence compatible with the internal chat API stub
- role-safe fixture behaviour tests
- no live LLM, no DB, no runtime evidence, no UI, no write actions

Current limitation: tests can call the fixture harness directly and pass `CandidateEvidence` into `InternalChatApiStubService`, but the API request itself does not accept a `FixtureKey`.

Primary goal: allow the internal chat API stub to accept an optional `FixtureKey` for internal/demo/test use.

When `FixtureKey` is supplied:

- resolve it through `InternalChatEvidenceFixtureHarnessService`;
- merge or supply the fixture's `CandidateEvidence` into the request;
- use fixture domain tags/source scopes where appropriate;
- preserve role-safe disclosure;
- return deterministic orchestrator envelope and deterministic draft;
- clearly mark the response as fixture-backed/synthetic evidence;
- keep all no-live-LLM/no-DB/no-runtime/no-write boundaries.

This is internal/demo/test support only. It is not live retrieval, production chat, or customer exposure.

Strict non-goals:

- no live LLM calls;
- no external API calls;
- no database connection;
- no database migrations;
- no chat persistence;
- no Workforce Platform runtime integration;
- no UI work;
- no operational payroll evidence fetch;
- no live object evidence fetch;
- no vector search or embeddings;
- no code execution;
- no mutation of external repos;
- no raw code snippets;
- no production/customer availability claims from fixture/code evidence alone;
- no payroll calculation;
- no write actions;
- no final customer-facing answer generation.

Expected implementation files:

- `app/schemas/internal_chat.py`
- `app/services/internal_chat_api_stub_service.py`
- `app/api/v1/internal_chat_stub.py`, only if needed
- `tests/test_internal_chat_api_stub_fixture_key.py`
- update existing API stub service/route tests if appropriate
- `docs/knowledge/minerva_internal_chat_fixture_key_api_support_v0_1.md`
- `docs/evaluation/minerva_internal_chat_fixture_key_api_support_v0_1/FIXTURE_KEY_API_BASELINE.md`
- `docs/evaluation/minerva_internal_chat_fixture_key_api_support_v0_1/FIXTURE_KEY_SAMPLE_RESPONSES.json`
- `docs/codex_prompts/2026-05-22_minerva_internal_chat_fixture_key_api_support_v01.md`

Implementation requirements:

1. Add optional `FixtureKey` to the internal chat request schema. Existing request bodies must remain compatible.
2. When `FixtureKey` exists, resolve through the fixture harness. If valid, merge fixture evidence with explicit evidence; append fixture domain tags and source scopes deterministically; set response metadata including `FixtureKey`, `FixtureEvidenceUsed`, `FixtureEvidenceStatus`, `FixtureEvidenceSynthetic`, warning text, and no-action attestation.
3. Explicit `CandidateEvidence` must be preserved; fixture evidence appended unless duplicate. Duplicate detection may use stable evidence id/title/source/type fields.
4. Extend response metadata with a `FixtureEvidence` section.
5. Include caveats that fixture evidence is internal/synthetic, code/fixture evidence cannot prove production/customer runtime availability, and no live runtime object evidence was fetched.
6. The existing route `POST /api/v1/internal/minerva/chat/stub` should accept `FixtureKey` if it already uses the schema.
7. Invalid fixture keys should return deterministic invalid/unsupported fixture response with `AnswerPermitted: false`, no final answer, no live LLM, no runtime fetch, no write action, no-action attestation, and safe `AvailableFixtureKeys`.
8. Create this prompt artefact and preserve the prompt substantially.
9. Create the knowledge doc describing purpose, synthetic/internal boundary, merge behaviour, role-safe disclosure, invalid fixture behaviour, no-live/no-DB/no-runtime/no-write boundaries, and production/customer availability caveats.
10. Create the evaluation baseline with valid/invalid sample requests, expected statuses, metadata, caveats, role-safe disclosure, and no-action attestation.
11. Create sample response JSON with at least developer, payroll administrator, payroll user, worker, and invalid fixture key examples.

Testing requirements:

- request without `FixtureKey` remains compatible;
- valid `FixtureKey` resolves fixture and supplies candidate evidence;
- explicit candidate evidence is preserved and fixture evidence appended;
- domain tags merge deterministically;
- source scopes merge deterministically;
- response includes `FixtureEvidenceUsed: true` and `FixtureEvidenceSynthetic: true`;
- response includes fixture evidence warning/caveat;
- developer fixture response can include technical evidence according to role policy;
- payroll user fixture response does not expose file/function/test names;
- worker fixture response remains role-restricted for code evidence;
- invalid fixture key returns deterministic invalid/unsupported fixture response;
- invalid fixture key does not call live LLM or generate final answer;
- fixture-backed response still has `IsFinalAnswer: false`;
- fixture-backed response still has `LiveLlmUsed: false`;
- fixture-backed response includes no-action attestation;
- fixture evidence is not treated as runtime object evidence;
- API route accepts `FixtureKey`.

Verification commands requested:

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_internal_chat_api_stub_fixture_key.py tests/test_internal_chat_evidence_fixture_harness_service.py tests/test_internal_chat_api_stub_service.py tests/test_internal_chat_api_stub_route.py tests/test_internal_chat_deterministic_answer_draft_service.py tests/test_internal_chat_orchestrator_service.py tests/test_code_evidence_answer_support_service.py tests/test_code_evidence_inventory_service.py tests/test_code_evidence_answer_policy_service.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
python -m json.tool docs/evaluation/minerva_internal_chat_fixture_key_api_support_v0_1/FIXTURE_KEY_SAMPLE_RESPONSES.json
git diff --check
git status --short
```

Do not commit.
