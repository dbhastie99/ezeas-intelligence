# Minerva Knowledge Capture — Admitted Draft PayRun Processing Bridge

This document is a reconstructed canonical source response created after the original full source response was unavailable in the repository/current Codex context. It is reconstructed from preserved thread continuance context, Platform Doctrine, Hardening Doctrine, and agreed workforce-platform doctrine. It replaces the incomplete/truncated attempted capture and should be treated as the authoritative source response for the Admitted Draft PayRun Processing Bridge v0.1 Minerva knowledge pack from this point forward.

## Purpose of this knowledge capture

This knowledge capture records the doctrine and implementation boundaries for:

**Admitted Draft PayRun Processing Bridge v0.1**

The bridge belongs to the workforce-platform Pay Process / payroll end-to-end hardening stream. Its purpose is to preserve the reasoning behind the next controlled transition: moving from an authorised pay-process admission into deterministic draft PayRunContact processing, without weakening the decision, admission, processing, readiness, finalisation, or payment boundaries.

This source response is intentionally authoritative for Minerva knowledge capture. Later structured Minerva knowledge documents may summarise, index, or navigate it, but they must not replace it as the canonical source response for this reconstructed slice.

## 1. What we are doing

This slice bridges authorised admission into deterministic draft PayRunContact processing.

It sits after PayRunActionDecision/admission and before review/finalisation. It is the controlled handoff from a governed admission decision into the deterministic Workforce Platform processing path that can calculate draft payroll output for the relevant PayRunContact.

The bridge does not decide whether the worker-period should be admitted. It does not finalise payroll. It does not make payments. It does not generate bank files. It does not replace payroll calculation services. It connects an already authorised admission to the correct draft processing path and preserves evidence of the handoff.

## 2. Why this slice is needed now

The platform now has the major foundations needed before runtime draft processing can be safely connected:

- Pay Process action register foundations;
- PayRunActionDecision governance;
- admission into draft PayRuns;
- readiness and review foundations;
- ProcessPeriod lifecycle status;
- operator surfaces for pay-process visibility and control.

The remaining gap is runtime processing of admitted worker-periods. Admission can explain why a worker-period is allowed into a draft PayRun, but admission is not the same as calculation. The next step is to process the admitted worker-period through deterministic services so draft payroll output can exist for operator review without jumping ahead to finalisation or payment.

## 3. The core doctrine

The canonical governed path is:

```text
source change
→ impact assessment
→ action register
→ PayRunActionDecision
→ admission authority
→ PayRun / PayRunContact resolved or created where authorised
→ deterministic draft PayRunContact processing
→ calculated draft payroll output
→ evidence/story
→ readiness update
```

Each step has a distinct responsibility and must not be collapsed. Source change and impact assessment identify payroll-relevant change. The action register records the governed action. PayRunActionDecision records the decision authority. Admission authority controls whether PayRun or PayRunContact creation/resolution is permitted. Deterministic draft processing calculates draft payroll output. Evidence/story preserves explainability. Readiness update presents the operator/control consequence.

Collapsing these steps would weaken governance. A processing bridge that decides admission would bypass PayRunActionDecision. A readiness update that pretends calculation occurred would bypass processing. A payment action that follows directly from admission would bypass review/finalisation controls.

## 4. PayRunActionDecision remains the authority source

The bridge must not independently decide whether a worker-period should be included in a PayRun.

Admission must be traceable to PayRunActionDecision or explicit policy-backed authority. If the decision does not authorise PayRun creation, the bridge must not create a PayRun. If the decision does not authorise PayRunContact creation, the bridge must not create a PayRunContact.

The bridge may read decision/admission artefacts and use them to resolve the authorised target, but it does not promote an action from pending to approved, does not infer approval from convenience, and does not treat processing success as retroactive admission authority.

## 5. Processing must be deterministic

Payroll outcomes must be calculated by deterministic Workforce Platform services.

Minerva must not calculate payroll dollars, tax, net pay, deductions, statutory obligations, award entitlements, payment amounts, bank-file values, or final payroll outcomes. Minerva may explain doctrine, cite evidence, and describe the expected controlled path, but it remains advisory rather than computational.

The processing bridge must therefore call or prepare a call into deterministic platform logic. The authority for payroll amounts remains the platform's payroll calculation path, not a generated explanation, a chat answer, or a reconstructed knowledge document.

