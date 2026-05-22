# Codex Prompt: Minerva Internal Chat Evidence Fixture Harness v0.1

Date: 2026-05-22

Repository: `ezeas-intelligence`

## Objective

Implement the next Minerva MVP slice:

`Minerva Internal Chat Evidence Fixture Harness v0.1`

## Context

The following Minerva internal-chat foundation slices are committed or expected committed:

1. Role-Scoped Code Evidence Foundation v0.1
   - role/disclosure model
   - code evidence target registry
   - inventory service
   - answer policy service

2. Code Evidence Answer Support v0.1
   - answer-support packet
   - evidence categories
   - support statuses
   - prohibited claim blocking
   - required caveats

3. Internal Chat Orchestrator Envelope v0.1
   - structured request/envelope
   - source scopes
   - role behaviour
   - no live LLM
   - no final answer generation

4. Internal Chat Deterministic Answer Draft v0.1
   - deterministic non-final answer draft
   - role-sensitive draft text
   - status-sensitive draft text
   - `IsFinalAnswer=false`

5. Internal Chat API Stub v0.1
   - `POST /api/v1/internal/minerva/chat/stub`
   - request/response schema
   - calls orchestrator and deterministic draft services
   - still no live LLM, no DB, no runtime evidence fetch, no persistence, no Workforce integration, no UI, no payroll calculation, no write action

## Current Limitation

The internal chat API stub can accept supplied candidate evidence, but there is not yet a controlled fixture/evidence harness for realistic platform questions.

## Primary Goal

Create a deterministic internal evidence fixture harness that supplies safe curated evidence packets to the internal chat API/service stack for realistic Minerva MVP questions.

This slice should let tests and future internal demos ask questions such as:

- Can the platform manually process an admitted draft action?
- What evidence supports the post-finalisation ObjectTime action?
- What does code evidence confirm, and what does it not confirm?
- Is the Asphalt safe classRates seeding aligned now?
- What is still deferred for conditional shiftwork?
- Why can code evidence not prove production/customer runtime availability?

This is still fixture/synthetic evidence only. It must not fetch live runtime data, connect to Workforce Platform, call live LLM, connect to a DB, mutate external repos, or expose customer chat.

## Strict Non-Goals

- no live LLM calls;
- no external API calls;
- no database connection;
- no database migrations;
- no chat persistence;
- no Workforce Platform runtime integration;
- no UI work;
- no operational payroll evidence fetch;
- no live object evidence fetch;
- no vector search / embeddings;
- no code execution;
- no mutation of external repos;
- no raw code snippets;
- no production/customer availability claims from fixture/code evidence alone;
- no payroll calculation;
- no write actions;
- no final customer-facing answer generation.

## Files To Inspect First

- `app/services/internal_chat_api_stub_service.py`
- `app/services/internal_chat_orchestrator_service.py`
- `app/services/internal_chat_deterministic_answer_draft_service.py`
- `app/services/code_evidence_answer_support_service.py`
- `app/services/code_evidence_inventory_service.py`
- `app/services/code_evidence_answer_policy_service.py`
- `app/schemas/internal_chat.py`
- `app/api/v1/internal_chat_stub.py`
- `tests/test_internal_chat_api_stub_service.py`
- `tests/test_internal_chat_api_stub_route.py`
- `tests/test_internal_chat_deterministic_answer_draft_service.py`
- `docs/evaluation/minerva_internal_chat_api_stub_v0_1/API_STUB_BASELINE.md`
- `docs/evaluation/minerva_internal_chat_api_stub_v0_1/INTERNAL_CHAT_API_STUB_SAMPLE_RESPONSE.json`

## Expected New Files

Service:

- `app/services/internal_chat_evidence_fixture_harness_service.py`

Tests:

- `tests/test_internal_chat_evidence_fixture_harness_service.py`

Knowledge doc:

- `docs/knowledge/minerva_internal_chat_evidence_fixture_harness_v0_1.md`

Evaluation baseline:

- `docs/evaluation/minerva_internal_chat_evidence_fixture_harness_v0_1/EVIDENCE_FIXTURE_HARNESS_BASELINE.md`

Prompt artefact:

- `docs/codex_prompts/2026-05-22_minerva_internal_chat_evidence_fixture_harness_v01.md`

Fixture pack:

- `docs/evaluation/minerva_internal_chat_evidence_fixture_harness_v0_1/INTERNAL_CHAT_EVIDENCE_FIXTURES.json`

Optional sample responses:

- `docs/evaluation/minerva_internal_chat_evidence_fixture_harness_v0_1/SAMPLE_FIXTURE_RESPONSES.json`

## Service Requirements

Create a deterministic fixture harness service with suggested structures:

- `InternalChatFixtureKey`
- `InternalChatEvidenceFixture`
- `InternalChatEvidenceFixtureHarnessService`
- `FixtureEvidenceStatus`

Suggested fixture keys:

- `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`
- `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`
- `POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY`
- `ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES`
- `ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED`
- `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`
- `ANALYTICS_EVIDENCE_DEFERRED`
- `RUNTIME_OBJECT_EVIDENCE_REQUIRED`

The service should list available fixture keys, return a fixture by key, return candidate evidence metadata compatible with `InternalChatApiStubService` / `InternalChatOrchestratorService`, include domain tags, expected source scopes, expected support status, expected role-safe caveats, prohibited claims, no-action attestation, and never read live DB/runtime state, call LLM, or inspect external repos at runtime unless already supplied as fixture metadata.

## Fixture Content Requirements

### A. ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED

Should include evidence that:

