# Minerva Knowledge Capture — Admitted Draft PayRun Bridge Manual Processing Action

## Purpose of this knowledge capture

This knowledge capture records the updated product decision and planned Workforce Platform slice:

**Admitted Draft PayRun Bridge Manual Processing Action v0.1**

This is a Minerva knowledge and evaluation slice only. It does not modify workforce-platform, connect to a database, call a live LLM, change runtime retrieval behaviour, expose chat, or mutate operational corpus/runtime state.

The slice clarifies that the earlier operator preview doctrine remains valid as safety doctrine, but the preferred operator workflow is no longer a separate visible preview journey. The existing Pay Process / Admin Queue action exposure model remains the operator's primary workflow.

## 1. What changed in product direction

The earlier preview-surface doctrine remains useful: preview is not execution, visibility is not mutation, and dry-run/preflight protects execution. That doctrine still belongs in Minerva answers about the bridge.

The product direction changed on the user-facing workflow. We are not adding a separate visible preview workflow as the operator's main path. The operator should not be forced through a distinct preview journey before taking the existing Pay Process action.

The backend preview/operator-action contract remains valuable, but it should now be treated as internal preflight and eligibility logic that supports the direct manual action.

## 2. Why the direct manual action model is better

The platform already exposes Pay Process actions to the operator. The clearest workflow is therefore for the operator to select the action directly from the existing Pay Process or Admin Queue action surface.

A separate visible preview workflow would add another user journey around the same action without adding authority. The better model keeps the operator in the existing action surface and lets the backend perform strict guard checks before any processing occurs.

This preserves a simple operator path while retaining the same safety boundaries: the action is visible where the platform already exposes actions, and the backend remains the authority for whether the action may execute.

## 3. Relationship to the existing preview/operator action contract

The existing preview/operator action contract is still important. Preview/preflight powers eligibility, blocker reasons, disabled or enabled state, and safe backend execution.

The change is that preview/preflight is internal safety logic, not a separate visible workflow or standalone user journey. The UI may display backend blocker and fix messages, but it should not turn preview into a required separate operator path.

Dry-run and preflight remain execution protection. They explain whether the action is safe, what would be targeted, what authority exists, and what blocks processing. They do not themselves execute processing.

## 4. Current implementation state before this slice

The current committed Workforce state before this planned manual action slice is:

- bridge service foundation exists;
- dry-run preview support exists;
- guarded operator action contract exists;
- no route exists for this manual processing action;
- no UI mutation button exists for this action;
- execution remains disabled in the current committed state.

This knowledge capture does not change that state. It only records the planned direction and answer boundaries.

## 5. Planned manual processing action workflow

The planned operator workflow is:

```text
existing Pay Process action surface
→ operator manually selects "Process admitted action"
→ backend runs strict preflight/guard checks
→ backend executes existing bridge only if safe
→ backend returns success/blocker packet
→ UI refreshes Pay Process state
```

The operator performs one explicit manual action. The backend performs the safety check and execution decision. The UI refreshes from backend state instead of inferring that processing succeeded.

## 6. Backend authority and guardrails

The backend must require:

- active PayRunActionDecision;
- authorised admission evidence;
- target PayRun matching route/context;
- safe draft, unfinalised, unfrozen, unpaid, no payment batch, and no bank file state;
- ProcessPeriod.LifecycleStatusCode allowed state;
- existing PayRunContact;
- deterministic processing entrypoint available;
- idempotency basis.

The backend is the source of eligibility truth, blocker reason, and execution result. The action must not bypass PayRunActionDecision or admission authority, and it must not silently mutate finalised, frozen, paid, payment-batch, or bank-file PayRuns.

## 7. UI responsibilities

The UI may surface the action and result packet in the existing Pay Process or Admin Queue context. It may show backend-provided enabled state, blocker/fix messages, success state, already-processed state, and operator next actions.

The UI must not infer eligibility independently. It must not decide from local row state that an action is safe. It must use backend authority for eligibility, blocker reason, and execution result.

After success, the UI should refresh Pay Process state, or use a refresh-compatible result, so the operator sees the updated control state from the backend.

## 8. Why manual action is not automation

Manual action is not automation. A human operator explicitly selects one admitted action from an existing action surface.

There is no broad automation, process-all action, policy ladder, hidden background processing, batch sweep, or unattended payroll processor. The planned slice is a guarded manual action for one admitted action at a time.

## 9. Why this is still bounded

This slice may execute one admitted action only after strict backend checks pass. That is a bounded bridge from an already admitted action into existing deterministic draft processing.

It does not finalise payroll, pay workers, create a bank file, create a payment batch, create PayRuns, create PayRunContacts, create manual adjustments, run retro execution, or run recovery execution.

It also does not mutate source truth, calculate payroll in Minerva, move decisioning into Minerva, or create a parallel payroll processor.

