# Minerva Knowledge Capture — Admitted Draft PayRun Bridge Operator Preview Surface

## Purpose of this knowledge capture

This knowledge capture preserves the doctrine for the planned Workforce Platform slice:

**Admitted Draft PayRun Bridge Operator Preview Surface v0.1**

The slice is planned as a read-only operator visibility layer over the already committed admitted draft PayRun processing bridge foundations. It exists so Minerva can later explain what the planned preview surface is intended to do, and more importantly what it must not imply. This is knowledge and evaluation capture only. It does not modify workforce-platform, connect to a database, call a live LLM, expose chat, change runtime retrieval behaviour, or mutate operational corpus/runtime state.

## 1. What the Operator Preview Surface is

The Operator Preview Surface is a read-only visibility surface over the admitted draft processing bridge and its guarded operator action contract.

It lets an operator inspect whether an admitted pay-process action is eligible for deterministic draft processing, what target PayRun and PayRunContact would be used, what authority supports the action, what guardrails passed or blocked, what deterministic processing entrypoint would be used, what readiness consequence exists, what actions remain prohibited, and what next safe operator steps are available.

It is not an execution surface. Preview visible in the UI is not execution. A bridge eligibility card is not a Process Now button. A next-action suggestion is not a mutation command.

## 2. Why this slice is needed now

Workforce Platform already has the bridge service foundation and guarded operator action contract. Those foundations preserve dry-run preview support and operator-action boundaries, but operators cannot yet see bridge eligibility in Pay Process surfaces.

The next useful step is visibility. Operators need a way to understand whether an admitted action has a safe draft-processing path, why it is eligible or blocked, and what evidence supports that conclusion, without granting processing execution from the UI.

This slice is therefore needed after the operator action contract but before any execution gate. It closes the visibility gap while preserving the separation between read-only preview and live processing.

## 3. Current implementation state before this slice

Workforce Platform has already committed the first two implementation slices:

- `dde4286 add admitted draft payrun processing bridge service`
- `e8f4f06 add admitted draft payrun bridge operator action contract`

The current state to preserve is:

- bridge service foundation exists;
- dry-run preview support exists;
- guarded operator-action contract exists;
- no route exists for live processing;
- no operator UI mutation button exists;
- no live processing occurs by default;
- no Process Now button exists;
- no payroll finalisation, payment, bank-file, or payment-batch behaviour is enabled by the bridge.

The preview surface must describe and expose this state without overstating it.

## 4. Planned Workforce slice

The planned Workforce Platform slice should combine:

- implementation closeout documentation;
- guarded preview/read endpoint;
- Pay Process operator surface read integration;
- Pay Process panel visibility where safe;
- Command Centre bridge eligibility visibility where safe;
- Admin Queue bridge preview visibility where safe;
- route tests for read-only/dry-run behaviour;
- UI build/tests where a UI card is added;
- no-mutation tests proving preview does not execute processing or mutate payroll state.

The slice should remain a preview/read slice. It may expose eligibility, blockers, authority, target, guardrails, processing entrypoint, readiness consequence, next safe steps, non-goals, and actions not taken. It must not execute processing.

## 5. The core doctrine

The doctrine is fixed:

- preview is not execution;
- visibility is not mutation;
- eligibility is not authorisation to process;
- next-action suggestion is not a command;
- dry-run endpoint is not a processing route;
- operator UI card is not a Process Now button.

These statements should appear in Minerva answers whenever the preview surface is discussed. The surface may help an operator understand the controlled bridge, but it must not collapse visibility into execution authority.

## 6. What the operator should see

The operator should see a preview packet or card that explains:

- eligibility for admitted draft processing;
- blockers that prevent safe draft processing;
- authority, including PayRunActionDecision or policy-backed admission evidence;
- admission evidence and source/action context;
- target PayRun that would be used if processing were later authorised;
- target PayRunContact that would be used if processing were later authorised;
- guardrails that passed, failed, or blocked;
- deterministic processing entrypoint that would be used;
- readiness consequence for review/control visibility;
- next safe operator steps;
- non-goals and actions that remain out of scope;
- actions not taken by preview.

Actions not taken should be explicit. Preview should say when it did not create a PayRun, did not create a PayRunContact, did not call processing, did not finalise, did not pay, did not generate a bank file, did not generate a payment batch, and did not mutate source truth.

## 7. Guarded endpoint doctrine

Any endpoint added by the planned Workforce slice must be read-only and dry-run by default.

