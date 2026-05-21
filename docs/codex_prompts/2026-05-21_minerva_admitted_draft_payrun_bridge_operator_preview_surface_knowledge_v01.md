# Codex Prompt Artefact - Minerva Admitted Draft PayRun Bridge Operator Preview Surface Knowledge v0.1

Date: 2026-05-21

Repository: `ezeas-intelligence`

Objective: implement the Minerva knowledge slice for **Admitted Draft PayRun Bridge Operator Preview Surface v0.1**.

## Scope

Create knowledge and evaluation artefacts only:

- `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_bridge_operator_preview_surface_v0_1/ANSWER_EVALUATION_BASELINE.md`
- `tests/test_admitted_draft_payrun_bridge_operator_preview_surface_knowledge.py`

## Doctrine To Preserve

- Preview is not execution.
- Visibility is not mutation.
- Eligibility is not authorisation to process.
- Next-action suggestion is not a command.
- Dry-run endpoint is not a processing route.
- Operator UI card is not a Process Now button.
- Endpoint is dry-run/read-only by default.
- Preview must not call processing or perform route execution.
- Preview must not create PayRuns or PayRunContacts.
- Preview must not finalise, pay, generate bank files, generate payment batches, automate payroll, or mutate source truth.
- Deterministic payroll authority remains in Workforce Platform services, not Minerva.

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

1. What is the Admitted Draft PayRun Bridge Operator Preview Surface?
2. Why is the Operator Preview Surface needed after the bridge operator action contract?
3. What does preview mean in this context?
4. Why is preview not execution?
5. What should the operator see in the preview card?
6. What should the guarded preview endpoint return?
7. Why must the endpoint be dry-run/read-only by default?
8. Why should there be no Process Now button yet?
9. What has already been implemented in Workforce Platform before this slice?
10. What is planned for the next Workforce slice?
11. What must this slice not implement?
12. How should Minerva explain this slice without overstating runtime behaviour?
13. What runtime-overstatement risks should Minerva avoid?
14. How does this slice preserve deterministic payroll authority?
15. What evidence/story should be exposed by the preview surface?
16. What is the next valid slice after preview visibility?

## Verification Commands

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_admitted_draft_payrun_bridge_operator_preview_surface_knowledge.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_admitted_draft_payrun_processing_bridge_source_response.py tests/test_admitted_draft_payrun_processing_bridge_knowledge_pack.py tests/test_admitted_draft_payrun_processing_bridge_answer_evaluation.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
git diff --check
git status --short
```
