# Workforce Ask Minerva Panel Integration v0.1

This knowledge note describes the first controlled design for integrating an Ask Minerva panel into Workforce Platform. It is retrieval guidance only. It does not implement Workforce UI, expose chat, fetch runtime evidence, call a live LLM, connect to a database, persist chat, calculate payroll, or perform write actions.

## What The Panel Is For

The Ask Minerva panel is for role-safe explanatory help inside Workforce surfaces. In v0.1 it should explain review context, implementation support, caveats, and next review steps. It must not become a payroll execution, authorisation, calculation, payment, finalisation, or source-truth mutation surface.

## Why Admin Queue Is First

The first recommended surface is PayRun Admin Queue. Admin Queue is the focused operator workbench for concrete review/action items. Operators already need to understand why an item is present, what a post-finalisation ObjectTime action means, why a finalised PayRun remains protected, whether treatment is only review/decision persistence, and what remains deferred.

PayRun Command Centre, PayRun Detail / Pay Process, Worker Story modal, Movement Review, dynamic Award Configurator treatment UI, and Analytics panels should come later.

## What Minerva Can Answer In V0.1

With fixture/static evidence, Minerva can explain:

- what a post-finalisation ObjectTime action means;
- why finalised PayRuns and PayRunContacts are protected;
- the difference between treatment decision and treatment execution;
- why supplementary may be recommended when backend evidence supports it;
- whether fixture/static evidence says anything has been paid or finalised;
- which Worker Story context is being discussed at a doctrine level;
- what finalised/protected means;
- what remains deferred;
- why runtime evidence is needed for object-specific pay questions.

## What Minerva Cannot Answer Without Runtime Evidence

Minerva cannot prove why a specific worker was paid a specific amount, why a specific worker received overtime, whether a tenant has a feature enabled, whether a particular PayRun object was available in production, or whether a specific live object was paid/finalised unless Workforce supplies authorised runtime object evidence in a later slice.

Code evidence and fixture evidence cannot prove live customer state, production deployment, runtime object state, payroll correctness, payment, or finalisation.

## Fixture-Key Mode

Fixture-key mode is for internal demo and UI wiring. Relevant fixture keys include `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`, `POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY`, `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`, `RUNTIME_OBJECT_EVIDENCE_REQUIRED`, and `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`.

Fixture evidence is synthetic/internal. It must not be treated as production, tenant, customer, runtime, payroll, payment, or finalisation evidence.

## Role-Safe Disclosure

Developer users may receive technical details where explicitly enabled. Payroll administrators and payroll managers receive implementation/operational confirmation with caveats. Payroll users receive operational guidance only. Customer administrators receive customer-safe implementation confirmation with runtime/tenant caveats. Worker-facing code evidence is not exposed, and `WORKER` is not supported in the Admin Queue panel v0.1.

## Runtime Evidence Gap

The runtime evidence gap is the difference between static evidence and object-specific truth. Future Workforce packets may include PayRunId, PayRunContactId, ProcessPeriodId, worker/contact labels, Admin Queue item metadata, Worker Story excerpts, Pay Process status, calculation story chapters, and an allowed evidence scope.

In v0.1, Minerva does not fetch runtime object evidence. Workforce must supply safe evidence in a later slice before Minerva can answer object-specific pay questions.

## Why Minerva Cannot Execute Payroll Actions

Minerva is advisory and explanatory in this panel. It cannot execute treatment decisions, calculate payroll, authorise payroll, mutate ObjectTime/source truth, create PayRuns or PayRunContacts, pay workers, finalise PayRuns, create payment batches, create bank files, or perform write actions.

Payroll execution remains Workforce-controlled and must remain governed by backend authority and payroll services, not Minerva chat output.

## PanelResponse Consumption

Workforce should render `PanelResponse` as the primary display contract. The panel should consume `Headline`, `Summary`, `DraftText`, `EvidenceChips`, `CaveatBanners`, `BoundaryBanners`, `RoleRestrictionNotice`, `RuntimeEvidenceNotice`, `SuggestedNextStep`, `TechnicalDetails` only where allowed, and `NoActionAttestation`.

The Workforce panel should not parse the whole orchestrator envelope as the primary UI. The envelope, evidence support packet, diagnostics, and audit details are internal/debug material.

## Retrieval Keywords

- Workforce Ask Minerva panel
- PayRun Admin Queue first surface
- Ask Minerva Admin Queue
- PanelResponse consumption
- fixture-key demo mode
- synthetic internal fixture evidence
- role-safe code evidence
- runtime object evidence gap
- Minerva cannot execute payroll actions
- Minerva cannot calculate payroll
- post-finalisation ObjectTime explanation
- treatment decision versus execution
- finalised PayRun protected
- Worker Story context
