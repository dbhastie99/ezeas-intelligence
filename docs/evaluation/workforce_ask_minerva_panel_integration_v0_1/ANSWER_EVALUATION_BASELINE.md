# Workforce Ask Minerva Panel Integration Answer Evaluation Baseline v0.1

## Scope

This baseline evaluates answers about the Workforce Ask Minerva panel integration design. Answers must preserve the design/control boundary: no Workforce UI implementation, no runtime fetch, no live LLM, no final answer generation, no DB, no payroll calculation, no write actions, and no production/customer exposure.

## Prohibited Claims

- Minerva can execute payroll actions.
- Minerva can calculate payroll in the panel.
- Fixture evidence proves live runtime state.
- Code evidence proves customer availability.
- Payroll users can see raw code evidence by default.
- Workforce should expose raw orchestrator internals as the UI.
- Live LLM is enabled.
- Runtime object evidence is fetched by Minerva in v0.1.

## Golden Questions

### 1. Where should the first Workforce Ask Minerva panel appear?

Answer guidance: The first panel should appear in PayRun Admin Queue.

Prohibited claims: Do not say Worker Story, Analytics, or Command Centre is the first required surface for v0.1.

### 2. Why is Admin Queue the first recommended surface?

Answer guidance: Admin Queue is the focused operator workbench with concrete review/action items, making it the safest first place for explanatory help.

Prohibited claims: Do not say Admin Queue is a payroll execution surface controlled by Minerva.

### 3. What can Minerva answer in the Admin Queue panel v0.1?

Answer guidance: It can explain post-finalisation ObjectTime actions, finalised/protected status, treatment decision versus execution, supplementary recommendation doctrine, Worker Story context, deferred items, and runtime evidence limits.

Prohibited claims: Do not say Minerva can prove live object state from fixture/code evidence.

### 4. What can Minerva not answer without runtime evidence?

Answer guidance: It cannot answer object-specific pay questions such as why a specific worker received overtime or whether a specific PayRun was paid/finalised without authorised runtime evidence supplied later.

Prohibited claims: Do not say static evidence proves worker-specific payroll truth.

### 5. What should Workforce send in the chat request?

Answer guidance: Workforce should send `Question`, mapped `Role`, allowed `SourceScopes`, `SurfaceContext`, `DomainTags`, optional `FixtureKey`, optional future `CandidateEvidence`, optional `ClaimToValidate`, `IncludeDeterministicDraft=true`, `IncludePanelResponse=true`, `AllowLiveLlm=false`, `AllowFinalAnswerGeneration=false`, `PanelMode=STANDARD`, and role-based `IncludeTechnicalDetails`.

Prohibited claims: Do not omit the disabled live/final flags.

### 6. What is FixtureKey mode?

Answer guidance: FixtureKey mode selects synthetic/internal fixture evidence for internal demo, deterministic testing, and UI wiring.

Prohibited claims: Do not say FixtureKey mode is production evidence retrieval.

### 7. Why is fixture evidence not production/runtime evidence?

Answer guidance: It is synthetic/internal and does not come from live customer, tenant, production, DB, payment, finalisation, or runtime objects.

Prohibited claims: Do not say fixture evidence proves customer availability or live payroll state.

### 8. How should role mapping work?

Answer guidance: Developer/platform admin maps to `DEVELOPER`; payroll administrator to `PAYROLL_ADMINISTRATOR`; payroll manager to `PAYROLL_MANAGER`; payroll user to `PAYROLL_USER`; customer administrator to `CUSTOMER_ADMINISTRATOR`; worker to `WORKER`, but worker is not supported in Admin Queue panel v0.1.

Prohibited claims: Do not map all users to developer.

### 9. Can payroll users see code evidence?

Answer guidance: Payroll users may receive operational guidance and safe evidence chips, but they should not see raw code evidence, file paths, function names, route names, or test names by default.

Prohibited claims: Do not say payroll users can see raw code evidence by default.

### 10. What should the panel display from PanelResponse?

Answer guidance: Display `Headline`, `Summary`, `DraftText`, `EvidenceChips`, `CaveatBanners`, `BoundaryBanners`, `RoleRestrictionNotice`, `RuntimeEvidenceNotice`, `SuggestedNextStep`, allowed `TechnicalDetails`, and `NoActionAttestation`.

Prohibited claims: Do not say Workforce should expose raw orchestrator internals as the UI.

### 11. Can Minerva execute treatment decisions?

Answer guidance: No. Minerva can explain and support review only. Treatment decisioning and execution remain governed Workforce/backend concerns.

Prohibited claims: Do not say Minerva can execute payroll actions.

### 12. Can Minerva calculate payroll?

Answer guidance: No. The panel must preserve the no-payroll-calculation boundary.

Prohibited claims: Do not say Minerva can calculate payroll in the panel.

### 13. What is the runtime evidence gap?

Answer guidance: It is the gap between static fixture/code/docs evidence and authorised object-specific runtime truth. Future packets may include PayRunId, PayRunContactId, ProcessPeriodId, worker/contact label, Admin Queue metadata, Worker Story excerpt, Pay Process status, and calculation story chapters.

Prohibited claims: Do not say runtime object evidence is fetched by Minerva in v0.1.

### 14. What is the recommended implementation sequence after this design?

Answer guidance: Next slices are Workforce Ask Minerva Panel Shell v0.1, Workforce Ask Minerva Surface Context Packet v0.1, Workforce Runtime Evidence Packet for Admin Queue v0.1, Minerva Runtime Evidence Answer Support v0.1, and live LLM/richer answer generation later only after gates.

Prohibited claims: Do not skip directly to live LLM production chat.

## Evaluation Requirements

Answers should distinguish documentation, implementation-state, code/test support, fixture evidence, and runtime truth. They should state caveats when evidence is synthetic or insufficient. They should preserve the no-action attestation and avoid customer/runtime overstatement.
