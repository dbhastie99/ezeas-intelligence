# Canonical Source Response: Pay Process Orchestration v0.1

Canonical source response preserved from the 20 May 2026 Pay Process Orchestration design thread. The content below is intentionally verbose and must not be summarised because it preserves reasoning for Minerva. This file is the authoritative full knowledge capture for Pay Process Orchestration v0.1; shorter structured notes are navigational aids only.

# Minerva Knowledge Pack — Pay Process Orchestration v0.1

## Purpose

Pay Process Orchestration v0.1 is the first "bring it together" payroll theme after the correction and retro foundation slices.

The earlier correction and retro work established the platform's ability to reason about changes, detect candidate correction situations, preserve evidence, govern review, and avoid unsafe mutation of finalised payroll truth. Those foundation slices gave Ezeas the doctrine for asking whether something may need payroll attention and for preventing Minerva from pretending that advisory knowledge is operational execution.

This knowledge pack now brings the major payroll-control surfaces together around the pay-process operating flow:

- ObjectTime and payroll source truth;
- ProcessPeriod and ProcessPeriodGroup context;
- PayRun-level review and operating surfaces;
- Admin Queue exception/review workbench consumption;
- supplementary close-for-review and regular close-for-review gates;
- stale approval detection;
- payment/bank batch freeze doctrine;
- non-ObjectTime source changes such as bank account, deduction, and tax setting changes;
- Slice 1 visibility and classification without execution.

The goal is not to make Minerva run payroll. The goal is to preserve the orchestration doctrine so future implementation slices, retrieval plans, and operator-facing answers can explain why a payroll source change belongs in a particular pay-process state and why the platform must respect review gates before doing anything operational.

This is a knowledge-capture pack, not a runtime feature.

It must not yet execute payment, mutate finalised payroll truth, create bank files, run full retro execution, or bypass review gates.

Pay Process Orchestration v0.1 must remain read-only, advisory, and doctrine-preserving unless a later Workforce implementation slice explicitly builds controlled runtime behaviour.

## Core Decision

The core decision is that Pay Process Orchestration is a governed operating layer over existing payroll source truth, review truth, and payment-control truth.

It is not a replacement for the existing Admin Queue.

It is not a replacement for ObjectTime.

It is not payroll calculation execution.

It is not bank execution.

It is not finalised truth mutation.

It is not full retro execution.

It is the classification and operating doctrine that lets the platform answer:

- what changed;
- which worker and period are affected;
- which payroll-control state matters;
- whether an action is current-period, supplementary, out-of-cycle, retro, no-impact, blocked, stale, or frozen;
- which surface should show the operator the issue;
- which review gate must be respected before further action.

The slice draws a hard line between operational visibility/classification and execution. Slice 1 is visibility/classification, not execution.

## Slice 1 Purpose

Slice 1 exists to create the first durable pay-process orchestration knowledge and classification foundation.

It should let the platform identify that a source-truth change has payroll significance, route that significance to the right worker-period context, and expose the right review or action state without performing payroll execution.

Slice 1 is operational visibility/classification rather than execution because the platform first needs a stable vocabulary and control spine:

- source family;
- worker;
- ProcessPeriodGroup;
- ProcessPeriod;
- action state;
- inclusion status;
- review gate;
- stale approval state;
- no-impact classification;
- supplementary/out-of-cycle/payment execution distinction.

Without those concepts, later execution slices would either hide decisions, bypass review, or incorrectly conflate payroll calculation, payment timing, and cash movement.

The purpose is not to process PayRuns. It is not to create bank files. It is not to push workers into payment. It is not to mutate finalised truth. It is not to perform complete retro execution. It is to preserve and expose the decision context needed before those operational steps can be safely designed.

## Existing Admin Queue Is Not Rebuilt

Admin Queue = cross-platform exception/review workbench

PayRun Control Centre = pay-process operating surface

The existing Admin Queue is consumed and not rebuilt.

The Admin Queue already represents a cross-platform exception and review workbench. It can surface payroll-related issues, worker attention, review needs, blockers, warnings, dirty source conditions, and other operator-facing exceptions. Rebuilding it inside Pay Process Orchestration would duplicate concepts, fragment operator attention, and create competing queues with unclear ownership.

Pay Process Orchestration should use the Admin Queue as an existing workbench surface and provide better payroll-process context to it. The doctrine is:

