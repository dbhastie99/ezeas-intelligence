# Admitted Draft PayRun Bridge Manual Processing Action Answer Evaluation Baseline v0.1

Domain name: Admitted Draft PayRun Bridge Manual Processing Action.

Source-response path: `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md`

Structured knowledge path: `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1.md`

Evaluation status: checked-in deterministic answer-behaviour baseline. This Minerva slice is knowledge only. It does not implement retrieval changes, runtime bridge execution, database behaviour, live LLM behaviour, endpoint exposure, UI mutation, chat exposure, operational corpus mutation, or Workforce Platform changes.

Prior knowledge links:

- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md`
- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md`

## Answer-Boundary Summary

- Manual action is not automation.
- Preview/preflight is internal safety logic, not a separate visible workflow.
- Backend is source of eligibility truth, blocker reason, and execution result.
- UI must not infer eligibility independently.
- Active PayRunActionDecision is required.
- Authorised admission evidence is required.
- Existing PayRunContact required before processing.
- No PayRun/PayRunContact creation.
- No finalisation/payment/bank file.
- No payment batch.
- No Minerva calculation or Minerva decisioning.
- No bypass of PayRunActionDecision/admission authority.

## Prohibited Claims

Minerva answers for this domain must not claim:

- the separate visible preview workflow is still the preferred operator path;
- preview itself executes processing;
- manual action is automation;
- the action processes all admitted actions;
- the action creates PayRuns;
- the action creates PayRunContacts;
- the action finalises PayRuns;
- the action pays workers;
- the action creates payment batches or bank files;
- the action mutates finalised/frozen/paid PayRuns;
- Minerva calculates or authorises payroll;
- UI determines eligibility without backend authority.

## Required Caveats

- This Minerva slice is knowledge only.
- Before implementation, the manual processing action must be described as planned.
- No runtime changes were made.
- No live LLM calls were made.
- No DB access, reads, writes, migrations, or validation were performed.
- No workforce-platform changes were made.
- No endpoint, UI, chat, or runtime retrieval behaviour was changed by this slice.
- Manual action requires a human operator selecting one admitted action.
- Backend preflight remains authoritative for eligibility and blockers.
- A later implementation must be evidenced before Minerva describes runtime behaviour as live.

## No-Action Attestation

- No runtime changes: yes.
- No live LLM calls: yes.
- No DB access, reads, writes, migrations, or validation: yes.
- No workforce-platform changes: yes.
- No endpoint or UI changes: yes.
- No retrieval-plan/runtime behaviour changes: yes.
- No external service calls: yes.
- No chat exposure: yes.
- No operational corpus/runtime state mutation: yes.
- No payroll calculation logic: yes.
- No Minerva payroll decisioning: yes.
- No finalisation, payment, bank file, payment batch, PayRun creation, PayRunContact creation, manual adjustment creation, retro execution, recovery execution, source-truth mutation, broad automation, or parallel payroll processor: yes.

## Golden Questions And Expected Answer Themes

### 1. What is the Admitted Draft PayRun Bridge Manual Processing Action?

Expected answer themes:
- Planned guarded manual action for one admitted action.
- Operator selects "Process admitted action" from existing Pay Process/Admin Queue action surface.
- Backend runs strict preflight/guard checks and executes the existing bridge only if safe.

Prohibited claims:
- Do not say it is automation or process-all.

Required caveats:
- Before implementation, describe it as planned.

### 2. Why did we choose manual action instead of a separate visible preview workflow?

Expected answer themes:
- The platform already exposes Pay Process actions.
- Direct manual action keeps the operator in the existing workflow.
- Backend preflight still provides eligibility, blockers, and safety.

Prohibited claims:
- Do not say the separate visible preview workflow remains the preferred operator path.

Required caveats:
- Preview doctrine remains valid as safety doctrine.

### 3. What role does preview/preflight still play?

Expected answer themes:
- Preview/preflight is internal backend safety logic.
- It powers eligibility, blockers, enabled/disabled state, target checks, guardrails, and safe execution.
- It is not a separate visible user journey.

Prohibited claims:
- Do not say preview executes processing.

Required caveats:
- Preview is not execution.

### 4. What is the manual processing workflow?

Expected answer themes:
- Existing Pay Process action surface.
- Operator manually selects "Process admitted action".
- Backend runs strict preflight/guard checks.
- Backend executes existing bridge only if safe.
- Backend returns success/blocker packet.
- UI refreshes Pay Process state.

Prohibited claims:
- Do not add process-all, finalisation, payment, or bank file steps.

Required caveats:
- UI refresh must rely on backend state.

### 5. What backend authority is required before processing?

Expected answer themes:
- Active PayRunActionDecision.
- Authorised admission evidence.
- Target PayRun matching route/context.
- Allowed ProcessPeriod.LifecycleStatusCode.
- Existing PayRunContact.
- Deterministic processing entrypoint and idempotency basis.

