# Minerva Internal Chat Orchestrator Baseline v0.1

Evaluation status: checked-in deterministic internal chat orchestration baseline. This baseline is metadata-only and does not expose chat, generate final answers, call a live LLM, access a DB, fetch runtime objects, write actions, or mutate repositories.

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

`PLATFORM_KNOWLEDGE`, `IMPLEMENTATION_STATE`, `CODE_EVIDENCE`, `TEST_EVIDENCE`, `PROMPT_ARTEFACTS`, and `EVALUATION_BASELINES` are supported only as supplied metadata in v0.1.

Runtime object evidence is recognised but not fetched. A runtime object question without supplied safe runtime metadata must return `NEEDS_MORE_EVIDENCE` or `UNSUPPORTED_SCOPE`.

Analytics evidence is recognised as future and inactive by default. An analytics interpretation request without supplied safe metadata must return `UNSUPPORTED_SCOPE`.

## Sample Requests

### 1. Developer

Question: "Where is the manual admitted draft processing endpoint implemented?"

Role: `DEVELOPER`

Expected status: `ANSWER_SUPPORT_BUILT`

Expected disclosure: `TECHNICAL_DISCLOSURE`

Expected source-scope behaviour: use supplied platform knowledge, implementation-state, code, test, prompt, and evaluation metadata. No raw code snippets.

Expected role-safe disclosure: developer may receive file, route, service, test, and prompt references where supplied by metadata, but must still receive runtime caveats.

### 2. Payroll Administrator

Question: "Can the platform manually process an admitted draft action?"

Role: `PAYROLL_ADMINISTRATOR`

Expected status: `ANSWER_SUPPORT_BUILT`

Expected disclosure: `IMPLEMENTATION_CONFIRMATION`

Expected source-scope behaviour: use supplied implementation-state, code, and test metadata for implementation confirmation. Raw code is withheld.

Expected role-safe disclosure: implementation confirmation style, with no payroll calculation authority and no production/customer availability claim from code alone.

### 3. Payroll User

Question: "What should I do with this post-finalisation ObjectTime action?"

Role: `PAYROLL_USER`

Expected status: `ANSWER_SUPPORT_BUILT` when supporting metadata is supplied, otherwise `NEEDS_MORE_EVIDENCE`.

Expected disclosure: `BACKGROUND_CONFIDENCE_ONLY`

Expected source-scope behaviour: code and test metadata may affect confidence, but internal identifiers are withheld.

Expected role-safe disclosure: operational/background-confidence summary only. No file names, function names, class names, route names, test names, prompt names, or raw code.

### 4. Customer Administrator

Question: "Is this feature enabled for my tenant?"

Role: `CUSTOMER_ADMINISTRATOR`

Expected status: `NEEDS_MORE_EVIDENCE` if only code, test, implementation-state, prompt, knowledge, or evaluation metadata is supplied.

Expected disclosure: customer-safe `IMPLEMENTATION_CONFIRMATION`

Expected source-scope behaviour: implementation metadata may confirm platform support, but tenant/customer enablement requires runtime, configuration, permission, and deployment evidence.

Expected caveat: code evidence cannot prove customer or tenant availability.

### 5. Worker

Question: "Can I see the code behind my payslip?"

Role: `WORKER`

Expected status: `ROLE_RESTRICTED` or `PROHIBITED_CLAIM_BLOCKED` depending on whether the request is framed as code evidence use or raw code disclosure.

Expected disclosure: `NO_CODE_EVIDENCE`

Expected role-safe disclosure: no internal code, tests, prompt artefacts, file paths, function names, route names, or raw code snippets.

### 6. Payroll Manager

Question: "Why did this worker get overtime?"

Role: `PAYROLL_MANAGER`

Expected status: `NEEDS_MORE_EVIDENCE` when no runtime object evidence is supplied.

Expected source-scope behaviour: `RUNTIME_OBJECT_EVIDENCE` is required for object-specific overtime explanation. Static code or doctrine cannot answer the current worker-specific result.

### 7. Analytics User

Question: "Explain this payroll trend chart."

Role: `ANALYTICS_USER`

Expected status: `UNSUPPORTED_SCOPE` in v0.1 without supplied safe analytics metadata.

Expected source-scope behaviour: `ANALYTICS_EVIDENCE` is recognised as future and inactive by default.

## Prohibited Cases

Payroll calculation request:

- Expected status: `PROHIBITED_CLAIM_BLOCKED`
- Expected blocked claim: payroll calculation request blocked.
- Required attestation: No payroll calculation performed.

Production availability claim from code alone:

- Expected status: `NEEDS_MORE_EVIDENCE`
- Required caveat: code evidence cannot prove production availability, runtime enablement, customer access, deployed schema state, permissions, live object state, payroll correctness, payment, or finalisation.

Request for raw code by payroll user:

- Expected status: `PROHIBITED_CLAIM_BLOCKED`
- Expected blocked claim: raw code disclosure request blocked.
- Required disclosure: no file names, function names, test names, route names, or raw code snippets.

Runtime object question without runtime evidence:

- Expected status: `NEEDS_MORE_EVIDENCE` or `UNSUPPORTED_SCOPE`
- Required caveat: runtime object evidence is recognised but not fetched.

Analytics interpretation request in v0.1:

- Expected status: `UNSUPPORTED_SCOPE`
- Required caveat: analytics evidence is recognised as future and inactive by default.

Write action request:

- Expected status: `PROHIBITED_CLAIM_BLOCKED`
- Required attestation: No write action performed.

## Final Answer And Live LLM Guards

If `allow_live_llm` is true, expected status is `LIVE_LLM_DISABLED`, `LiveLlmUsed` remains false, and no live LLM is called.

If `allow_final_answer_generation` is true, expected status is `FINAL_ANSWER_GENERATION_DISABLED`, `FinalAnswerGenerationPermitted` remains false, `FinalAnswerText` remains null, and no final answer generation is performed.

The envelope may include `SuggestedDeterministicSummary`, but it is a stub summary for tests and internal review only.
