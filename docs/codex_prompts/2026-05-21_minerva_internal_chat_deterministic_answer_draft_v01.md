# Codex Prompt: Minerva Internal Chat Deterministic Answer Draft v0.1

Objective: implement a deterministic, non-LLM answer-draft layer on top of the Minerva internal chat orchestrator envelope.

## Scope

Create `app/services/internal_chat_deterministic_answer_draft_service.py`.

The service consumes an `InternalChatResponseEnvelope` or equivalent structured fields and returns a deterministic internal draft. It must not generate final customer-facing answer text.

Required output flags:

- `DeterministicDraftAvailable`
- `IsFinalAnswer`
- `FinalAnswerGenerationPermitted`
- `LiveLlmUsed`

Required values:

- `DeterministicDraftAvailable`: true when safe deterministic text is produced.
- `IsFinalAnswer`: false.
- `FinalAnswerGenerationPermitted`: false.
- `LiveLlmUsed`: false.

## Draft Statuses

- `DRAFT_READY`
- `DRAFT_BLOCKED`
- `DRAFT_NEEDS_MORE_EVIDENCE`
- `DRAFT_ROLE_RESTRICTED`
- `DRAFT_PROHIBITED_CLAIM_BLOCKED`
- `DRAFT_RUNTIME_EVIDENCE_REQUIRED`
- `DRAFT_UNSUPPORTED_SCOPE`
- `DRAFT_LIVE_LLM_DISABLED`

## Formatting Modes

- `CONCISE`
- `STANDARD`
- `TECHNICAL`

Formatting mode changes draft layout only. It does not change safety semantics.

## Sample Questions

Developer: "Where is the manual admitted draft processing endpoint implemented?"

Payroll administrator: "Can the platform manually process an admitted draft action?"

Payroll user: "What should I do with this post-finalisation ObjectTime action?"

Customer administrator: "Is this enabled for my tenant?"

Worker: "Can I see the code behind my payslip?"

Payroll manager: "Why did this worker get overtime?"

Analytics user: "Explain this payroll trend chart."

Blocked request: "Please calculate payroll for this worker."

Prohibited claim: "tests prove production availability"

## Guardrails

No live LLM called.

No DB accessed.

No external repo mutated.

No payroll calculation performed.

No write action performed.

No runtime object evidence fetched.

No final answer generation performed.

No UI exposed.

No chat persistence performed.

No raw code snippets.

No production, customer, tenant, runtime, payment, finalisation, payroll correctness, or deployed-schema claims from code alone.

## Expected Role Behaviour

Developer drafts may include role-visible technical evidence references when present in the envelope. Raw code snippets remain prohibited.

Payroll administrator drafts use implementation-confirmation wording and include runtime/customer availability caveats.

Payroll user drafts use operational wording and hide file, function, route, service, class, prompt, and test names.

Customer administrator drafts use customer-safe implementation confirmation only and must not imply tenant availability.

Worker drafts do not expose code evidence and should be role restricted when the question requires code evidence.

Analytics user drafts defer analytics interpretation unless safe analytics metadata is supplied.

## Expected Status Behaviour

`SUPPORTED` maps to a ready deterministic draft with caveats.

`PARTIALLY_SUPPORTED` maps to partial-support wording.

`UNSUPPORTED` maps to insufficient-evidence wording.

`NEEDS_IMPLEMENTATION_STATE_REVIEW` maps to wording that code exists but curated implementation-state evidence is missing.

`NEEDS_RUNTIME_EVIDENCE` maps to runtime evidence required wording.

`ROLE_RESTRICTED` maps to role-safe limitation wording.

`PROHIBITED_CLAIM_BLOCKED` maps to blocked wording that does not affirm the claim.

Runtime object scope without supplied evidence maps to `DRAFT_RUNTIME_EVIDENCE_REQUIRED`.

Analytics scope without supplied evidence maps to `DRAFT_UNSUPPORTED_SCOPE`.