The endpoint may return a preview packet, bridge eligibility state, authority evidence, target references, guardrail results, blockers, proposed deterministic processing entrypoint, readiness consequence, prohibited actions, and safe next steps. It must not call processing. It must not execute a processing route. It must not create, update, finalise, pay, freeze, or regenerate payroll state.

A guarded/dry-run endpoint is not a processing endpoint. Route naming, response shape, tests, and UI copy should make that boundary clear.

## 8. Pay Process surface integration doctrine

The preview card should appear as read-only visibility in Pay Process operator contexts, such as the Pay Process panel, Command Centre, or Admin Queue where safe.

The card should show bridge eligibility, blocker state, authority, target PayRun/PayRunContact, guardrail status, processing entrypoint, readiness consequence, next safe steps, non-goals, and actions not taken. It should not expose chat. It should not include a Process Now button. It should not mutate Admin Queue state or rebuild Admin Queue data.

In Command Centre or Admin Queue contexts, the preview should behave as bridge eligibility and evidence visibility only. It must not become an Admin Queue rebuild, a parallel payroll processor, or a broad automation control surface.

## 9. Why no Process Now button yet

There should be no Process Now button in this slice because live execution needs a separate explicit execution gate.

That later gate would need a permission model, audit model, idempotency runtime, readiness refresh model, failure-handling model, source/target locking or conflict strategy, and clear financial-control boundaries. It would also need explicit tests proving that execution is authorised, deterministic, idempotent, and blocked at finalisation/payment/bank-file boundaries.

The preview slice is deliberately earlier and safer. It answers what would be targeted and why, not whether the operator may execute processing now.

## 10. What this slice may implement

This planned Workforce slice may implement:

- implementation closeout doc;
- guarded preview/read endpoint;
- route tests;
- Pay Process preview UI card;
- Admin Queue/Command Centre read integration where safe;
- UI build/tests;
- no-mutation assertions.

These permissions do not authorise execution. They authorise visibility, dry-run response contracts, and tests proving the preview surface remains read-only.

## 11. What this slice must not implement

This planned Workforce slice must not implement:

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

It must also not imply that preview creates payroll artefacts, finalises payroll, pays workers, generates bank files, or moves deterministic payroll authority to Minerva.

## 12. Minerva answer guidance

Before implementation, Minerva should describe the Operator Preview Surface as a planned read-only visibility slice. It should say Workforce Platform already has the bridge service foundation, dry-run preview support, and guarded operator-action contract, but the larger preview surface endpoint/UI integration is planned, not yet proven live by this knowledge capture.

After implementation, Minerva may describe the preview surface only to the extent supported by ingested implementation evidence and tests. It should still preserve the doctrine that preview is not execution, visibility is not mutation, and a dry-run/read endpoint is not a processing route.

Minerva should not claim operators can process now unless a later explicit execution gate is designed, implemented, tested, and ingested as evidence. Minerva should not calculate payroll or decide payroll authority.

## 13. Runtime-overstatement risks

The main runtime-overstatement risk is saying "the bridge is live" or "operators can process now" merely because preview visibility exists.

Other risks include claiming that the UI card performs processing, that the guarded endpoint creates PayRuns or PayRunContacts, that next safe steps are commands, that eligibility is execution authorisation, that Minerva calculates payroll, or that deterministic processing authority moved into Minerva.

Minerva answers must distinguish implemented read visibility from execution. If evidence only proves preview, Minerva should say preview is visible and read-only, not that processing is available from the UI.

## 14. Evidence/story expectations

Preview packets should expose a clear evidence story:

- authority;
- target PayRun;
- target PayRunContact;
- guardrails;
- deterministic processing entrypoint;
- blockers;
- readiness consequence;
- non-goals;
- actions not taken.

The evidence/story should let an operator understand why the action is eligible or blocked, what would be targeted if a later execution gate existed, and what preview did not do.

## 15. Next valid slice after preview surface

After preview visibility, a later explicit execution decision gate may be designed. That later slice should be separate and should not be assumed from this preview surface.

An execution route would require explicit authority, permission, audit, idempotency, readiness refresh, and failure-handling design. The existence of a preview endpoint or UI card does not create that execution route.

## 16. Suggested Minerva golden questions

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

## 17. Answer guidance for golden questions

### 1. What is the Admitted Draft PayRun Bridge Operator Preview Surface?

Answer guidance: It is a read-only visibility layer over the admitted draft processing bridge and guarded operator action contract. It lets operators inspect eligibility, authority, targets, guardrails, blockers, processing entrypoint, readiness consequence, next safe steps, and actions not taken without executing processing.

