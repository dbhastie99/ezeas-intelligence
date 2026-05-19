# Slice Knowledge Record - Minerva Correction Workflow Scenario Reasoning Capture v0.1

## Purpose

This slice captures payroll-operator correction workflow reasoning as durable Minerva-accessible knowledge. It records why the Workforce correction review plan changed from the original 5-slice model to the revised 8-slice model, without implementing runtime workflow code.

## Product Objective

Preserve the reasoning needed for future Minerva answers about why a correction review item is current reprocess, supplementary, retro, off-cycle, recovery, or blocked.

## User Story

As a future Minerva user or operator, I need the system to explain correction treatment decisions using durable reasoning about ObjectTime changes, ProcessPeriod lifecycle, PayRun finalisation, payment window state, payment date/reporting treatment, banking netting, off-cycle windows, and bucket impact.

## Source Truth

Source truth for this slice is curated reasoning captured in `docs/knowledge/payroll_correction_workflow_reasoning_v0_1.md`. It is not runtime evidence, DB evidence, workflow execution evidence, analytics evidence, or implementation proof.

## Current Platform Context

Workforce correction review planning has completed the front-door, persistence/admin queue, and supplementary/retro readiness preview slices. Discussion of payroll operator scenarios showed that the next work needed lifecycle and payment-routing reasoning before serious supplementary or retro calculation preview.

## Why This Slice Exists Now

The earlier 5-slice correction-review plan moved from readiness into supplementary and retro calculation too quickly. The revised plan needs durable reasoning for finalisation lock, payment date/reporting period, off-cycle payment options, banking netting, payment aggregation, and bucket impact review before later implementation slices.

## What This Slice Implements

- A curated payroll correction workflow reasoning artefact.
- A saved Codex prompt artefact.
- This slice knowledge record.
- Tests that assert the reasoning artefact includes the revised 8-slice plan, required scenarios, doctrines, Minerva answer examples, and boundary statements.

## What This Slice Explicitly Does Not Implement

This slice does not add runtime Minerva behaviour, call a live LLM, expose a chat endpoint, access a DB, mutate corpus, change workforce-platform code, change analytics code, implement ProcessPeriod lifecycle, implement payment windows, implement off-cycle payments, implement banking netting, implement bucket recalculation, implement supplementary calculation, implement retro calculation, or claim runtime execution.

## Affected Tables / Models

None. No DB/schema changes.

## Affected Services

None.

## Affected API / Routes

None.

## Affected UI

None.

## Affected Tests

- `tests/test_payroll_correction_workflow_reasoning_capture.py`

Regression tests for controlled multi-source retrieval and answer preparation remain relevant because this artefact is intended for future Minerva retrieval/answer-preparation use, but this slice does not integrate it into runtime retrieval.

## Evidence / Story Requirements

- OriginalPlan: record the original 5-slice correction-review model.
- RevisionReason: explain why slices 4 and 5 were insufficient.
- RevisedPlan: record the revised 8-slice Workforce plan.
- ScenarioReasoning: capture the ten payroll operator scenarios.
- DoctrineCapture: preserve source truth, open rebuild, finalised immutability, finalisation lock, payment date, off-cycle, banking netting, payment aggregation, ProcessPeriod lifecycle, prompt/knowledge, and slice knowledge doctrines.
- TreatmentDecisionModel: list the evidence needed to decide current reprocess, supplementary, retro, off-cycle, recovery, or blocked treatment.
- MinervaAnswerPatterns: include concise answer patterns, not final live answer generation.
- BoundaryResult: explicitly state no runtime Minerva, live LLM, chat, DB, corpus mutation, workforce-platform code, or analytics code changes.

## Irreversible Actions Prohibited

No corpus mutation, no DB writes, no schema changes, no runtime exposure, no endpoint registration, no live LLM call, no workforce-platform implementation, no analytics implementation, no payment execution, no payroll finalisation, and no production deployment.

## Payroll / Compliance Consequences

No direct payroll or compliance execution occurs. The artefact preserves reasoning that future Workforce slices must use when deciding payment date/reporting period, finalisation lock consequences, off-cycle payment treatment, banking netting, recovery routing, and audit preservation.

## Security / Role / Tenant Consequences

No live data, tenant data, DB access, RBAC integration, or runtime exposure occur in this slice. Future workflow implementation must enforce tenant, role, and authorisation gates before retrieval, review, payment, recovery, or correction execution.

## Analytics Consequences

None directly. Analytics implementation and reporting integration remain future work.

## Minerva Consequences

This artefact gives future Minerva retrieval and answer-preparation slices durable reasoning for explaining correction workflow treatment. It is reasoning evidence only and must not be cited as proof that workflow runtime exists.

## Platform Doctrine Implications

- Prompt Is Not Knowledge Doctrine
- Slice Knowledge Preservation Doctrine
- Source Truth Change Capture Doctrine
- Finalised Payroll Immutability Doctrine
- Payment Date Determines Reporting Period Doctrine
- Attribution Period Is Not Payment Period Doctrine
- Calculation Identity vs Payment Aggregation Doctrine

## Hardening Implications

- Do not treat captured reasoning as implementation proof.
- Do not expose live Minerva answers from this artefact without future retrieval and answer gates.
- Do not let payment aggregation erase PayRun calculation identity.
- Do not let banking netting mutate calculation truth.
- Do not let current-pay adjustments hide retro or supplementary correction lineage.
- Do not claim DB, workflow, analytics, or production runtime behaviour from this knowledge-capture slice.

## Likely Gotchas

- Closed for finalisation is an admission boundary, not only a display state.
- Negative deltas before banking and after payment have different treatment.
- Payment date and attribution period are distinct.
- Off-cycle payment periods solve timeliness without reopening the regular locked period.
- Payment batches can aggregate money movement without merging PayRun calculation identity.
- Bucket/semantic totals must be reviewed before serious supplementary or retro calculation.

## Acceptance Criteria

- Reasoning artefact exists under `docs/knowledge`.
- It records the original 5-slice and revised 8-slice plans.
- It explains why the plan changed.
- It captures all required scenarios and doctrines.
- It includes the "Questions Minerva Must Be Able To Answer" section with answer patterns.
- It states implementation is pending for future Workforce slices.
- It explicitly states no runtime Minerva, live LLM, chat endpoint, DB access, corpus mutation, workforce-platform code change, or analytics code change occurred.
- Tests pass.

## Verification Commands

- `python -m pytest tests/test_payroll_correction_workflow_reasoning_capture.py -q`
- `python -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `python -m pytest tests/test_controlled_multi_source_answer_preparation.py -q`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/knowledge/payroll_correction_workflow_reasoning_v0_1.md`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md`

## Post-Implementation Review Notes

Placeholder.

## Follow-Up Slices

- Workforce ProcessPeriod lifecycle and ObjectTime ingress implementation.
- Workforce payment window routing and finalisation lock implementation.
- Bucket / semantic totals correction impact review.
- Supplementary delta and payment netting preview.
- Retro model and dependency scan foundation.
- Retro replay preview.
- Minerva controlled onboarding of this reasoning as retrievable curated evidence.

## Current Status

Initial correction workflow scenario reasoning capture slice.
