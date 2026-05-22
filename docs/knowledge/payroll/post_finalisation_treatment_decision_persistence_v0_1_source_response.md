# Minerva Knowledge Capture — Post-Finalisation Treatment Decision Persistence and Admin Queue Workspace

## Purpose of this knowledge capture

This knowledge capture records the Minerva doctrine for **Post-Finalisation Treatment Decision Persistence and Admin Queue Workspace Knowledge v0.1**.

This is a Minerva knowledge and evaluation slice only. It does not modify workforce-platform, connect to a database, call a live LLM, change runtime retrieval behaviour, expose chat, mutate operational corpus/runtime state, perform payroll calculation, create supplementary pay runs, execute out-of-cycle pay runs, execute retro/correction runs, create payments, create banking files, or change finalisation behaviour.

The slice helps Minerva explain what happens when ObjectTime/source truth changes after a regular PayRun has been finalised, why the finalised run remains protected, how Admin Queue acts as the operator workbench, and why committing a treatment decision is distinct from executing payroll treatment.

## 1. What problem this workflow solves

Source truth can change after a regular PayRun has been finalised. For example, ObjectTime for a worker-period may be corrected after the regular PayRun has already been locked by finalisation.

The platform must protect the finalised regular PayRun and avoid silently changing the finalised PayRunContact. At the same time, the source change must not disappear. It should surface as a governed treatment item for operator review so the operator can decide, with backend evidence, whether supplementary, out-of-cycle, later-treatment, or correction handling is appropriate.

## 2. Source truth changed after finalisation

The ObjectTime example is a worker-period source-truth change after finalisation. ObjectTime/source truth changed after finalisation for a worker-period, so the operator must review the impact instead of expecting the finalised PayRun to be dirtied or reprocessed.

The review should classify whether the change belongs to a same-cycle supplementary path, an out-of-cycle path, a later-treatment path, or a correction/retro path. That classification must be evidence-backed and backend-driven.

## 3. Finalised PayRun protection doctrine

Finalised PayRuns are protected payroll records. A later ObjectTime edit must not silently mutate, dirty, or reprocess the finalised regular PayRun.

The finalised PayRunContact is protected in the same doctrine. It must not be silently mutated, dirtied, or reprocessed because a later ObjectTime/source-truth edit occurred. Any consequence of the source-truth change must be handled through a governed treatment path.

Finalised PayRuns and PayRunContacts must not be silently mutated by post-finalisation ObjectTime/source-truth changes. The finalised PayRun and finalised PayRunContact must remain protected.

## 4. Admin Queue as workbench

Admin Queue is the operator workbench for reviewing and clearing queue items. The operator should be able to inspect the treatment item, understand the backend recommendation, review evidence, open related ObjectTime/source-truth context, inspect Worker Story and finalisation details, and commit an available treatment decision where the backend supports persistence.

Command Centre remains the deeper evidence/control-room surface. Admin Queue should keep the operator in the workbench for queue-item treatment, while Command Centre remains available for fuller evidence and control-room investigation.

## 5. Treatment review versus treatment execution

Reviewing a treatment item is not payroll execution. Committing a treatment path is also not payroll execution.

A committed treatment decision records the selected treatment path, such as supplementary, out-of-cycle, later-treatment, or correction handling, where backend persistence exists. It does not by itself create a supplementary PayRun, execute a retro/correction run, process an out-of-cycle run, pay the worker, create a payment batch, create a bank file, or alter finalisation.

## 6. Treatment decision persistence

Where persistence exists, the operator may commit the backend-recommended treatment path. The committed decision must be durable, idempotent, worker-period/source scoped, and visible back in Admin Queue / Pay Process.

The persisted decision should identify the worker-period/source change it applies to, the treatment path classification, recommendation evidence, blockers if any, and whether execution is available. A repeat commit for the same scoped decision should not duplicate or multiply treatment state.

If treatment decision persistence is not available, the platform must say so honestly. The UI and Minerva should use a clear status such as `NOT_IMPLEMENTED_YET` rather than pretending that a commit succeeded.

## 7. Supplementary recommendation

A same finalised regular PayRun process-period ObjectTime change may be recommended as supplementary where backend evidence supports same-cycle supplementary treatment.

Supplementary recommendation is not automatic for every post-finalisation change. The backend must classify the source change, evidence, current lifecycle, blockers, and treatment availability. Retro must not be offered unless the evidence says this is a retro/correction scenario.

## 8. Out-of-cycle / later treatment

Out-of-cycle or later treatment may be recommended where the source change does not belong to the same current supplementary treatment path, where timing or lifecycle evidence points outside same-cycle supplementary handling, or where evidence is insufficient for a current supplementary commit.

The operator should see the recommended path and the reason. If evidence is insufficient, Minerva and the UI should say that honestly rather than inventing a stronger treatment claim.

## 9. Worker Story context

The Worker Story opened from the post-finalisation treatment item is the finalised regular-run worker story. It is evidence about the protected finalised regular PayRun outcome and the worker-period as finalised.

It is not the future supplementary/correction story. If a future supplementary, out-of-cycle, or correction run is created, that future treatment run will produce its own worker story.

