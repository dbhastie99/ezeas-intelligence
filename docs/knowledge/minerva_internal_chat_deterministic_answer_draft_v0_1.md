# Minerva Internal Chat Deterministic Answer Draft v0.1

This document defines the deterministic internal answer-draft layer for Minerva. The layer consumes the `InternalChatResponseEnvelope` from the chat orchestrator and produces a safe, structured, non-LLM draft for internal testing.

It is not final natural-language answer generation. It is not customer-facing chat. It creates no endpoint, UI, persistence model, database connection, runtime evidence fetch, or Workforce Platform integration.

## Purpose

The deterministic draft converts the existing envelope into concise review text that can be used by internal tests and future endpoint/UI slices. It reflects support status, role disclosure mode, required caveats, blocked claims, withheld evidence, next steps, and no-action boundaries.

The draft may set `DeterministicDraftAvailable` to true, but it must keep:

- `IsFinalAnswer` false
- `FinalAnswerGenerationPermitted` false
- `LiveLlmUsed` false

## Relationship To The Chat Orchestrator Envelope

The draft service does not gather evidence. It accepts an already-built internal chat envelope or equivalent fields. The envelope remains the source of truth for role, disclosure mode, source scopes, support status, role-safe evidence summary, caveats, blocked claims, no-action attestation, and next-step recommendation.

The draft service does not call `CodeEvidenceAnswerSupportService` directly in v0.1. It drafts only from the structured envelope.

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

- `CONCISE`: single compact deterministic draft.
- `STANDARD`: answer, evidence support, caveats, and next step.
- `TECHNICAL`: deterministic status, role, disclosure mode, support status, answer, evidence support, caveats, and next step.

All modes are deterministic. None of them permit raw code snippets, final answers, live LLM calls, payroll calculation, runtime fetches, or write actions.

## Role-Sensitive Drafting

- `DEVELOPER`: may include role-visible technical references such as file, route, service, and test names when already present in the role-safe evidence summary. Must include runtime caveats. Must not include raw code snippets.
- `PAYROLL_ADMINISTRATOR`: uses implementation-confirmation language. It may mention limited implementation evidence when policy allows. It must include runtime and customer availability caveats.
- `PAYROLL_MANAGER`: follows payroll-administrator style for implementation evidence. Object-specific pay explanations require runtime object evidence.
- `PAYROLL_USER`: uses operational wording. It must not expose file names, function names, route names, class names, test names, or raw code snippets. If evidence is insufficient, it states what is not known.
- `CUSTOMER_ADMINISTRATOR`: uses customer-safe implementation confirmation only. It must not imply tenant or customer availability without runtime, configuration, permission, deployment, and object-state evidence.
- `WORKER`: receives no code evidence. Requests for code behind worker-facing records are role restricted or answered with worker-safe limitation wording.
- `ANALYTICS_USER`: analytics evidence is recognised, but analytics interpretation remains inactive by default in v0.1 unless safe analytics metadata is supplied.

## Status-Sensitive Drafting

- `SUPPORTED`: the draft may say evidence supports the position, with caveats.
- `PARTIALLY_SUPPORTED`: the draft says evidence partially supports the position and that missing support remains.
- `UNSUPPORTED`: the draft says evidence does not support the answer.
- `NEEDS_IMPLEMENTATION_STATE_REVIEW`: the draft says code evidence exists but curated implementation-state evidence is missing or did not match.
- `NEEDS_RUNTIME_EVIDENCE`: the draft says runtime, production, tenant, customer, or object-specific availability cannot be confirmed from current evidence.
- `ROLE_RESTRICTED`: the draft avoids restricted evidence and explains the role-safe limitation.
- `PROHIBITED_CLAIM_BLOCKED`: the draft does not affirm the claim as true and states that the claim is blocked or unsupported.

## Caveats

Required caveats from the envelope are preserved by default. The draft must clearly state that code evidence supports implementation confidence only and does not prove production availability, customer availability, runtime enablement, deployed schema state, permissions, live object state, payroll result correctness, payment, or finalisation.

Runtime object questions without runtime evidence produce `DRAFT_RUNTIME_EVIDENCE_REQUIRED` or `DRAFT_NEEDS_MORE_EVIDENCE`. Analytics questions in v0.1 produce deferred analytics wording unless safe analytics metadata is supplied.

## No-Action Boundaries

Every draft carries this boundary:

- No live LLM called.
- No DB accessed.
- No external repo mutated.
- No payroll calculation performed.
- No write action performed.
- No runtime object evidence fetched.
- No final answer generation performed.
- No UI exposed.
- No chat persistence performed.

The draft service does not calculate payroll, authorise payroll, approve actions, process payruns, mutate data, write to external repositories, call APIs, execute code, query databases, fetch runtime object evidence, use vector search, create embeddings, or generate final customer-facing answers.

## Next Valid Slice Recommendations

1. Add a controlled internal endpoint that returns the deterministic draft and envelope without persistence.
2. Add authorised runtime object metadata intake for object, tenant, customer, deployment, permission, and availability questions.
3. Add analytics metadata intake for safe chart and trend explanations.
4. Add final-answer rehearsal only after the deterministic draft, citation, and role-safe disclosure policies are tested.
5. Add UI only after final-answer policy and runtime evidence boundaries are implemented.