- the Admin Queue is where cross-platform exceptions and review actions can be seen;
- the PayRun Control Centre is where the pay-process operating state can be inspected;
- Pay Process Orchestration determines classification, routing, and control context;
- the Admin Queue should consume those classifications where relevant.

The reason the Admin Queue is not rebuilt is that Pay Process Orchestration is not a queue product. It is a payroll-control and routing layer. A payroll source-truth change may create an Admin Queue item, but the queue is not the source of truth for the payroll impact. The source of truth remains the underlying domain evidence and the pay-process action classification.

Rebuilding the Admin Queue would also blur review responsibility. Operators need one exception/review workbench, not a new payroll-only queue that looks similar but follows different rules. Pay Process Orchestration should strengthen the existing queue by giving it precise worker-period-source-family context.

## ObjectTime Is the Primary Payroll Source-Truth Driver

ObjectTime drives payroll calculation impact.

ObjectTime is the primary payroll source-truth driver because it represents worked-time source evidence that directly affects payroll calculation.

When ObjectTime changes, the payroll calculation may change because the worker's hours, dates, time categories, interpretation inputs, or payable work evidence may have changed. That is why ObjectTime change detection belongs at the centre of Pay Process Orchestration v0.1.

ObjectTime is not merely a display row. It is source-truth evidence for the worker's worked-time contribution to a payroll period. Payroll treatment depends on the complete ObjectTime set for the worker and ProcessPeriod, not only on the changed database row.

This is why ObjectTime is treated differently from bank accounts, tax settings, and deductions.

Bank accounts drive payment instruction resolution.

Tax settings drive withholding/gross-to-net context.

Deductions drive deduction application and remittance context.

Those changes can be payroll-adjacent and financially important, but they are not ObjectTime-style payroll source truth. They do not mean the worker's worked-time source evidence for a ProcessPeriod changed.

ObjectTime drives payroll calculation impact because changes to worked-time source truth can change payroll lines, ordinary hours, overtime, allowances, leave interactions, and period-level calculation outcomes. Bank, tax, and deduction changes have their own doctrine and should not be forced into the ObjectTime impact model.

## ObjectTime Impact Action Scope

ObjectTime impact action scope = Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime

The ObjectTime impact action scope is worker-period scoped, not row-scoped.

The action belongs to:

- Worker;
- ProcessPeriodGroup;
- ProcessPeriod;
- SourceFamily:ObjectTime.

The reason for this scope is that payroll impact is assessed at the level where payroll calculation happens. A single ObjectTime row change may affect calculation, but the calculation result depends on the worker's complete ObjectTime set for the ProcessPeriod and the applicable ProcessPeriodGroup context.

If the platform created one action per changed row, repeated edits would fragment the evidence and create multiple competing review items for the same worker-period payroll question. That would make review harder and would imply that each row can be assessed independently, which is not safe for payroll calculation.

Instead, repeated edits should update one active action and preserve every edit in evidence.

The active action should represent the current need to reassess the worker's ObjectTime set for that ProcessPeriod. The evidence trail should preserve all edits so the operator can see what changed over time, why the action is still active, and whether an approval has become stale.

The action is period-scoped because the question is: given the current ObjectTime truth for this worker in this ProcessPeriod, what payroll impact classification applies now?

It is not row-scoped because the question is not: did this one row independently create one isolated payroll outcome?

## Period-Level ObjectTime Assessment

One ObjectTime record change requires assessment of the worker's ObjectTime set for the ProcessPeriod.

Payroll calculation is period contextual. A row change can alter totals, overtime thresholds, ordinary-time patterns, allowance triggers, leave interactions, and comparison against expected work evidence. Those outcomes are not always visible from the changed row alone.

Therefore, the assessment must consider:

- the changed ObjectTime evidence;
- other ObjectTime rows for the same worker and ProcessPeriod;
- inclusion status for the ProcessPeriod;
- the ProcessPeriodGroup context;
- whether the ProcessPeriod is open, closed for regular review, still open for supplementary review, frozen, or fully closed;
- whether prior approval attached to an earlier assessed snapshot;
- whether the changed evidence creates no payroll impact or deferred field-level impact detection.

The doctrine is deliberately conservative. A single source edit should not be ignored merely because the edited field looks small. Until field-level impact filters are implemented, the platform should preserve the action and classify limitations honestly.

## ObjectTime Is 1:1 With ProcessPeriod

ObjectTime is 1:1 with ProcessPeriod for this design.

For Pay Process Orchestration v0.1, ObjectTime impact is resolved against the ProcessPeriod to which the worked-time evidence belongs. This design avoids cross-period ambiguity in the first slice and keeps action scope aligned with the payroll period that must be assessed.

