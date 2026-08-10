# LEAVESTUDIOMINERVADEMO1 — Minerva consumer/planner/renderer closeout

Date: 2026-08-11 (Australia/Sydney)

## Outcome

ezeas-intelligence now validates the exact `LEAVE_STUDIO_CONTEXT_V1` transport, classifies bounded administrator questions, creates an authoritative typed answer plan, optionally renders that plan through a constrained OpenAI-compatible client, validates the renderer output, and returns deterministic fallback on every represented failure.

The implementation freeze proven locally is:

- ezeas-intelligence: `618493f62aa0015be80ccbb3056d831e15840a36`
- Workforce Platform producer/UI: `e549e5aa0949dbe83abc10cc100fc3513ac6ce9e`

The sibling producer SHA was committed and clean before the live proof. Minerva accepted its exact pinned request fixture and returned the typed answer contract.

## Historical reconciliation

Administrator-context authority `bed51350bf935f2ab9c7b581f2f4fd3ba29ce663` and bounded renderer authority `71dafb6edeac5d5a474f284c139aa3d5feb31dcb` diverge after `d1c170b64cda7426c87bd32f5d3408198bb5b1de`. No accepted convergence existed.

This branch starts from `bed51350…`, preserves its historical QLD LSL API, admin configuration validation, evidence framing, and tests, and re-implements the renderer principles generically. It does not cherry-pick QLD-LSL-specific assumptions or replace the historical endpoints.

## Contract and planner

- Request: `LEAVE_STUDIO_MINERVA_QUESTION_V1`
- Response: `LEAVE_STUDIO_MINERVA_ANSWER_V1`
- Context: `LEAVE_STUDIO_CONTEXT_V1`
- Context fixture SHA-256: `6ba4678cef22435db71c29b93e2ddbd02a2cfcfb9ddd013f49d5b422e3cd50fb`
- Request fixture SHA-256: `ae9e3e94f588914dc5b4133b966abf7a28ee9f6c21e6e30d553dc8b87ecd9644`
- Context fingerprint: `4c279802b6470a8ce5ae2d13a794e93ecba527f92b46a35d82b44d950a962ddc`

Every selected material fact retains one of the four governed authority classes. Missing facts remain explicit. Readiness, HOLD paths, and runtime support are separate. Applicability answers preserve the absence of worker context.

The planner implements the bounded vocabulary through `UNKNOWN_OR_UNSUPPORTED`, including entitlement/accrual/basis/evidence/privacy/payment/readiness/runtime/lineage/applicability and specialised LSL/QLeave categories.

## Renderer

Renderer instruction: `LEAVE_STUDIO_CONFIGURATION_RENDERER_V1`.

The renderer is disabled by default. It receives only query intent, deterministic answer plan, approved facts, approved evidence identities, exact boundary, and review step. It does not receive the raw question, full Studio context, database records, or secrets.

Validation requires exact fact IDs, evidence IDs, WhatMatters, boundary, and next step. It rejects malformed JSON, new sources, worker eligibility, recommendations, contradictory runtime claims, new numbers/money, and unsupported qualitative vocabulary. Provider disablement, missing configuration, timeout, service failure, and validation failure all preserve the deterministic answer.

## Proof

- Focused Minerva plus historical admin/planner suite: 95 passed after the QLD LSL HOLD repair.
- Earlier combined focused regression: 94 passed before the repair; successor rerun passed 95.
- Five policy families and the six adversarial questions passed deterministic tests and live HTTP proof.
- Exact request fixture returned planner fingerprint `65284956cebb16b08cdbdc98493e8a195c521b7a5281c4ae2c4cc5bae0d6e5cf`.
- Live deterministic planning duration: 0–1 ms in the sample.

No complete opt-in Minerva provider tuple was configured, so a real external LLM call was not claimed. Live runtime returned `RendererUsed=false` and `RendererFallbackReason=disabled`. Fake success and all represented fallback/rejection paths passed.

## Boundaries

Minerva has no `leaveengine-db` connection and performs no policy/version resolution, worker eligibility, calculation, balance inference, publication, Leave Request, payroll, or ledger mutation. The only policy truth is the typed Studio context supplied by Workforce Platform.

Status: `COMPLETED_LEAVESTUDIOMINERVADEMO1_LOCAL_CROSS_REPO_PROOF_LLM_LIVE_PROOF_HELD_NO_CONFIGURED_PROVIDER`

The next programme outcome after owner demonstration/review is `LEAVEVERSIONASSURANCE1`. It was not started.

