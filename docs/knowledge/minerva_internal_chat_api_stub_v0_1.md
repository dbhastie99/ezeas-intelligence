# Minerva Internal Chat API Stub v0.1

This document defines the first callable internal Minerva chat surface. The stub accepts a structured Minerva chat request, builds the existing internal chat orchestrator envelope, builds the code evidence answer-support packet through that envelope, and optionally builds the deterministic non-final answer draft.

It is not final chat. It is not a production or customer chat endpoint. It is not Workforce Platform integration. It does not use a live LLM, database, external API, runtime evidence fetch, vector search, embeddings, code execution, chat persistence, UI, payroll calculation, or write action.

## Purpose

The API stub gives internal tests and future integration slices a deterministic callable boundary for Minerva chat behaviour. It combines:

- `OrchestratorEnvelope`
- `EvidenceSupportPacket`
- `DeterministicDraft`
- `NoActionAttestation`
- role-safe disclosure metadata
- explicit no-live-LLM, no-runtime, no-DB, no-write boundaries

The response is deterministic for the same request. It never produces `FinalAnswerText`.

## Request DTO

The internal request accepts:

- `Question`: user question.
- `Role`: one of `DEVELOPER`, `PAYROLL_ADMINISTRATOR`, `PAYROLL_MANAGER`, `PAYROLL_USER`, `CUSTOMER_ADMINISTRATOR`, `WORKER`, or `ANALYTICS_USER`.
- `SourceScopes`: list of source scopes, including `PLATFORM_KNOWLEDGE`, `IMPLEMENTATION_STATE`, `CODE_EVIDENCE`, `TEST_EVIDENCE`, `PROMPT_ARTEFACTS`, `EVALUATION_BASELINES`, `RUNTIME_OBJECT_EVIDENCE`, and `ANALYTICS_EVIDENCE`.
- `SurfaceContext`: optional object used only as deterministic metadata; it is not persisted.
- `DomainTags`: optional topic tags for deterministic matching.
- `CandidateEvidence`: optional safe metadata list or object.
- `ClaimToValidate`: optional claim string.
- `AllowFinalAnswerGeneration`: optional bool, default false.
- `AllowLiveLlm`: optional bool, default false.
- `IncludeDeterministicDraft`: optional bool, default true.

Invalid roles or unknown scopes are rejected by the API stub instead of being silently mapped to another role.

## Response DTO

The stub returns:

- `Status`
- `RequestEcho`
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
- `DisclosureMetadata`
- `Boundaries`
- `Diagnostics`
- `AuditSummary`

`RequestEcho` deliberately avoids echoing raw candidate evidence. It echoes question, role, scopes, domain tags, surface-context keys, evidence count, and requested safety flags only.

## Relationship To The Orchestrator Envelope

`InternalChatApiStubService` validates the request and then calls `InternalChatOrchestratorService.orchestrate`. The orchestrator remains the source of truth for source-scope handling, role disclosure mode, answer-support packet construction, unsupported scopes, blocked claims, required caveats, and no-action envelope metadata.

The API stub does not fetch evidence. Candidate evidence must be supplied as safe metadata.

## Relationship To The Deterministic Draft

When `IncludeDeterministicDraft` is true, the stub passes the returned `InternalChatResponseEnvelope` to `InternalChatDeterministicAnswerDraftService.build_draft`. The draft is role-sensitive and status-sensitive, but it is not a final answer.

The fixed draft flags remain:

- `IsFinalAnswer`: false
- `FinalAnswerGenerationPermitted`: false
- `LiveLlmUsed`: false

## Role Behaviour

- `DEVELOPER`: may receive technical evidence summary when supplied. Raw code snippets remain disabled.
- `PAYROLL_ADMINISTRATOR`: receives implementation-confirmation style draft text and runtime caveats.
- `PAYROLL_MANAGER`: follows payroll-administrator disclosure for implementation evidence. Worker-specific payroll explanations require runtime object evidence.
- `PAYROLL_USER`: receives operational wording. File names, function names, route names, class names, test names, prompt names, and raw code snippets are withheld.
- `CUSTOMER_ADMINISTRATOR`: receives customer-safe implementation confirmation only. Tenant availability and customer availability require runtime, deployment, configuration, permission, and object-state evidence.
- `WORKER`: receives no code evidence. Code requests are role restricted or blocked.
- `ANALYTICS_USER`: analytics evidence is recognised but inactive by default in v0.1 unless safe analytics metadata is supplied.

## Scope Behaviour

Static metadata scopes are supported for internal review:

- `PLATFORM_KNOWLEDGE`
- `IMPLEMENTATION_STATE`
- `CODE_EVIDENCE`
- `TEST_EVIDENCE`
- `PROMPT_ARTEFACTS`
- `EVALUATION_BASELINES`

Runtime object evidence is recognised but not fetched. Without safe supplied metadata, `RUNTIME_OBJECT_EVIDENCE` remains needs-evidence or unsupported. Analytics evidence is recognised as future and inactive by default. Without safe supplied metadata, `ANALYTICS_EVIDENCE` remains deferred.

## Boundaries

Every response carries this no-action boundary:

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

The stub does not prove production availability, customer availability, tenant availability, runtime enablement, deployed schema state, permissions, live object state, payroll result correctness, payment, or finalisation.

## Sample Questions

- "Where is the manual admitted draft processing endpoint implemented?"
- "Can the platform manually process an admitted draft action?"
- "What should I do with this post-finalisation ObjectTime action?"
- "Is this feature enabled for my tenant?"
- "Can I see the code behind my payslip?"
- "Why did this worker get overtime?"
- "Explain this payroll trend chart."
- "Calculate this worker's overtime pay."
- "Please approve and process this payrun now."

## Deferred Items

- Production/customer chat route exposure.
- Workforce Platform integration.
- Authentication and authorisation integration beyond deterministic role field validation.
- DB-backed chat persistence.
- Live LLM answer generation.
- Runtime object evidence fetch.
- Analytics evidence intake and interpretation.
- Vector search, embeddings, and retrieval over stored chat.
- UI work.
- Payroll calculation and write-action execution.
