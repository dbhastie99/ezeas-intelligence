# Post-Finalisation Treatment Decision Persistence Answer Evaluation Baseline v0.1

Domain name: Post-Finalisation Treatment Decision Persistence and Admin Queue Workspace.

Source-response path: `docs/knowledge/payroll/post_finalisation_treatment_decision_persistence_v0_1_source_response.md`

Structured knowledge path: `docs/knowledge/payroll/post_finalisation_treatment_decision_persistence_v0_1.md`

Evaluation status: checked-in deterministic answer-behaviour baseline. This Minerva slice is knowledge only. It does not implement retrieval changes, runtime retrieval behaviour, database behaviour, live LLM behaviour, endpoint exposure, UI mutation, chat exposure, operational corpus mutation, workforce-platform changes, payroll calculation, treatment execution, supplementary PayRun creation, out-of-cycle execution, retro execution, payment/banking, or finalisation changes.

## Answer-Boundary Summary

- ObjectTime/source truth can change after a regular PayRun is finalised.
- The finalised PayRun is protected.
- The finalised PayRunContact is protected.
- Finalised PayRun/PayRunContact are not mutated, dirtied, or silently reprocessed by later ObjectTime edits.
- Admin Queue is the operator treatment workspace.
- Command Centre remains the deeper evidence/control-room surface.
- ObjectTime edit from Admin Queue is source-truth edit, not treatment execution.
- Treatment decision commitment is different from treatment execution.
- Commit to supplementary does not create a supplementary PayRun.
- Backend owns treatment recommendation, treatment path classification, commit availability, blockers, evidence, and whether execution is available.
- UI displays backend state and must not infer the treatment path independently.
- Worker Story opened before a future treatment run exists is the finalised regular-run worker story.
- A future supplementary/correction run will have its own Worker Story.
- Finalisation details should show protected status and payroll totals where available.
- If persistence is unavailable, answer with `NOT_IMPLEMENTED_YET` or equivalent honest caveat.

## Prohibited Claims

Minerva answers for this domain must not claim:

- committing supplementary means a supplementary PayRun was created;
- committing a treatment decision means the worker has been paid;
- the finalised regular PayRun was reprocessed;
- the finalised PayRunContact was dirtied;
- retro should be offered for every post-finalisation source change;
- Worker Story shown is the future supplementary story;
- Minerva calculated or authorised the treatment;
- UI decides treatment path independently from backend evidence.

## Required Caveats

- This Minerva slice is knowledge only.
- No runtime changes were made.
- No live LLM calls were made.
- No DB access, reads, writes, migrations, or validation were performed.
- No workforce-platform changes were made.
- No endpoint, UI, chat, or runtime retrieval behaviour was changed by this slice.
- No operational corpus/runtime state was mutated.
- No payroll calculation was performed.
- No supplementary, out-of-cycle, retro, or correction run was created or executed.
- No payment, banking, or finalisation change occurred.
- If persistence is not available, Minerva must say so honestly and must not fake commit success.
- Runtime claims require later implementation evidence.

## No-Action Attestation

- This Minerva slice is knowledge only: yes.
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
- No supplementary execution: yes.
- No out-of-cycle execution: yes.
- No retro/correction execution: yes.
- No payment/banking: yes.
- No finalisation changes: yes.

## Golden Questions And Expected Answer Themes

### 1. What happens when ObjectTime changes after a regular PayRun is finalised?

Expected answer themes:
- Finalised regular PayRun remains protected.
- Finalised PayRunContact remains protected.
- Source change surfaces in Admin Queue / Pay Process for governed treatment.

Prohibited claims:
- Do not say the finalised PayRun or PayRunContact is silently reprocessed.

Required caveats:
- Treatment review depends on backend evidence.

### 2. Why can’t the finalised regular PayRun just be reprocessed?

Expected answer themes:
- Finalisation protects the regular PayRun.
- Later source-truth edits need governed treatment rather than mutation.
- Audit/evidence must remain explicit.

Prohibited claims:
- Do not say finalised payroll can simply be recalculated in place.

Required caveats:
- Later treatment may be supplementary, out-of-cycle, later-treatment, or correction based on evidence.

### 3. What does “finalised PayRun protected” mean?

Expected answer themes:
- Protected finalised PayRun is not silently mutated, dirtied, or reprocessed.
- Protected finalised PayRunContact is not silently mutated, dirtied, or reprocessed.

Prohibited claims:
- Do not say later ObjectTime save dirties the finalised PayRunContact.

Required caveats:
- Treatment consequences must be governed separately.

### 4. What is a post-finalisation treatment decision?

Expected answer themes:
- Durable, idempotent, worker-period/source scoped decision.
- Classifies treatment path after source truth changed post-finalisation.
- Visible back in Admin Queue / Pay Process where persistence exists.

Prohibited claims:
- Do not say the decision itself executes payroll.

Required caveats:
- If persistence is unavailable, say `NOT_IMPLEMENTED_YET`.

### 5. What is the difference between committing a treatment decision and executing treatment?

