# Workforce Ask Minerva Panel Integration Design v0.1

## 1. Purpose

This is a design/control slice before wiring an Ask Minerva panel into Workforce Platform. It defines the first Workforce surface, request and response contracts, role/source controls, fixture/demo behaviour, safety boundaries, and deferred runtime evidence work.

This slice does not implement Workforce UI, expose production chat, add runtime retrieval, connect to a database, call a live LLM, persist chat, calculate payroll, or perform write actions.

## 2. Current Minerva capability

The current internal chat stack provides:

- internal route: `POST /api/v1/internal/minerva/chat/stub`;
- API stub request fields for question, role, source scopes, surface context, domain tags, fixture key, candidate evidence, claim validation, deterministic draft, and panel response;
- fixture-key evidence support for deterministic internal/demo questions;
- deterministic draft support, explicitly non-final;
- panel response contract for UI-friendly display;
- role-safe disclosure over implementation, code, test, prompt, knowledge, and evaluation evidence;
- no live LLM;
- no database access;
- no runtime object evidence fetch;
- no final answer generation;
- no chat persistence;
- no write actions, payroll calculation, payment, banking, or finalisation action.

## 3. First Workforce surfaces

Recommended initial surface: **PayRun Admin Queue**.

Reason: Admin Queue is now the focused operator workbench. It contains concrete review/action items and is the clearest first location for role-safe explanatory help. It is where an operator naturally asks why an item exists, what a post-finalisation ObjectTime action means, whether a treatment decision is only review/persistence, and why finalised payroll records remain protected.

Secondary later surfaces:

- PayRun Command Centre;
- PayRun Detail / Pay Process panel;
- Worker Story modal;
- Movement Review;
- Award Configurator dynamic shift treatment rule UI, later;
- Analytics panels, later.

## 4. First panel use cases

The first safe Admin Queue panel questions should be explanatory and review-oriented:

- What does this post-finalisation ObjectTime action mean?
- Why can't the finalised PayRun be reprocessed?
- What is the difference between treatment decision and execution?
- Why is supplementary recommended?
- Has anything actually been paid or finalised?
- Which Worker Story am I looking at?
- What does finalised/protected mean?
- What remains deferred?
- Why does Minerva need runtime evidence to answer object-specific pay questions?

These use cases must not ask Minerva to authorise treatment, execute payroll, calculate payroll, pay a worker, mutate source truth, or confirm live customer state without supplied runtime evidence.

## 5. Request contract from Workforce

Workforce should call the internal stub only from an internal/demo integration path in v0.1. The request should use these fields:

- `Question`: operator question text.
- `Role`: Minerva role value after Workforce role mapping.
- `SourceScopes`: allowed static scopes for the panel, plus runtime evidence scope only when a later slice safely supplies evidence.
- `SurfaceContext`: surface metadata such as surface name, route/screen identity, selected queue item identity, and non-sensitive labels.
- `DomainTags`: payroll and surface tags such as `payrun`, `admin_queue`, `post_finalisation`, `objecttime`, `worker_story`, `treatment_review`.
- `FixtureKey`: optional, internal/demo v0.1 only.
- `CandidateEvidence`: optional, reserved for future Workforce-supplied runtime evidence packets.
- `ClaimToValidate`: optional claim text when the panel validates whether a proposed statement is supportable.
- `IncludeDeterministicDraft`: `true`.
- `IncludePanelResponse`: `true`.
- `AllowLiveLlm`: `false`.
- `AllowFinalAnswerGeneration`: `false`.
- `PanelMode`: `STANDARD` by default.
- `IncludeTechnicalDetails`: `true` only for `DEVELOPER`; `false` for payroll/customer/worker roles by default.

Example v0.1 internal/demo request:

```json
{
  "Question": "What does this post-finalisation ObjectTime action mean?",
  "Role": "PAYROLL_ADMINISTRATOR",
  "SourceScopes": [
    "PLATFORM_KNOWLEDGE",
    "IMPLEMENTATION_STATE",
    "CODE_EVIDENCE",
    "TEST_EVIDENCE",
    "PROMPT_ARTEFACTS",
    "EVALUATION_BASELINES"
  ],
  "SurfaceContext": {
    "Surface": "PAYRUN_ADMIN_QUEUE",
    "Panel": "ASK_MINERVA",
    "RuntimeEvidenceSupplied": false
  },
  "DomainTags": ["payrun", "admin_queue", "post_finalisation", "objecttime"],
  "FixtureKey": "POST_FINALISATION_OBJECTTIME_ACTION_SURFACED",
  "IncludeDeterministicDraft": true,
  "IncludePanelResponse": true,
  "AllowLiveLlm": false,
  "AllowFinalAnswerGeneration": false,
  "PanelMode": "STANDARD",
  "IncludeTechnicalDetails": false
}
```

## 6. Role mapping

Expected Workforce role mapping for v0.1:

| Workforce user category | Minerva role |
| --- | --- |
| Developer / platform admin | `DEVELOPER` |
| Payroll administrator | `PAYROLL_ADMINISTRATOR` |
| Payroll manager | `PAYROLL_MANAGER` |
| Payroll user | `PAYROLL_USER` |
| Customer administrator | `CUSTOMER_ADMINISTRATOR` |
| Worker | `WORKER` |

`WORKER` is a known role but is not supported in the Admin Queue panel v0.1.

