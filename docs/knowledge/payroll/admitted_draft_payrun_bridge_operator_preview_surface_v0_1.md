# Admitted Draft PayRun Bridge Operator Preview Surface v0.1

Status: v0.1 structured Minerva knowledge pack.

Source-response authority: [admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md](admitted_draft_payrun_bridge_operator_preview_surface_v0_1_source_response.md).

Prior bridge knowledge links:

- [admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md)
- [admitted_draft_payrun_processing_bridge_v0_1.md](admitted_draft_payrun_processing_bridge_v0_1.md)
- [ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md)

This is knowledge-only documentation. It does not implement runtime retrieval changes, database behaviour, live LLM behaviour, endpoint exposure, UI mutation, chat exposure, operational corpus mutation, or workforce-platform changes.

## Domain And Scope

The Operator Preview Surface is a read-only visibility layer over the admitted draft PayRun processing bridge and guarded operator action contract. It belongs to the Pay Process / Command Centre / Admin Queue visibility boundary and exists so operators can inspect eligibility and evidence without executing processing.

The preview surface may show what PayRun and PayRunContact would be targeted if a later execution gate existed. It must not create or mutate those targets.

## Core Doctrine

- Preview is not execution.
- Visibility is not mutation.
- Eligibility is not authorisation to process.
- Next-action suggestion is not a command.
- Dry-run endpoint is not a processing route.
- Operator UI card is not a Process Now button.

The endpoint is dry-run/read-only by default. The preview must not call processing, must not execute a route that mutates payroll state, and must not act as a processing endpoint.

## Current Workforce Implementation State

Before this planned slice, Workforce Platform has:

- `dde4286 add admitted draft payrun processing bridge service`;
- bridge service foundation;
- dry-run preview support;
- `e8f4f06 add admitted draft payrun bridge operator action contract`;
- guarded operator-action contract;
- no route;
- no UI mutation button;
- no live processing by default.

This structured pack preserves those boundaries for Minerva answer behaviour.

## Planned Workforce Slice

The planned Workforce slice should combine:

- implementation closeout documentation;
- guarded preview/read endpoint;
- route tests;
- Pay Process preview UI card;
- Pay Process panel read integration;
- Command Centre bridge eligibility visibility;
- Admin Queue bridge preview visibility where safe;
- UI build/tests;
- no-mutation assertions.

The slice should prove read visibility and dry-run behaviour. It should not prove or imply execution.

## Preview Packet Expectations

The preview packet or UI card should expose:

- eligibility;
- blockers;
- authority;
- admission evidence;
- target PayRun;
- target PayRunContact;
- guardrails;
- deterministic processing entrypoint;
- readiness consequence;
- next safe operator steps;
- non-goals;
- prohibited actions;
- actions not taken.

Actions not taken should include no processing call, no route execution, no PayRun creation, no PayRunContact creation, no finalisation, no payment, no bank file, no payment batch, no automation, no source-truth mutation, and no deterministic payroll authority transfer to Minerva.

## Guarded Endpoint Model

Any preview endpoint must be dry-run/read-only by default. It may return eligibility, blockers, authority evidence, target references, guardrails, proposed deterministic processing entrypoint, readiness consequence, safe next steps, prohibited actions, and actions not taken.

It must not call processing. It must not create PayRuns or PayRunContacts. It must not finalise, pay, generate a bank file, generate a payment batch, mutate source truth, rebuild Admin Queue, or start broad automation.

## Pay Process Surface Model

The Pay Process panel, Command Centre, or Admin Queue may show a bridge eligibility card when safe. The card should be read-only and should support operator understanding of the bridge state.

The card must not include a Process Now button. It must not expose chat. It must not mutate Admin Queue state. It must not become a parallel payroll processor or execution control.

## Why Execution Is Later

Live processing requires a separate explicit execution gate. That later gate would need permission controls, audit controls, idempotency runtime, readiness refresh, failure-handling design, and finalisation/payment/bank-file guardrails.

The preview surface does not implement that gate. Execution route should not be assumed from preview visibility.

## Strict Non-Goals

This slice must not implement:

- live processing execution;
- Process Now button;
- PayRun creation;
- PayRunContact creation;
- finalisation;
- payment;
- bank file;
- payment batch;
- broad automation;
- Minerva decisioning;
- Minerva payroll calculation;
- retro execution;
- recovery execution;
- source-truth mutation;
- Admin Queue rebuild;
- parallel payroll processor.

## Minerva Answer Boundaries

Minerva should answer that this is a planned or evidenced read-only preview surface, depending on available implementation evidence. It should not say operators can process now unless a later explicit execution gate has been designed, implemented, tested, and ingested as evidence.

Minerva may explain authority, target, guardrails, blockers, readiness consequence, non-goals, and actions not taken. Minerva must not calculate payroll, decide payroll authority, call processing, or imply deterministic payroll authority moved to Minerva.

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

## No-Action Attestation

