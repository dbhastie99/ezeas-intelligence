# Admitted Draft PayRun Processing Bridge Answer Evaluation Baseline v0.1

Domain name: Admitted Draft PayRun Processing Bridge.

Source-response path: `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`

Structured knowledge path: `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md`

Evaluation status: checked-in deterministic answer-behaviour baseline. This is evaluation-only documentation for Minerva answer guidance. It does not implement retrieval changes, runtime bridge execution, database behaviour, live LLM behaviour, endpoint exposure, UI exposure, or Workforce Platform changes.

Canonical answer posture: Minerva should answer this domain as doctrine, design, and current intended bridge behaviour from the preserved knowledge pack. Minerva must not claim the runtime bridge is implemented and live unless later implementation evidence is ingested, tested, and explicitly in scope.

## Answer-Boundary Summary

- Admission is not processing.
- PayRunActionDecision remains the authority source.
- The bridge must not decide inclusion independently.
- The bridge must not create PayRuns or PayRunContacts unless authorised.
- Processing must use deterministic Workforce Platform services.
- Minerva must not calculate payroll outcomes.
- The bridge must reuse existing deterministic processing paths.
- If the existing processing path is unsafe or unclear, the bridge must stop with a blocker.
- The bridge processes only draft, unfinalised, unfrozen PayRuns.
- Finalised, paid, frozen, payment-batch-generated, or bank-file-generated PayRuns must not be silently mutated.
- ProcessPeriod.LifecycleStatusCode is payroll-control truth.
- IsOpen/IsClosed alone is insufficient.
- ObjectTime payroll impact is worker-period scoped.
- Idempotency is required.
- Evidence/story continuity is required.
- Readiness is an operator/control consequence, not a substitute for calculation.
- A parallel payroll processor is prohibited.

## Prohibited Answer Claims

Minerva answers for this domain must not claim:

- Minerva calculates payroll outcomes.
- Minerva calculates gross, net, tax, deductions, statutory obligations, entitlements, payment, payment batch, or bank-file values.
- The bridge finalises PayRuns.
- The bridge pays workers.
- The bridge creates bank files.
- The bridge creates payment batches.
- The bridge can mutate finalised PayRuns.
- The bridge can mutate paid PayRuns.
- The bridge can mutate frozen PayRuns.
- The bridge can mutate payment-batch-generated PayRuns.
- The bridge can mutate bank-file-generated PayRuns.
- Admission is the same as processing.
- PayRunActionDecision is optional.
- IsOpen/IsClosed alone is enough lifecycle truth.
- ObjectTime impact is only row-scoped.
- The bridge may invent a parallel payroll processor.
- The runtime bridge is implemented and live unless implementation evidence is later ingested and tested.
- The structured knowledge document replaces the source response.
- Readiness is a substitute for deterministic calculation.

## Required Runtime Caveat

Answers must preserve this caveat when discussing implementation state: this baseline proves deterministic answer guidance only. It does not prove runtime bridge implementation, production readiness, live Minerva answer generation, live retrieval, database execution, endpoint exposure, UI exposure, or Workforce Platform runtime integration.

## No-Action Attestation

- No runtime changes: yes.
- No live LLM calls: yes.
- No DB access, reads, writes, migrations, or validation: yes.
- No workforce-platform changes: yes.
- No endpoint or UI changes: yes.
- No external service calls: yes.
- No corpus mutation: yes; this checked-in evaluation baseline is a controlled local test artefact.
- No payroll calculation logic: yes.
- No Minerva payroll decisioning: yes.
- No finalisation, payment, bank file, payment batch, retro execution, manual adjustment execution, or broad automation ladder: yes.

## Golden Questions And Expected Answer Themes

### 1. What is the Admitted Draft PayRun Processing Bridge?

