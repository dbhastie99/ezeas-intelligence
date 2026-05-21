# Codex Prompt Artefact - Minerva Admitted Draft PayRun Bridge Manual Processing Action Knowledge v0.1

Date: 2026-05-21

Repository: `ezeas-intelligence`

Objective: implement the Minerva knowledge slice for **Admitted Draft PayRun Bridge Manual Processing Action v0.1**.

## Scope

Create knowledge and evaluation artefacts only:

- `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_manual_processing_action_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_bridge_manual_processing_action_v0_1/ANSWER_EVALUATION_BASELINE.md`
- `tests/test_admitted_draft_payrun_bridge_manual_processing_action_knowledge.py`

## Product Decision

Do not create a separate visible preview workflow for the operator. The existing Pay Process/Admin Queue action exposure model remains the primary workflow.

The backend preview/operator-action contract remains useful as internal preflight and eligibility logic. Preview/preflight is internal safety logic, not a separate visible workflow.

## Manual Workflow

```text
existing Pay Process action surface
→ operator manually selects "Process admitted action"
→ backend runs strict preflight/guard checks
→ backend executes existing bridge only if safe
→ backend returns success/blocker packet
→ UI refreshes Pay Process state
```

## Doctrine To Preserve

- Manual action is not automation.
- Preview is not execution.
- Visibility is not mutation.
- Backend is source of eligibility truth, blocker reason, and execution result.
- UI must not infer eligibility independently.
- Active PayRunActionDecision is required.
- Authorised admission evidence is required.
- Existing PayRunContact required.
- No PayRun/PayRunContact creation.
- No finalisation/payment/bank file.
- No Minerva calculation or Minerva decisioning.
- No bypass of PayRunActionDecision/admission authority.

## No-Action Attestation

- No runtime changes.
- No live LLM calls.
- No DB access, reads, writes, migrations, or validation.
- No workforce-platform changes.
- No endpoint or UI changes in this Minerva slice.
- No retrieval-plan/runtime behaviour changes.
- No chat exposure.
- No operational corpus/runtime state mutation.
- No payroll calculation logic.
- No Minerva payroll decisioning.

## Golden Questions

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

## Source Links To Preserve

- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md`
- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_implementation_state.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md`

## Verification Commands

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_admitted_draft_payrun_bridge_manual_processing_action_knowledge.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_admitted_draft_payrun_bridge_operator_preview_surface_knowledge.py tests/test_admitted_draft_payrun_processing_bridge_source_response.py tests/test_admitted_draft_payrun_processing_bridge_knowledge_pack.py tests/test_admitted_draft_payrun_processing_bridge_answer_evaluation.py tests/test_admitted_draft_payrun_processing_bridge_implementation_state.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
git diff --check
git status --short
```
