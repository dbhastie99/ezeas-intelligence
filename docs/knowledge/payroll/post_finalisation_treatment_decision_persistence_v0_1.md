# Post-Finalisation Treatment Decision Persistence and Admin Queue Workspace v0.1

Status: v0.1 structured Minerva knowledge pack.

Source-response authority: [post_finalisation_treatment_decision_persistence_v0_1_source_response.md](post_finalisation_treatment_decision_persistence_v0_1_source_response.md).

This is knowledge-only documentation. It does not implement runtime retrieval changes, database behaviour, live LLM behaviour, endpoint exposure, UI mutation, chat exposure, operational corpus mutation, workforce-platform changes, payroll calculation, treatment execution, supplementary PayRun creation, out-of-cycle execution, retro execution, payment/banking, or finalisation changes.

## Domain And Scope

This knowledge pack explains the doctrine for source truth changing after a regular PayRun has been finalised. ObjectTime/source truth may change for a worker-period after finalisation. The finalised regular PayRun and finalised PayRunContact must remain protected while the source change is surfaced in Admin Queue / Pay Process for governed treatment review.

The slice covers treatment decision persistence knowledge only. It distinguishes treatment decision commitment from supplementary, out-of-cycle, later-treatment, or retro/correction payroll execution.

## Core Doctrine

- A post-finalisation ObjectTime change is a source-truth change after the regular PayRun has been finalised.
- The finalised PayRun is protected.
- The finalised PayRunContact is protected.
- Finalised PayRuns and PayRunContacts must not be silently mutated.
- No finalised PayRun mutation should occur because of a later ObjectTime edit.
- No finalised PayRunContact mutation should occur because of a later ObjectTime edit.
- Admin Queue is the operator workbench for treatment review and queue clearance.
- Command Centre remains the deeper evidence/control-room surface.
- ObjectTime edit from Admin Queue is source-truth edit, not treatment execution.
- Treatment decision persistence, where available, records a durable scoped decision.
- Committing a treatment decision does not create a PayRun, pay a worker, execute a supplementary run, execute an out-of-cycle run, or execute a retro/correction run.

## Treatment Decision Persistence

Where persistence exists, the operator may commit the backend-recommended treatment path. The decision must be durable, idempotent, worker-period/source scoped, and visible in Admin Queue / Pay Process.

If treatment decision persistence is not available, the platform must say `NOT_IMPLEMENTED_YET` or equivalent honest status. It must not fake the commit.

The committed decision should record:

- worker-period/source scope;
- treatment path classification;
- backend recommendation;
- evidence and blockers;
- commit availability;
- whether execution is available;
- actions taken and actions not taken.

## Treatment Decision Versus Execution

Treatment decision commitment is not treatment execution. It records the selected governed path. Payroll execution is separate future or separately implemented work.

Commit to supplementary does not mean a supplementary PayRun was created. It does not mean the worker was paid. It does not mean finalisation changed. It does not mean the finalised regular PayRun was reprocessed.

## Backend-Driven Recommendation

The backend owns:

- treatment recommendation;
- treatment commit availability;
- treatment path classification;
- retro/supplementary/out-of-cycle recommendation;
- evidence and blockers;
- whether execution is available.

The UI displays backend decisions and backend evidence. The UI must not infer treatment path independently from local row state.

Supplementary may be recommended when backend evidence supports same finalised regular PayRun process-period supplementary treatment for the source change. Retro should not be offered unless evidence supports a retro/correction scenario. Out-of-cycle or later treatment may be recommended when the source change does not belong to the current supplementary treatment path or evidence is insufficient.

## Admin Queue Workspace

Admin Queue treatment workspace is the operator workbench. It should let the operator review the queue item in-place, inspect evidence, open ObjectTime/source-truth context, view Worker Story, inspect finalisation details, see recommendation and blockers, and commit an available backend-recommended treatment decision.

UX expectations include:

- readable human labels rather than GUID-first presentation;
- technical IDs collapsed or secondary;
- wider modals;
- sticky footer actions;
- no duplicate Close/Cancel controls;
- no duplicate bottom navigation buttons;
- action labels that match real available backend actions;
- readable Review Treatment and ObjectTime workspaces;
- finalisation details with protected status and payroll totals where available.

