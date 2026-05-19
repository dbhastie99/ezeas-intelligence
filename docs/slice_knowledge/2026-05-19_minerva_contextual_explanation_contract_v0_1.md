# Slice Knowledge Record - Minerva Contextual Explanation Contract / Object Story Integration Plan v0.1

## Purpose

This slice generalises Admin Queue explanation into a reusable contextual explanation contract across forms, fields, objects, review items, calculation surfaces, configuration screens, and payroll review surfaces.

## Product Objective

Define and test the generic context envelope that future Minerva UI/runtime surfaces must provide before controlled retrieval, answer preparation, provenance, rehearsal, and gate evaluation can be considered.

## User Story

As a payroll operator, administrator, or reviewer, I need Minerva to understand where a question came from and what evidence is available before it attempts an explanation, so field help, form guidance, object story, treatment, blocker, and evidence-gap questions are gated by context rather than hard-coded per subject.

## Source Truth

Source truth is the controlled Minerva evidence-to-answer stack, payroll correction reasoning artefact, and context contract fixtures. This slice does not read live UI, DB, runtime, Admin Queue, CorrectionReview, LeaveType, tenant data, or production state.

## Current Platform Context

The current controlled phase has completed the retrieval harness, controlled multi-source retrieval, controlled answer preparation, payroll correction workflow reasoning capture, controlled citation/provenance packet, controlled answer rehearsal, and controlled answer gate. Those slices remain deterministic and local; none authorise live answers, DB reads, runtime truth, chat exposure, or production readiness.

## Why This Slice Exists Now

Before any UI/runtime integration, Minerva needs a generic context contract rather than bespoke services for hundreds of subjects. A Leave Type field, Admin Queue row, PayRun detail, Worksite form, deduction template, award configuration, payment setup, and payroll bucket surface should all enter the pipeline through one context model.

## What This Slice Implements

- `app/services/contextual_explanation_contract_service.py`.
- `ContextualExplanationContractService.review_context(...)`.
- Function wrapper `build_contextual_explanation_contract_review(...)`.
- Contract statuses for ready, caveated, missing field metadata, missing object story, missing source change, missing lifecycle, missing payment context, missing actions-not-taken, runtime/DB/production evidence requirement, live exposure block, and not ready.
- Recommended flows for field help, form guidance, object story, Admin Queue, treatment reasoning, evidence gap, and blocked states.
- Answer eligibility classification.
- Readiness summaries for field help, object story, and runtime evidence.
- Boundary flags proving no live LLM, final answer, chat, DB, runtime integration, corpus mutation, answer display, or persistence occurred.
- Focused tests for Leave Type field help and CorrectionReview/Admin Queue examples.

## What This Slice Explicitly Does Not Implement

No live UI, DB access, API, chat, live LLM call, final answer generation, persistence, corpus mutation, Admin Queue runtime read, CorrectionReview runtime read, LeaveType runtime read, Workforce runtime integration, Analytics runtime integration, deployment action, or production-readiness claim.

## Affected Tables / Models

None. No DB/schema changes.

## Affected Services

- `app/services/contextual_explanation_contract_service.py`

Existing retrieval, answer preparation, provenance, rehearsal, gate, and payroll correction reasoning services remain unchanged.

## Affected API / Routes

None.

## Affected UI

None.

## Affected Tests

- `tests/test_contextual_explanation_contract.py`

Regression tests remain relevant for:

- `tests/test_controlled_answer_gate.py`
- `tests/test_controlled_answer_rehearsal.py`
- `tests/test_controlled_citation_provenance_packet.py`
- `tests/test_payroll_correction_workflow_reasoning_capture.py`
- Developer Log durable filter tests.

## Evidence / Story Requirements

The context sections are `SurfaceContext`, `SubjectContext`, optional `FieldContext`, `ObjectContext`, `StoryContext`, `UserQuestionContext`, `EvidenceContext`, and `AnswerControlContext`.

Field help requires field metadata plus field catalogue or domain knowledge. Object-specific answers require object story. Admin Queue explanations require actions taken, actions not taken, and status/lifecycle summary. Treatment explanations require lifecycle, treatment/routing, actions not taken, and payment context for payment/banking/netting/recovery questions. "What changed?" requires source-change or before-after summary. "What has not happened?" requires actions not taken. Runtime, DB, and production truth require matching authorised evidence.