Expected answer themes:
- State that the bridge is a controlled handoff from authorised PayRun admission into deterministic draft PayRunContact processing.
- Place it after PayRunActionDecision/admission and before review, finalisation, payment, payment batch generation, or bank file generation.
- Explain that it preserves evidence of the handoff without becoming decisioning or payroll calculation authority.

Prohibited claims:
- Do not say the bridge decides admission, finalises PayRuns, pays workers, creates bank files, or calculates payroll outcomes.

Required caveats:
- Phrase as doctrine/design/current intended bridge behaviour unless later implementation evidence proves runtime execution.

### 2. Why is this bridge needed after PayRun admission?

Expected answer themes:
- Admission explains why a worker-period is allowed into a draft PayRun, but admission is not processing.
- The bridge is needed to connect authorised admission to deterministic draft processing so draft payroll output can exist for review.
- The bridge must not jump ahead to finalisation or payment.

Prohibited claims:
- Do not equate admission with processing or say admission alone calculates payroll output.

Required caveats:
- Explain the need as an intended governed transition, not proof of a live runtime bridge.

### 3. What is the canonical governed path from source change to readiness update?

Expected answer themes:
- Preserve the full path: source change -> impact assessment -> action register -> PayRunActionDecision -> admission authority -> PayRun / PayRunContact resolved or created where authorised -> deterministic draft PayRunContact processing -> calculated draft payroll output -> evidence/story -> readiness update.
- Explain that each step has a separate control purpose and must not be collapsed.
- State that readiness follows deterministic processing output and evidence, not the other way around.

Prohibited claims:
- Do not omit PayRunActionDecision, admission authority, deterministic processing, evidence/story, or readiness consequence.

Required caveats:
- Do not present this path as runtime execution evidence unless separately proven.

### 4. Why does PayRunActionDecision remain the authority source?

Expected answer themes:
- PayRunActionDecision records governed decision authority.
- It controls inclusion and PayRun/PayRunContact creation authority.
- The bridge may read decision/admission artefacts but must not decide inclusion independently or infer approval from convenience.

Prohibited claims:
- Do not say PayRunActionDecision is optional or that processing success creates retroactive authority.

Required caveats:
- Keep the answer framed as authority doctrine unless runtime implementation evidence is later in scope.

### 5. Can the bridge create a PayRun by itself?

Expected answer themes:
- No. The bridge cannot create a PayRun on its own authority.
- It may resolve an existing authorised PayRun or create one only where policy or decision/admission evidence authorises creation.
- If no authorised PayRun can be resolved or created, the bridge must stop with a blocker.

Prohibited claims:
- Do not say the bridge can create a PayRun merely because processing needs a target.

Required caveats:
- Do not imply runtime creation exists unless supported by later implementation evidence.

### 6. Can the bridge create a PayRunContact by itself?

Expected answer themes:
- No. The bridge cannot create a PayRunContact on its own authority.
- It may resolve an existing authorised PayRunContact or create one only where decision/admission evidence authorises creation.
- Creation must be idempotent and traceable to source action, decision, admission, and processing evidence.

Prohibited claims:
- Do not say the bridge can create PayRunContacts merely for processing convenience.

Required caveats:
- Do not imply runtime creation exists unless supported by later implementation evidence.

### 7. What guardrails protect finalised, frozen, paid, or payment-batch-generated PayRuns?

Expected answer themes:
- The bridge may process only draft, unfinalised, unfrozen PayRuns.
- It must not silently mutate finalised, paid, frozen, payment-batch-generated, bank-file-generated, or lifecycle-closed PayRuns.
- Late changes must route to governed later treatment, supplementary, retro, recovery, explicit regeneration, or blocker workflows.

Prohibited claims:
- Do not say finalised, paid, frozen, payment-batch-generated, or bank-file-generated PayRuns can be silently mutated.

Required caveats:
- Describe guardrails as required doctrine unless runtime enforcement evidence is later tested.

### 8. Why must the bridge use existing deterministic processing paths?

