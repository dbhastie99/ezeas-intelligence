# Codex Prompt Artefact: Minerva Internal Chat Orchestrator Envelope v0.1

Date: 2026-05-21

Objective: implement a deterministic internal chat orchestration envelope for Minerva MVP without live LLM calls, external APIs, UI, DB access, chat persistence, runtime object fetching, write actions, payroll calculations, vector search, embeddings, code execution, or external repo mutation.

## Implementation Scope

Create `app/services/internal_chat_orchestrator_service.py`.

The service must accept an `InternalChatRequest` containing:

- question text;
- user role;
- requested source scopes;
- optional surface context;
- optional domain/topic tags;
- optional candidate evidence metadata;
- optional claimed answer to validate;
- `allow_final_answer_generation`, default false;
- `allow_live_llm`, default false.

Create a deterministic `InternalChatResponseEnvelope` containing status, role, disclosure mode, requested scopes, used scopes, unsupported scopes, evidence support packet, evidence summaries, required caveats, prohibited claims, blocked claims, answer permission flags, final answer generation flag, live LLM flag, final answer text, deterministic summary, no-action attestation, audit summary, and next step recommendation.

## Required Statuses

- `READY_FOR_ANSWER_SUPPORT`
- `ANSWER_SUPPORT_BUILT`
- `ANSWER_NOT_PERMITTED`
- `ROLE_RESTRICTED`
- `NEEDS_MORE_EVIDENCE`
- `PROHIBITED_CLAIM_BLOCKED`
- `LIVE_LLM_DISABLED`
- `FINAL_ANSWER_GENERATION_DISABLED`
- `UNSUPPORTED_SCOPE`

## Required Source Scopes

- `PLATFORM_KNOWLEDGE`
- `IMPLEMENTATION_STATE`
- `CODE_EVIDENCE`
- `TEST_EVIDENCE`
- `PROMPT_ARTEFACTS`
- `EVALUATION_BASELINES`
- `RUNTIME_OBJECT_EVIDENCE`
- `ANALYTICS_EVIDENCE`

For v0.1, platform knowledge, implementation-state, code evidence, test evidence, prompt artefacts, and evaluation baselines are supported only as supplied metadata. Runtime object evidence is recognised but not fetched. Analytics evidence is recognised as future and inactive by default.

## Role Behaviour

Use `CodeEvidenceAnswerSupportService` for role policy, evidence support, disclosure mode, prohibited code claims, required caveats, and no-action answer-support packet boundaries.

Role expectations:

- `DEVELOPER`: technical disclosure, no raw code snippets.
- `PAYROLL_ADMINISTRATOR`: implementation confirmation, no raw code.
- `PAYROLL_USER`: background-confidence only, no file/function/test names by default.
- `CUSTOMER_ADMINISTRATOR`: customer-safe implementation confirmation and runtime/customer availability caveat.
- `WORKER`: code evidence excluded or role restricted.
- `PAYROLL_MANAGER`: mapped to payroll administrator policy in v0.1.
- `ANALYTICS_USER`: mapped to payroll-user style confidence until analytics policy exists.

## Sample Questions

- "Where is the manual admitted draft processing endpoint implemented?"
- "Can the platform manually process an admitted draft action?"
- "What should I do with this post-finalisation ObjectTime action?"
- "Is this feature enabled for my tenant?"
- "Can I see the code behind my payslip?"
- "Why did this worker get overtime?"
- "Explain this payroll trend chart."

## Guards

No live LLM called.

No DB accessed.

No external repo mutated.

No payroll calculation performed.

No write action performed.

No runtime object evidence fetched.

No final answer generation performed.

No UI exposed.

No chat persistence performed.

Final answer generation remains disabled. If `allow_final_answer_generation` is true, return `FINAL_ANSWER_GENERATION_DISABLED`, keep `FinalAnswerGenerationPermitted` false, and keep `FinalAnswerText` null.

Live LLM remains disabled. If `allow_live_llm` is true, return `LIVE_LLM_DISABLED` and keep `LiveLlmUsed` false.

## Tests

Create `tests/test_internal_chat_orchestrator_service.py` covering role behaviour, source-scope behaviour, runtime and analytics deferred scopes, production availability from code alone, payroll calculation blocking, write action blocking, live LLM disablement, final-answer disablement, no-action attestation, required caveats, deterministic summary, role-safe summary differences, no raw code snippets, and doc artefact existence.
