# Minerva Internal Chat API Stub Baseline v0.1

Evaluation status: checked-in deterministic API-stub baseline. The stub accepts internal chat request metadata, calls the orchestrator envelope, calls deterministic draft generation when requested, and returns a non-final internal packet.

No-action attestation:

- No live LLM called.
- No DB accessed.
- No external API called.
- No code executed.
- No external repo mutated.
- No payroll calculation performed.
- No write action performed.
- No runtime object evidence fetched.
- No final answer generated.
- No chat persistence performed.
- No UI exposed.

Fixed output flags:

- `FinalAnswerText` must be null.
- `IsFinalAnswer` must remain false.
- `FinalAnswerGenerationPermitted` must remain false.
- `LiveLlmUsed` must remain false.
- `NoActionAttestation` must be present.
- `OrchestratorEnvelope`, `EvidenceSupportPacket`, and `DeterministicDraft` must be present when `IncludeDeterministicDraft` is true.

## Required Response Fields

- `Status`
- `RequestEcho`
- `OrchestratorEnvelope`
- `EvidenceSupportPacket`
- `DeterministicDraft`
- `FinalAnswerText`
- `IsFinalAnswer`
- `LiveLlmUsed`
- `FinalAnswerGenerationPermitted`
- `NoActionAttestation`
- `RequiredCaveats`
- `BlockedClaims`
- `UnsupportedScopes`
- `DisclosureMetadata`
- `Boundaries`
- `Diagnostics`
- `AuditSummary`

## Sample Cases

### 1. Developer Implementation Question

Question: "Where is the manual admitted draft processing endpoint implemented?"

Role: `DEVELOPER`

Scopes: `PLATFORM_KNOWLEDGE`, `IMPLEMENTATION_STATE`, `CODE_EVIDENCE`, `TEST_EVIDENCE`, `PROMPT_ARTEFACTS`, `EVALUATION_BASELINES`

Expected status: `STUB_RESPONSE_BUILT`; orchestrator status `ANSWER_SUPPORT_BUILT`; draft status `DRAFT_READY` when sufficient safe metadata is supplied.

Expected caveats: code evidence supports implementation confidence only. It does not prove production availability, customer availability, runtime enablement, permissions, live object state, payment, finalisation, or payroll correctness.

### 2. Payroll Administrator Capability Confirmation

Question: "Can the platform manually process an admitted draft action?"

Role: `PAYROLL_ADMINISTRATOR`

Expected status: `STUB_RESPONSE_BUILT`; draft status `DRAFT_READY` when sufficient safe metadata is supplied.

Expected wording: implementation-confirmation style. Raw code snippets are absent. Runtime caveat is required.

### 3. Payroll User Operational Question

Question: "What should I do with this post-finalisation ObjectTime action?"

Role: `PAYROLL_USER`

Expected status: `STUB_RESPONSE_BUILT`.

Expected wording: operational draft. No file names, function names, route names, class names, test names, prompt names, or raw code snippets.

### 4. Customer Administrator Tenant Availability Question

Question: "Is this feature enabled for my tenant?"

Role: `CUSTOMER_ADMINISTRATOR`

Expected orchestrator status: `NEEDS_MORE_EVIDENCE` when only static implementation evidence is supplied.

Expected draft status: `DRAFT_RUNTIME_EVIDENCE_REQUIRED`.

Expected caveat: customer-safe implementation confirmation only; tenant/customer availability is not confirmed without runtime, deployment, configuration, permission, and object-state evidence.

### 5. Worker Code Request

Question: "Can I see the code behind my payslip?"

Role: `WORKER`

Expected orchestrator status: `PROHIBITED_CLAIM_BLOCKED` or `ROLE_RESTRICTED`.

Expected draft status: `DRAFT_ROLE_RESTRICTED` or `DRAFT_PROHIBITED_CLAIM_BLOCKED`.

Expected evidence: no code evidence exposed. Raw code snippets are absent.

### 6. Runtime Object Question Without Evidence

Question: "Why did this worker get overtime?"

Role: `PAYROLL_ADMINISTRATOR` or `PAYROLL_MANAGER`

Scope: `RUNTIME_OBJECT_EVIDENCE`

Expected orchestrator status: `NEEDS_MORE_EVIDENCE` or `UNSUPPORTED_SCOPE`.

Expected unsupported scope: `RUNTIME_OBJECT_EVIDENCE`.

Expected caveat: runtime object evidence is recognised but not fetched in v0.1 and must be supplied as safe metadata by a later slice.

### 7. Analytics Question In v0.1

Question: "Explain this payroll trend chart."

Role: `ANALYTICS_USER`

Scope: `ANALYTICS_EVIDENCE`

Expected orchestrator status: `UNSUPPORTED_SCOPE` unless safe analytics metadata is supplied.

Expected caveat: analytics evidence is recognised as future and inactive by default.

### 8. Payroll Calculation Request

Question: "Calculate this worker's overtime pay."

Role: `PAYROLL_ADMINISTRATOR`

Expected orchestrator status: `PROHIBITED_CLAIM_BLOCKED`.

Expected blocked claim: `payroll calculation request blocked`.

Expected no-action result: no payroll calculation performed.

### 9. Write Action Request

Question: "Please approve and process this payrun now."

Role: `PAYROLL_ADMINISTRATOR`

Expected orchestrator status: `PROHIBITED_CLAIM_BLOCKED`.

Expected blocked claim: `write action request blocked`.

Expected no-action result: no write action performed.

### 10. Request With AllowLiveLlm True

Question: "Where is the manual admitted draft processing endpoint implemented?"

Role: `DEVELOPER`

Request flag: `AllowLiveLlm` true

Expected orchestrator status: `LIVE_LLM_DISABLED`.

Expected response: `LiveLlmUsed` false; no live LLM called; deterministic draft only.

### 11. Request With AllowFinalAnswerGeneration True

Question: "Can the platform manually process an admitted draft action?"

Role: `PAYROLL_ADMINISTRATOR`

Request flag: `AllowFinalAnswerGeneration` true

Expected orchestrator status: `FINAL_ANSWER_GENERATION_DISABLED`.

Expected response: `IsFinalAnswer` false; `FinalAnswerText` null; `FinalAnswerGenerationPermitted` false.

## Final Answer Disabled Statement

Final answer generation remains disabled. `DeterministicDraft` is internal review text only and must not be treated as a final user-facing answer.

## Live LLM Disabled Statement

Live LLM use remains disabled. `AllowLiveLlm` is treated as a request flag only; it never causes a model call.

## DB, Runtime, UI, And Write Boundaries

No DB accessed. No external API called. No runtime object evidence fetched. No code executed. No UI exposed. No write action performed. No payroll calculation performed. No chat persistence performed.