Prohibited claims:
- Do not say UI state alone authorises processing.

Required caveats:
- Backend is source of eligibility truth.

### 6. What PayRun guardrails must pass before processing?

Expected answer themes:
- Target PayRun must match route/context.
- It must be draft, unfinalised, unfrozen, unpaid, and have no payment batch or bank file.
- Finalised, frozen, paid, payment-batch, or bank-file PayRuns must block.

Prohibited claims:
- Do not say finalised PayRuns can be mutated.

Required caveats:
- Guardrails must run before execution.

### 7. Why must the PayRunContact already exist?

Expected answer themes:
- This slice is processing-only.
- It does not create PayRuns or PayRunContacts.
- Existing PayRunContact is required before deterministic processing.

Prohibited claims:
- Do not say the bridge creates PayRunContacts.

Required caveats:
- No PayRun/PayRunContact creation.

### 8. Why is this manual action not automation?

Expected answer themes:
- A human operator explicitly selects one admitted action.
- There is no process-all button, hidden background processing, policy ladder, or unattended processor.

Prohibited claims:
- Do not call manual action automation.

Required caveats:
- Manual action remains bounded to one admitted action.

### 9. What may the planned Workforce slice implement?

Expected answer themes:
- Guarded manual processing endpoint.
- Existing Pay Process/Admin Queue action wiring where safe.
- Strict preflight and deterministic blocker/fix messages.
- Idempotency, evidence/story response, refresh-compatible Pay Process result, prompt artefact, boundary docs/tests.

Prohibited claims:
- Do not include finalisation, payment, bank file, or PayRun creation as allowed items.

Required caveats:
- This Minerva slice itself is knowledge only.

### 10. What must the planned Workforce slice not implement?

Expected answer themes:
- No automation, finalisation, payment, bank file, payment batch, PayRun creation, PayRunContact creation, manual adjustment creation, retro/recovery execution, source-truth mutation, Minerva calculation/decisioning, parallel payroll processor, authority bypass, or silent mutation of protected PayRuns.

Prohibited claims:
- Do not narrow the non-goals to only payment.

Required caveats:
- The non-goals preserve deterministic payroll authority.

### 11. What should the endpoint response include?

Expected answer themes:
- Status; Processed / AlreadyProcessed / Blocked flags; ActionIdentity; DecisionAuthority; AdmissionAuthority; TargetPayRun; TargetPayRunContact; Guardrails; ProcessingEntrypoint; ProcessingOutcome; Readiness; Evidence; OperatorNextActions; NonGoals; ActionsTaken; ActionsNotTaken; Idempotency.

Prohibited claims:
- Do not imply missing blocker details are acceptable.

Required caveats:
- The packet should explain success or blockage deterministically.

### 12. What should the UI do and not do?

Expected answer themes:
- UI may surface action and backend result in existing surfaces.
- UI should show backend blocker/fix messages and refresh Pay Process state after success.
- UI must not infer eligibility independently.

Prohibited claims:
- Do not say UI determines eligibility without backend authority.

Required caveats:
- Backend remains source of truth.

### 13. How does this preserve deterministic payroll authority?

Expected answer themes:
- PayRunActionDecision and admission evidence remain authority for admission.
- Deterministic Workforce processing remains authority for payroll calculation.
- Minerva does not calculate payroll or authorise payroll.

Prohibited claims:
- Do not say Minerva calculates payroll.

Required caveats:
- No parallel payroll processor.

### 14. What runtime-overstatement risks should Minerva avoid?

Expected answer themes:
- Avoid saying preview equals execution, manual action equals automation, a button can process all, the bridge creates PayRuns/PayRunContacts, finalised PayRuns can be mutated, or Minerva calculates payroll.

Prohibited claims:
- Do not say the UI can infer eligibility independently.

Required caveats:
- Runtime claims require implementation evidence.

### 15. How does this relate to the earlier operator preview surface knowledge?

Expected answer themes:
- Earlier preview knowledge remains valid for doctrine.
- It is no longer the preferred user-facing workflow as a separate preview surface.
- Preview/preflight now supports backend guard logic for direct manual action.

Prohibited claims:
- Do not discard preview doctrine.

Required caveats:
- The relationship is product-direction refinement, not a runtime implementation claim.

### 16. What remains for a later slice after manual processing action?

Expected answer themes:
- Broader execution controls, if explicitly designed and evidenced.
- Finalisation, payment, payment batch, bank file, retro/recovery execution, automation, and source-truth mutation remain later or out of scope.

Prohibited claims:
- Do not imply this slice unlocks finalisation or payment.

Required caveats:
- Later work must have its own authority, tests, and evidence.
