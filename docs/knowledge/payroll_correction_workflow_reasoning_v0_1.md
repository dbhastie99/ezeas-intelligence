# Payroll Correction Workflow Reasoning v0.1

## Purpose

This curated Minerva knowledge artefact captures the payroll-operator workflow reasoning that changed the Workforce correction review plan from the original 5-slice model into the revised 8-slice model. It preserves scenario reasoning and treatment doctrine only. It does not implement Workforce runtime behaviour, Analytics runtime behaviour, DB-backed retrieval, chat exposure, live LLM calls, or Minerva runtime behaviour.

## Boundary Statement

- No runtime Minerva behaviour was added.
- No live LLM was called.
- No chat endpoint was exposed.
- No DB was accessed.
- No corpus mutation occurred.
- No workforce-platform code changed.
- No analytics code changed.
- This is curated reasoning evidence only.
- Implementation is pending for future Workforce slices and this artefact does not claim runtime execution.

## Original 5-Slice Workforce Correction Review Plan

The original plan was:

1. Correction Review Front Door.
2. Persistence and Admin Queue.
3. Supplementary/Retro Readiness Preview.
4. Supplementary Delta Preview.
5. Retro Replay Preview.

That plan was useful for proving an initial operator review path, but slices 4 and 5 were no longer sufficient after detailed payroll scenarios were discussed.

## Why Slices 4 and 5 Were No Longer Sufficient

The original fourth and fifth slices moved too quickly from review readiness into calculation preview. The scenarios showed that the system first needs explicit lifecycle and payment-routing reasoning:

- Finalisation lock changes the admission boundary for late ObjectTime and source-truth changes.
- Payment date can control reporting or tax year treatment even when work was performed in an earlier attribution period.
- Off-cycle payment periods or payment windows may be needed when many late timesheets arrive after regular finalisation lock.
- Banking netting can reduce a not-yet-executed payment, but cannot rewrite an already executed bank payment.
- Payment aggregation can combine multiple PayRuns into one bank payment while each PayRun keeps its own calculation identity and audit story.
- Bucket and semantic total impact must be reviewed before serious supplementary or retro calculation, otherwise attributed-period totals, processed/payment-period totals, locked snapshots, source lineage, and double-counting prevention can be confused.

## Revised 8-Slice Workforce Plan

The revised plan is:

1. Correction Review Front Door - completed.
2. Persistence + Admin Queue - completed.
3. Supplementary/Retro Readiness Preview - completed.
4. ProcessPeriod Lifecycle + ObjectTime Ingress + Payment Window Routing.
5. Bucket / Semantic Totals Correction Impact Review.
6. Supplementary Delta + Payment Netting Preview.
7. Retro Model + Dependency Scan Foundation.
8. Retro Replay Preview.

This replaced the earlier 5-slice plan because the workflow required finalisation lock, payment date/reporting treatment, off-cycle periods, banking netting, and bucket impact review before serious calculation preview.

## Core Payroll Operator Scenarios

### 1. Approved Timesheet Amended After Pay Finalisation

A timesheet or ObjectTime record was approved in error. Pay was finalised. The time is later reduced. The model must preserve source-change evidence, the original finalised payroll truth, the corrected due truth, and the delta treatment. The original finalised PayRun is not silently mutated. The correction review should show what changed, what was originally relied upon, what is now due, and whether the delta routes to supplementary, retro, off-cycle, recovery, or blocked treatment.

### 2. ObjectTime Changes While PayRun Is Still Open

If the ProcessPeriod is open and the PayRunContact is not finalised or relied upon, open CalcInterpreterLine output may be rebuilt or superseded through dirty reprocessing. In this situation the platform can treat the changed ObjectTime as source truth for the still-open calculation and rebuild open calculation lines rather than preserving them as finalised historical payroll truth.

### 3. ObjectTime Changes After PayRun Finalisation But Before Payment Close

If ObjectTime changes after PayRun finalisation but before finalisation lock or payment close, the change can create supplementary review. If the relevant banking or payment window remains open, the supplementary delta may be netted into the banking/payment process. This still preserves calculation identity; it does not mutate the original finalised calculation truth.

