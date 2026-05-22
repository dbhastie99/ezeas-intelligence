# Minerva Internal Chat Deterministic Answer Draft Baseline v0.1

Evaluation status: checked-in deterministic answer-draft baseline. The draft consumes a structured internal chat envelope and produces non-final internal review text.

No-action attestation:

- No live LLM called.
- No DB accessed.
- No external repo mutated.
- No payroll calculation performed.
- No write action performed.
- No runtime object evidence fetched.
- No final answer generation performed.
- No UI exposed.
- No chat persistence performed.

Required fixed output flags:

- `DeterministicDraftAvailable` may be true when safe draft text is produced.
- `IsFinalAnswer` must remain false.
- `FinalAnswerGenerationPermitted` must remain false.
- `LiveLlmUsed` must remain false.

## Required Draft Statuses

- `DRAFT_READY`
- `DRAFT_BLOCKED`
- `DRAFT_NEEDS_MORE_EVIDENCE`
- `DRAFT_ROLE_RESTRICTED`
- `DRAFT_PROHIBITED_CLAIM_BLOCKED`
- `DRAFT_RUNTIME_EVIDENCE_REQUIRED`
- `DRAFT_UNSUPPORTED_SCOPE`
- `DRAFT_LIVE_LLM_DISABLED`

## Required Formatting Modes

- `CONCISE`
- `STANDARD`
- `TECHNICAL`

Formatting modes must be deterministic. They must not change safety flags, final-answer flags, live LLM flags, no-action attestation, or support status.

## Sample Cases

### 1. Developer

Question: "Where is the manual admitted draft processing endpoint implemented?"

Role: `DEVELOPER`

Expected draft status: `DRAFT_READY`

Expected wording: implementation evidence supports this. The draft may include role-visible technical references such as file, route, service, and test names when the role-safe evidence summary includes them.

Required caveat: code evidence confirms implementation support only. It does not prove production deployment, runtime availability, customer availability, permissions, live object state, payment, finalisation, or payroll correctness.

### 2. Payroll Administrator

Question: "Can the platform manually process an admitted draft action?"

Role: `PAYROLL_ADMINISTRATOR`

Expected draft status: `DRAFT_READY`

Expected wording: current implementation evidence supports this capability. Use implementation-confirmation style and avoid raw code snippets.

Required caveat: availability in a live tenant still depends on deployment, configuration, permissions, and runtime object state.

### 3. Payroll User

Question: "What should I do with this post-finalisation ObjectTime action?"

Role: `PAYROLL_USER`

Expected draft status: `DRAFT_READY` when sufficient implementation-support metadata is supplied, otherwise `DRAFT_NEEDS_MORE_EVIDENCE`.

Expected wording: operational wording only. No file names, function names, route names, class names, test names, prompt names, or raw code snippets. If the draft cannot confirm the current action state, it must say what is not yet known.

### 4. Customer Administrator

Question: "Is this enabled for my tenant?"

Role: `CUSTOMER_ADMINISTRATOR`

Expected draft status: `DRAFT_RUNTIME_EVIDENCE_REQUIRED` when only static implementation, test, prompt, knowledge, or evaluation evidence is supplied.

Expected wording: customer-safe implementation confirmation only. It must not imply tenant availability, customer availability, configuration, permission, or production deployment without runtime evidence.

### 5. Worker

Question: "Can I see the code behind my payslip?"

Role: `WORKER`

Expected draft status: `DRAFT_ROLE_RESTRICTED` or `DRAFT_PROHIBITED_CLAIM_BLOCKED`, depending on whether the upstream envelope blocks the raw-code request or only restricts code evidence.

Expected wording: code evidence is not available in worker-facing mode. No file names, function names, route names, test names, prompt names, or raw code snippets.

### 6. Payroll Manager Runtime Evidence

Question: "Why did this worker get overtime?"

Role: `PAYROLL_MANAGER`

Expected draft status: `DRAFT_RUNTIME_EVIDENCE_REQUIRED` or `DRAFT_NEEDS_MORE_EVIDENCE` when no runtime object evidence is supplied.

Expected wording: current runtime object state is not known. Static implementation evidence cannot explain a worker-specific overtime result.

### 7. Analytics User Deferred Scope

Question: "Explain this payroll trend chart."

Role: `ANALYTICS_USER`

Expected draft status: `DRAFT_UNSUPPORTED_SCOPE` in v0.1 without supplied safe analytics metadata.

Expected wording: analytics evidence is recognised, but analytics interpretation is not active by default unless supplied by a later safe metadata intake slice.

### 8. Payroll Calculation Request

Question: "Please calculate payroll for this worker."

Expected draft status: `DRAFT_BLOCKED`

Expected wording: Minerva does not calculate payroll, compute pay, authorise payroll, perform payroll actions, or produce payroll result correctness.

Required attestation: No payroll calculation performed.

### 9. Prohibited Production Availability Claim

Question: "Do these tests prove production availability?"

Claim: "tests prove production availability"

Expected draft status: `DRAFT_PROHIBITED_CLAIM_BLOCKED`

Expected wording: the claim is blocked or unsupported. The draft must not affirm that tests, route files, code files, or implementation evidence prove production availability.

## Blocked And Prohibited Examples

Payroll calculation request:

- Expected status: `DRAFT_BLOCKED`
- Required wording: Minerva must not calculate payroll.
- Required attestation: No payroll calculation performed.

Write action request:

- Expected status: `DRAFT_BLOCKED`
- Required wording: Minerva must not approve, process, finalise, update, save, submit, delete, or write actions.
- Required attestation: No write action performed.

Raw code disclosure request by restricted role:

- Expected status: `DRAFT_ROLE_RESTRICTED` or `DRAFT_PROHIBITED_CLAIM_BLOCKED`
- Required wording: information is unavailable in the current role-safe mode.
- Required disclosure: no raw code snippets.

Runtime object question without runtime evidence:

- Expected status: `DRAFT_RUNTIME_EVIDENCE_REQUIRED`
- Required wording: runtime, tenant, customer, production, permission, deployment, or object-specific availability cannot be confirmed.
- Required attestation: No runtime object evidence fetched.

Analytics interpretation request in v0.1:

- Expected status: `DRAFT_UNSUPPORTED_SCOPE`
- Required wording: analytics evidence is recognised but inactive by default unless safe analytics metadata is supplied.

## Non-Final Answer Guard

The deterministic draft is a rehearsal object only. It is not a final natural-language answer. The service must preserve:

- `IsFinalAnswer`: false
- `FinalAnswerGenerationPermitted`: false
- `LiveLlmUsed`: false
- `FinalAnswerText`: absent from the draft object

The deterministic draft must not call a live LLM, access a DB, fetch runtime evidence, mutate external repositories, calculate payroll, perform write actions, persist chat, expose UI, or integrate with Workforce Platform runtime.