- guarded manual processing endpoint exists: `POST /api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process`
- PayRun Detail/Admin Queue action wiring exists;
- active `PayRunActionDecision` and authorised admission are required;
- existing `PayRunContact` is required;
- processing delegates through `AdmittedDraftPayRunProcessingBridgeService`;
- `PayRunProcessingService.process(..., target_contact_id=...)` remains only processing entrypoint;
- not automation, not process-all, not finalisation/payment/banking.

### B. POST_FINALISATION_OBJECTTIME_ACTION_SURFACED

Should include evidence that ObjectTime/source truth changed after finalisation is surfaced in Admin Queue, finalised PayRun remains protected, action is worker-period scoped, treatment review is required, and no finalised mutation occurs.

### C. POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY

Should include evidence that review treatment is in place; ObjectTime can be reviewed/edited through the existing source-truth path where allowed; Worker Story / finalisation details are review surfaces; treatment execution remains not implemented; supplementary/retro/payment/finalisation execution is not performed.

### D. ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES

Should include evidence that DAY1/OT1/OT2/SAT1/SUN1/PHOL1 are aligned from parsed universe to materialised RateSource evidence; Step 06 wrote 30 safe classRates rows; diagnostic status is `SAFE_CLASSRATES_SEEDED_WITH_REMAINING_GATES`; remaining confirmation-gated RateSource columns remain blocked.

### E. ASPHALT_CONDITIONAL_SHIFTWORK_REMAINS_GATED

Should include evidence that AFT1/AFT2/NGT1/NGT2 exist as placeholders; `RateSource.IsShiftWorker` exists and propagation has been hardened; ObjectTime source `ShiftType` is exposed in canonical input; dynamic shift treatment engine is future/deferred unless already implemented; non-rotating night shift, unrelieved shiftworker overtime, and break/change-to-shift continuation remain gated.

### F. CODE_EVIDENCE_CANNOT_PROVE_RUNTIME

Should include evidence hierarchy and caveats: code evidence confirms implementation support; code cannot prove production deployment, customer availability, migration applied, runtime object state, or payroll correctness.

### G. ANALYTICS_EVIDENCE_DEFERRED

Should include that Analytics is registered as a future/optional evidence target and full analytics evidence intake is deferred/inactive in v0.1.

### H. RUNTIME_OBJECT_EVIDENCE_REQUIRED

Should include that object-specific questions require runtime object evidence and, without runtime object evidence, Minerva must say needs evidence.

## Integration With API Stub Service

Preferred option: keep API stub request unchanged. Tests call fixture harness service directly and pass `CandidateEvidence` into `InternalChatApiStubService`.

Optional option: add optional `FixtureKey` to internal chat request schema and resolve it through fixture harness service. If invalid, return deterministic validation/unsupported fixture response.

Implemented path for this slice: service-only fixture harness; no `FixtureKey` schema extension.

## Deterministic Sample Responses

Create samples showing:

- developer answer for manual admitted draft processing;
- payroll administrator answer for manual admitted draft processing;
- payroll user answer for post-finalisation ObjectTime action;
- customer administrator asks if feature is enabled for tenant;
- worker asks for code;
- analytics user asks to interpret trend chart.

These are still deterministic drafts / non-final.

## Testing Requirements

Create `tests/test_internal_chat_evidence_fixture_harness_service.py`.

Minimum tests:

1. Fixture harness lists all required fixture keys.
2. Each fixture has domain tags, source scopes, candidate evidence, expected support status, required caveats, and no-action attestation.
3. Manual admitted draft fixture includes endpoint and non-goals.
4. Post-finalisation ObjectTime fixture includes finalised PayRun protected / treatment review required.
5. Asphalt safe classRates fixture includes `SAFE_CLASSRATES_SEEDED_WITH_REMAINING_GATES` and DAY1/OT1/OT2/SAT1/SUN1/PHOL1.
6. Conditional shiftwork fixture says remaining dynamic/conditional gates remain deferred.
7. Code evidence runtime caveat fixture says code cannot prove production/customer/runtime availability.
8. Analytics fixture is deferred/inactive by default.
9. Runtime object evidence fixture requires runtime object evidence.
10. Fixture evidence can be passed into `InternalChatApiStubService` and produce deterministic draft response.
11. Developer fixture response may show technical evidence references.
12. Payroll user fixture response hides technical file/function/test names.
13. Worker fixture response role-restricts code evidence.
14. No fixture includes raw code snippets.
15. No fixture claims final answer generation, live LLM, DB, runtime fetch, or write action.
16. Invalid fixture key returns deterministic not-found/unsupported status if `FixtureKey` support is added.

Regression tests:

- `tests/test_internal_chat_api_stub_service.py`
- `tests/test_internal_chat_api_stub_route.py`
- `tests/test_internal_chat_deterministic_answer_draft_service.py`
- `tests/test_internal_chat_orchestrator_service.py`
- `tests/test_code_evidence_answer_support_service.py`
- `tests/test_code_evidence_inventory_service.py`
- `tests/test_code_evidence_answer_policy_service.py`

Verification commands:

1. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_internal_chat_evidence_fixture_harness_service.py tests/test_internal_chat_api_stub_service.py tests/test_internal_chat_api_stub_route.py tests/test_internal_chat_deterministic_answer_draft_service.py tests/test_internal_chat_orchestrator_service.py tests/test_code_evidence_answer_support_service.py tests/test_code_evidence_inventory_service.py tests/test_code_evidence_answer_policy_service.py`
2. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py`
3. `git diff --check`
4. `git status --short`

Do not commit.
