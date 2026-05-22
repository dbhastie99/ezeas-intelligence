# Minerva Internal Chat Panel Response Contract v0.1

## Purpose

The internal chat stub already returns a rich orchestrator envelope, evidence support packet, deterministic draft, fixture metadata, disclosure metadata, caveats, and no-action attestations. A future Workforce Platform Ask Minerva panel should not need to parse that full internal envelope directly.

The panel response contract is a deterministic adapter over the internal chat stub response. It converts the internal response into a stable, role-safe presentation packet with:

- a headline, summary, and non-final draft text;
- compact evidence chips;
- grouped caveat and boundary banners;
- blocked claim and unsupported scope messages;
- fixture/runtime/no-action boundary notices;
- role-sensitive technical detail availability.

## Relationship To The Internal Chat Stub

`InternalChatPanelResponseService` accepts an `InternalChatApiStubResponse` or equivalent dictionary and produces `PanelResponse`. The API route can include this packet when `IncludePanelResponse=true`.

The panel response does not replace the internal envelope. It is a presentation contract layered on top of it.

## Role-Sensitive Rendering

Developer role may request technical details with `PanelMode=TECHNICAL` or `IncludeTechnicalDetails=true`. Technical details can include role-safe file, route, test, symbol, fixture, support, and scope references. Raw code snippets remain excluded.

Payroll administrator and payroll manager roles receive implementation confirmation language, runtime caveats, and safe evidence chips.

Payroll user receives operational wording. File names, function names, route names, test names, and raw code details are hidden.

Customer administrator receives customer-safe implementation confirmation with tenant, production, and runtime availability caveats.

Worker receives a role restriction notice and no internal code evidence details.

Analytics user receives an analytics deferred/inactive notice in v0.1 unless a later slice supplies safe analytics metadata.

## Evidence Chips And Caveat Banners

Evidence chips are compact deterministic labels such as:

- Fixture evidence
- Synthetic/internal
- Implementation-state
- Code evidence
- Test evidence
- Runtime evidence required
- Live LLM disabled
- No payroll calculation
- No write action
- Final answer disabled

Caveat banners group repeated caveats into stable banner types:

- `RUNTIME_AVAILABILITY_CAVEAT`
- `FIXTURE_SYNTHETIC_EVIDENCE_CAVEAT`
- `CODE_EVIDENCE_LIMITATION`
- `TEST_EVIDENCE_LIMITATION`
- `FINAL_ANSWER_DISABLED`
- `LIVE_LLM_DISABLED`
- `ROLE_RESTRICTION`
- `UNSUPPORTED_SCOPE`

Technical panel mode may include additional individual caveat banners for developer review.

## Boundaries

This contract is internal/demo/test support only. It is not final customer-facing chat and does not enable final answer generation.

The response must preserve these boundaries:

- `IsFinalAnswer=false`
- `FinalAnswerGenerationPermitted=false`
- `LiveLlmUsed=false`
- no live LLM call
- no database access
- no external API call
- no runtime object fetch
- no payroll calculation
- no write action
- no chat persistence
- no Workforce Platform UI integration

Fixture evidence remains synthetic/internal. It can support deterministic test scenarios, but it cannot prove production, tenant, customer, runtime, live object, migration, payroll correctness, payment, or finalisation state.

## Future Panel Consumption

A future Workforce Platform Ask Minerva panel should render `PanelResponse` as the first-level contract:

- use `PanelStatus` for panel state;
- show `Headline`, `Summary`, and `DraftText` as non-final internal draft content;
- render `EvidenceChips` as compact labels;
- render `CaveatBanners` and `BoundaryBanners` prominently;
- hide `TechnicalDetails` unless `TechnicalDetailsAvailable=true`;
- preserve `NoActionAttestation` for audit/debug display;
- never treat the panel packet as a final answer.
