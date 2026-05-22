# Codex Prompt: Minerva Internal Chat Panel Response Contract v0.1

Date: 2026-05-22

Repository: `ezeas-intelligence`

## Objective

Implement the next Minerva MVP slice:

Internal Chat Panel Response Contract v0.1

## Context

The following Minerva internal-chat MVP foundations are committed:

1. Role-Scoped Code Evidence Foundation v0.1
2. Code Evidence Answer Support v0.1
3. Internal Chat Orchestrator Envelope v0.1
4. Internal Chat Deterministic Answer Draft v0.1
5. Internal Chat API Stub v0.1
6. Internal Chat Evidence Fixture Harness v0.1
7. Internal Chat Fixture-Key API Support v0.1
8. Internal Chat Endpoint Smoke Harness v0.1

Current capability:

- `POST /api/v1/internal/minerva/chat/stub` exists.
- Request accepts optional `FixtureKey`.
- `FixtureKey` resolves through `InternalChatEvidenceFixtureHarnessService`.
- Response includes orchestrator envelope, evidence support packet, deterministic draft, fixture metadata, role-safe disclosure, required caveats, no-action attestation.
- Smoke harness validates internal/demo fixture cases.
- Live LLM remains disabled.
- Final answer generation remains disabled.
- Runtime evidence is not fetched.
- DB is not accessed.
- No chat persistence exists.
- No Workforce UI exists yet.

Current limitation:

The internal chat stub response is structurally rich, but not yet shaped for an in-platform Ask Minerva panel. A future Workforce Platform panel should not have to interpret the entire internal envelope directly. It needs a stable, role-safe presentation contract:

- headline / answer draft summary;
- evidence chips;
- caveat banners;
- role-safe evidence list;
- blocked/prohibited claim messages;
- no-action/no-runtime boundary;
- next-step text;
- technical detail availability depending on role.

## Primary Goal

Create a deterministic panel-ready response contract on top of the existing internal chat stub response.

This slice should convert the rich internal chat response into a UI-friendly response packet that a future Workforce Platform Ask Minerva panel can consume.

This is still internal/demo/test support only. It is not live LLM. It is not final customer-facing chat. It is not Workforce Platform UI integration yet.

## Strict Non-Goals

- no live LLM calls;
- no external API calls;
- no database connection;
- no database migrations;
- no chat persistence;
- no Workforce Platform integration;
- no UI work in `workforce-platform`;
- no operational payroll evidence fetch;
- no live object evidence fetch;
- no vector search / embeddings;
- no code execution beyond local tests;
- no mutation of external repos;
- no raw code snippets;
- no production/customer availability claims from fixture/code evidence alone;
- no payroll calculation;
- no write actions;
- no final customer-facing answer generation.

## Requested Implementation

Inspect first:

- `app/services/internal_chat_api_stub_service.py`
- `app/services/internal_chat_deterministic_answer_draft_service.py`
- `app/services/internal_chat_orchestrator_service.py`
- `app/services/internal_chat_evidence_fixture_harness_service.py`
- `app/schemas/internal_chat.py`
- `app/api/v1/internal_chat_stub.py`
- fixture-key, endpoint smoke, smoke script, and sample output tests/docs

Expected new or changed files:

- service: `app/services/internal_chat_panel_response_service.py`
- schema update: `app/schemas/internal_chat.py`
- optional route support: `app/api/v1/internal_chat_stub.py`
- tests: `tests/test_internal_chat_panel_response_service.py`
- knowledge doc: `docs/knowledge/minerva_internal_chat_panel_response_contract_v0_1.md`
- evaluation baseline: `docs/evaluation/minerva_internal_chat_panel_response_contract_v0_1/PANEL_RESPONSE_CONTRACT_BASELINE.md`
- sample response: `docs/evaluation/minerva_internal_chat_panel_response_contract_v0_1/PANEL_RESPONSE_SAMPLE.json`
- prompt artefact: `docs/codex_prompts/2026-05-22_minerva_internal_chat_panel_response_contract_v01.md`

## Service Requirements

Create `InternalChatPanelResponseService`.

It should accept an `InternalChatApiStub` response or equivalent dictionary/model, optional role, optional panel mode `COMPACT`, `STANDARD`, or `TECHNICAL`, and optional `include_technical_details` defaulting false.

