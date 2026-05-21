# Admitted Draft PayRun Bridge Manual Processing Action v0.1

Status: v0.1 structured Minerva knowledge pack.

Source-response authority: [admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md](admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md).

This is knowledge-only documentation. It does not implement runtime retrieval changes, database behaviour, live LLM behaviour, endpoint exposure, UI mutation, chat exposure, operational corpus mutation, or workforce-platform changes.

## Domain And Scope

The Admitted Draft PayRun Bridge Manual Processing Action is the planned direct manual operator action for one admitted draft processing action. The operator uses the existing Pay Process/Admin Queue action surface, selects "Process admitted action", and the backend performs strict preflight and guard checks before executing the existing bridge only if safe.

The earlier preview-surface doctrine remains valid, but preview/preflight is internal safety logic, not a separate visible workflow and not the preferred operator path.

## Product Decision

The product decision is to avoid creating a separate user-facing preview journey. The platform already has Pay Process action surfaces, so the operator should use the existing action model.

The backend preview/operator-action contract remains valuable as preflight. It powers eligibility, disabled/enabled state, deterministic blocker/fix messages, target checks, idempotency checks, and safe execution gating.

## Current Workforce Implementation State

Before this planned slice, Workforce Platform has:

- bridge service foundation;
- dry-run preview support;
- guarded operator action contract;
- no route for this manual action;
- no UI mutation button for this action;
- execution disabled in the current committed state.

This Minerva slice is knowledge only and does not change that state.

## Manual Workflow

```text
existing Pay Process action surface
→ operator manually selects "Process admitted action"
→ backend runs strict preflight/guard checks
→ backend executes existing bridge only if safe
→ backend returns success/blocker packet
→ UI refreshes Pay Process state
```

Manual action is not automation. A human operator chooses one admitted action. There is no process-all action, hidden background execution, policy ladder, or unattended payroll processor.

## Backend Authority

The backend is the source of eligibility truth, blocker reason, and execution result. Before processing, the backend must require:

- active PayRunActionDecision;
- authorised admission evidence;
- target PayRun matching route/context;
- safe draft, unfinalised, unfrozen, unpaid, no payment batch, and no bank file state;
- ProcessPeriod.LifecycleStatusCode allowed state;
- existing PayRunContact required;
- deterministic processing entrypoint available;
- idempotency basis.

The action must not bypass PayRunActionDecision/admission authority.

## UI Responsibilities

The UI may surface the action in existing Pay Process/Admin Queue surfaces and show backend-provided result, status, blocker/fix messages, and operator next actions.

The UI must not infer eligibility independently. It must not decide from local state that processing is safe. It must refresh Pay Process state after success or use a backend refresh-compatible response.

## Planned Workforce Slice May Implement

- guarded manual processing endpoint;
- action wiring in existing Pay Process/Admin Queue surfaces where safe;
- strict preflight;
- deterministic blocker/fix messages;
- idempotency;
- evidence/story response;
- Pay Process refresh-compatible result;
- prompt artefact and boundary docs/tests.

## Strict Non-Goals

This planned slice must not implement:

- no automation;
- no finalisation;
- no payment;
- no bank file;
- no payment batch;
- no PayRun creation;
- no PayRunContact creation;
- no PayRun/PayRunContact creation;
- no manual adjustment creation;
- no retro execution;
- no recovery execution;
- no source-truth mutation;
- no Minerva calculation;
- no Minerva decisioning;
- no parallel payroll processor;
- no bypass of PayRunActionDecision/admission authority;
- no silent mutation of finalised/frozen/paid/payment-batch/bank-file PayRuns.

It must not create PayRuns or PayRunContacts, finalise PayRuns, pay workers, generate payment batches, generate bank files, or mutate finalised/frozen/paid PayRuns.

## Response Packet Expectations

The endpoint response packet should include Status, Processed / AlreadyProcessed / Blocked flags, ActionIdentity, DecisionAuthority, AdmissionAuthority, TargetPayRun, TargetPayRunContact, Guardrails, ProcessingEntrypoint, ProcessingOutcome, Readiness, Evidence, OperatorNextActions, NonGoals, ActionsTaken, ActionsNotTaken, and Idempotency.

## Minerva Answer Boundaries

Before implementation, Minerva should describe this as a planned Workforce slice. After implementation, Minerva should distinguish guarded manual action from automation and from broad live processing.

Minerva must never claim finalisation, payment, banking, payment batch creation, PayRun creation, PayRunContact creation, payroll calculation, or source-truth mutation from this slice.

## Relationship To Prior Knowledge

Prior bridge and preview knowledge remains relevant:

- [docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md)
- [docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md](admitted_draft_payrun_processing_bridge_v0_1.md)
- [docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md)
- [docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md](admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md)
- [docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md](admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md)
- [docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md](admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md)
- [docs/evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md)

The preview knowledge remains valid for safety doctrine: preview is not execution, visibility is not mutation, and dry-run/preflight protects execution. It is no longer the preferred user-facing workflow as a separate visible preview surface.

## Prohibited Claims

Minerva answers must not claim:

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

## No-Action Attestation

