# Slice Knowledge Record — Minerva Controlled Answer Gate / Safety Boundary v0.1

## Purpose

This slice gates controlled answer rehearsals before any future exposure. It decides whether rehearsal output can remain in controlled test use, can be previewed internally with caveats, or must be blocked before any Admin Queue, live operator, or final-answer surface exists.

## Product Objective

Create the deterministic safety boundary between answer-shaped rehearsal text and any future Minerva answer surface.

## User Story

As a payroll operator or reviewer, I need Minerva answer rehearsals to be blocked or caveated before exposure so object-specific, runtime, DB, deployment, production, and live-response claims cannot leak into operational use without authorised evidence.

## Source Truth

Source truth is controlled answer rehearsal output and controlled local evidence/provenance packets only. No live DB state, live runtime state, deployment state, production state, tenant data, or external source is read.

## Current Platform Context

The current controlled phase has completed the retrieval harness, controlled multi-source retrieval, controlled multi-source answer preparation, payroll correction workflow reasoning capture, controlled citation/provenance packets, and controlled answer rehearsal. Those slices provide local deterministic inputs only; none authorise final answers, runtime use, DB reads, chat exposure, or production-readiness claims.

## Why This Slice Exists Now

Answer-shaped rehearsal text can be mistaken for a final answer. Before any future Admin Queue or live answer surface, Minerva needs a deterministic gate that records exposure eligibility, caveats, missing evidence, blocked claims, and audit packet shape.

## What This Slice Implements

- `app/services/controlled_answer_gate_service.py`.
- `ControlledAnswerGateService.evaluate_gate(...)`.
- Function wrapper `build_controlled_answer_gate_decision(...)`.
- Gate statuses and severities for controlled test, caveated internal preview, prohibited claims, missing object/runtime/DB/deployment/production evidence, live exposure block, and out-of-scope inputs.
- Exposure-mode handling for `CONTROLLED_TEST_ONLY`, `INTERNAL_PREVIEW`, `ADMIN_QUEUE_ASSISTANT_DRAFT`, and `LIVE_OPERATOR_RESPONSE`.
- Deterministic allowed/blocked exposure modes, caveats, missing evidence, blocked claims, allowed claims, warnings, gate reasons, boundary flags, next step, and audit packet shape.
- `FinalAnswerPermitted = false` for every decision.
- `AnswerDisplayed = false` and `PersistedToDb = false`.

## What This Slice Explicitly Does Not Implement

This slice does not call a live LLM, generate a final user-facing answer, expose chat, add API/UI, connect to DB, read DB, write DB, persist answer attempts, mutate live corpus, ingest Code Evidence, ingest live documents, integrate with Workforce Platform runtime, integrate with Analytics runtime, claim runtime readiness, claim production readiness, add embeddings, use vector DB, or make external calls.

## Affected Tables / Models

None. No DB/schema changes. Persistable audit packet shape only; no persistence.

## Affected Services

- `app/services/controlled_answer_gate_service.py`

Existing retrieval, answer preparation, provenance, and rehearsal services remain unchanged.

## Affected API / Routes

None.

## Affected UI

None.

## Affected Tests

- `tests/test_controlled_answer_gate.py`

Regression coverage remains relevant for:

- `tests/test_controlled_answer_rehearsal.py`
- `tests/test_controlled_citation_provenance_packet.py`
- `tests/test_controlled_multi_source_answer_preparation.py`
- `tests/test_payroll_correction_workflow_reasoning_capture.py`
- Developer Log durable filter tests.

## Evidence / Story Requirements

The gate decision records gate status, severity, allowed exposure, blocked exposure modes, required caveats, missing evidence, blocked claims, allowed claims, warnings, gate reasons, final-answer prohibition, controlled-rehearsal-only flag, persistable audit packet shape, boundary flags, and next step.

Object-specific answer use requires object story evidence such as CorrectionReview story, SourceChangeSummary, PayrollImpactSummary, ProcessPeriodLifecycleStatus, PaymentWindowStatus, and ActionsTaken/ActionsNotTaken. Runtime, DB, deployment, and production claims require matching authorised evidence.

## Irreversible Actions Prohibited

No corpus mutation, durable ingestion, Code Evidence ingestion, DB read, DB write, schema change, runtime integration, endpoint registration, chat exposure, live LLM call, deployment action, production-readiness assertion, or cross-repo runtime integration is allowed.

## Payroll / Compliance Consequences

None directly. This is Minerva answer safety gating only.

## Security / Role / Tenant Consequences

No live data, no tenant data, no DB access, no RBAC integration. Future live use requires RBAC-before-retrieval and object-story evidence.

## Analytics Consequences

None directly.

## Minerva Consequences

This is the safety boundary between controlled rehearsal and future answer exposure. It keeps answer-shaped text behind a deterministic gate and preserves that internal preview is not live operator response.

## Platform Doctrine Implications

- Source/Status Boundary Preservation Doctrine.
- Retrieval Before Exposure Doctrine.
- Answer Preparation Is Not Final Answer Doctrine.
- Citation/Provenance Before Final Answer Doctrine.
- Controlled Rehearsal Is Not Final Answer Doctrine.
- Answer Gate Before Exposure Doctrine.
- Prompt Is Not Knowledge Doctrine.
- Slice Knowledge Preservation Doctrine.
- No Live Minerva Runtime Until Explicitly Authorised.

## Hardening Implications

- Block live exposure.
- Block production/readiness overclaims.
- Require object evidence for object-specific answers.
- Require DB/runtime/deployment evidence for those claim types.
- Persistable audit shape exists but no DB writes yet.

## Likely Gotchas

- Answer-shaped rehearsal text can be mistaken for final answer.
- General doctrine can be previewed with caveats, but object-specific answers need object story evidence.
- Internal preview is not live operator response.
- Audit packet shape is not persistence.

## Acceptance Criteria

- Controlled test-only rehearsal can be allowed when claims and boundary flags are clean.
- Internal preview can be allowed only with required caveats.
- Live operator response is blocked.
- Object-specific questions without object evidence are blocked.
- Production/live/prohibited overclaims are blocked.
- DB/runtime/deployment/production claims require matching evidence.
- Dirty boundary flags block.
- Missing caveats block preview.
- Audit packet shape includes question hash, decision code, evidence references, missing evidence, blocked claims, caveats, `FinalAnswerPermitted = false`, `AnswerDisplayed = false`, and readiness flag.
- No DB persistence, answer display, live LLM, chat exposure, runtime integration, or production-readiness claim occurs.

## Verification Commands

- `python -m py_compile app/services/controlled_answer_gate_service.py`
- `python -m pytest tests/test_controlled_answer_gate.py -q`
- `python -m pytest tests/test_controlled_answer_rehearsal.py -q`
- `python -m pytest tests/test_controlled_citation_provenance_packet.py -q`
- `python -m pytest tests/test_controlled_multi_source_answer_preparation.py -q`
- `python -m pytest tests/test_payroll_correction_workflow_reasoning_capture.py -q`
- `python -m pytest -q -k "developer_log and durable"`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_controlled_answer_gate_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_controlled_answer_gate_v0_1.md`

## Post-Implementation Review Notes

Placeholder.

## Follow-Up Slices

- Admin Queue Explanation Contract / Object Story Integration Plan.
- Controlled answer persistence/audit implementation.
- Internal read-only answer surface, still no live LLM unless explicitly approved.
- Runtime/object story evidence integration later.

## Current Status

Initial controlled answer gate slice.