Expected answer themes:
- Commit records selected treatment path.
- Execution creates/runs supplementary, out-of-cycle, or correction payroll.
- Commit alone does not create PayRun, pay worker, bank, or finalise.

Prohibited claims:
- Do not say commit to supplementary created a supplementary PayRun.

Required caveats:
- Execution remains future or separately implemented.

### 6. When should supplementary be recommended?

Expected answer themes:
- Backend evidence supports same finalised regular PayRun process-period supplementary treatment.
- Recommendation is evidence-based, not automatic.

Prohibited claims:
- Do not offer supplementary solely from UI row state.

Required caveats:
- Backend owns the recommendation.

### 7. When should out-of-cycle or later treatment be considered?

Expected answer themes:
- Source change does not belong to current same-cycle supplementary path.
- Lifecycle/timing evidence points outside same-cycle supplementary treatment.
- Evidence is insufficient for current supplementary commit.

Prohibited claims:
- Do not force all post-finalisation changes into supplementary.

Required caveats:
- The reason should be visible to the operator.

### 8. Why should retro not be offered unless evidence supports a retro scenario?

Expected answer themes:
- Retro/correction is specific, not universal.
- Offering retro without evidence overstates the treatment path.
- Backend evidence must support retro/correction.

Prohibited claims:
- Do not say retro is offered for every post-finalisation source change.

Required caveats:
- Use supplementary/out-of-cycle/later-treatment where evidence supports those paths.

### 9. What does the Admin Queue treatment workspace let the operator do?

Expected answer themes:
- Review the item in-place.
- Inspect evidence, blockers, recommendation, ObjectTime context, Worker Story, and finalisation details.
- Commit available backend-recommended treatment decision where persistence exists.

Prohibited claims:
- Do not say Admin Queue itself executes payroll treatment merely by review.

Required caveats:
- Command Centre remains deeper evidence/control-room surface.

### 10. Is editing ObjectTime from Admin Queue the same as treatment execution?

Expected answer themes:
- No. It is source-truth edit.
- It should use the same ObjectTime edit path as Payroll Output.
- It is not supplementary, out-of-cycle, or retro execution.

Prohibited claims:
- Do not say ObjectTime save creates a treatment PayRun.

Required caveats:
- Save should refresh queue/pay-process state.

### 11. What should happen after ObjectTime is saved from Admin Queue?

Expected answer themes:
- Persist source truth.
- Close the modal.
- Refresh Admin Queue / Pay Process state.

Prohibited claims:
- Do not say save means payroll treatment has executed.

Required caveats:
- The resulting treatment state should come from backend refresh/state.

### 12. Which Worker Story is shown before the supplementary/correction run exists?

Expected answer themes:
- The finalised regular-run worker story.
- It is evidence for the protected regular PayRun outcome.

Prohibited claims:
- Do not say it is the future supplementary/correction story.

Required caveats:
- The UI and Minerva should label the story context clearly.

### 13. What happens to Worker Story after a future supplementary run is created?

Expected answer themes:
- Future treatment run produces its own Worker Story.
- Multiple stories for same ProcessPeriod must be distinguished.

Prohibited claims:
- Do not collapse regular-run and treatment-run stories into one ambiguous story.

Required caveats:
- Future treatment story remains deferred unless separately implemented.

### 14. What should finalisation details show?

Expected answer themes:
- Finalised/protected status.
- Useful finalised payroll summary.
- Payroll totals like gross, net, tax, deductions, employer amounts where available.

Prohibited claims:
- Do not invent totals when unavailable.

Required caveats:
- If totals are unavailable, say so honestly.

### 15. What information should be hidden or secondary rather than GUID-first?

Expected answer themes:
- Technical IDs and duplicate GUID chips.
- Readable human labels and meaningful fields should lead.

Prohibited claims:
- Do not present GUID-first duplicate chips as the primary user explanation.

Required caveats:
- Technical IDs may remain available as secondary/collapsed detail.

### 16. What does the backend decide versus what the UI displays?

Expected answer themes:
- Backend decides recommendation, classification, commit availability, blockers, evidence, and execution availability.
- UI displays backend decisions and must not infer independently.

Prohibited claims:
- Do not say UI decides treatment path independently from backend evidence.

Required caveats:
- Backend-driven treatment recommendation is mandatory.

### 17. What remains deferred after treatment decision persistence?

Expected answer themes:
- Supplementary execution.
- Out-of-cycle execution.
- Retro execution.
- Payment/banking.
- Finalisation changes.
- Treatment workflow execution.
- Future Worker Story for treatment run.
- Live Minerva runtime evidence.

Prohibited claims:
- Do not say this knowledge slice executes payroll.

Required caveats:
- Deferred items require separate implementation and evidence.

### 18. What must Minerva avoid overstating?

Expected answer themes:
- Do not overstate decision commit as execution.
- Do not claim PayRun creation, payment, reprocessing, dirtying finalised PayRunContact, Minerva calculation/authorisation, or UI-independent treatment decisioning.

Prohibited claims:
- All prohibited claims listed above apply.

Required caveats:
- State evidence boundaries and implementation limits.

