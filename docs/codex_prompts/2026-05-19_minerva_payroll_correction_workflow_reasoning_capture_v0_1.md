# Minerva Payroll Correction Workflow Reasoning Capture v0.1

Create a curated Minerva knowledge artefact explaining the payroll-operator workflow reasoning that changed the Workforce correction review plan from the original 5-slice model into the revised 8-slice model.

This is a knowledge-capture slice only. It is not runtime Minerva, live LLM, chat exposure, DB-backed retrieval, workforce-platform implementation, or analytics implementation.

## Required Artefacts

- `docs/knowledge/payroll_correction_workflow_reasoning_v0_1.md`
- `docs/codex_prompts/2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md`
- `docs/slice_knowledge/2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md`
- `tests/test_payroll_correction_workflow_reasoning_capture.py`

## Required Reasoning To Capture

Capture:

- the original 5-slice Workforce correction-review plan;
- why slices 4 and 5 were no longer sufficient;
- the revised 8-slice plan;
- payroll operator scenarios that drove the revision;
- doctrines agreed in discussion;
- treatment decision model;
- what Minerva should be able to answer from this reasoning later.

## Core Scenarios

Include:

1. Approved timesheet amended after pay finalisation.
2. ObjectTime changes while PayRun is still open.
3. ObjectTime changes after PayRun finalisation but before payment close.
4. ObjectTime changes after ProcessPeriod is closed for finalisation.
5. Negative supplementary delta before banking.
6. Negative delta after payment.
7. Fifty late timesheets after finalisation lock.
8. Year-end payment date.
9. Payment aggregation across multiple PayRuns.
10. Bucket impact checkpoint.

## Doctrines

Include the Source Truth Change Capture Doctrine, Open Calculation Rebuild Doctrine, Finalised Payroll Immutability Doctrine, Admission Boundary Doctrine, ProcessPeriod Finalisation Lock Doctrine, Finalisation Lock Routes Late Changes Doctrine, Payment Date Determines Reporting Period Doctrine, Attribution Period Is Not Payment Period Doctrine, Off-Cycle Payment Period Doctrine, Banking Netting Doctrine, Calculation Identity vs Payment Aggregation Doctrine, Payment Aggregation Separation Doctrine, ProcessPeriod Lifecycle Doctrine, ProcessPeriod Lifecycle Event Doctrine, Payment Batch Lifecycle Separation Doctrine, Prompt Is Not Knowledge Doctrine, and Slice Knowledge Preservation Doctrine.

## Revised 8-Slice Workforce Plan

Record:

1. Correction Review Front Door - completed.
2. Persistence + Admin Queue - completed.
3. Supplementary/Retro Readiness Preview - completed.
4. ProcessPeriod Lifecycle + ObjectTime Ingress + Payment Window Routing.
5. Bucket / Semantic Totals Correction Impact Review.
6. Supplementary Delta + Payment Netting Preview.
7. Retro Model + Dependency Scan Foundation.
8. Retro Replay Preview.

Explain that this replaced the earlier 5-slice plan because the workflow required finalisation lock, payment date/reporting treatment, off-cycle periods, banking netting, and bucket impact review before serious calculation preview.

## Boundary Requirements

State:

- No runtime Minerva behaviour was added.
- No live LLM was called.
- No chat endpoint was exposed.
- No DB was accessed.
- No corpus mutation occurred.
- No workforce-platform code changed.
- No analytics code changed.
- This is curated reasoning evidence only.

## Verification

Run:

- `python -m pytest tests/test_payroll_correction_workflow_reasoning_capture.py -q`
- `python -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `python -m pytest tests/test_controlled_multi_source_answer_preparation.py -q`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/knowledge/payroll_correction_workflow_reasoning_v0_1.md`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md`

Suggested commit message:

`minerva-payroll-correction-workflow-reasoning-v01`
