# Slice Knowledge Record — Minerva Controlled Answer Rehearsal Over Provenance Packets v0.1

## Purpose

This slice creates deterministic controlled answer rehearsals from provenance packets without final answer generation. It previews how a future Minerva payroll-operator answer could be structured while preserving that rehearsal is not chat exposure, not runtime output, and not final answer generation.

## Product Objective

Give Minerva a controlled, citation-aware rehearsal layer after claim-level provenance and before any future answer gate or UI/runtime exposure.

## User Story

As a payroll operator, I need Minerva's future explanation shape to be rehearsed over provenance-backed claims so unsupported, prohibited, runtime-specific, and production-readiness claims are excluded before any answer gate is considered.

## Source Truth

Source truth is controlled provenance packet output and controlled local reasoning/evidence artefacts only. No live DB state, live runtime state, production deployment evidence, external document ingestion, live corpus state, or chat history is read or created.

## Current Platform Context

The current controlled Minerva sequence has completed:

- Controlled retrieval harness.
- Controlled multi-source evidence retrieval.
- Controlled multi-source answer preparation.
- Payroll correction workflow reasoning capture.
- Controlled citation/provenance packet.

Those slices established local fixture retrieval, source/status boundary preservation, answer-preparation caveats, curated payroll operator reasoning, and claim-level provenance without enabling Minerva runtime behaviour.

## Why This Slice Exists Now

After provenance mapping, Minerva needs controlled answer rehearsal before any answer gate or UI/runtime exposure. Provenance packets identify which claims can be cited and which claims are unsupported or prohibited; this slice rehearses answer sections over those packets without converting them into final answers.

## What This Slice Implements

- `app/services/controlled_answer_rehearsal_service.py`.
- Deterministic `ControlledAnswerRehearsalEnvelope` output.
- Rehearsal status, mode, audience, controlled draft, answer sections, included/excluded claims, citation plan, caveats, evidence gaps, prohibited/unsupported claim exclusions, boundary flags, final-answer prohibition, and next step.
- Payroll operator rehearsal patterns for retro vs current adjustment, supplementary vs dirty reprocess, negative delta before/after payment, payment date/year-end, object-specific evidence insufficiency, and prohibited overclaims.
- `CONTROLLED_REHEARSAL_ONLY` labelling and `FinalAnswerPermitted = false`.

## What This Slice Explicitly Does Not Implement

This slice does not call a live LLM, generate a final user-facing natural-language answer, expose chat, add endpoint/UI, connect to DB, read DB, write DB, mutate live corpus, ingest Code Evidence, ingest live documents, integrate with Workforce Platform runtime, integrate with Analytics runtime, claim runtime readiness, claim production readiness, add embeddings, use vector DB, or make external calls.

## Affected Tables / Models

None. No DB/schema changes.

## Affected Services

- `app/services/controlled_answer_rehearsal_service.py`

Existing retrieval, answer-preparation, and provenance services remain unchanged.

## Affected API / Routes

None.

## Affected UI

None.

## Affected Tests

- `tests/test_controlled_answer_rehearsal.py`

Regression coverage remains relevant for:

- `tests/test_controlled_citation_provenance_packet.py`
- `tests/test_controlled_multi_source_answer_preparation.py`
- `tests/test_controlled_multi_source_evidence_retrieval.py`
- `tests/test_payroll_correction_workflow_reasoning_capture.py`
- Developer Log durable filter tests.

## Evidence / Story Requirements

The rehearsal envelope records answer sections, claim inclusion/exclusion, citation plan, caveats, evidence gaps, prohibited claim exclusion, unsupported claim exclusion, and no-action boundary flags.

Payroll correction workflow rehearsals include short explanation, evidence basis, why the treatment applies, why alternatives are not appropriate, what has not happened, and evidence gaps / next safe step.

Insufficient-evidence rehearsals include what can be answered, what cannot be answered, additional evidence required, and next safe step.

Object-specific answers require CorrectionReviewId / object story, SourceChangeSummary, ProcessPeriodLifecycleStatus, PaymentWindowStatus, PayRun / PayRunContact state, payment execution state, and DB/runtime evidence.

## Irreversible Actions Prohibited

No corpus mutation, durable ingestion, Code Evidence ingestion, DB writes, schema changes, runtime exposure, endpoint registration, live LLM call, deployment action, production-readiness assertion, or cross-repo runtime integration is allowed by this slice.

## Payroll / Compliance Consequences

None directly. This is Minerva controlled rehearsal only.

## Security / Role / Tenant Consequences

No live data, no tenant data, no DB access, no RBAC integration. Future live use requires RBAC-before-retrieval and answer-use gates.

## Analytics Consequences

None directly.

## Minerva Consequences

This is the first controlled preview of what Minerva might say to a payroll operator, still non-runtime. It shows answer structure and citation needs without enabling final answer generation or chat exposure.

## Platform Doctrine Implications

- Source/Status Boundary Preservation Doctrine.
- Retrieval Before Exposure Doctrine.
- Answer Preparation Is Not Final Answer Doctrine.
- Citation/Provenance Before Final Answer Doctrine.
- Controlled Rehearsal Is Not Final Answer Doctrine.
- Prompt Is Not Knowledge Doctrine.
- Slice Knowledge Preservation Doctrine.
- No Live Minerva Runtime Until Explicitly Authorised.

## Hardening Implications

- Do not expose rehearsal as final answer.
- Do not answer object-specific questions without object story/runtime evidence.
- Exclude prohibited overclaims.
- Preserve no-live-LLM/no-chat/no-DB boundaries.

## Likely Gotchas

- Answer-shaped text may look final but is still rehearsal.
- Object-specific explanations require object-level evidence.
- Payment/tax/STP treatment requires runtime/payment evidence.
- Citations/provenance are required before final answer.

## Acceptance Criteria

- Rehearsal can be built from a controlled citation/provenance packet.
- Payroll operator question patterns produce deterministic answer sections.
- Included supported claims have citation plans.
- Unsupported and prohibited claims are excluded.
- Object-specific questions without object story/runtime evidence return `INSUFFICIENT_EVIDENCE_FOR_REHEARSAL`.
- Prohibited live/runtime/production overclaims are blocked or excluded.
- `ControlledRehearsalOnly = true`.
- `FinalAnswerPermitted = false`.
- No live LLM, chat, DB, runtime integration, corpus mutation, or production-readiness claim occurs.

## Verification Commands

- `python -m py_compile app/services/controlled_answer_rehearsal_service.py`
- `python -m pytest tests/test_controlled_answer_rehearsal.py -q`
- `python -m pytest tests/test_controlled_citation_provenance_packet.py -q`
- `python -m pytest tests/test_controlled_multi_source_answer_preparation.py -q`
- `python -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `python -m pytest tests/test_payroll_correction_workflow_reasoning_capture.py -q`
- `python -m pytest -q -k "developer_log and durable"`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_controlled_answer_rehearsal_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_controlled_answer_rehearsal_v0_1.md`

## Post-Implementation Review Notes

Placeholder.

## Follow-Up Slices

- Controlled Answer Gate / Safety Boundary.
- Admin Queue Explanation Contract / Object Story Integration Plan.
- Internal read-only answer surface, still no live LLM unless explicitly approved.
- Runtime/object story evidence integration later.

## Current Status

Initial controlled answer rehearsal slice.
