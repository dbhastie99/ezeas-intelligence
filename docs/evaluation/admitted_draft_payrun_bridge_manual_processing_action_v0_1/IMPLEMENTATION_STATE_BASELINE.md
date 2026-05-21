# Admitted Draft PayRun Bridge Manual Processing Action Implementation State Baseline v0.1

Domain name: Admitted Draft PayRun Bridge Manual Processing Action.

Implementation-state document: `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1_implementation_state.md`

Source-response path: `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md`

Structured knowledge path: `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1.md`

Answer evaluation baseline path: `docs/evaluation/admitted_draft_payrun_bridge_manual_processing_action_v0_1/ANSWER_EVALUATION_BASELINE.md`

Evaluation status: checked-in deterministic implementation-state baseline. This is documentation/evaluation only. It does not implement retrieval changes, runtime bridge execution, database behaviour, live LLM behaviour, endpoint exposure, UI exposure, chat exposure, corpus/runtime mutation, or Workforce Platform changes.

## Implementation Summary

- The manual processing action is implemented in Workforce Platform.
- It is a guarded manual action, not automation.
- It is operator-triggered and backend-guarded.
- It is one-action scoped and not process-all.
- PayRun Detail and Admin Queue UI wiring exists.
- Backend preflight remains mandatory before execution.

## Endpoint

Implemented endpoint:

```text
POST /api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process
```

The endpoint is guarded, manual-only, one-action scoped, and not process-all.

## Required Authority

- The endpoint identifies one action through `PayRunActionDecisionId` / `DecisionId`, or action/admission context.
- Exactly one matching decision is required.
- Active non-stale `PayRunActionDecision` is required.
- Accepted/authorised admission evidence with draft-processing authority is required.
- Backend authority determines eligibility, blockers, and execution result.

## Preflight Requirements

Backend preflight requires:

- active non-stale `PayRunActionDecision`;
- accepted/authorised admission evidence;
- route `PayRunId` matches target `PayRun`;
- safe draft `PayRun`;
- existing `PayRunContact`;
- safe `ProcessPeriod.LifecycleStatusCode`;
- deterministic processing entrypoint;
- idempotency basis.

## Execution Path

- Execution delegates to `AdmittedDraftPayRunProcessingBridgeService`.
- The only processing entrypoint remains `PayRunProcessingService.process(..., target_contact_id=...)`.
- No parallel payroll processor was introduced.

## UI Wiring

- PayRun Detail Pay Process action table shows Process admitted action from backend `ManualProcessingAction`.
- Admin Queue surfaces admitted draft action items from the same backend packet.
- UI wires/enables the action only when backend marks it eligible.
- Blocked actions show backend status/blockers.
- UI refreshes Pay Process state after the action result.

## Deferred Items

- Durable persisted admission lookup remains future work where environments do not expose admission packets.
- Dedicated readiness refresh adapter remains future work.
- The response still returns `READINESS_UPDATE_PENDING`.

## Non-Goals

- No automation.
- No process-all.
- No finalisation.
- No payment.
- No bank file.
- No payment batch.
- No `PayRun` creation.
- No `PayRunContact` creation.
- No manual adjustment.
- No retro execution.
- No recovery execution.
- No source-truth mutation.
- No Minerva calculation.
- No Minerva decisioning.
- No parallel payroll processor.
- No mutation of finalised, frozen, paid, payment-batch, or bank-file PayRuns.

## Prohibited Current-State Claims

Minerva answers must not claim:

- automation is implemented;
- process-all is implemented;
- finalisation is implemented;
- payment is implemented;
- bank file generation is implemented;
- payment batch generation is implemented;
- the bridge creates PayRuns;
- the bridge creates PayRunContacts;
- Minerva calculates payroll;
- Minerva authorises payroll;
- finalised PayRuns can be mutated;
- frozen PayRuns can be mutated;
- paid PayRuns can be mutated;
- UI state alone authorises execution.

## No-Action/No-Runtime Attestation

- No retrieval-plan change from this Minerva slice: yes.
- No runtime retrieval change from this Minerva slice: yes.
- No database access from this Minerva slice: yes.
- No live LLM call from this Minerva slice: yes.
- No Workforce Platform change from this Minerva slice: yes.
- No endpoint implementation from this Minerva slice: yes.
- No UI implementation from this Minerva slice: yes.
- No chat exposure from this Minerva slice: yes.
- No runtime execution from this Minerva slice: yes.
- No payroll calculation from this Minerva slice: yes.
- No payment, finalisation, payment batch, or banking from this Minerva slice: yes.
- No corpus/runtime state mutation from this Minerva slice: yes.