The 1:1 doctrine means the action should not treat one ObjectTime row as spanning multiple ProcessPeriods for Slice 1. If future data models need split-period treatment, that should be a later explicit design. Slice 1 should preserve the simpler and safer rule:

- one worker;
- one ProcessPeriodGroup;
- one ProcessPeriod;
- one ObjectTime source-family action.

This also keeps approval, stale detection, inclusion status, and supplementary routing understandable for operators.

## ProcessPeriodGroup Must Be Effective-Date Aware

Historical ObjectTime must use effective-date-aware ProcessPeriodGroup resolution.

The ProcessPeriodGroup matters because it carries the payroll-cycle context that determines the relevant ProcessPeriod. However, historical ObjectTime must not be resolved using only the worker's current payroll group or today's configuration if the source evidence belongs to an earlier time.

Effective-date-aware ProcessPeriodGroup resolution is required because workers can change payroll groups, employment context can change, payroll calendars can change, and historical source evidence must be interpreted in the period context that applied at the relevant date.

Without effective-date awareness, the platform could route an old ObjectTime change into the wrong ProcessPeriodGroup, produce the wrong ProcessPeriod, and create a misleading action. That would make stale approvals, supplementary decisions, and retro candidates unreliable.

Slice 1 should preserve this doctrine even if the first implementation only classifies and tests the concept. It should not silently resolve all ObjectTime using current state.

## ProcessPeriod State and Routing

ProcessPeriod state determines treatment routing.

Regular close for review, supplementary close for review, and bank/payment batch generation are separate gates.

A worker-period ObjectTime action can mean different things depending on the ProcessPeriod lifecycle:

- before regular close for review, it may be ordinary current-period reprocessing visibility;
- after regular close for review but before supplementary close for review, it may be a supplementary candidate;
- after supplementary close for review, it should not silently enter the same-cycle supplementary path;
- after bank/payment batch generation, it must not silently change the generated cash movement package;
- after full close, it may need later governed correction, retro, or review.

The state matters because payroll operations are not merely calculation. Operators need stable populations for review and payment preparation. If source truth changes after a review gate, the platform must surface the issue and classify it rather than silently reopen the gate.

ProcessPeriod routing is therefore the control layer that keeps source-truth changes from bypassing payroll review.

## Supplementary Close for Review

Supplementary close for review is required.

A regular close-for-review gate is not enough because real payroll processes often have late source changes after the regular run is reviewed but before payment preparation is complete. The platform needs a governed same-cycle corrective treatment path that is not the same as silently reopening the regular run.

Supplementary close-for-review gives operators a separate gate:

- the regular run can be reviewed and stabilised;
- late approved or changed source evidence can be classified as supplementary where allowed;
- same-cycle corrective treatment can be reviewed separately;
- the supplementary window can be closed before payment preparation;
- changes after that point can be routed to later governed treatment.

Without supplementary close for review, the platform would collapse late changes into either unsafe regular-run mutation or overly broad retro/out-of-cycle handling. The doctrine needs the middle state because late payroll source changes are common and need controlled same-cycle treatment.

## Supplementary vs Out-of-Cycle vs Bank Execution

Supplementary = extra/corrective payroll treatment

Out-of-cycle = payment timing

Bank/payment execution = cash movement

These concepts must remain distinct.

Supplementary is payroll treatment. It means an extra or corrective payroll treatment path for a period, commonly for late or changed source evidence that should be handled separately from the regular run.

Out-of-cycle is payment timing. It means a payment occurs outside the ordinary scheduled payment timing. A supplementary payroll treatment may or may not be paid out-of-cycle. An out-of-cycle payment may or may not originate from supplementary payroll treatment.

Bank/payment execution is cash movement. It means the creation, transmission, or execution of payment instructions such as bank files or payment batches.

The platform must not conflate these because each has different controls:

- supplementary treatment controls payroll calculation/review treatment;
- out-of-cycle controls when payment happens;
- bank/payment execution controls cash movement and financial freeze.

The distinction prevents Minerva and the platform from answering as if "supplementary" automatically means "paid immediately" or as if "out-of-cycle" automatically means "a new payroll calculation source changed." They are related operational concepts, but they are not synonyms.

## Bank File / Payment Batch Generation Is an Absolute Freeze

Once the bank file/payment batch is generated, its contents cannot be silently changed.