Suggested response fields:

- `PanelStatus`
- `Role`
- `DisclosureMode`
- `Headline`
- `Summary`
- `DraftText`
- `IsFinalAnswer`
- `FinalAnswerGenerationPermitted`
- `LiveLlmUsed`
- `EvidenceChips`
- `CaveatBanners`
- `BoundaryBanners`
- `BlockedClaims`
- `UnsupportedScopes`
- `FixtureEvidenceNotice`
- `RuntimeEvidenceNotice`
- `RoleRestrictionNotice`
- `SuggestedNextStep`
- `PrimaryDisplaySections`
- `SecondaryDisplaySections`
- `TechnicalDetailsAvailable`
- `TechnicalDetails`
- `NoActionAttestation`
- `AuditSummary`

Panel statuses requested:

- `PANEL_READY`
- `PANEL_NEEDS_MORE_EVIDENCE`
- `PANEL_ROLE_RESTRICTED`
- `PANEL_PROHIBITED_CLAIM_BLOCKED`
- `PANEL_UNSUPPORTED_SCOPE`
- `PANEL_INVALID_FIXTURE`
- `PANEL_DRAFT_ONLY`

Headline examples:

- supported payroll administrator: "Implementation evidence supports this, with runtime caveats."
- needs runtime evidence: "Runtime evidence is required before this can be confirmed."
- role restricted: "This evidence is not available for this role."
- invalid fixture key: "The requested internal fixture key was not found."
- analytics deferred: "Analytics evidence is recognised but not active in this MVP."

Evidence chip examples:

- `Fixture evidence`
- `Synthetic/internal`
- `Code evidence`
- `Test evidence`
- `Implementation-state`
- `Runtime evidence required`
- `Live LLM disabled`
- `No payroll calculation`
- `No write action`

Caveat banners should group runtime, fixture/synthetic, code limitation, test limitation, final answer disabled, live LLM disabled, role restriction, and unsupported scope caveats.

## Role Behaviour

Developer:

- technical details may include file/test/route references if present in role-safe evidence;
- no raw code snippets;
- technical mode may show detailed caveats.

Payroll administrator:

- implementation confirmation language;
- limited implementation evidence allowed if already role-safe;
- runtime/customer caveats visible.

Payroll user:

- operational summary;
- no file/function/test names;
- code evidence only background confidence.

Customer administrator:

- customer-safe implementation confirmation;
- tenant/customer availability caveat.

Worker:

- no code evidence;
- worker-facing restriction notice.

Analytics user:

- analytics deferred/inactive notice in v0.1.

## API And Smoke Harness

Preferred API integration: add optional request field `IncludePanelResponse: bool = false`. When true, the internal chat stub response includes `PanelResponse` built by `InternalChatPanelResponseService`.

Smoke harness may optionally include panel response summaries without breaking existing sample structure.

## Testing Requirements

Create `tests/test_internal_chat_panel_response_service.py` covering import/build, payroll administrator, payroll user hiding technical names, developer technical details, worker role restriction, customer administrator runtime caveat, analytics deferred, runtime evidence required, invalid fixture key, deterministic compact chips, caveat grouping, disabled final answer/live LLM flags, no-action attestation, no raw snippets, technical details hidden by default, optional API integration, JSON validation, artefact existence, and mojibake marker absence.

Regression tests requested:

- `tests/test_internal_chat_api_stub_fixture_key.py`
- `tests/test_internal_chat_endpoint_smoke_harness.py`
- `tests/test_internal_chat_evidence_fixture_harness_service.py`
- `tests/test_internal_chat_api_stub_service.py`
- `tests/test_internal_chat_api_stub_route.py`
- `tests/test_internal_chat_deterministic_answer_draft_service.py`
- `tests/test_internal_chat_orchestrator_service.py`
- `tests/test_code_evidence_answer_support_service.py`
- `tests/test_code_evidence_inventory_service.py`
- `tests/test_code_evidence_answer_policy_service.py`

Verification commands requested:

1. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest ...`
2. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m json.tool docs/evaluation/minerva_internal_chat_panel_response_contract_v0_1/PANEL_RESPONSE_SAMPLE.json`
3. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py`
4. `git diff --check`
5. `git status --short`

Instruction: do not commit.
