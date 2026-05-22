# Codex Prompt: Minerva Internal Chat API Stub v0.1

Date: 2026-05-22

Objective:
Implement the next Minerva MVP slice:

Minerva Internal Chat API Stub v0.1

Context:
The following Minerva internal-chat foundation slices are now committed:

1. Role-Scoped Code Evidence Foundation v0.1
   - `app/services/code_evidence_inventory_service.py`
   - `app/services/code_evidence_answer_policy_service.py`
   - role/disclosure modes
   - code evidence target registry
   - raw code snippets disabled by default
   - code cannot prove runtime/production/customer availability

2. Code Evidence Answer Support v0.1
   - `app/services/code_evidence_answer_support_service.py`
   - support statuses
   - role-safe evidence summary
   - prohibited claim blocking
   - required caveats
   - final answer generation disabled

3. Internal Chat Orchestrator Envelope v0.1
   - `app/services/internal_chat_orchestrator_service.py`
   - request/envelope structure
   - source scopes
   - role behaviour
   - runtime/analytics scopes recognised but deferred
   - live LLM disabled
   - final answer generation disabled

4. Internal Chat Deterministic Answer Draft v0.1
   - `app/services/internal_chat_deterministic_answer_draft_service.py`
   - deterministic draft statuses
   - role-sensitive draft text
   - status-sensitive draft text
   - `IsFinalAnswer = false`
   - `FinalAnswerGenerationPermitted = false`
   - `LiveLlmUsed = false`

Primary goal:
Create an internal-only API/service stub that accepts a Minerva chat request and returns:

- internal chat orchestrator envelope;
- code/evidence answer-support packet;
- deterministic non-final answer draft;
- no-action attestation;
- role-safe disclosure metadata;
- explicit no-live-LLM/no-runtime/no-write boundaries.

This is the first callable internal chat surface.

It is still not a production/customer chat endpoint.
It is still not Workforce Platform integration.
It is still not live LLM.
It is still not DB-backed.
It is still not chat persistence.

Strict non-goals:

- no live LLM calls;
- no external API calls;
- no database connection;
- no database migrations;
- no chat persistence;
- no user authentication integration beyond deterministic role field validation;
- no Workforce Platform integration;
- no UI work;
- no operational payroll evidence fetch;
- no runtime object evidence fetch;
- no vector search / embeddings;
- no code execution;
- no mutation of external repos;
- no raw code snippets;
- no production/customer availability claims from code alone;
- no payroll calculation;
- no write actions;
- no final user-facing answer generation.

Expected implementation:
Follow existing ezeas-intelligence conventions.

First inspect:

- `app/services/internal_chat_orchestrator_service.py`
- `app/services/internal_chat_deterministic_answer_draft_service.py`
- `app/services/code_evidence_answer_support_service.py`
- `app/services/code_evidence_answer_policy_service.py`
- existing FastAPI app/router structure
- existing API route tests
- existing pydantic/schema conventions
- `tests/test_internal_chat_orchestrator_service.py`
- `tests/test_internal_chat_deterministic_answer_draft_service.py`
- `tests/test_code_evidence_answer_support_service.py`

Expected files:

- `app/services/internal_chat_api_stub_service.py`
- API/router if repo conventions support it
- schema file if repo convention uses schema files
- `tests/test_internal_chat_api_stub_service.py`
- route tests if a route is added
- `docs/knowledge/minerva_internal_chat_api_stub_v0_1.md`
- `docs/evaluation/minerva_internal_chat_api_stub_v0_1/API_STUB_BASELINE.md`
- `docs/codex_prompts/2026-05-22_minerva_internal_chat_api_stub_v01.md`
- optional sample response fixture

Request model:

- `Question`: string
- `Role`: one of supported roles
- `SourceScopes`: list of source scopes
- `SurfaceContext`: optional object/dict
- `DomainTags`: optional list
- `CandidateEvidence`: optional list/dict metadata
- `ClaimToValidate`: optional string
- `AllowFinalAnswerGeneration`: optional bool, default false
- `AllowLiveLlm`: optional bool, default false
- `IncludeDeterministicDraft`: optional bool, default true

Response model:

- `Status`
- `RequestEcho` or question/role/scopes
- `OrchestratorEnvelope`
- `EvidenceSupportPacket`
- `DeterministicDraft`
- `FinalAnswerText`: null
- `IsFinalAnswer`: false
- `LiveLlmUsed`: false
- `FinalAnswerGenerationPermitted`: false
- `NoActionAttestation`
- `RequiredCaveats`
- `BlockedClaims`
- `UnsupportedScopes`
- `Diagnostics`/`AuditSummary`

Service orchestration:

- validate request role/scope fields;
- call `InternalChatOrchestratorService`;
- pass the returned envelope to `InternalChatDeterministicAnswerDraftService`;
- combine results into a response packet;
- preserve no-action attestation;
- never call live LLM;
- never call DB;
- never fetch runtime object evidence;
- never execute code;
- never mutate anything.

