# Admitted Draft PayRun Bridge Operator Preview Surface Answer Evaluation Baseline v0.1

Domain name: Admitted Draft PayRun Bridge Operator Preview Surface.

Source-response path: `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md`

Structured knowledge path: `docs/knowledge/payroll/admitted_draft_payrun_bridge_operator_preview_surface_v0_1.md`

Evaluation status: checked-in deterministic answer-behaviour baseline. This Minerva slice is knowledge only. It does not implement retrieval changes, runtime bridge execution, database behaviour, live LLM behaviour, endpoint exposure, UI mutation, chat exposure, operational corpus mutation, or Workforce Platform changes.

Prior bridge knowledge links:

- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1_source_response.md`
- `docs/knowledge/payroll/admitted_draft_payrun_processing_bridge_v0_1.md`
- `docs/evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md`

## Answer-Boundary Summary

- Preview is not execution.
- Visibility is not mutation.
- Eligibility is not authorisation to process.
- Next-action suggestion is not a command.
- Dry-run endpoint is not a processing route.
- Operator UI card is not a Process Now button.
- Endpoint is dry-run/read-only by default.
- Preview must not call processing or perform route execution.
- Preview must not create PayRuns or PayRunContacts.
- Preview must not finalise, pay, generate bank files, generate payment batches, or automate payroll.
- Deterministic payroll authority remains in Workforce Platform services, not Minerva.

## Prohibited Claims

Minerva answers for this domain must not claim:

- operators can execute admitted draft processing from the UI;
- the bridge route performs processing;
- the UI has a Process Now button;
- preview mutates PayRuns;
- preview creates PayRuns or PayRunContacts;
- preview finalises or pays;
- preview generates bank files;
- preview is automation;
- Minerva calculates payroll;
- deterministic processing authority moved to Minerva.

## Required Caveats

- This Minerva slice is knowledge only.
- No runtime changes were made.
- No live LLM calls were made.
- No DB access, reads, writes, migrations, or validation were performed.
- No workforce-platform changes were made.
- No endpoint, UI, chat, or runtime retrieval behaviour was changed by this slice.
- A preview endpoint or UI card is not evidence of processing execution.
- Operators cannot process now from the preview surface.
- Execution route should not be assumed; a later explicit execution gate would be required.

## No-Action Attestation

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
- No finalisation, payment, bank file, payment batch, retro execution, recovery execution, source-truth mutation, Admin Queue rebuild, broad automation, or parallel payroll processor: yes.

## Golden Questions And Expected Answer Themes

### 1. What is the Admitted Draft PayRun Bridge Operator Preview Surface?

Expected answer themes:
- A read-only visibility layer over the admitted draft processing bridge and guarded operator action contract.
- Shows eligibility, authority, targets, guardrails, blockers, processing entrypoint, readiness consequence, next safe steps, and actions not taken.
- Does not execute processing.

Prohibited claims:
- Do not say the preview surface processes payroll, mutates PayRuns, or gives operators a Process Now button.

Required caveats:
- Preview is not execution and visibility is not mutation.

### 2. Why is the Operator Preview Surface needed after the bridge operator action contract?

Expected answer themes:
- The bridge service foundation, dry-run preview support, and guarded operator-action contract exist.
- Operators still need Pay Process surface visibility into eligibility and blockers.
- The slice adds read visibility before execution authority.

Prohibited claims:
- Do not say the operator action contract already exposes live UI processing.

Required caveats:
- The need is visibility, not execution.

### 3. What does preview mean in this context?

Expected answer themes:
- Preview means dry-run/read-only inspection.
- It shows what would be targeted and why if a later execution gate existed.
- It returns evidence and actions not taken.

Prohibited claims:
- Do not describe preview as a mutation command.

Required caveats:
- Preview does not call processing or route execution.

### 4. Why is preview not execution?

Expected answer themes:
- It does not call processing.
- It does not create PayRuns or PayRunContacts.
- It does not finalise, pay, generate bank files, generate payment batches, automate payroll, or mutate source truth.

Prohibited claims:
- Do not say dry-run preview performs processing.

Required caveats:
- Dry-run endpoint is not a processing route.

### 5. What should the operator see in the preview card?

Expected answer themes:
- Eligibility, blockers, authority, admission evidence, target PayRun, target PayRunContact, guardrails, deterministic processing entrypoint, readiness consequence, next safe steps, non-goals, prohibited actions, and actions not taken.

Prohibited claims:
- Do not say the card should include a Process Now button.

Required caveats:
- The card is read-only.

### 6. What should the guarded preview endpoint return?

Expected answer themes:
- A read-only preview packet with eligibility, blockers, authority evidence, target references, guardrails, proposed deterministic processing entrypoint, readiness consequence, prohibited actions, next safe steps, and actions not taken.

Prohibited claims:
- Do not say the endpoint returns live processing results from a mutation.

Required caveats:
- Endpoint is dry-run/read-only by default.

### 7. Why must the endpoint be dry-run/read-only by default?

Expected answer themes:
- It prevents accidental payroll mutation.
- It preserves the boundary between visibility and execution.
- It ensures no PayRun or PayRunContact creation, no processing call, no finalisation, no payment, no bank file, no payment batch, and no source-truth mutation.

Prohibited claims:
- Do not say dry-run mode is optional for this preview endpoint.

Required caveats:
- A guarded preview endpoint is not a processing endpoint.

### 8. Why should there be no Process Now button yet?

Expected answer themes:
- Live execution needs a separate explicit execution gate.
- That gate needs permissions, audit, idempotency runtime, readiness refresh, and failure-handling design.
- This slice is only read visibility.

Prohibited claims:
- Do not say operators can execute admitted draft processing from the UI.

Required caveats:
- No Process Now button yet.

### 9. What has already been implemented in Workforce Platform before this slice?

Expected answer themes:
- `dde4286` added bridge service foundation and dry-run preview support.
- `e8f4f06` added guarded operator-action contract.
- Current boundaries include no route, no UI mutation button, and no live processing by default.

Prohibited claims:
- Do not claim the preview UI integration is already proven by this knowledge slice.

Required caveats:
- Implementation evidence must be ingested before Minerva describes later runtime behaviour as live.

### 10. What is planned for the next Workforce slice?

Expected answer themes:
- Implementation closeout documentation.
- Guarded preview/read endpoint.
- Pay Process panel, Command Centre, and Admin Queue read integration where safe.
- Route tests, UI build/tests, and no-mutation assertions.

Prohibited claims:
- Do not include execution route or Process Now button as part of this planned slice.

Required caveats:
- Planned slice remains read-only preview.

### 11. What must this slice not implement?

Expected answer themes:
- No live processing execution, Process Now button, PayRun creation, PayRunContact creation, finalisation, payment, bank file, payment batch, broad automation, Minerva decisioning, Minerva payroll calculation, retro execution, recovery execution, source-truth mutation, Admin Queue rebuild, or parallel payroll processor.

Prohibited claims:
- Do not narrow the non-goals to only finalisation and payment.

Required caveats:
- The strict boundaries protect deterministic payroll authority and source truth.

### 12. How should Minerva explain this slice without overstating runtime behaviour?

Expected answer themes:
- Explain it as planned or evidenced read-only preview visibility depending on available implementation evidence.
- Preserve preview is not execution, visibility is not mutation, and dry-run endpoint is not a processing route.
- Say operators cannot process now from the preview surface.

Prohibited claims:
- Do not say the bridge is live for execution merely because preview exists.

Required caveats:
- Runtime claims require implementation evidence and tests.

### 13. What runtime-overstatement risks should Minerva avoid?

Expected answer themes:
- Avoid saying the bridge is live for execution, operators can process now, the UI card performs processing, preview creates payroll artefacts, eligibility is execution authorisation, or Minerva calculates payroll.

Prohibited claims:
- Do not claim deterministic processing authority moved to Minerva.

Required caveats:
- Preview visibility is read-only evidence, not execution.

### 14. How does this slice preserve deterministic payroll authority?

Expected answer themes:
- It exposes the deterministic processing entrypoint that would be used later.
- It does not calculate payroll in Minerva.
- It does not create a parallel payroll processor.

Prohibited claims:
- Do not say Minerva calculates payroll outcomes.

Required caveats:
- Deterministic Workforce Platform services remain payroll authority.

### 15. What evidence/story should be exposed by the preview surface?

Expected answer themes:
- Authority, target PayRun, target PayRunContact, guardrails, processing entrypoint, blockers, readiness consequence, non-goals, prohibited actions, and actions not taken.

Prohibited claims:
- Do not omit actions not taken.

Required caveats:
- Evidence/story explains what would be targeted and what preview did not do.

### 16. What is the next valid slice after preview visibility?

Expected answer themes:
- A later explicit execution decision gate may be designed.
- It must be separate from preview visibility.
- Execution route should not be assumed from a preview endpoint or UI card.

Prohibited claims:
- Do not say the next slice is automatically live execution.

Required caveats:
- Execution needs explicit authority, permission, audit, idempotency, readiness refresh, and failure-handling design.
