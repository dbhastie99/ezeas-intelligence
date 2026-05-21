# Admitted Draft PayRun Processing Bridge v0.1

Status: v0.1 structured Minerva knowledge pack.

This structured knowledge pack is derived from the reconstructed canonical source response:
[admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md).
The reconstructed source response remains authoritative for this slice. This file preserves the doctrine in a structured form for Minerva retrieval and answer guidance; it does not introduce runtime implementation, database schema, live LLM behaviour, endpoint behaviour, UI behaviour, or workforce-platform changes.

## Domain And Scope

- Workforce Platform.
- Pay Process.
- PayRun admission.
- Draft PayRunContact processing.
- Readiness and review evidence.
- Minerva explanation support.

The slice sits after governed PayRunActionDecision/admission and before review, finalisation, payment, payment batch generation, or bank file generation.

## Problem Statement

After authorised admission, the platform needs a controlled bridge into deterministic draft PayRunContact processing. Admission explains why a worker-period may enter a draft PayRun, but admission is not processing and does not itself calculate payroll output. The gap this slice addresses is the governed handoff from authorised admission evidence to an existing deterministic Workforce Platform processing path that can produce draft payroll output for review.

The bridge must not invent admission authority, payroll calculation authority, finalisation authority, payment authority, or a new payroll engine.

## Canonical Governed Path

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

Each step has a separate control purpose. Source change and impact assessment identify payroll-relevant change. The action register records the governed action. PayRunActionDecision records the decision authority. Admission authority controls whether PayRun or PayRunContact creation or resolution is permitted. Deterministic draft processing calculates draft payroll output. Evidence/story preserves explainability. Readiness update presents the operator/control consequence.

## Key Responsibilities

- Authority check: read PayRunActionDecision/admission evidence and confirm the action is authorised.
- PayRun resolution: resolve an existing authorised target PayRun, or create one only where existing decision/admission evidence authorises creation.
- PayRunContact resolution: resolve an existing authorised PayRunContact, or create one only where existing decision/admission evidence authorises creation.
- Draft/unfinalised/unfrozen guardrail: process only draft, unfinalised, unfrozen PayRuns that have not crossed payment, bank-file, or lifecycle close controls.
- Deterministic processing call: reuse existing deterministic Workforce Platform processing paths.
- Idempotency: repeated handling of the same admitted action must not duplicate PayRuns, PayRunContacts, admission artefacts, or payable result lines.
- Evidence/story payload: preserve source truth, action, decision, admission, selected PayRun, selected PayRunContact, processing result, blockers, and readiness consequence.
- Readiness-compatible outcome: produce or expose an outcome that can support review readiness without pretending readiness is calculation.

## Authority Model

PayRunActionDecision remains the authority source. The bridge does not independently decide whether a worker-period should be included in a PayRun. It may read decision and admission artefacts, resolve the authorised target, and hand off to deterministic processing, but it must not promote a pending action to approved, infer approval from convenience, or treat processing success as retroactive admission authority.

If the decision does not authorise PayRun creation, the bridge must not create a PayRun. If the decision does not authorise PayRunContact creation, the bridge must not create a PayRunContact. The bridge does not create PayRuns or PayRunContacts unless authorised by existing decision/admission evidence.

## Processing Model

Payroll outcomes must be produced by deterministic Workforce Platform services. The bridge must inspect and reuse the existing deterministic PayRun/PayRunContact processing path where safe. It must not calculate payroll dollars, tax, net pay, statutory obligations, deductions, award entitlements, payment amounts, bank-file values, or final payroll outcomes.

A parallel payroll processor is prohibited. A second processor would create conflicting payroll truth, duplicate calculation logic, and create a second authority path outside the established Workforce Platform runtime. If the existing processing path is unsafe, unclear, unavailable, or not callable for the admitted worker-period, the bridge must stop with a blocker.

## Guardrails

The bridge must only process draft, unfinalised, and unfrozen PayRuns.

It must not silently mutate finalised PayRuns, paid PayRuns, frozen PayRuns, payment-batch-generated PayRuns, bank-file-generated PayRuns, or lifecycle-closed PayRuns. Once a financial-control freeze point is reached, late changes must route to governed later treatment, supplementary handling, retro handling, recovery handling, explicit regeneration workflows, or review. This bridge is for admitted draft processing only.

## Lifecycle Model

ProcessPeriod.LifecycleStatusCode is payroll-control truth. IsOpen/IsClosed alone is insufficient because payroll control needs materially different states, including open, regular closed for review, supplementary review open, supplementary review closed, payment/bank batch generated, and closed.

The same worker-period change may need ordinary draft processing, supplementary review, a blocker, or later governed treatment depending on lifecycle status. The bridge must respect lifecycle context before processing.

## ObjectTime Worker-Period Scope

ObjectTime payroll impact is worker-period scoped, not row scoped.

The canonical action scope is:

```text
Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime
```

Processing must consider worker-period context because payroll depends on period totals, spans, breaks, worksite, appointment, classification, attributes, and award rules. A single ObjectTime row can affect interpretation across the worker-period. The deterministic processor must operate on the correct payroll context, not an isolated row-level assumption.

