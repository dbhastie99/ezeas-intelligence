# Minerva Internal Chat Orchestrator Envelope v0.1

This document defines the deterministic internal chat orchestration envelope for the next Ask Minerva path. The envelope accepts a question, role, requested source scopes, supplied evidence metadata, and optional validation claim, then returns a structured response object. It does not expose a chat UI and does not generate final natural-language answers.

## Purpose

The orchestrator is a bridge between code evidence answer-support packets and a future internal Ask Minerva endpoint or panel. It gives Minerva a stable contract for accepting a chat-shaped request, applying role and source boundaries, building answer support, blocking prohibited claims or actions, and returning a reviewable envelope.

This is not yet a chat UI. It creates no endpoint, panel, session, persistence model, database record, or Workforce Platform integration.

## No Live LLM

The v0.1 envelope never calls a live LLM. If `allow_live_llm` is supplied as true, the envelope returns `LIVE_LLM_DISABLED`, keeps `LiveLlmUsed` false, and preserves the no-action attestation.

The envelope may provide a deterministic `SuggestedDeterministicSummary` for tests and internal review. That summary is not a final answer.

## Source Scopes

The orchestrator recognises these source scopes:

- `PLATFORM_KNOWLEDGE`
- `IMPLEMENTATION_STATE`
- `CODE_EVIDENCE`
- `TEST_EVIDENCE`
- `PROMPT_ARTEFACTS`
- `EVALUATION_BASELINES`
- `RUNTIME_OBJECT_EVIDENCE`
- `ANALYTICS_EVIDENCE`

For v0.1, `PLATFORM_KNOWLEDGE`, `IMPLEMENTATION_STATE`, `CODE_EVIDENCE`, `TEST_EVIDENCE`, `PROMPT_ARTEFACTS`, and `EVALUATION_BASELINES` are supported only as supplied metadata or evidence categories. The service does not fetch documents, execute code, query repositories, or call external APIs.

Runtime object evidence is recognised but not fetched. If a request needs live object, tenant, customer, production, or runtime evidence and no safe synthetic runtime metadata is supplied, the envelope returns `NEEDS_MORE_EVIDENCE` or `UNSUPPORTED_SCOPE`.

Analytics evidence is recognised as future and inactive by default. If an analytics request is made without safe synthetic metadata, the envelope returns `UNSUPPORTED_SCOPE` and records that analytics interpretation remains deferred.

## Role And Disclosure Policy

The orchestrator uses `CodeEvidenceAnswerSupportService`, which applies `CodeEvidenceAnswerPolicyService`.

- `DEVELOPER` receives `TECHNICAL_DISCLOSURE`, including technical evidence summaries and permitted internal references, but no raw code snippets.
- `PAYROLL_ADMINISTRATOR` receives `IMPLEMENTATION_CONFIRMATION`, with implementation evidence translated away from raw code.
- `PAYROLL_USER` receives `BACKGROUND_CONFIDENCE_ONLY`, with no file, function, route, class, or test names by default.
- `CUSTOMER_ADMINISTRATOR` receives customer-safe `IMPLEMENTATION_CONFIRMATION`, with runtime and customer availability caveats.
- `WORKER` receives `NO_CODE_EVIDENCE`; code, test, and prompt evidence are excluded or role restricted.
- `PAYROLL_MANAGER` maps to payroll administrator evidence policy for this internal slice.
- `ANALYTICS_USER` maps to payroll-user style background confidence until analytics-specific policy is implemented.

## Code Evidence Answer Support

When code evidence, implementation confirmation, test evidence, prompt artefacts, knowledge, or evaluation baselines are relevant, the orchestrator builds a `CodeEvidenceAnswerSupportPacket`. The packet supplies:

- evidence summary;
- role-safe evidence summary;
- disclosure mode;
- required caveats;
- prohibited claims;
- blocked claims;
- final answer generation set to false;
- no-action attestation.

The orchestrator wraps that packet with chat-source scope decisions, live LLM and final-answer gates, audit summary, next step recommendation, and no-action flags.

## Statuses

- `READY_FOR_ANSWER_SUPPORT`
- `ANSWER_SUPPORT_BUILT`
- `ANSWER_NOT_PERMITTED`
- `ROLE_RESTRICTED`
- `NEEDS_MORE_EVIDENCE`
- `PROHIBITED_CLAIM_BLOCKED`
- `LIVE_LLM_DISABLED`
- `FINAL_ANSWER_GENERATION_DISABLED`
- `UNSUPPORTED_SCOPE`

`READY_FOR_ANSWER_SUPPORT` is reserved for future staged orchestration. In v0.1 the public service returns the completed envelope status after policy and evidence support are applied.

## Prohibited Requests

The envelope blocks write actions, payroll calculations, raw code disclosure for restricted roles, and claims that code proves production, customer, runtime, payment, finalisation, or payroll correctness.

Examples of blocked or caveated cases:

- payroll calculation request;
- write action request;
- production availability claim from code alone;
- request for raw code by payroll user, customer administrator, or worker;
- runtime object question without runtime evidence;
- analytics interpretation request in v0.1 without supplied metadata.

## Final Answer Generation

Final natural-language answer generation remains disabled. If `allow_final_answer_generation` is true, the service returns `FINAL_ANSWER_GENERATION_DISABLED`, keeps `FinalAnswerGenerationPermitted` false, keeps `FinalAnswerText` null, and may include only a deterministic summary for tests.

## No-Action And No-Write Boundaries

Every envelope confirms:

- No live LLM called.
- No DB accessed.
- No external repo mutated.
- No payroll calculation performed.
- No write action performed.
- No runtime object evidence fetched.
- No final answer generation performed.
- No UI exposed.
- No chat persistence performed.

The orchestrator does not perform code execution, DB connection, database migration, vector search, embeddings, operational payroll evidence ingestion, runtime Workforce integration, Analytics runtime integration, UI exposure, or mutation of external repositories.

## Next Slice Recommendations

Recommended next slices:

1. Add a controlled internal endpoint that accepts and returns this envelope without persistence.
2. Add authorised runtime object evidence metadata intake for object-specific questions.
3. Add analytics evidence intake for safe chart and trend metadata.
4. Add final answer rehearsal that consumes the envelope without calling a live LLM.
5. Add UI only after role-safe final-answer policy and citation rendering are implemented.