Expected answer themes:
- Payroll outcomes must come from deterministic Workforce Platform services.
- Reusing existing processing paths preserves payroll authority and avoids duplicate calculation logic.
- A parallel payroll processor would create conflicting payroll truth and is prohibited.

Prohibited claims:
- Do not say Minerva or the bridge may invent a new payroll engine or parallel payroll processor.

Required caveats:
- Do not claim the existing path has been connected at runtime unless evidence exists in scope.

### 9. What should happen if the existing processing path is unsafe or unclear?

Expected answer themes:
- The bridge must stop with an evidence-bearing blocker.
- It must not improvise payroll calculation or pretend draft output exists.
- The blocker should preserve why the path is unsafe, unclear, unavailable, unsupported, or not callable.

Prohibited claims:
- Do not say the bridge may proceed by calculating payroll itself or creating a parallel processing path.

Required caveats:
- Explain blocker behaviour as doctrine/design unless runtime implementation evidence is later available.

### 10. Why must Minerva not calculate payroll outcomes?

Expected answer themes:
- Minerva is advisory and evidence intelligence only.
- Deterministic Workforce Platform services must calculate payroll dollars, gross, net, tax, statutory obligations, deductions, award entitlements, payment amounts, payment batch values, bank-file values, and final payroll outcomes.
- Minerva may explain doctrine, cite evidence, and identify blockers, but not calculate or decide payroll.

Prohibited claims:
- Do not say Minerva calculates gross/net/tax/deductions/entitlements/payment/bank-file values.

Required caveats:
- Preserve the Minerva advisory/no-payroll-calculation boundary in every implementation-state answer.

### 11. What is the difference between admission and processing?

Expected answer themes:
- Admission is authority to include or target a worker-period under governed decision evidence.
- Processing is deterministic calculation of draft payroll output.
- Admission alone does not calculate payroll output and does not replace deterministic processing.

Prohibited claims:
- Do not say admission is processing or that admission proves calculated draft output exists.

Required caveats:
- Do not claim processing occurred unless runtime evidence later proves it.

### 12. Why is ObjectTime payroll impact worker-period scoped?

Expected answer themes:
- ObjectTime payroll impact is worker-period scoped, not row scoped.
- The action scope is Worker + ProcessPeriodGroup + ProcessPeriod + SourceFamily:ObjectTime.
- Payroll depends on worker-period totals, spans, breaks, worksite, appointment, classification, attributes, and award rules, so a single row can affect broader period interpretation.

Prohibited claims:
- Do not say ObjectTime impact is only row-scoped or that processing can safely ignore worker-period context.

Required caveats:
- Keep this as payroll scope doctrine unless runtime processing evidence is later in scope.

### 13. What idempotency risks does the bridge need to prevent?

Expected answer themes:
- Prevent duplicate PayRuns, PayRunContacts, admission records, result lines, readiness records, and evidence/story records.
- Repeated execution of the same admitted action should resolve to the same intended target.
- Stable idempotency inputs may include PayRun, Contact/PayRunContact, ProcessPeriodGroup, ProcessPeriod, ActionKey, SourceFamily, DecisionId, and snapshot/version.

Prohibited claims:
- Do not allow repeated execution to create duplicate payroll artefacts or duplicate payable output.

Required caveats:
- Do not claim a specific runtime key is implemented unless later evidence proves it.

### 14. What evidence should the bridge preserve?

Expected answer themes:
- Preserve source truth, impact assessment, action register entry, PayRunActionDecision, admission authority, selected PayRun, selected PayRunContact, processing path/result, blockers, readiness consequence, and actions not taken.
- Evidence/story continuity supports operators, audit, Worker Story, and Minerva explanations.
- Evidence should explain what authorised the result, what happened, what was blocked, and what remains ready for review.

Prohibited claims:
- Do not omit authority, target, processing outcome, blocker, readiness, or actions-not-taken evidence.

Required caveats:
- Do not claim evidence is being written at runtime unless later implementation evidence proves it.