Developer may see technical details when requested. Payroll administrator and payroll manager receive implementation/operational confirmation with caveats. Payroll user receives operational guidance only. Customer administrator receives customer-safe implementation confirmation with tenant/runtime caveats. Worker-facing code evidence is not exposed.

## 7. Source scopes for v0.1

Allowed for Workforce panel v0.1:

- `PLATFORM_KNOWLEDGE`;
- `IMPLEMENTATION_STATE`;
- `CODE_EVIDENCE`, role-filtered;
- `TEST_EVIDENCE`, role-filtered;
- `PROMPT_ARTEFACTS`, role-filtered;
- `EVALUATION_BASELINES`;
- `RUNTIME_OBJECT_EVIDENCE` only if supplied safely in a later slice; Minerva must not fetch it in v0.1.

Deferred:

- `ANALYTICS_EVIDENCE` live interpretation;
- live DB/object evidence fetch;
- live LLM;
- vector search / embeddings;
- chat persistence.

## 8. Fixture-key / demo mode

Fixture-key mode supports initial internal integration tests and UI wiring demos without runtime evidence. Suitable fixture keys include:

- `POST_FINALISATION_OBJECTTIME_ACTION_SURFACED`;
- `POST_FINALISATION_TREATMENT_WORKSPACE_REVIEW_ONLY`;
- `CODE_EVIDENCE_CANNOT_PROVE_RUNTIME`;
- `RUNTIME_OBJECT_EVIDENCE_REQUIRED`;
- `ADMITTED_DRAFT_MANUAL_PROCESSING_IMPLEMENTED`.

Fixture evidence is synthetic/internal. Fixture evidence must not be treated as live customer, tenant, production, runtime, payroll, payment, or finalisation evidence. Fixture mode is suitable for internal demo and UI wiring only.

## 9. Panel response consumption

Workforce should consume `PanelResponse` as the first-level panel display contract. The UI should not parse the entire orchestrator envelope directly for primary display.

Workforce should display or route these `PanelResponse` fields:

- `Headline`;
- `Summary`;
- `DraftText`;
- `EvidenceChips`;
- `CaveatBanners`;
- `BoundaryBanners`;
- `RoleRestrictionNotice`;
- `RuntimeEvidenceNotice`;
- `SuggestedNextStep`;
- `TechnicalDetails`, only where allowed;
- `NoActionAttestation`.

The orchestrator envelope, evidence support packet, diagnostics, and audit summary remain internal/debug material, not the primary panel rendering contract.

## 10. Safety and boundary requirements

The Workforce Ask Minerva panel v0.1 must preserve these boundaries:

- no live LLM;
- no final answer generation;
- no DB/runtime fetch;
- no payroll calculation;
- no write actions;
- no treatment decisioning by Minerva;
- no payment, finalisation, banking, bank file, or payment batch action;
- no source-truth mutation;
- no chat persistence;
- no production/customer exposure;
- no Minerva authorisation of payroll action.

Minerva can explain and support review only. It cannot authorise payroll action, execute treatment decisions, calculate payroll, pay workers, finalise PayRuns, mutate source truth, or prove live object state from fixture/code evidence.

## 11. Runtime evidence gap

Object-specific questions such as "why did this worker get overtime?" require runtime object evidence supplied by Workforce in a future slice. Static knowledge, implementation-state, code, test, prompt, and evaluation evidence can explain design and implementation support, but they cannot prove what happened for a specific worker, PayRun, tenant, or production object.

Future safe evidence may include:

- `PayRunId`;
- `PayRunContactId`;
- `ProcessPeriodId`;
- worker/contact label;
- Admin Queue item/action metadata;
- Worker Story excerpt;
- Pay Process status;
- calculation story chapters;
- allowed evidence scope.

In v0.1, Minerva does not fetch this evidence. Workforce must not imply that `RUNTIME_OBJECT_EVIDENCE` was fetched unless a later slice explicitly supplies an authorised packet and the response attests to that supplied evidence.

## 12. Recommended Workforce integration sequence

1. Workforce Ask Minerva Panel Shell v0.1
   - UI panel only.
   - Calls fixture-key API stub.
   - No runtime evidence.
   - No live LLM.

2. Workforce Ask Minerva Surface Context Packet v0.1
   - Pass Admin Queue/PayRun surface context.
   - Still no DB fetch by Minerva.

3. Workforce Runtime Evidence Packet for Admin Queue v0.1
   - Workforce constructs safe runtime evidence packet.
   - Minerva consumes supplied evidence only.

4. Minerva Runtime Evidence Answer Support v0.1
   - Minerva interprets supplied runtime evidence.

5. Live LLM / richer answer generation later, only after gates.

## 13. Minerva answer doctrine for Workforce panel

Minerva answers must be explanatory, not authoritative payroll execution. They must show caveats when evidence is synthetic, static, insufficient, or missing. They must distinguish documentation, implementation support, code/test support, prompt/evaluation support, and runtime truth.

Minerva must not overstate. Code evidence can support implementation confidence but cannot prove customer availability, production deployment, runtime object state, payroll correctness, payment, finalisation, or migration state. Fixture evidence can support deterministic demo scenarios but cannot prove live state.

## 14. Non-goals / no-action attestation

No runtime, DB, UI, Workforce, live LLM, payroll, write, external API, vector search, embedding, chat persistence, customer exposure, operational evidence ingestion, database migration, code execution, or external repo mutation changes were made by this design/control slice.

No Workforce Platform code was changed. No production/live chat exposure was added.