- No runtime changes: yes.
- No live LLM calls: yes.
- No DB access, reads, writes, migrations, or validation: yes.
- No workforce-platform changes: yes.
- No endpoint or UI changes in this Minerva slice: yes.
- No retrieval-plan/runtime behaviour changes: yes.
- No chat exposure: yes.
- No operational corpus/runtime state mutation: yes.
- No payroll calculation logic: yes.
- No Minerva payroll decisioning: yes.

## Golden Questions And Answer Guidance

### 1. What is the Admitted Draft PayRun Bridge Operator Preview Surface?

Answer guidance: It is a read-only visibility layer over the admitted draft processing bridge and guarded operator action contract. It shows eligibility, evidence, targets, guardrails, blockers, readiness consequence, next safe steps, and actions not taken without executing processing.

### 2. Why is the Operator Preview Surface needed after the bridge operator action contract?

Answer guidance: The bridge service foundation and guarded operator action contract exist, but operators cannot yet see bridge eligibility in Pay Process surfaces. The preview surface adds visibility without execution.

### 3. What does preview mean in this context?

Answer guidance: Preview means dry-run/read-only inspection of what would be targeted and why if a later execution gate existed. It is not mutation and does not call processing.

### 4. Why is preview not execution?

Answer guidance: Preview does not call processing, execute a route, create PayRuns, create PayRunContacts, finalise, pay, generate bank files, generate payment batches, automate payroll, or mutate source truth.

### 5. What should the operator see in the preview card?

Answer guidance: The operator should see eligibility, blockers, authority, admission evidence, target PayRun, target PayRunContact, guardrails, deterministic processing entrypoint, readiness consequence, next safe steps, non-goals, prohibited actions, and actions not taken.

### 6. What should the guarded preview endpoint return?

Answer guidance: It should return a read-only preview packet with eligibility, blockers, authority evidence, target references, guardrails, proposed deterministic entrypoint, readiness consequence, prohibited actions, next safe steps, and actions not taken.

### 7. Why must the endpoint be dry-run/read-only by default?

Answer guidance: Dry-run/read-only default behaviour prevents accidental payroll mutation and preserves the boundary that endpoint visibility is not processing execution.

### 8. Why should there be no Process Now button yet?

Answer guidance: Execution requires a later explicit gate with permissions, audit, idempotency, readiness refresh, and failure handling. This slice only provides preview visibility.

### 9. What has already been implemented in Workforce Platform before this slice?

Answer guidance: `dde4286` added the bridge service foundation and dry-run preview support. `e8f4f06` added the guarded operator-action contract. There is no route, no UI mutation button, and no live processing by default.

### 10. What is planned for the next Workforce slice?

Answer guidance: The next slice should add closeout docs, a guarded preview/read endpoint, Pay Process panel/Command Centre/Admin Queue read integration where safe, UI build/tests, route tests, and no-mutation assertions.

### 11. What must this slice not implement?

Answer guidance: It must not implement live processing execution, Process Now button, PayRun creation, PayRunContact creation, finalisation, payment, bank file, payment batch, broad automation, Minerva decisioning, Minerva payroll calculation, retro execution, recovery execution, source-truth mutation, Admin Queue rebuild, or a parallel payroll processor.

### 12. How should Minerva explain this slice without overstating runtime behaviour?

Answer guidance: Minerva should describe the slice as read-only preview visibility and should caveat implementation state based on available evidence. It must say preview is not execution, visibility is not mutation, and dry-run endpoint is not a processing route.

### 13. What runtime-overstatement risks should Minerva avoid?

Answer guidance: Avoid claiming that the bridge is live for execution, operators can process now, the UI card performs processing, preview creates payroll artefacts, eligibility is execution authority, or Minerva calculates payroll.

### 14. How does this slice preserve deterministic payroll authority?

Answer guidance: It exposes the deterministic processing entrypoint that would be used later but does not calculate payroll and does not create a parallel processor. Deterministic Workforce Platform services remain payroll authority.

### 15. What evidence/story should be exposed by the preview surface?

Answer guidance: It should expose authority, target PayRun, target PayRunContact, guardrails, processing entrypoint, blockers, readiness consequence, non-goals, prohibited actions, and actions not taken.

### 16. What is the next valid slice after preview visibility?

Answer guidance: A later explicit execution decision gate may be designed. It must be separate and cannot be assumed from a preview endpoint or UI card.

## Retrieval Keywords And Aliases

- admitted draft bridge preview
- operator preview surface
- guarded preview endpoint
- dry-run pay process endpoint
- Pay Process bridge preview
- Command Centre bridge eligibility
- Admin Queue bridge preview
- no Process Now button
- preview is not execution
- visibility is not mutation
- actions not taken
- deterministic payroll authority
- execution gate later
- bridge eligibility card
- read-only preview
- dry-run/read-only by default
- no route execution
- no processing call
- no PayRun creation
- no PayRunContact creation
- no finalisation/payment/bank file/automation