### 4. ObjectTime Changes After ProcessPeriod Is Closed For Finalisation

Closed for finalisation means payroll managers are reviewing and the period no longer accepts changes into PayRuns. Late changes default to correction review, retro routing, supplementary routing, off-cycle routing, or blocked treatment according to evidence and lifecycle status. The ProcessPeriod finalisation lock is an admission boundary, not just a display state.

### 5. Negative Supplementary Delta Before Banking

A worker was finalised at $1,000 but corrected due is $500. If payment has not been executed and banking/payment aggregation remains open, the -$500 delta may be netted so the bank payment is $500. This is payment-layer netting, not mutation of calculation truth. The original finalised calculation remains auditable and the payment batch explains the netted payment.

### 6. Negative Delta After Payment

If $1,000 has already been paid and corrected due is $500, the -$500 becomes overpayment/recovery review. It cannot be merged into the already executed bank payment. The correction workflow must preserve the paid historical truth and route the $500 overpayment through governed recovery or adjustment review.

### 7. Fifty Late Timesheets After Finalisation Lock

If many workers cannot submit timesheets before period lock and payroll must proceed to banking, the platform needs a governed off-cycle payment period or off-cycle payment window option. Workers should not be forced to wait until the next regular cycle merely because the regular ProcessPeriod is locked. The off-cycle option must preserve separate lifecycle, approval, payment date, and audit treatment.

### 8. Year-End Payment Date

Work may be performed before year end, but if payment enters the bank after year end, the payment date controls reporting/tax year treatment unless a specific statutory rule says otherwise. Work attribution and payment reporting period are distinct. The workflow must not assume that attributed period automatically controls reporting period.

### 9. Payment Aggregation Across Multiple PayRuns

A payment batch may net regular, supplementary, retro, and adjustment runs into one bank payment. That aggregation must preserve each PayRun's calculation identity and audit story. The payment batch explains money movement; the PayRuns explain calculation reasons.

### 10. Bucket Impact Checkpoint

Before serious supplementary or retro calculation, the payroll bucket model must be reviewed for attributed vs processed/payment period, open vs locked/finalised snapshots, semantic totals, delta/source lineage, and double-counting prevention. This checkpoint protects correction review from mixing current-effective, historical-finalised, payment-period, and attributed-period totals.

## Treatment Decision Model

The decision model should ask:

1. What changed in source truth, and what evidence proves the source truth change?
2. Was the affected ProcessPeriod open, closed for finalisation, finalised, payment-open, payment-executed, or production-locked?
3. Was the PayRunContact open, finalised, relied upon, paid, reversed, or superseded?
4. Can open CalcInterpreterLine rows be rebuilt through dirty reprocessing, or must finalised rows be preserved?
5. Is the delta positive, negative, zero, blocked, or dependent on another source/config change?
6. Is the payment window still open for banking netting?
7. Has the payment already executed, making negative deltas recovery/overpayment review rather than banking netting?
8. Does payment date cross a reporting or tax-year boundary?
9. Is off-cycle payment needed to prevent delayed payment after finalisation lock?
10. What bucket snapshots, semantic totals, and lineage checks are needed before calculation preview?

## Doctrines Captured