### 2. Why is the Operator Preview Surface needed after the bridge operator action contract?

Answer guidance: Workforce has service foundation, dry-run preview support, and a guarded operator action contract, but operators cannot yet see bridge eligibility in Pay Process surfaces. The preview surface closes that visibility gap while preserving the no-execution boundary.

### 3. What does preview mean in this context?

Answer guidance: Preview means a dry-run/read-only view of what would be targeted and why if a later execution gate existed. It returns evidence, eligibility, blockers, target references, guardrails, entrypoint, readiness consequence, and safe next steps without mutation.

### 4. Why is preview not execution?

Answer guidance: Preview does not call processing, create PayRuns, create PayRunContacts, finalise, pay, generate bank files, generate payment batches, or mutate source truth. It is visibility only.

### 5. What should the operator see in the preview card?

Answer guidance: The card should show eligibility, blockers, authority, admission evidence, target PayRun, target PayRunContact, guardrails, deterministic processing entrypoint, readiness consequence, next safe steps, non-goals, and actions not taken.

### 6. What should the guarded preview endpoint return?

Answer guidance: It should return a read-only preview packet containing eligibility, blockers, authority evidence, target PayRun/PayRunContact references, guardrail results, proposed deterministic processing entrypoint, readiness consequence, prohibited actions, next safe steps, and actions not taken.

### 7. Why must the endpoint be dry-run/read-only by default?

Answer guidance: The endpoint exists to expose safe visibility before execution authority exists. Dry-run/read-only default behaviour prevents accidental payroll mutation, route execution, PayRun or PayRunContact creation, finalisation, payment, bank-file generation, payment-batch generation, and source-truth mutation.

### 8. Why should there be no Process Now button yet?

Answer guidance: Live execution requires a separate explicit execution gate with permissions, audit, idempotency runtime, readiness refresh, and failure-handling design. The preview slice only explains what would be targeted and why.

### 9. What has already been implemented in Workforce Platform before this slice?

Answer guidance: The committed state includes `dde4286` bridge service foundation and dry-run preview support, plus `e8f4f06` guarded operator-action contract. There is no route, no UI mutation button, and no live processing by default.

### 10. What is planned for the next Workforce slice?

Answer guidance: The next slice should add implementation closeout docs, a guarded preview/read endpoint, Pay Process operator surface read integration, Command Centre/Admin Queue read visibility where safe, UI build/tests, route tests, and no-mutation assertions.

### 11. What must this slice not implement?

Answer guidance: It must not implement live processing execution, Process Now button, PayRun creation, PayRunContact creation, finalisation, payment, bank file, payment batch, broad automation, Minerva decisioning, Minerva payroll calculation, retro execution, recovery execution, source-truth mutation, Admin Queue rebuild, or a parallel payroll processor.

### 12. How should Minerva explain this slice without overstating runtime behaviour?

Answer guidance: Minerva should call it a planned or evidenced read-only preview surface, depending on implementation evidence. It should state preview is not execution, visibility is not mutation, dry-run endpoint is not a processing route, and operators cannot process now from the preview surface.

### 13. What runtime-overstatement risks should Minerva avoid?

Answer guidance: Minerva must avoid saying the bridge is live for execution, operators can process now, the UI card performs processing, preview creates payroll artefacts, eligibility is execution authorisation, or Minerva calculates payroll.

### 14. How does this slice preserve deterministic payroll authority?

Answer guidance: It exposes the deterministic processing entrypoint that would be used later while refusing to calculate payroll in Minerva or create a parallel processor. Payroll authority remains with deterministic Workforce Platform services.

### 15. What evidence/story should be exposed by the preview surface?

Answer guidance: The preview should expose authority, target PayRun, target PayRunContact, guardrails, processing entrypoint, blockers, readiness consequence, non-goals, and actions not taken.

### 16. What is the next valid slice after preview visibility?

Answer guidance: A later explicit execution decision gate may be designed after preview visibility. It must be a separate slice and should not be assumed from the presence of a preview endpoint or UI card.

## 18. Prohibited claims

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

## 19. Source links

- [admitted_draft_payrun_processing_bridge_v0_1_source_response.md](admitted_draft_payrun_processing_bridge_v0_1_source_response.md)
- [admitted_draft_payrun_processing_bridge_v0_1.md](admitted_draft_payrun_processing_bridge_v0_1.md)
- [ANSWER_EVALUATION_BASELINE.md](../../evaluation/admitted_draft_payrun_processing_bridge_v0_1/ANSWER_EVALUATION_BASELINE.md)