### 15. How should readiness be updated after processing?

Expected answer themes:
- Readiness should reflect deterministic processing output, blocker state, evidence completeness, and review implications.
- Readiness is an operator/control consequence, not a substitute for calculation.
- If processing is blocked, readiness should expose the blocker rather than claim draft output exists.

Prohibited claims:
- Do not say readiness replaces deterministic calculation or proves payroll is correct by itself.

Required caveats:
- Do not claim runtime readiness updates are implemented unless later evidence proves it.

### 16. What may this slice implement?

Expected answer themes:
- For the broader doctrine, a runtime bridge slice may discover existing processing entrypoints, bridge admitted action to PayRun/PayRunContact targets, enforce draft guardrails, check authority, resolve targets idempotently, call safe deterministic processing paths, stop with blocker status, preserve evidence/story, and expose readiness-compatible status.
- This Minerva slice may implement deterministic evaluation and answer-behaviour coverage only.
- The structured pack and this baseline do not implement runtime behaviour.

Prohibited claims:
- Do not say this evaluation slice implements runtime retrieval, runtime bridge execution, DB changes, Workforce Platform changes, or payroll calculation.

Required caveats:
- State explicitly that this slice is evaluation-only.

### 17. What must this slice not implement?

Expected answer themes:
- It must not implement workforce-platform changes, runtime bridge execution, database migrations, live LLM calls, external service calls, production chat exposure, endpoint/UI changes, payroll calculation logic, Minerva payroll decisioning, finalisation, payment, bank files, payment batches, retro execution, manual adjustment execution, broad automation, or a parallel payroll processor.
- It must not mutate corpus unless controlled local fixture/evaluation artefacts are the existing repo convention.
- It must not expose production behaviour.

Prohibited claims:
- Do not claim any runtime, database, live LLM, endpoint, UI, Workforce Platform, finalisation, payment, bank-file, or payment-batch implementation.

Required caveats:
- Answer as strict non-goal and boundary preservation.

### 18. Why is this a large but bounded slice?

Expected answer themes:
- It is large because it crosses action, admission, processing, lifecycle/freeze controls, evidence/story, and readiness boundaries.
- It is bounded because it only bridges authorised admission to existing deterministic draft processing.
- It does not implement finalisation, payment, retro execution, broad automation, a guardrail engine, or a new payroll engine.

Prohibited claims:
- Do not expand the slice into the entire payroll lifecycle or a parallel processor.

Required caveats:
- For this evaluation slice, state that only answer-behaviour coverage is implemented.

### 19. How should Minerva explain admitted draft processing without overstating runtime behaviour?

Expected answer themes:
- Minerva should use caveated doctrine/design phrasing.
- It should explain authorised admission, draft/unfinalised/unfrozen targets, existing deterministic processing, evidence/story continuity, readiness/review consequence, and blockers where the safe path is not evidenced.
- It must not claim runtime implementation exists unless implementation evidence exists in the repo and is in scope.

Prohibited claims:
- Do not say the runtime bridge is implemented and live unless later evidence is ingested and tested.
- Do not say the structured knowledge document replaces the authoritative source response.

Required caveats:
- Always preserve runtime-overstatement caveats in implementation-state answers.

### 20. How does this bridge preserve deterministic payroll authority?

Expected answer themes:
- It acts only after governed decision/admission authority.
- It targets only draft/unfinalised/unfrozen PayRuns.
- It reuses deterministic Workforce Platform processing services, stops on unsafe or unclear paths, preserves idempotency, preserves evidence/story, and keeps Minerva advisory rather than computational.
- It protects PayRunActionDecision authority and avoids parallel payroll processing.

Prohibited claims:
- Do not say Minerva or the bridge becomes payroll calculation authority, decisioning authority, finalisation authority, payment authority, or bank-file authority.

Required caveats:
- Distinguish doctrine/design/current intended behaviour from runtime implementation evidence.