Where multiple stories exist for the same ProcessPeriod, the UI and Minerva must distinguish them clearly. Users must understand whether they are viewing finalised regular-run evidence or a later treatment-run story.

## 10. Finalisation details context

Finalisation details should show finalised/protected status and useful finalised payroll summary context. Where available, this should include payroll totals similar to the totals shown in Worker Story, such as gross, net, tax, deductions, employer amounts, and other finalised totals relevant to the protected PayRun.

Finalisation details should not only navigate the operator to Command Centre. If totals are unavailable, the system and Minerva should say so honestly instead of inventing values.

## 11. ObjectTime editing from Admin Queue

ObjectTime may be edited from Admin Queue through the same source-truth edit path used elsewhere, such as Payroll Output. The workspace should be the same editable ObjectTime workspace rather than a narrower duplicate path.

Saving ObjectTime is a source-truth edit. It is not treatment execution, not supplementary execution, not retro execution, and not out-of-cycle payroll execution. After ObjectTime save, the modal should close and Admin Queue / Pay Process state should refresh so the operator sees updated source-change and treatment state.

## 12. Admin Queue workspace UX expectations

Admin Queue treatment workspace UX should support readable in-place review:

- readable human labels instead of GUID-first presentation;
- wider modals;
- sticky footer actions;
- no duplicated Close/Cancel;
- no duplicated bottom navigation buttons;
- technical IDs collapsed or secondary;
- action labels should match real available actions.

The ObjectTime modal should be wide enough and avoid cramped label wrapping. It should not show duplicate Close controls where Cancel already exists. The modal header should avoid GUID-first duplicate chips when the same information is already displayed in readable fields.

Review Treatment should be wide/readable, use sticky footer actions, remove duplicate bottom navigation buttons, and clearly show the next treatment action.

## 13. What the backend owns

The backend owns:

- treatment recommendation;
- treatment commit availability;
- treatment path classification;
- retro/supplementary/out-of-cycle recommendation;
- evidence and blockers;
- whether execution is available.

The UI must not infer these independently. The UI displays backend evidence, backend recommendation, backend commit availability, backend blockers, and backend execution availability. It should not decide locally that supplementary, out-of-cycle, later-treatment, or retro handling is available.

## 14. What remains deferred

Deferred items include:

- supplementary execution;
- out-of-cycle execution;
- retro execution;
- payment/banking;
- finalisation changes;
- treatment workflow execution;
- future worker story for supplementary/correction run;
- live Minerva runtime evidence unless later implemented.

Treatment decision persistence, where implemented, records a governed decision. It does not implement these deferred execution items.

## 15. Minerva explanation requirements

Minerva must help users understand:

- why the finalised run cannot be reprocessed;
- whether a decision has merely been committed or actually executed;
- why supplementary is recommended;
- why retro is not offered;
- why a current worker story is finalised regular-run evidence;
- what remains future/deferred;
- what evidence supports the answer.

Minerva must state evidence limitations when persistence, execution, totals, or source detail are not available in the knowledge/evidence it can cite.

## 16. Prohibited claims

Minerva answers must not claim:

- committing supplementary means a supplementary PayRun was created;
- committing a treatment decision means the worker has been paid;
- the finalised regular PayRun was reprocessed;
- the finalised PayRunContact was dirtied;
- retro should be offered for every post-finalisation source change;
- Worker Story shown is the future supplementary story;
- Minerva calculated or authorised the treatment;
- UI decides treatment path independently from backend evidence.

## 17. Suggested Minerva golden questions

1. What happens when ObjectTime changes after a regular PayRun is finalised?
2. Why can’t the finalised regular PayRun just be reprocessed?
3. What does “finalised PayRun protected” mean?
4. What is a post-finalisation treatment decision?
5. What is the difference between committing a treatment decision and executing treatment?
6. When should supplementary be recommended?
7. When should out-of-cycle or later treatment be considered?
8. Why should retro not be offered unless evidence supports a retro scenario?
9. What does the Admin Queue treatment workspace let the operator do?
10. Is editing ObjectTime from Admin Queue the same as treatment execution?
11. What should happen after ObjectTime is saved from Admin Queue?
12. Which Worker Story is shown before the supplementary/correction run exists?
13. What happens to Worker Story after a future supplementary run is created?
14. What should finalisation details show?
15. What information should be hidden or secondary rather than GUID-first?
16. What does the backend decide versus what the UI displays?
17. What remains deferred after treatment decision persistence?
18. What must Minerva avoid overstating?

## 18. Answer guidance for golden questions

### 1. What happens when ObjectTime changes after a regular PayRun is finalised?

Answer guidance: The finalised regular PayRun remains protected. The source-truth change should surface in Admin Queue / Pay Process for governed treatment review rather than silently dirtying or reprocessing the finalised PayRun or PayRunContact.

### 2. Why can’t the finalised regular PayRun just be reprocessed?

Answer guidance: Finalisation protects the regular PayRun as a completed payroll record. Later source-truth edits must be handled through governed treatment paths so audit, evidence, and payroll consequences remain explicit.