Route:
If the repo has an API/FastAPI convention, add an internal-only route such as `POST /internal/minerva/chat/stub` or a consistent existing route. The route must be clearly marked internal/stub in naming and docs. It must not be wired as customer-facing production chat.

Request behaviour:

- If request asks for live LLM: do not call LLM; return `LiveLlmUsed` false; include `LIVE_LLM_DISABLED` / `FINAL_ANSWER_GENERATION_DISABLED` state.
- If request asks for final answer generation: do not produce final answer; deterministic draft may be returned; `IsFinalAnswer` false; `FinalAnswerText` null.
- If request asks for runtime object evidence but does not supply safe metadata: return needs evidence / unsupported scope.
- If request asks for analytics evidence: recognise analytics as future/deferred unless safe metadata supplied.
- If request asks for payroll calculation or write action: block.

Role behaviour:

- Developer: may receive technical evidence summary if supplied. No raw code snippets.
- Payroll Administrator: implementation confirmation style draft. No raw code. Runtime caveat required.
- Payroll User: operational draft. No file/function/test names.
- Customer Administrator: customer-safe implementation confirmation. Tenant/customer availability caveat.
- Worker: no code evidence. Role-restricted if asking for code.

No-action attestation:

Every response must include:

- No live LLM called.
- No DB accessed.
- No external API called.
- No code executed.
- No external repo mutated.
- No payroll calculation performed.
- No write action performed.
- No runtime object evidence fetched.
- No final answer generated.

Knowledge doc:
Create `docs/knowledge/minerva_internal_chat_api_stub_v0_1.md` explaining purpose, relationship to orchestrator envelope, relationship to deterministic answer draft, why this is not final chat, role/scope/request/response behaviour, no-live-LLM/no-DB/no-write/no-runtime boundaries, and deferred route/UI/persistence/live LLM/runtime evidence items.

Evaluation baseline:
Create `API_STUB_BASELINE.md` with sample request/response expectations for:

- developer implementation question: "Where is the manual admitted draft processing endpoint implemented?"
- payroll administrator capability confirmation: "Can the platform manually process an admitted draft action?"
- payroll user operational question: "What should I do with this post-finalisation ObjectTime action?"
- customer administrator tenant availability question: "Is this feature enabled for my tenant?"
- worker code request: "Can I see the code behind my payslip?"
- runtime object question without evidence: "Why did this worker get overtime?"
- analytics question in v0.1: "Explain this payroll trend chart."
- payroll calculation request: "Calculate this worker's overtime pay."
- write action request: "Please approve and process this payrun now."
- request with `allow_live_llm` true.
- request with `allow_final_answer_generation` true.

Testing requirements:

- Developer request returns orchestrator envelope and deterministic draft.
- Payroll administrator request returns implementation-confirmation style draft and runtime caveat.
- Payroll user request hides technical file/function/test names.
- Customer administrator request includes customer availability caveat.
- Worker code request is role restricted / no code evidence.
- `allow_live_llm=true` does not call LLM and returns `LiveLlmUsed` false.
- `allow_final_answer_generation=true` still returns `IsFinalAnswer` false and `FinalAnswerText` null.
- Runtime object scope without evidence returns needs evidence / unsupported scope.
- Analytics scope returns deferred/inactive unless safe metadata supplied.
- Payroll calculation/write request is blocked.
- Response includes no-action attestation.
- Response includes `EvidenceSupportPacket` and `DeterministicDraft`.
- Raw code snippets are absent.
- Response is deterministic for same input.
- Route tests if route is added.
- Knowledge/evaluation/prompt artefacts exist and contain guardrails.
- Mojibake marker checks are required for corrupted arrow, dash, and replacement-character sequences.

Verification commands:

1. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_internal_chat_api_stub_service.py tests/test_internal_chat_deterministic_answer_draft_service.py tests/test_internal_chat_orchestrator_service.py tests/test_code_evidence_answer_support_service.py tests/test_minerva_code_evidence_role_model_knowledge.py tests/test_code_evidence_inventory_service.py tests/test_code_evidence_answer_policy_service.py`
2. If route test added: `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_internal_chat_api_stub_route.py`
3. `C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py`
4. `git diff --check`
5. `git status --short`

Output required:
Report files changed, new service path, route path or deferred reason, schema paths, knowledge doc path, evaluation baseline path, prompt artefact path, optional fixture path, request fields implemented, response fields implemented, how orchestrator and deterministic draft services are used, live LLM/final answer state, no-action attestation, runtime/analytics deferral, payroll calculation/write blocking, confirmation that no DB/live LLM/runtime/UI/write/repo mutation occurred, test results, `git diff --check`, `git status --short`, blockers, and deferred items.

Do not commit.
