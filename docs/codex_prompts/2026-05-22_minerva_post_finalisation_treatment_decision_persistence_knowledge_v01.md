# Codex Prompt Artefact - Minerva Post-Finalisation Treatment Decision Persistence Knowledge v0.1

Date: 2026-05-22

Repository: `ezeas-intelligence`

Objective: implement the Minerva knowledge/evaluation slice for **Post-Finalisation Treatment Decision Persistence and Admin Queue Workspace Knowledge v0.1**.

## Scope

Create knowledge and evaluation artefacts only:

- `docs/knowledge/payroll/post_finalisation_treatment_decision_persistence_v0_1_source_response.md`
- `docs/knowledge/payroll/post_finalisation_treatment_decision_persistence_v0_1.md`
- `docs/evaluation/post_finalisation_treatment_decision_persistence_v0_1/ANSWER_EVALUATION_BASELINE.md`
- `tests/test_post_finalisation_treatment_decision_persistence_knowledge.py`

## Product Direction

When ObjectTime/source truth changes after a regular PayRun has been finalised:

- the finalised regular PayRun remains protected;
- the finalised PayRunContact is not dirtied or silently reprocessed;
- the source change appears in Admin Queue / Pay Process;
- the operator reviews the treatment in-place;
- the operator may commit the recommended treatment path where backend evidence and persistence support it;
- committing a treatment decision is not the same as executing a supplementary, out-of-cycle, or retro/correction run.

## Doctrine To Preserve

- Admin Queue is the operator workbench.
- Command Centre remains the deeper evidence/control-room surface.
- ObjectTime edit from Admin Queue is source-truth edit, not treatment execution.
- ObjectTime save should persist source truth, close the modal, and refresh Admin Queue / Pay Process state.
- Finalised PayRuns and finalised PayRunContacts must not be silently mutated, dirtied, or reprocessed.
- Worker Story opened before a future treatment run exists is the finalised regular-run worker story.
- A future supplementary/correction run will produce its own Worker Story.
- Finalisation details should show finalised/protected status and payroll totals where available.
- Backend owns treatment recommendation, commit availability, path classification, evidence, blockers, and execution availability.
- UI must not infer treatment path independently from backend evidence.
- If persistence is unavailable, say `NOT_IMPLEMENTED_YET`.

## Admin Queue Workspace UX

- readable human labels instead of GUID-first presentation;
- wider modals;
- sticky footer actions;
- no duplicated Close/Cancel;
- no duplicated bottom navigation buttons;
- technical IDs collapsed or secondary;
- action labels should match real available actions.

## No-Action Attestation

- No workforce-platform changes.
- No runtime retrieval behaviour changes.
- No retrieval-plan changes.
- No database connection, reads, writes, migrations, or validation.
- No live LLM calls.
- No chat exposure.
- No operational corpus/runtime state mutation.
- No payroll calculation.
- No supplementary PayRun creation.
- No supplementary execution.
- No out-of-cycle execution.
- No retro/correction execution.
- No payment or banking execution.
- No finalisation changes.
- This Minerva slice is knowledge only.

## Golden Questions

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

## Prohibited Claims

- committing supplementary means a supplementary PayRun was created;
- committing a treatment decision means the worker has been paid;
- the finalised regular PayRun was reprocessed;
- the finalised PayRunContact was dirtied;
- retro should be offered for every post-finalisation source change;
- Worker Story shown is the future supplementary story;
- Minerva calculated or authorised the treatment;
- UI decides treatment path independently from backend evidence.

## Verification Commands

```powershell
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_post_finalisation_treatment_decision_persistence_knowledge.py
C:\Users\dbhas\AppData\Local\Programs\Python\Python312\python.exe -m pytest tests/test_worker_story_baseline_capture_pilot.py tests/test_completed_domain_baseline_decision_ledger.py
git diff --check
git status --short
```

