# Admitted Draft PayRun Bridge Manual Processing Action Implementation State v0.1

Status: current implementation-state addendum for Minerva knowledge and answer evaluation.

This addendum records implementation evidence supplied for the Workforce Platform manual processing action slice. It updates Minerva answer posture for the Admitted Draft PayRun Bridge Manual Processing Action without changing retrieval behaviour, corpus/runtime state, database state, live LLM behaviour, chat exposure, or Workforce Platform code.

## 1. Current status

The manual processing action is implemented in Workforce Platform as a guarded manual action. It is operator-triggered, backend-guarded, and scoped to one admitted draft processing action.

This is not automation. It is not an unattended payroll processor, policy ladder, scheduled job, hidden background action, or process-all workflow.

## 2. Workforce files changed

Reported Workforce Platform changed files:

- `workforce_platform/services/AdmittedDraftPayRunBridgeManualProcessingActionService.py`
- `workforce_platform/api/v1/PayRuns.py`
- `workforce_platform/schemas/spine/PayRunSchema.py`
- `workforce_platform/services/PayRunPayProcessControlService.py`
- `workforce_platform/tests/test_admitted_draft_payrun_bridge_manual_processing_action.py`
- `apps/ui/src/pages/PayRunDetailPage.tsx`
- `apps/ui/src/pages/PayRunAdminQueuePage.tsx`
- `docs/codex_prompts/2026-05-21_admitted_draft_payrun_bridge_manual_processing_action_v01.md`
- `docs/slice_knowledge/2026-05-21_admitted_draft_payrun_bridge_manual_processing_action_v0_1.md`

## 3. Endpoint implemented

Implemented endpoint:

```text
POST /api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process
```

The endpoint is guarded, manual-only, one-action scoped, and not process-all. It does not expose broad or bulk admitted-action processing.

## 4. Action identity and authority requirements

The endpoint identifies one action through `PayRunActionDecisionId` / `DecisionId`, or through action/admission context that resolves to exactly one matching decision.

Execution requires exactly one matching decision plus authorised admission evidence. The decision must be active and non-stale, and the admission evidence must be accepted/authorised with draft-processing authority.

## 5. Preflight requirements

Backend preflight is mandatory before execution. It requires:

- active non-stale `PayRunActionDecision`;
- accepted/authorised admission evidence;
- route `PayRunId` matches target `PayRun`;
- safe draft `PayRun`;
- existing `PayRunContact`;
- safe `ProcessPeriod.LifecycleStatusCode`;
- deterministic processing entrypoint;
- idempotency basis.

Preflight uses the existing operator action / bridge preview path before execution and blocks unsafe or ambiguous cases.

## 6. Execution path

Execution delegates to `AdmittedDraftPayRunProcessingBridgeService`.

The only processing entrypoint remains:

```text
PayRunProcessingService.process(..., target_contact_id=...)
```

The manual action does not introduce a parallel payroll processor or alternate calculation path.

## 7. UI integration

PayRun Detail Pay Process action table shows the Process admitted action from backend `ManualProcessingAction`.

Admin Queue surfaces admitted draft action items from the same backend packet.

The UI wires and enables the action only when the backend marks it eligible. If blocked, the UI shows backend status and blockers rather than inferring eligibility from local state.

## 8. Readiness behaviour

The response returns `READINESS_UPDATE_PENDING`.

A dedicated readiness refresh adapter was not newly built and remains future work. The UI refreshes Pay Process state after the action result.

## 9. Idempotency behaviour

Idempotency is exposed through the request basis plus the bridge admission/idempotency key.

Where durable packet storage is unavailable, the response states the persistence limitation.

## 10. Non-goals preserved

This implementation preserves these non-goals:

- no automation;
- no process-all;
- no finalisation;
- no payment;
- no bank file;
- no payment batch;
- no `PayRun` creation;
- no `PayRunContact` creation;
- no manual adjustment;
- no retro execution;
- no recovery execution;
- no source-truth mutation;
- no Minerva calculation;
- no Minerva decisioning;
- no parallel payroll processor.

It also preserves the boundary that finalised, frozen, paid, payment-batch, or bank-file PayRuns must not be mutated by this action.

## 11. Deferred items

Deferred Workforce Platform items:

- durable persisted admission lookup;
- dedicated readiness refresh adapter.

## 12. Verification evidence

Reported verification results:

- `py_compile` passed.
- Focused backend tests passed: 31 passed.
- Related selector initially failed during collection because unrelated contract tests import missing `requests`.
- Related selector excluding the contract folder passed: 63 passed, 1178 deselected.
- UI build passed.
- Vite reported an existing large chunk warning.
- `git diff --check` passed with CRLF warnings only.

## 13. Minerva answer guidance

Minerva may now say:

- the manual processing endpoint exists;
- PayRun Detail and Admin Queue action wiring exists;
- the action is manual and backend-guarded;
- only one admitted action is processed;
- backend preflight is mandatory;
- the endpoint is not automation, not process-all, and not finalisation/payment/banking.

Minerva must not say:

- automation is implemented;
- process-all is implemented;
- finalisation is implemented;
- payment is implemented;
- bank file generation is implemented;
- the bridge creates PayRuns or PayRunContacts;
- Minerva calculates or authorises payroll;
- finalised, frozen, or paid PayRuns can be mutated.

## 14. Source links

- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md`
- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_bridge_manual_processing_action_v0_1/ANSWER_EVALUATION_BASELINE.md`

## No-Action Attestation

- No retrieval-plan change happened in this Minerva slice.
- No runtime retrieval change happened in this Minerva slice.
- No database access happened in this Minerva slice.
- No live LLM call happened in this Minerva slice.
- No Workforce Platform edit happened in this Minerva slice.
- No endpoint implementation happened in this Minerva slice.
- No UI implementation happened in this Minerva slice.
- No runtime execution happened in this Minerva slice.
- No payroll calculation happened in this Minerva slice.
- No payment, finalisation, payment batch, or banking happened in this Minerva slice.
- No corpus/runtime state was mutated by this Minerva slice.
