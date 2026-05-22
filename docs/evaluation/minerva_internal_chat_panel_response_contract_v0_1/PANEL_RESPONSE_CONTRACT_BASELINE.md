# Minerva Internal Chat Panel Response Contract Baseline v0.1

## Contract Scope

`InternalChatPanelResponseService` converts internal chat stub responses into panel-ready packets. The contract is deterministic, fixture-backed, role-safe, and internal only.

It does not call a live LLM, access a database, fetch runtime evidence, calculate payroll, perform write actions, persist chat, or expose a Workforce UI.

## Expected Panel Statuses

- `PANEL_READY`
- `PANEL_NEEDS_MORE_EVIDENCE`
- `PANEL_ROLE_RESTRICTED`
- `PANEL_PROHIBITED_CLAIM_BLOCKED`
- `PANEL_UNSUPPORTED_SCOPE`
- `PANEL_INVALID_FIXTURE`
- `PANEL_DRAFT_ONLY`

## Sample Cases

### Developer Admitted Draft Evidence Question

Fixture: `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`

Expected status: `PANEL_READY`

Expected chips: `Fixture evidence`, `Synthetic/internal`, `Implementation-state`, `Code evidence`, `Test evidence`, `Live LLM disabled`, `No payroll calculation`, `No write action`, `Final answer disabled`

Expected banners: runtime availability caveat, fixture/synthetic evidence caveat, code evidence limitation, test evidence limitation, final answer disabled, live LLM disabled.

Technical details: available only when technical mode or `IncludeTechnicalDetails=true` is requested. May include file, route, symbol, test, fixture, support, and scope references. Raw code snippets remain prohibited.

### Payroll Administrator Asphalt classRates Question

Fixture: `ASPHALT_SAFE_CLASSRATES_SEEDED_WITH_GATES`

Expected status: `PANEL_READY`

Expected headline: "Implementation evidence supports this, with runtime caveats."

Expected chips: `Fixture evidence`, `Synthetic/internal`, `Implementation-state`, `Code evidence`, `Test evidence`, `Live LLM disabled`, `No payroll calculation`, `No write action`, `Final answer disabled`

Expected banners: runtime availability caveat, fixture/synthetic evidence caveat, code evidence limitation, test evidence limitation, final answer disabled, live LLM disabled.

### Payroll User Post-Finalisation ObjectTime Question

Fixture: `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`

Expected status: `PANEL_READY`

Expected headline: "The workflow is supported where the platform makes it available."

Expected role behaviour: operational summary only. File paths, function names, route names, symbol names, and test names must not appear.

### Customer Administrator Production Availability Question

Fixture: `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`

Expected status: `PANEL_NEEDS_MORE_EVIDENCE`

Expected headline: "Runtime evidence is required before this can be confirmed."

Expected chips: include `Runtime evidence required`, `Live LLM disabled`, `No payroll calculation`, and `No write action`.

Expected banners: runtime availability caveat, fixture/synthetic evidence caveat, code evidence limitation, final answer disabled, live LLM disabled.

### Worker Code Evidence Question

Fixture: `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`

Expected status: `PANEL_ROLE_RESTRICTED`

Expected headline: "This evidence is not available for this role."

Expected role behaviour: worker-facing restriction notice. No internal code, test, prompt, file, function, route, or test references.

### Analytics Deferred Question

Fixture: `ANALYTICS_EVIDENCE_DEFERRED`

Expected status: `PANEL_UNSUPPORTED_SCOPE`

Expected headline: "Analytics evidence is recognised but not active in this MVP."

Expected banners: unsupported scope, final answer disabled, live LLM disabled, and fixture/synthetic evidence caveat where applicable.

### Runtime Object Evidence Required Question

Fixture: `RUNTIME_OBJECT_EVIDENCE_REQUIRED`

Expected status: `PANEL_NEEDS_MORE_EVIDENCE`

Expected headline: "Runtime evidence is required before this can be confirmed."

Expected chips: `Runtime evidence required`, `Live LLM disabled`, `No payroll calculation`, `No write action`, `Final answer disabled`

Expected notice: authorised runtime object evidence is required and no runtime object evidence was fetched.

### Invalid Fixture Key

Fixture: `NOT_A_FIXTURE`

Expected status: `PANEL_INVALID_FIXTURE`

Expected headline: "The requested internal fixture key was not found."

Expected next step: use one of the listed internal fixture keys or omit `FixtureKey`.

## Prohibited Display Behaviours

- Do not display raw code snippets.
- Do not expose file, function, route, symbol, or test names to payroll user, customer administrator, worker, or analytics user panels.
- Do not claim production, customer, tenant, runtime, or live object availability from fixture or code evidence alone.
- Do not claim a payroll calculation was performed.
- Do not claim a write action was performed.
- Do not claim final customer-facing answer generation occurred.
- Do not claim live LLM, DB, external API, runtime fetch, chat persistence, or UI integration occurred.

## Boundary Expectations

Every panel response must keep:

- `IsFinalAnswer=false`
- `FinalAnswerGenerationPermitted=false`
- `LiveLlmUsed=false`
- no-action attestation present with all external/runtime/write/final-answer flags false.