## 10. What this slice may implement

The planned Workforce slice may implement:

- guarded manual processing endpoint;
- action wiring in existing Pay Process/Admin Queue surfaces where safe;
- strict preflight;
- deterministic blocker/fix messages;
- idempotency;
- evidence/story response;
- Pay Process refresh-compatible result;
- prompt artefact and boundary docs/tests.

These allowed items are implementation planning boundaries. This Minerva slice itself implements only knowledge, evaluation, prompt, and test artefacts.

## 11. What this slice must not implement

The planned Workforce slice must not implement:

- no automation;
- no finalisation;
- no payment;
- no bank file;
- no payment batch;
- no PayRun creation;
- no PayRunContact creation;
- no manual adjustment creation;
- no retro execution;
- no recovery execution;
- no source-truth mutation;
- no Minerva calculation;
- no Minerva decisioning;
- no parallel payroll processor;
- no bypass of PayRunActionDecision/admission authority;
- no silent mutation of finalised/frozen/paid/payment-batch/bank-file PayRuns.

In short: no PayRun/PayRunContact creation, no finalisation/payment/bank file, no automation, and no payroll authority transfer to Minerva.

## 12. Response/evidence expectations

The guarded manual processing endpoint response packet should include:

- Status;
- Processed / AlreadyProcessed / Blocked flags;
- ActionIdentity;
- DecisionAuthority;
- AdmissionAuthority;
- TargetPayRun;
- TargetPayRunContact;
- Guardrails;
- ProcessingEntrypoint;
- ProcessingOutcome;
- Readiness;
- Evidence;
- OperatorNextActions;
- NonGoals;
- ActionsTaken;
- ActionsNotTaken;
- Idempotency.

The packet should make clear what happened, what did not happen, why the backend allowed or blocked processing, and what the operator should do next.

## 13. Minerva answer guidance

Before implementation, Minerva should describe the Admitted Draft PayRun Bridge Manual Processing Action as a planned Workforce slice.

After implementation, Minerva should distinguish the guarded manual action from automation and from broad live processing. It should say that a human operator selects one admitted action, the backend performs strict preflight/guard checks, and the bridge executes only if safe and evidenced by implementation/test artefacts.

Minerva must never claim finalisation, payment, banking, payment batch creation, PayRun creation, PayRunContact creation, payroll calculation, or source-truth mutation from this slice.

## 14. Runtime-overstatement risks

Minerva should avoid these runtime-overstatement risks:

- saying preview equals execution;
- saying manual action equals automation;
- saying a button can process all;
- saying bridge creates PayRuns/PayRunContacts;
- saying finalised PayRuns can be mutated;
- saying Minerva calculates payroll.

It should also avoid implying that UI eligibility is authoritative. Backend preflight remains the source of truth.

## 15. Relationship to prior Minerva documents

This manual processing action knowledge depends on, but updates the product direction from, prior bridge and preview documents:

- [admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md): establishes the admitted draft bridge doctrine and deterministic processing boundary.
- [admitted_draft_payrun_processing_bridge_v0_1.md](admitted_draft_payrun_processing_bridge_v0_1.md): structured bridge knowledge pack for retrieval.
- [ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md): bridge answer evaluation baseline.
- [admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md](admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md): implementation-state addendum for bridge foundations.
- [admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md](admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md): preserves preview doctrine, now treated as internal safety/preflight doctrine rather than the preferred visible workflow.
- [admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md](admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md): structured preview knowledge pack.
- [ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md): preview answer evaluation baseline.

The operator preview knowledge remains valid for the doctrine that preview is not execution, visibility is not mutation, and dry-run/preflight protects execution. It is no longer the preferred user-facing workflow as a separate preview surface.

## 16. Suggested Minerva golden questions

1. What is the Admitted Draft PayRun Bridge Manual Processing Action?
2. Why did we choose manual action instead of a separate visible preview workflow?
3. What role does preview/preflight still play?
4. What is the manual processing workflow?
5. What backend authority is required before processing?
6. What PayRun guardrails must pass before processing?
7. Why must the PayRunContact already exist?
8. Why is this manual action not automation?
9. What may the planned Workforce slice implement?
10. What must the planned Workforce slice not implement?
11. What should the endpoint response include?
12. What should the UI do and not do?
13. How does this preserve deterministic payroll authority?
14. What runtime-overstatement risks should Minerva avoid?
15. How does this relate to the earlier operator preview surface knowledge?
16. What remains for a later slice after manual processing action?

## 17. Answer guidance for golden questions

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

## 18. Prohibited claims

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

## 19. Source links

- [docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md)
- [docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md](admitted_draft_payrun_processing_bridge_v0_1.md)
- [docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md)
- [docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md](admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md)
- [docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md](admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md)
- [docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md](admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md)
- [docs/evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md)