## Idempotency Model

Repeated execution of the same admitted action must not create duplicate PayRuns, duplicate PayRunContacts, duplicate admission artefacts, or duplicate payable result lines.

Stable idempotency inputs may include PayRun, Contact or PayRunContact, ProcessPeriodGroup, ProcessPeriod, ActionKey, SourceFamily, DecisionId, and snapshot/version. The exact runtime key depends on existing platform structures, but the doctrine is fixed: the same admitted action must resolve to the same intended processing target and must not multiply payroll artefacts.

## Evidence And Story Model

Evidence/story continuity is required. The bridge must preserve enough evidence for operators, Worker Story, and Minerva to explain:

- what source truth changed;
- what impact assessment and action register entry existed;
- which PayRunActionDecision/admission authority applied;
- which PayRun and PayRunContact were selected or created where authorised;
- which deterministic processing path was used or why it was blocked;
- what draft processing result exists;
- what readiness consequence follows.

Evidence/story continuity is what lets Minerva explain why a draft result exists without becoming a calculation authority.

## Readiness Model

Readiness update is an operator/control consequence, not a substitute for calculation. Readiness should reflect deterministic processing output, blocker state, evidence completeness, and review implications.

If processing succeeds, readiness may show that the admitted draft result is available for review. If processing is blocked because the target is frozen, unclear, unsupported, missing authorised authority, or missing a safe deterministic processing path, readiness should expose the blocker rather than claim draft payroll output exists.

## Minerva Answer Boundaries

Minerva may explain doctrine, cite evidence, describe the expected governed path, identify blockers, and explain why deterministic platform processing remains the payroll authority.

Minerva must not calculate payroll dollars, tax, net pay, statutory obligations, deductions, award entitlements, payment amounts, bank-file values, or final payroll outcomes. Minerva must not decide worker-period inclusion, grant admission authority, finalise payroll, pay workers, generate bank files, generate payment batches, execute retro, execute manual adjustments, or claim runtime behaviour that is not evidenced.

Minerva is advisory only for this slice. Payroll calculation authority remains deterministic Workforce Platform processing.

## Implementation Boundaries

Allowed behaviours for the doctrine/design boundary:

- discover existing processing service entrypoints;
- bridge an admitted action to target PayRun/PayRunContact processing;
- enforce draft/unfinalised/unfrozen guardrails;
- check decision/admission authority;
- resolve targets idempotently;
- call an existing deterministic processing path where safe;
- stop with blocker status where the existing path is unsafe, unclear, unavailable, or not callable;
- preserve evidence/story payload;
- produce readiness-compatible result/status.

Strict non-goals:

- no runtime implementation in this knowledge slice;
- no workforce-platform changes;
- no database migrations;
- no live LLM calls;
- no external service calls;
- no endpoint or UI changes;
- no payroll calculation logic;
- no Minerva payroll decisioning;
- no finalisation;
- no payment;
- no bank file;
- no payment batch;
- no retro execution;
- no manual adjustment execution;
- no broad automation ladder;
- no parallel payroll processor.

## Golden Questions And Answer Guidance

### 1. What is the Admitted Draft PayRun Processing Bridge?

Answer guidance: It is the controlled handoff from authorised PayRun admission into deterministic draft PayRunContact processing. It sits after PayRunActionDecision/admission and before review/finalisation, payment, payment batch generation, or bank file generation.

### 2. Why is this bridge needed after PayRun admission?

Answer guidance: Admission explains why a worker-period is allowed into a draft PayRun, but admission is not processing. The bridge is needed so authorised admission can reach deterministic draft processing and produce draft payroll output for review without jumping to finalisation or payment.

### 3. What is the canonical governed path from source change to readiness update?

Answer guidance: The governed path is source change, impact assessment, action register, PayRunActionDecision, admission authority, PayRun / PayRunContact resolved or created where authorised, deterministic draft PayRunContact processing, calculated draft payroll output, evidence/story, and readiness update. The steps must not be collapsed.

### 4. Why does PayRunActionDecision remain the authority source?

Answer guidance: PayRunActionDecision records the governed decision authority. The bridge must not decide inclusion independently, infer approval from convenience, or use processing success as retroactive admission authority.

### 5. Can the bridge create a PayRun by itself?

Answer guidance: No. The bridge may resolve an existing authorised PayRun or create one only where policy or decision/admission evidence authorises creation. If no authorised PayRun can be resolved or created, the bridge must stop with a blocker.

### 6. Can the bridge create a PayRunContact by itself?

Answer guidance: No. The bridge may resolve an existing authorised PayRunContact or create one only where decision/admission evidence authorises creation. It must not create a PayRunContact merely because processing needs a target.

### 7. What guardrails protect finalised, frozen, paid, or payment-batch-generated PayRuns?

Answer guidance: The bridge may only process draft, unfinalised, and unfrozen PayRuns. It must not silently mutate finalised, paid, frozen, payment-batch-generated, bank-file-generated, or lifecycle-closed PayRuns; late changes must route to governed later treatment or blockers.

