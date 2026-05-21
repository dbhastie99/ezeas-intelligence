# Codex Prompt Artefact - Minerva Admitted Draft PayRun Bridge Manual Processing Action Implementation State v0.1

Date: 2026-05-21

Repository: `ezeas-intelligence`

Objective: implement the Minerva implementation-state slice for **Admitted Draft PayRun Bridge Manual Processing Action Implementation State v0.1**.

## Scope

Create documentation and evaluation artefacts only:

- `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1_implementation_state.md`
- `docs/evaluation/admitted_draft_payrun_bridge_manual_processing_action_v0_1/IMPLEMENTATION_STATE_BASELINE.md`
- `tests/test_admitted_draft_payrun_bridge_manual_processing_action_implementation_state.py`
- `docs/codex_prompts/2026-05-21_minerva_admitted_draft_payrun_bridge_manual_processing_action_implementation_state_v01.md`

## Implementation Truth To Capture

- Workforce Platform implemented the manual admitted-draft processing action slice.
- Implemented endpoint: `POST /api/v1/pay-runs/{id}/pay-process/admitted-draft-actions/process`.
- The endpoint is guarded, manual-only, one-action scoped, and not process-all.
- The endpoint identifies one action through `PayRunActionDecisionId` / `DecisionId`, or action/admission context.
- Exactly one matching active non-stale decision is required.
- Accepted/authorised admission evidence with draft-processing authority is required.
- Preflight uses the existing operator action / bridge preview path before execution.
- Preflight requires route `PayRunId` to match target `PayRun`.
- Preflight requires safe draft `PayRun` state.
- Preflight requires existing `PayRunContact`.
- Preflight respects `ProcessPeriod.LifecycleStatusCode`.
- Preflight requires deterministic processing entrypoint and idempotency basis.
- Execution delegates to `AdmittedDraftPayRunProcessingBridgeService`.
- `PayRunProcessingService.process(..., target_contact_id=...)` remains the only processing entrypoint.
- PayRun Detail and Admin Queue UI wiring exists.
- UI wires the action only when backend marks it eligible.
- Blocked actions show backend status/blockers.
- UI refreshes Pay Process state after action result.
- Response returns `READINESS_UPDATE_PENDING`.
- Dedicated readiness refresh adapter remains future work.
- Durable persisted admission lookup remains future work where environments do not expose admission packets.

## Non-Goals To Preserve

- No automation.
- No process-all.
- No finalisation.
- No payment.
- No bank file.
- No payment batch.
- No PayRun creation.
- No PayRunContact creation.
- No manual adjustment.
- No retro execution.
- No recovery execution.
- No source-truth mutation.
- No Minerva calculation.
- No Minerva decisioning.
- No parallel payroll processor.

## Minerva Answer Guidance

Minerva may now say the manual processing endpoint exists, PayRun Detail/Admin Queue action wiring exists, the action is manual and backend-guarded, one admitted action is processed, and backend preflight is mandatory.

Minerva must not say automation, process-all, finalisation, payment, bank file generation, PayRun creation, PayRunContact creation, Minerva payroll calculation, Minerva payroll authorisation, or mutation of finalised/frozen/paid PayRuns is implemented.

## No-Action Attestation

- No runtime changes.
- No live LLM calls.
- No database connection.
- No DB access, reads, writes, migrations, or validation.
- No workforce-platform edit.
- No retrieval-plan/runtime behaviour changes.
- No chat exposure.
- No operational corpus/runtime state mutation.
- No payroll calculation logic.
- No Minerva payroll decisioning.

## Verification Commands

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_admitted_draft_payrun_bridge_manual_processing_action_implementation_state.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_admitted_draft_payrun_bridge_manual_processing_action_knowledge.py tests/test_admitted_draft_payrun_bridge_operator_preview_surface_knowledge.py tests/test_admitted_draft_payrun_processing_bridge_source_response.py tests/test_admitted_draft_payrun_processing_bridge_knowledge_pack.py tests/test_admitted_draft_payrun_processing_bridge_answer_evaluation.py tests/test_admitted_draft_payrun_processing_bridge_implementation_state.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
git diff --check
git status --short
```

Do not commit.