Bank/payment batch generation is an absolute freeze point because it creates a financial-control boundary. After cash movement instructions are prepared, the platform must not silently alter them because doing so would create payment-control risk, reconciliation risk, audit ambiguity, and potential mismatch between what was approved and what is paid.

If source truth changes after bank/payment batch generation, the platform can surface the change, classify it, and route it for governed follow-up. It must not mutate the generated batch behind the operator's back.

This freeze is stronger than ordinary review stability. Regular review close and supplementary review close are payroll review gates. Bank/payment batch generation is a cash-movement gate. It must be treated as an absolute control boundary.

The key rule is not only that the bank file should not change. The key rule is that the contents cannot be silently changed. If a future product supports void/reissue, regeneration, reversal, or exception handling, those must be explicit governed actions with evidence.

## Inclusion Status Matters

Slice 1 needs inclusion status rather than only readiness.

Readiness alone says whether something appears ready or blocked. Inclusion status answers whether the worker/source evidence is included in the relevant PayRun or treatment population.

For Pay Process Orchestration, inclusion status matters because the platform needs to know whether an ObjectTime change affects:

- a worker already included in a draft or reviewed PayRun;
- a worker excluded from the current PayRun;
- a source row that should be included but is missing;
- a source row that is outside the current ProcessPeriod;
- a supplementary candidate;
- a later correction or retro path.

Without inclusion status, the platform may say something is ready while missing the more important question: included where, in which worker-period treatment, under which pay-process gate?

Inclusion status is also needed for stale approval detection. If approval attached to a snapshot that included a particular source set, and the source set changes, the platform needs to know whether the approved inclusion basis still matches current source truth.

## Approved Actions Become Stale If Source Truth Changes

Approval attaches to the assessed snapshot.

Approved actions become stale if source truth changes.

An approval means the operator approved the classification or treatment based on the source evidence and assessment available at that time. It does not mean all future edits to ObjectTime, bank instructions, tax settings, or deduction instructions are automatically approved.

If the source truth changes after approval, the approval must be treated as attached to the earlier assessed snapshot. The platform should surface that the action may need reassessment, reapproval, or a new decision depending on the change and lifecycle state.

This doctrine protects review integrity. Otherwise, a worker-period action could be approved, then source truth could change, and the system would still behave as if the approval covered the new truth. That would bypass review.

Stale approval detection is also why repeated edits should update one active action while preserving every edit in evidence. Operators need to see that approval was valid for one snapshot and is now stale because the underlying source evidence changed.

## No-Impact Changes

NO_PAYROLL_IMPACT

FIELD_LEVEL_IMPACT_FILTER_DEFERRED

NO_PAYROLL_IMPACT_DETECTION_NOT_IMPLEMENTED

No-impact changes are important, but Slice 1 must be honest about what is implemented.

Some source edits may not affect payroll. For example, a metadata-only change or a field that has no calculation impact might eventually be classified as no payroll impact. However, field-level no-impact detection is deferred for Slice 1 because correct impact detection requires careful mapping between fields, source families, payroll calculation rules, inclusion state, and period context.

The doctrine is:

- NO_PAYROLL_IMPACT is a valid classification concept;
- FIELD_LEVEL_IMPACT_FILTER_DEFERRED means field-specific filtering is intentionally not implemented yet;
- NO_PAYROLL_IMPACT_DETECTION_NOT_IMPLEMENTED means the platform must not claim it has completed no-impact detection if it has not.

Field-level no-impact detection is deferred because an apparently small field may still affect payroll through interpretation, inclusion, evidence provenance, audit, or downstream treatment. It is safer in Slice 1 to preserve the action and classify the limitation than to prematurely drop evidence.

## Bank Account Doctrine

A bank account change is not tied to a PayRun.

Bank account changes are date-effective payment instruction truth.

Bank accounts drive payment instruction resolution.

A bank account change affects where payment should go, not whether ObjectTime worked-time source evidence changed. It is not ObjectTime-style payroll source truth and should not be forced into the ObjectTime impact action scope.

The reason a bank account change is not tied to a PayRun is that bank instructions are date-effective payment instruction truth. A worker's bank account setup may apply to payments with payment dates in a particular effective range, and payment resolution depends on the payment date and payment instruction rules, not simply on the existence of one PayRun.

A bank account change may matter for payment readiness, payment allocation, bank-file preparation, or payment execution. It may create an action or review need. But it should be classified according to payment instruction doctrine, not as if it were a change to worked-time source truth.