### 8. Why must the bridge use existing deterministic processing paths?

Answer guidance: Payroll outcomes must come from deterministic Workforce Platform services. Reusing the existing processing path preserves payroll authority and avoids duplicate calculation logic or conflicting payroll truth.

### 9. What should happen if the existing processing path is unsafe or unclear?

Answer guidance: The bridge must stop with an evidence-bearing blocker. It must not improvise payroll calculation, create a parallel processor, or pretend readiness/output exists when the safe deterministic path is unavailable.

### 10. Why must Minerva not calculate payroll outcomes?

Answer guidance: Minerva is advisory only. Payroll dollars, tax, net pay, statutory obligations, deductions, award entitlements, payment amounts, bank-file values, and final payroll outcomes must be calculated by deterministic platform services, not generated explanation.

### 11. What is the difference between admission and processing?

Answer guidance: Admission is authority to include or target a worker-period under governed decision evidence. Processing is deterministic calculation of draft payroll output. Admission alone does not calculate payroll output.

### 12. Why is ObjectTime payroll impact worker-period scoped?

Answer guidance: ObjectTime impact is scoped to Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime because payroll depends on worker-period totals, spans, breaks, worksite, appointment, classification, attributes, and award rules. A single row can affect the broader worker-period calculation context.

### 13. What idempotency risks does the bridge need to prevent?

Answer guidance: It must prevent duplicate PayRuns, duplicate PayRunContacts, duplicate admission artefacts, and duplicate payable result lines. Stable action, decision, admission, period, source family, PayRun, PayRunContact, and snapshot/version inputs should resolve repeated execution to the same intended target.

### 14. What evidence should the bridge preserve?

Answer guidance: It should preserve source truth, impact/action evidence, PayRunActionDecision, admission authority, selected PayRun, selected PayRunContact, processing path/result, blocked or unsupported conditions, and readiness consequence for Worker Story, operators, audit, and Minerva.

### 15. How should readiness be updated after processing?

Answer guidance: Readiness should reflect deterministic processing output, blocker state, evidence completeness, and review implications. It is an operator/control consequence and must not be treated as a substitute for calculation.

### 16. What may this slice implement?

Answer guidance: As doctrine, the slice may support discovery of existing processing entrypoints, admitted action to PayRun/PayRunContact bridge design, draft guardrails, authority checks, idempotent target resolution, safe deterministic processing calls, blocker status, evidence/story payloads, and readiness-compatible status. This structured pack itself does not implement runtime behaviour.

### 17. What must this slice not implement?

Answer guidance: It must not implement finalisation, payment, bank files, payment batches, Minerva decisioning, Minerva payroll calculation, broad automation, guardrail engines, manual payroll adjustments, retro execution, recovery execution, source-truth mutation, Admin Queue rebuild, or a parallel payroll processor.

### 18. Why is this a large but bounded slice?

Answer guidance: It crosses action, admission, processing, lifecycle/freeze controls, evidence, and readiness boundaries. It remains bounded because it only bridges authorised admission to existing deterministic draft processing and does not implement the rest of the payroll lifecycle.

### 19. How should Minerva explain admitted draft processing without overstating runtime behaviour?

Answer guidance: Minerva should describe the doctrine and evidenced design: authorised admission, draft/unfinalised/unfrozen targets, existing deterministic processing, evidence/story continuity, readiness/review consequence, and blockers where the safe path is not evidenced. It must not claim runtime processing exists unless implementation evidence in the repo proves it.

### 20. How does this bridge preserve deterministic payroll authority?

Answer guidance: It acts only after governed decision/admission authority, targets only safe draft PayRuns, reuses deterministic Workforce Platform processing, stops on unsafe or unclear paths, preserves idempotency and evidence/story, and keeps Minerva advisory rather than computational.

## Retrieval Keywords And Aliases

- admitted draft PayRun processing bridge
- PayRunActionDecision
- PayRunActionDecision admission authority
- Pay Process admission
- admission authority
- action register
- draft PayRunContact processing
- deterministic payroll processing
- deterministic payroll processing path
- readiness update
- ProcessPeriod LifecycleStatusCode
- ProcessPeriod.LifecycleStatusCode
- ObjectTime worker-period scope
- no parallel payroll processor
- Minerva advisory only
- payroll calculation authority
- finalised PayRun guardrail
- payment batch guardrail
- payment batch generated guardrail
- finalised PayRun guardrail
- payment-batch-generated PayRun
- bank-file-generated PayRun

## Non-Goal Warnings

- Do not treat Minerva as a payroll calculator.
- Do not treat admission as processing.
- Do not treat IsOpen/IsClosed as sufficient lifecycle control.
- Do not mutate finalised, frozen, paid, payment-batch-generated, bank-file-generated, or lifecycle-closed PayRuns.
- Do not create a new payroll engine.
- Do not overstate runtime implementation. If implementation evidence is absent, phrase answers as doctrine/design and identify blockers.

## Source Linkage

- Canonical source response: `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`
- Relative link: [admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md)