Boundary flags must remain false for live LLM, final answer, chat exposure, DB read/write, runtime integration, live corpus mutation, answer display, and persistence.

## Irreversible Actions Prohibited

No corpus mutation, durable ingestion, Code Evidence ingestion, DB read, DB write, schema change, runtime integration, endpoint registration, chat exposure, live LLM call, deployment action, production-readiness assertion, or cross-repo runtime integration is allowed.

## Payroll / Compliance Consequences

None directly. This is Minerva context contract only.

## Security / Role / Tenant Consequences

No live data or tenant data is read. Future UI/runtime use must enforce account, tenant, and RBAC checks before retrieval and before object story access.

## Analytics Consequences

None directly.

## Minerva Consequences

This completes the current controlled evidence-to-answer phase by defining how future UI/object contexts enter the pipeline. It preserves the distinction between context readiness and answer generation.

## Platform Doctrine Implications

- Context Before Answer Doctrine.
- Generic Explanation Contract Doctrine.
- Object Story Required for Object-Specific Answers Doctrine.
- Field Metadata Required for Field Help Doctrine.
- Retrieval Before Exposure Doctrine.
- Answer Gate Before Exposure Doctrine.
- No Live Minerva Runtime Until Explicitly Authorised.
- Slice Knowledge Preservation Doctrine.
- Prompt Is Not Knowledge Doctrine.

## Hardening Implications

- Avoid one-off subject-specific services for every form or object.
- Missing evidence must block or caveat answers.
- Field help requires metadata and field/domain knowledge.
- Object-specific answers require object story/context.
- Treatment questions require lifecycle and actions-not-taken context.
- Banking, netting, payment, and recovery questions require payment context.
- Live exposure remains blocked.

## Likely Gotchas

- The generic contract should not become a generic answer engine.
- Field help and treatment recommendation need different evidence.
- Object status alone is not enough; story and actions-not-taken matter.
- CorrectionReview is one example, not the whole model.
- A surface route plus object id is not object story evidence.
- Caveated readiness is not final answer permission.

## Acceptance Criteria

- Leave Type field help with field metadata and field/domain knowledge is ready for `FIELD_HELP_PIPELINE`.
- Leave Type field help missing field metadata or field/domain knowledge returns `CONTEXT_MISSING_FIELD_METADATA`.
- CorrectionReview Admin Queue explanation with story and actions-not-taken is ready for `ADMIN_QUEUE_EXPLANATION_PIPELINE`.
- CorrectionReview treatment without lifecycle returns `CONTEXT_MISSING_LIFECYCLE_CONTEXT`.
- Banking/netting/payment treatment without payment context returns `CONTEXT_MISSING_PAYMENT_CONTEXT`.
- "What changed?" without source-change summary returns `CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY`.
- "What has not happened?" without actions-not-taken returns `CONTEXT_MISSING_ACTIONS_NOT_TAKEN`.
- Live operator response returns `CONTEXT_BLOCKED_LIVE_EXPOSURE` and `BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED`.
- Object-specific answer without object story returns `CONTEXT_MISSING_OBJECT_STORY`.
- Every review preserves false no-live/no-DB/no-chat/no-answer/no-persistence boundary flags.

## Verification Commands

- `python -m py_compile app/services/contextual_explanation_contract_service.py`
- `python -m pytest tests/test_contextual_explanation_contract.py -q`
- `python -m pytest tests/test_controlled_answer_gate.py -q`
- `python -m pytest tests/test_controlled_answer_rehearsal.py -q`
- `python -m pytest tests/test_controlled_citation_provenance_packet.py -q`
- `python -m pytest tests/test_payroll_correction_workflow_reasoning_capture.py -q`
- `python -m pytest -q -k "developer_log and durable"`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/knowledge/minerva_contextual_explanation_contract_v0_1.md`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_contextual_explanation_contract_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_contextual_explanation_contract_v0_1.md`

## Post-Implementation Review Notes

Placeholder.

## Follow-Up Slices

- Workforce Admin Queue object-story contract alignment.
- Field catalogue / form metadata source design.
- Controlled answer persistence/audit implementation.
- Internal read-only answer surface.
- Runtime/object story evidence integration later.

## Current Status

CONTEXTUAL_EXPLANATION_CONTRACT_READY