- No runtime changes: yes.
- No live LLM calls: yes.
- No DB access, reads, writes, migrations, or validation: yes.
- No workforce-platform changes: yes.
- No endpoint or UI changes in this Minerva slice: yes.
- No retrieval-plan/runtime behaviour changes: yes.
- No chat exposure: yes.
- No operational corpus/runtime state mutation: yes.
- No payroll calculation logic: yes.
- No Minerva payroll decisioning: yes.

## Golden Questions And Answer Guidance

### 1. What is the Admitted Draft PayRun Bridge Manual Processing Action?

Answer guidance: It is a planned guarded manual action where an operator selects one admitted action from the existing Pay Process/Admin Queue surface, the backend runs strict preflight/guard checks, and the existing bridge executes only if safe.

### 2. Why did we choose manual action instead of a separate visible preview workflow?

Answer guidance: The platform already exposes Pay Process actions. Keeping the operator in that action surface is simpler and clearer, while backend preflight still provides eligibility, blockers, and execution safety.

### 3. What role does preview/preflight still play?

Answer guidance: Preview/preflight remains internal backend safety logic. It powers eligibility, disabled/enabled state, blocker/fix messages, target checks, guardrails, and safe execution, but it is not a separate visible user journey.

### 4. What is the manual processing workflow?

Answer guidance: Existing Pay Process action surface -> operator manually selects "Process admitted action" -> backend runs strict preflight/guard checks -> backend executes the existing bridge only if safe -> backend returns a success/blocker packet -> UI refreshes Pay Process state.

### 5. What backend authority is required before processing?

Answer guidance: The backend needs an active PayRunActionDecision, authorised admission evidence, route/context match to the target PayRun, allowed ProcessPeriod.LifecycleStatusCode, existing PayRunContact, deterministic processing entrypoint, and idempotency basis.

### 6. What PayRun guardrails must pass before processing?

Answer guidance: The target PayRun must match the route/context and be in a safe draft state: unfinalised, unfrozen, unpaid, with no payment batch and no bank file. Finalised, frozen, paid, payment-batch, or bank-file PayRuns must block.

### 7. Why must the PayRunContact already exist?

Answer guidance: This manual action is processing only. It must not create PayRuns or PayRunContacts, so an existing PayRunContact is required before deterministic processing can run.

### 8. Why is this manual action not automation?

Answer guidance: A human operator explicitly selects one admitted action. There is no process-all button, hidden background processing, broad automation, policy ladder, or unattended payroll processor.

### 9. What may the planned Workforce slice implement?

Answer guidance: It may implement a guarded manual processing endpoint, existing Pay Process/Admin Queue action wiring where safe, strict preflight, deterministic blocker/fix messages, idempotency, evidence/story response, refresh-compatible Pay Process result, and prompt/boundary docs/tests.

### 10. What must the planned Workforce slice not implement?

Answer guidance: It must not implement automation, finalisation, payment, bank file, payment batch, PayRun creation, PayRunContact creation, manual adjustment creation, retro/recovery execution, source-truth mutation, Minerva calculation/decisioning, a parallel payroll processor, authority bypass, or silent mutation of finalised/frozen/paid/payment-batch/bank-file PayRuns.

### 11. What should the endpoint response include?

Answer guidance: It should include Status, Processed/AlreadyProcessed/Blocked flags, ActionIdentity, DecisionAuthority, AdmissionAuthority, TargetPayRun, TargetPayRunContact, Guardrails, ProcessingEntrypoint, ProcessingOutcome, Readiness, Evidence, OperatorNextActions, NonGoals, ActionsTaken, ActionsNotTaken, and Idempotency.

### 12. What should the UI do and not do?

Answer guidance: The UI may surface the action and backend result in existing action surfaces, show blocker/fix messages, and refresh Pay Process state after success. It must not infer eligibility independently or treat local UI state as execution authority.

### 13. How does this preserve deterministic payroll authority?

Answer guidance: PayRunActionDecision and admission evidence remain authority for admission, and deterministic Workforce processing remains authority for payroll calculation. Minerva does not calculate payroll, authorise payroll, or become a parallel processor.

### 14. What runtime-overstatement risks should Minerva avoid?

Answer guidance: Avoid saying preview equals execution, manual action equals automation, one button can process all, the bridge creates PayRuns/PayRunContacts, finalised PayRuns can be mutated, the UI determines eligibility, or Minerva calculates payroll.

### 15. How does this relate to the earlier operator preview surface knowledge?

Answer guidance: The earlier preview knowledge remains valid for safety doctrine, but the preferred user-facing workflow changed. Preview/preflight is now internal backend guard logic supporting direct manual action, not a separate visible preview workflow.

### 16. What remains for a later slice after manual processing action?

Answer guidance: Later slices may address broader execution controls only if explicitly designed and evidenced. Finalisation, payment, bank file creation, payment batches, retro/recovery execution, automation, and source-truth mutation remain outside this slice.

## Retrieval Keywords And Aliases

- manual admitted draft processing action
- process admitted action
- backend preflight
- bridge manual processing
- PayRunActionDecision authority
- admission evidence
- existing PayRunContact required
- not automation
- not preview workflow
- Pay Process action surface
- Admin Queue action
- ProcessPeriod LifecycleStatusCode
- no PayRun creation
- no finalisation payment bank file
- backend eligibility truth
- UI must not infer eligibility independently
- authorised admission evidence