This distinction matters because bank-account changes can occur after payroll calculation but before payment execution. They may change payment destination without changing gross-to-net payroll calculation. The platform must explain that difference clearly.

## Deduction Doctrine

Deduction setup changes are not ObjectTime-style payroll source truth.

Deduction setup changes are date-effective deduction instruction changes.

Deductions drive deduction application and remittance context.

A deduction setup change can affect net pay, deduction application, recovery, obligation handling, remittance, or third-party payment context. But it is not a change to ObjectTime worked-time source evidence.

Deduction setup must be treated as date-effective deduction instruction truth. Its impact depends on the deduction's effective date, applicability, priority, affordability, balance, payroll period, payment date where relevant, and remittance context.

The platform must not collapse deduction setup changes into the ObjectTime impact model. Doing so would confuse the reason for recalculation or review. ObjectTime answers "did worked-time source truth change for this worker-period?" Deduction setup answers "did deduction instruction context change for the relevant effective payroll/payment context?"

The distinction also protects remittance doctrine. A deduction may affect not only worker net pay but also obligation and remittance handling. That context is broader than ObjectTime.

## Tax Doctrine

Tax setting changes are gross-to-net and payment-date context.

Tax settings drive withholding/gross-to-net context.

Tax setting changes are not ObjectTime-style payroll source truth. They influence how gross pay becomes net pay through withholding and tax configuration, often in relation to payment-date context.

The payroll calculation may need tax context, but the source-family doctrine is different from ObjectTime. ObjectTime provides worked-time source evidence. Tax settings provide gross-to-net and payment-date context for withholding.

This matters because a tax setting may change after worked-time evidence is stable. The question is not whether the worker worked different hours. The question is whether withholding context or payment-date tax treatment changed for the relevant payment or payroll calculation.

The platform should preserve that separation so Minerva does not tell users that tax setting changes are ObjectTime changes or that ObjectTime impact action scope covers all gross-to-net doctrine.

## Key Consequence

The key consequence is that Pay Process Orchestration v0.1 is a control and classification doctrine, not an execution feature.

Slice 1 is visibility/classification, not execution.

It brings together ObjectTime source-truth impact, ProcessPeriod and ProcessPeriodGroup routing, Admin Queue consumption, PayRun Control Centre operating visibility, close-for-review gates, supplementary treatment, out-of-cycle timing, bank/payment execution freeze, stale approvals, inclusion status, no-impact limitations, and non-ObjectTime source-family doctrine.

It must not silently modernise or compress those distinctions.

It must preserve the repeated doctrine because the repetition is useful: it prevents future slices from collapsing payroll treatment, payment timing, and cash movement into one unsafe concept.

The result should be that Minerva can answer detailed user questions without pretending to run payroll:

- Pay Process Orchestration classifies and explains;
- ObjectTime drives payroll calculation impact;
- bank accounts drive payment instruction resolution;
- tax settings drive withholding/gross-to-net context;
- deductions drive deduction application and remittance context;
- the Admin Queue remains the cross-platform exception/review workbench;
- the PayRun Control Centre remains the pay-process operating surface;
- bank/payment batch generation is an absolute freeze;
- approval attaches to an assessed snapshot;
- source-truth changes after approval can make approval stale;
- no-impact detection exists as doctrine but field-level filtering is deferred;
- Slice 1 is operational visibility/classification rather than execution.

## Suggested Minerva Golden Questions

What is the full purpose of Pay Process Orchestration v0.1?

Why is the Admin Queue not rebuilt?

What is the ObjectTime impact action scope?

Why is the ObjectTime impact action period-scoped rather than row-scoped?

What is the difference between supplementary, out-of-cycle, and bank/payment execution?

Why is bank/payment batch generation an absolute freeze point?

Why is a bank account change not tied to a PayRun?

Why are deductions not ObjectTime-style payroll source truth?

Why are tax settings gross-to-net/payment-date context?

What is the consequence of Slice 1?

## Expected Answer Anchors

Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime

Admin Queue = cross-platform exception/review workbench

PayRun Control Centre = pay-process operating surface

Supplementary = payroll treatment / extra or corrective payroll treatment

Supplementary = extra/corrective payroll treatment

Out-of-cycle = payment timing

Bank/payment execution = cash movement

bank/payment batch generation is an absolute freeze

approval attaches to assessed snapshot

bank account changes are date-effective payment instruction truth

deduction setup changes are date-effective deduction instruction changes

tax setting changes are gross-to-net/payment-date context

Slice 1 is visibility/classification, not execution