### 3. What does “finalised PayRun protected” mean?

Answer guidance: It means the finalised PayRun and finalised PayRunContact must not be silently mutated, dirtied, or reprocessed by later ObjectTime/source-truth edits.

### 4. What is a post-finalisation treatment decision?

Answer guidance: It is a durable, scoped decision about how to treat a source-truth change discovered after finalisation, such as supplementary, out-of-cycle, later-treatment, or correction handling, based on backend evidence.

### 5. What is the difference between committing a treatment decision and executing treatment?

Answer guidance: Committing records the selected treatment path where persistence exists. Execution would create or run the supplementary, out-of-cycle, or correction payroll process. Commitment alone does not execute payroll, pay a worker, or create a PayRun.

### 6. When should supplementary be recommended?

Answer guidance: Supplementary should be recommended when backend evidence supports same finalised regular PayRun process-period supplementary handling for the source change.

### 7. When should out-of-cycle or later treatment be considered?

Answer guidance: Consider out-of-cycle or later treatment when the change does not belong to the current same-cycle supplementary path, when lifecycle/timing evidence points elsewhere, or when evidence is insufficient for supplementary commitment.

### 8. Why should retro not be offered unless evidence supports a retro scenario?

Answer guidance: Retro/correction is a specific treatment path. It should not be offered for every post-finalisation source change because doing so overstates the evidence and may send the operator down the wrong payroll workflow.

### 9. What does the Admin Queue treatment workspace let the operator do?

Answer guidance: It lets the operator review the treatment item in-place, inspect evidence, open ObjectTime/source-truth context, view Worker Story and finalisation details, see blockers/recommendations, and commit an available backend-recommended treatment decision.

### 10. Is editing ObjectTime from Admin Queue the same as treatment execution?

Answer guidance: No. Editing ObjectTime is a source-truth edit through the same source-truth path used elsewhere. It is not supplementary, out-of-cycle, or retro payroll execution.

### 11. What should happen after ObjectTime is saved from Admin Queue?

Answer guidance: Save should persist source truth, close the ObjectTime modal, and refresh Admin Queue / Pay Process state so the operator sees the current treatment state.

### 12. Which Worker Story is shown before the supplementary/correction run exists?

Answer guidance: The Worker Story opened from the post-finalisation treatment item is the finalised regular-run worker story, not a future supplementary/correction story.

### 13. What happens to Worker Story after a future supplementary run is created?

Answer guidance: If a future supplementary, out-of-cycle, or correction run is created, that future treatment run will produce its own Worker Story. The UI and Minerva must distinguish it from the finalised regular-run story.

### 14. What should finalisation details show?

Answer guidance: Finalisation details should show finalised/protected status and useful finalised payroll summary totals where available, similar to Worker Story totals. If totals are unavailable, the system should say so honestly.

### 15. What information should be hidden or secondary rather than GUID-first?

Answer guidance: Technical IDs and duplicate GUID chips should be collapsed or secondary. The workspace should lead with readable human labels and meaningful payroll/context fields.

### 16. What does the backend decide versus what the UI displays?

Answer guidance: The backend decides recommendation, treatment path classification, commit availability, retro/supplementary/out-of-cycle recommendation, blockers, evidence, and whether execution is available. The UI displays those backend decisions and must not infer them independently.

### 17. What remains deferred after treatment decision persistence?

Answer guidance: Supplementary execution, out-of-cycle execution, retro execution, payment/banking, finalisation changes, treatment workflow execution, future Worker Story for a later treatment run, and live Minerva runtime evidence remain deferred unless separately implemented.

### 18. What must Minerva avoid overstating?

Answer guidance: Minerva must not claim a committed decision created a supplementary PayRun, paid a worker, reprocessed the finalised regular PayRun, dirtied the finalised PayRunContact, calculated or authorised treatment, or that UI independently decides treatment paths.

## 19. Source links

Relevant existing Minerva/payroll docs:

- [admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md)
- [admitted_draft_payrun_processing_bridge_v0_1.md](admitted_draft_payrun_processing_bridge_v0_1.md)
- [admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md](admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md)
- [admitted_draft_payrun_bridge_manual_processing_action_v0_1.md](admitted_draft_payrun_bridge_manual_processing_action_v0_1.md)
- [admitted_draft_payrun_bridge_manual_processing_action_v0_1_implementation_state.md](admitted_draft_payrun_bridge_manual_processing_action_v0_1_implementation_state.md)
- [PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md](../../PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md)
- [OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md](../../OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md)
- [WORKER_STORY_EVALUATION_RUNBOOK.md](../../WORKER_STORY_EVALUATION_RUNBOOK.md)
- [FINALISATION_READINESS_EVALUATION_RUNBOOK.md](../../FINALISATION_READINESS_EVALUATION_RUNBOOK.md)
- [PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md](../../PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md)
- [PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md](../../PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md)
- [CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md](../../CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md)
- [2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md](../../codex_prompts/2026-05-19_minerva_payroll_correction_workflow_reasoning_capture_v0_1.md)