## 6. The bridge must use existing processing paths

The bridge must inspect and reuse the existing deterministic PayRun/PayRunContact processing path where safe.

It must not invent a parallel payroll processor. A parallel processor would create conflicting payroll truth, duplicate calculation logic, and a second authority path outside the established Workforce Platform runtime.

If the existing path is unsafe, unclear, unavailable, or not callable for the admitted worker-period, the bridge must stop with a blocker. The correct result in that case is evidence-bearing blockage, not improvised payroll calculation.

## 7. Draft/unfinalised/unfrozen guardrail

The bridge may only process draft, unfinalised, and unfrozen PayRuns.

It must not silently mutate finalised PayRuns, paid PayRuns, frozen PayRuns, or payment-batch-generated PayRuns. It must not change payroll truth after financial-control freeze points under the appearance of ordinary draft processing.

Late changes must route to governed later treatment, supplementary, retro, recovery, or explicit regeneration workflows. The bridge is for admitted draft processing, not post-finalisation correction or cash movement.

## 8. ProcessPeriod lifecycle matters

ProcessPeriod.LifecycleStatusCode is payroll-control truth, not cosmetic UI state.

IsOpen/IsClosed is insufficient because payroll control needs to distinguish materially different states: open, regular closed for review, supplementary review open, supplementary review closed, payment/bank batch generated, and closed.

The bridge must respect lifecycle context because the same worker-period change can require different treatment depending on whether the relevant period is still open for ordinary processing, closed for review, in supplementary review, already frozen by payment/bank batch generation, or fully closed.

## 9. PayRunContact creation and resolution

PayRunContact may only be resolved or created where authorised by the decision/admission path.

Resolution should prefer an existing authorised PayRunContact where one already represents the admitted worker-period in the target draft PayRun. Creation must be idempotent and must preserve source action, decision, admission, and processing evidence.

The bridge must not create a new PayRunContact simply because processing needs a target. The target must be justified by the governed admission path and recorded so repeated execution does not duplicate contacts or obscure why the contact exists.

## 10. PayRun creation and resolution

PayRun creation/resolution must obey policy and decision authority.

The bridge should prefer an existing authorised target PayRun where available. It must not create a PayRun on its own authority. If policy or decision authority allows PayRun creation, creation must be traceable, idempotent, and scoped to the admitted action and relevant ProcessPeriod context.

If no authorised PayRun can be resolved or created, the bridge must stop with a blocker rather than invent a target PayRun.

## 11. ObjectTime worker-period scope

ObjectTime payroll impact is worker-period scoped, not row scoped.

The canonical action scope is:

```text
Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime
```

Processing must consider relevant worker-period context because payroll depends on period totals, spans, breaks, worksite, appointment, classification, attributes, and award rules. A single ObjectTime row can affect totals and interpretation across the worker-period. A deterministic processor must therefore operate on the correct payroll context, not on an isolated row-level assumption.

## 12. Idempotency requirement

Repeated execution of the same admitted action must not create duplicate PayRuns, duplicate PayRunContacts, duplicate admission artefacts, or duplicate payable result lines.

The bridge must use a stable idempotency basis such as PayRun, Contact/PayRunContact, ProcessPeriodGroup, ProcessPeriod, ActionKey, SourceFamily, DecisionId, or snapshot/version. The exact runtime key may depend on existing platform structures, but the doctrine is fixed: the same admitted action must resolve to the same intended processing target and must not multiply payroll artefacts.

Idempotency is not only a database concern. It is a payroll-control concern because duplicate processing can overstate pay, confuse readiness, and damage the audit story.

## 13. Evidence and story continuity

Every generated or updated processing result must preserve evidence/story context.

The evidence/story should include source truth, action, decision, admission, selected PayRun, selected PayRunContact, processing result, blocked or unsupported conditions, and readiness consequence.

This continuity lets operators and Minerva answer why a draft result exists, what authorised it, what processing path was used, what happened, and what remains blocked or ready for review.

## 14. Readiness integration

After processing, readiness/review status should update or become ready to update.

Readiness is not a substitute for calculation. It is the operator/control view of whether the processed result can proceed. A readiness update should reflect deterministic processing output, blocked conditions, evidence completeness, and review implications.

If processing succeeds, readiness may show that the admitted draft result is available for review. If processing is blocked because the target is frozen, unclear, unsupported, or missing an authorised path, readiness should expose the blocker rather than pretend draft output exists.