## ObjectTime Editing

ObjectTime opened from Admin Queue should use the same editable source-truth workspace used elsewhere, such as Payroll Output.

Saving ObjectTime persists source truth. It is not treatment execution. After save, the ObjectTime modal should close and Admin Queue / Pay Process state should refresh.

## Worker Story And Finalisation Details

The Worker Story opened from a post-finalisation treatment item is the finalised regular-run worker story before any future treatment run exists. It is not the future supplementary/correction story.

If a future supplementary, out-of-cycle, or correction run is created, that future run will produce its own Worker Story. Where multiple stories exist for the same ProcessPeriod, UI and Minerva must distinguish finalised regular-run evidence from future treatment-run evidence.

Finalisation details should show finalised/protected status and useful payroll totals where available. If payroll totals are unavailable, the system should say so honestly.

## Deferred Items

Deferred unless separately implemented:

- supplementary execution;
- out-of-cycle execution;
- retro execution;
- payment/banking;
- finalisation changes;
- treatment workflow execution;
- future worker story for supplementary/correction run;
- live Minerva runtime evidence.

## Minerva Answer Boundaries

Minerva should explain:

- why the finalised run cannot be reprocessed;
- why finalised PayRun/PayRunContact are not mutated;
- whether a treatment decision was merely committed or actually executed;
- why supplementary is recommended;
- why retro is not offered unless evidence supports retro;
- why the current Worker Story is finalised regular-run evidence;
- what remains deferred;
- what evidence supports the answer.

Minerva must report evidence limitations when persistence, execution, totals, or implementation state are unavailable.

## Prohibited Claims

Minerva answers must not claim:

- committing supplementary means a supplementary PayRun was created;
- committing a treatment decision means the worker has been paid;
- the finalised regular PayRun was reprocessed;
- the finalised PayRunContact was dirtied;
- retro should be offered for every post-finalisation source change;
- Worker Story shown is the future supplementary story;
- Minerva calculated or authorised the treatment;
- UI decides treatment path independently from backend evidence.

## No-Action Attestation

- No workforce-platform changes: yes.
- No runtime retrieval behaviour changes: yes.
- No retrieval-plan changes: yes.
- No database connection, reads, writes, migrations, or validation: yes.
- No live LLM calls: yes.
- No chat exposure: yes.
- No operational corpus/runtime state mutation: yes.
- No payroll calculation: yes.
- No supplementary PayRun creation: yes.
- No supplementary execution: yes.
- No out-of-cycle execution: yes.
- No retro/correction execution: yes.
- No payment or banking execution: yes.
- No finalisation changes: yes.
- This Minerva slice is knowledge only: yes.

## Golden Questions And Answer Guidance

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

## Retrieval Keywords And Aliases

- post-finalisation ObjectTime change
- treatment decision persistence
- commit to supplementary
- treatment decision versus execution
- finalised PayRun protected
- finalised regular-run worker story
- future supplementary worker story
- Admin Queue treatment workspace
- ObjectTime edit from Admin Queue
- no finalised PayRun mutation
- no retro unless evidence supports retro
- backend-driven treatment recommendation
- finalised PayRunContact protected
- worker-period/source scoped decision
- NOT_IMPLEMENTED_YET treatment persistence
- sticky footer treatment review
- GUID-first technical IDs secondary
- finalisation details payroll totals

## Source Links

- [post_finalisation_treatment_decision_persistence_v0_1_source_response.md](post_finalisation_treatment_decision_persistence_v0_1_source_response.md)
- [admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md)
- [admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md](admitted_draft_payrun_bridge_manual_processing_action_v0_1_source_response.md)
- [admitted_draft_payrun_bridge_manual_processing_action_v0_1_implementation_state.md](admitted_draft_payrun_bridge_manual_processing_action_v0_1_implementation_state.md)
- [PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md](../../PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md)
- [OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md](../../OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md)
- [WORKER_STORY_EVALUATION_RUNBOOK.md](../../WORKER_STORY_EVALUATION_RUNBOOK.md)
- [FINALISATION_READINESS_EVALUATION_RUNBOOK.md](../../FINALISATION_READINESS_EVALUATION_RUNBOOK.md)
- [PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md](../../PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md)
- [PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md](../../PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md)