- Source Truth Change Capture Doctrine: source changes must be preserved with evidence, provenance, original truth, corrected truth, and delta treatment.
- Open Calculation Rebuild Doctrine: open, unrelied-upon calculation output may be rebuilt or superseded through dirty reprocessing.
- Finalised Payroll Immutability Doctrine: finalised payroll truth is preserved and corrected through review, supplementary, retro, off-cycle, recovery, or blocked paths rather than silent mutation.
- Admission Boundary Doctrine: lifecycle state determines whether changed source truth can enter the current PayRun or must route elsewhere.
- ProcessPeriod Finalisation Lock Doctrine: once closed for finalisation, a ProcessPeriod no longer accepts ordinary changes into PayRuns.
- Finalisation Lock Routes Late Changes Doctrine: late changes after finalisation lock route to correction review, retro, supplementary, off-cycle, recovery, or blocked treatment.
- Payment Date Determines Reporting Period Doctrine: payment date controls reporting/tax year treatment unless a specific statutory rule says otherwise.
- Attribution Period Is Not Payment Period Doctrine: work attribution period and payment reporting period are separate facts.
- Off-Cycle Payment Period Doctrine: governed off-cycle payment periods or windows can handle late payable work without waiting for the next regular cycle.
- Banking Netting Doctrine: open banking/payment aggregation may net positive and negative deltas before payment execution.
- Calculation Identity vs Payment Aggregation Doctrine: PayRuns preserve calculation identity while payment batches may aggregate money movement.
- Payment Aggregation Separation Doctrine: payment aggregation does not erase each PayRun's calculation identity, source evidence, or audit story.
- ProcessPeriod Lifecycle Doctrine: ProcessPeriod state controls source ingress, correction routing, finalisation, and payment readiness.
- ProcessPeriod Lifecycle Event Doctrine: lifecycle transitions are treatment evidence and must be recorded as events.
- Payment Batch Lifecycle Separation Doctrine: payment batch open, approved, transmitted, executed, and closed states are separate from calculation finalisation states.
- Prompt Is Not Knowledge Doctrine: this prompt and discussion are not durable knowledge until curated into a checked-in artefact.
- Slice Knowledge Preservation Doctrine: the slice knowledge record preserves why this reasoning was captured, what it does not implement, and what follow-up slices require.

## Questions Minerva Must Be Able To Answer

### Why is this retro and not an adjustment into the current pay?

Answer pattern: identify the source change, the affected historical attribution period, finalisation/payment lifecycle state, and why current-period adjustment would hide historical correction lineage or reporting treatment.

### Why is this supplementary and not dirty reprocessing?

Answer pattern: show that the original PayRunContact or ProcessPeriod was finalised or relied upon, so open CalcInterpreterLine rebuild is no longer appropriate and a supplementary delta review is required.

### Why can this negative delta be netted before banking but become recovery after payment?

Answer pattern: before payment execution, banking/payment aggregation may net the delta into the bank file; after payment execution, the original money movement is historical paid truth and the negative delta routes to overpayment/recovery review.

### Why did the system create an off-cycle payment option?

Answer pattern: explain that regular ProcessPeriod finalisation lock prevents ordinary ingress, but workers may still need timely payment for late approved time, so a governed off-cycle payment period/window preserves payment timeliness and audit separation.

### Why does payment date matter at year end?

Answer pattern: distinguish performed-work attribution from payment reporting period and state that payment date controls reporting/tax year treatment unless a specific statutory rule says otherwise.

### When do CalcInterpreterLine rows get rebuilt versus preserved?

Answer pattern: rebuild or supersede CalcInterpreterLine rows while the PayRun/PayRunContact remains open and unrelied upon; preserve finalised/relied-upon rows and route changes through correction review after finalisation or payment boundaries.

### Why is the original finalised PayRun not changed?

Answer pattern: finalised payroll immutability preserves audit history, relied-upon calculation truth, and payment/reporting evidence; corrections create explicit deltas rather than rewriting finalised truth.

### What evidence is missing before treatment can be decided?

Answer pattern: require source-change evidence, ProcessPeriod state, PayRunContact finalisation/reliance state, payment batch/window state, payment execution status, payment date/reporting context, bucket snapshot impact, and any statutory rule that overrides normal payment-date treatment.

## Minerva Future Use

Future Minerva answers should use this reasoning to explain why a review item is treated as current reprocess, supplementary, retro, off-cycle, recovery, or blocked. Minerva must cite this artefact only as curated reasoning evidence, not as proof that Workforce implementation exists. Runtime implementation evidence, tests, DB evidence, workflow code, and deployment evidence remain separate future requirements.

## Current Status

Curated reasoning captured. Workforce implementation is pending for future slices. Analytics implementation is pending for future slices. Runtime Minerva exposure is not authorised.