## 15. What this slice may implement

This slice may implement:

- discovery of existing processing service entrypoints;
- admitted action to target PayRun/PayRunContact processing bridge;
- draft/unfinalised/unfrozen guardrails;
- decision/admission authority checks;
- idempotent target resolution;
- safe call into existing processing path where available;
- blocker status if existing path is unsafe or unclear;
- evidence/story payload;
- readiness-compatible result/status;
- tests proving non-finalisation and non-payment boundaries.

These implementation permissions are bounded by the doctrine above. The bridge may connect governed admission to deterministic draft processing; it may not become a payroll engine, a payment workflow, or a decisioning system.

## 16. What this slice must not implement

This slice must not implement:

- no finalisation;
- no payment;
- no bank file;
- no payment batch;
- no Minerva decisioning;
- no Minerva payroll calculation;
- no broad automation ladder;
- no guardrail engine;
- no manual payroll adjustment;
- no retro execution;
- no recovery execution;
- no source-truth mutation;
- no Admin Queue rebuild;
- no parallel payroll processor.

These non-goals protect the slice boundary. The bridge is allowed to prepare or perform deterministic draft processing where authorised and safe, but it must not cross into financial execution, broad automation, source-truth mutation, or alternative calculation authority.

## 17. How Minerva should explain this slice

Minerva should describe the bridge as the controlled handoff from authorised admission into deterministic draft processing.

Minerva should answer from evidence and doctrine. It should explain that the bridge starts after governed decision/admission authority, targets draft/unfinalised/unfrozen PayRuns, uses existing deterministic processing paths, preserves evidence/story, and feeds readiness/review visibility.

Minerva must not pretend the slice finalises payroll, pays workers, creates bank files, calculates payroll independently, or grants admission authority. If the evidence does not show the deterministic processing path is available and safe, Minerva should describe the blocker instead of overstating runtime behaviour.

## 18. Why this is a large but bounded slice

This is larger than a probe because it crosses action, admission, processing, and readiness boundaries.

It must understand where authority comes from, how target PayRuns and PayRunContacts are resolved, where draft processing lives, how lifecycle/freeze controls are enforced, and how processing evidence becomes operator-ready status.

It remains bounded because it does not implement payment, finalisation, retro execution, broad automation, a guardrail engine, or a new payroll engine. Its job is the controlled bridge into existing deterministic draft processing, not the entire payroll lifecycle.

## 19. Suggested Minerva golden questions

1. What is the Admitted Draft PayRun Processing Bridge?
2. Why is this bridge needed after PayRun admission?
3. What is the canonical governed path from source change to readiness update?
4. Why does PayRunActionDecision remain the authority source?
5. Can the bridge create a PayRun by itself?
6. Can the bridge create a PayRunContact by itself?
7. What guardrails protect finalised, frozen, paid, or payment-batch-generated PayRuns?
8. Why must the bridge use existing deterministic processing paths?
9. What should happen if the existing processing path is unsafe or unclear?
10. Why must Minerva not calculate payroll outcomes?
11. What is the difference between admission and processing?
12. Why is ObjectTime payroll impact worker-period scoped?
13. What idempotency risks does the bridge need to prevent?
14. What evidence should the bridge preserve?
15. How should readiness be updated after processing?
16. What may this slice implement?
17. What must this slice not implement?
18. Why is this a large but bounded slice?
19. How should Minerva explain admitted draft processing without overstating runtime behaviour?
20. How does this bridge preserve deterministic payroll authority?

## 20. How does this bridge preserve deterministic payroll authority?

The bridge preserves deterministic payroll authority by acting only after governed decision/admission authority and by keeping calculation inside deterministic Workforce Platform services.

It only targets draft, unfinalised, and unfrozen PayRuns. It reuses existing deterministic processing services rather than creating a parallel payroll processor. It stops with a blocker if the existing processing path is unsafe, unclear, unavailable, or not callable for the admitted worker-period.

It prevents duplicate execution through idempotent target resolution and stable action/decision/admission context. It preserves evidence/story so the source truth, action, decision, admission, selected PayRun, selected PayRunContact, processing result, and readiness consequence remain explainable.

Minerva remains advisory rather than computational. It can explain the doctrine and evidence, but it must not calculate payroll outcomes or replace deterministic platform authority.
