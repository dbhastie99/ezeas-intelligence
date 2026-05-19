# Saved Codex Prompt - Minerva Contextual Explanation Contract / Object Story Integration Plan v0.1

Implement Minerva Slice 8 of 8 for the current controlled evidence-to-answer phase in `C:\Projects\ezeas-intelligence`.

Create a deterministic generic contextual explanation contract, not an Admin Queue-specific integration. CorrectionReview/Admin Queue and Leave Type field help are representative examples only.

Add `app/services/contextual_explanation_contract_service.py` with a `ContextualExplanationContractService` that accepts a `MinervaExplanationContext` dict and returns `ContextualExplanationContractReview`.

The input contract should cover:

- `SurfaceContext`: page id, route, component id, surface type, mode.
- `SubjectContext`: subject type, entity type, domain, object id, object status.
- Optional `FieldContext`: field name, label, current value, allowed values, validation state, help key, field-level marker.
- `ObjectContext`: object summary, lifecycle state, relevant ids, status, related entity ids, treatment/lifecycle/payment/source-change metadata where present.
- `StoryContext`: story/evidence JSON availability, actions taken, actions not taken, missing evidence, summaries.
- `UserQuestionContext`: question text, intent, role, audience.
- `EvidenceContext`: domain knowledge, field catalogue, platform doctrine, slice knowledge, object story, runtime, DB, deployment, production evidence, reference ids.
- `AnswerControlContext`: requested exposure, live/final answer request, object-specific/runtime/DB/production truth requirements.

The output review should include contract status, severity, subject type, question intent, supported and blocked question types, required/available/missing evidence, caveats, recommended Minerva flow, answer eligibility, readiness summaries, boundary flags, and next step.

Rules:

- Field help requires surface, subject, field context, and field catalogue or domain knowledge. Missing field metadata returns `CONTEXT_MISSING_FIELD_METADATA`; ready context routes to `FIELD_HELP_PIPELINE`.
- Change-impact guidance requires field context, domain knowledge, and platform doctrine or slice knowledge. Missing doctrine may be caveated; missing field/domain evidence blocks.
- Admin Queue explanation requires subject context, object story or story context, actions taken/not taken, and status/lifecycle summary. Missing story returns `CONTEXT_MISSING_OBJECT_STORY`.
- Treatment explanation requires object story, lifecycle context, treatment/routing summary, domain reasoning or doctrine, and actions not taken. CorrectionReview retro/supplementary questions require correction path/treatment equivalent, ProcessPeriod lifecycle context, payment-window context where payment is involved, and actions not taken.
- Banking, netting, payment, or recovery treatment questions without payment context return `CONTEXT_MISSING_PAYMENT_CONTEXT`.
- "What changed?" requires source-change or before-after summary; missing evidence returns `CONTEXT_MISSING_SOURCE_CHANGE_SUMMARY`.
- "What has not happened?" requires actions not taken; missing evidence returns `CONTEXT_MISSING_ACTIONS_NOT_TAKEN`.
- Object-specific answers require object story.
- Runtime, DB, and production truth require matching evidence.
- `LIVE_OPERATOR_RESPONSE` or `LiveAnswerRequested = true` returns `CONTEXT_BLOCKED_LIVE_EXPOSURE` and `BLOCKED_LIVE_EXPOSURE_NOT_AUTHORISED`.
- Every output must include false boundary flags for live LLM, final answer, chat, DB read/write, runtime integration, corpus mutation, answer display, and persistence.

Add `tests/test_contextual_explanation_contract.py` covering:

- Leave Type field help ready.
- Leave Type field help missing metadata.
- CorrectionReview Admin Queue explanation ready.
- CorrectionReview retro treatment missing lifecycle.
- Banking/netting treatment missing payment context.
- What changed missing source-change summary.
- What has not happened missing actions-not-taken.
- Live operator response blocked.
- Object-specific answer without object story blocked.
- Boundary flags false for every output.

Add docs:

- `docs/knowledge/minerva_contextual_explanation_contract_v0_1.md`.
- `docs/codex_prompts/2026-05-19_minerva_contextual_explanation_contract_v0_1.md`.
- `docs/slice_knowledge/2026-05-19_minerva_contextual_explanation_contract_v0_1.md`.

Do not add API, UI, DB access, live LLM, chat, corpus mutation, runtime integration, Analytics integration, persistence, or final answers.

Close status: `CONTEXTUAL_EXPLANATION_CONTRACT_READY`.
