# Minerva Contextual Explanation Contract v0.1

## Purpose

This artefact defines a generic context contract for future Minerva explanations. It is not specific to CorrectionReview or Admin Queue. The same envelope must support forms, fields, object detail pages, review queues, calculation surfaces, configuration screens, and payroll reconciliation surfaces.

The contract decides whether a future UI or runtime surface has provided enough context and evidence to enter the controlled Minerva evidence-to-answer pipeline. It does not produce final answers.

## Supported Explanation Categories

- Field help.
- Form guidance.
- Validation or blocker explanation.
- Object lifecycle or status explanation.
- Admin Queue or review item explanation.
- Calculation or object story explanation.
- Configuration impact explanation.
- Treatment recommendation.
- Evidence gap explanation.

## Context Packet Sections

`SurfaceContext` identifies the page, route, component, surface type, and mode.

`SubjectContext` identifies the subject type, entity type, domain, object id, and object status.

`FieldContext` is optional and required for field-level help. It identifies field name, label, current value, allowed values, validation state, help key, and whether the question is field-level.

`ObjectContext` carries object summary, lifecycle state, relevant ids, status, related entity ids, treatment codes, lifecycle context, payment context, or source-change summaries when available.

`StoryContext` carries whether story JSON, evidence JSON, actions taken, actions not taken, and missing evidence are available, plus summaries and lists.

`UserQuestionContext` carries question text, intent, role, and audience.

`EvidenceContext` records which source classes are available, including domain knowledge, field catalogue, platform doctrine, slice knowledge, object story, runtime evidence, DB evidence, deployment evidence, production evidence, and evidence reference ids.

`AnswerControlContext` records requested exposure mode and whether live, final, object-specific, runtime, DB, or production truth is requested.

## Field Help Example

A Leave Type form can ask: "What does Accrual method mean?"

Required context:

- `SurfaceContext` for the Leave Type form.
- `SubjectContext` with `SubjectType = LeaveType`.
- `FieldContext` with `FieldName = AccrualMethod` and `FieldLabel = Accrual method`.
- `FieldCatalogueAvailable = true` or `DomainKnowledgeAvailable = true`.

If the field metadata and source knowledge are present, Minerva may route to `FIELD_HELP_PIPELINE` in controlled mode. If field metadata or field/domain knowledge is absent, the contract returns `CONTEXT_MISSING_FIELD_METADATA`.

## Admin Queue / CorrectionReview Example

An Admin Queue row can ask: "Why is this in Admin Queue?"

Required context:

- `SubjectContext` for `CorrectionReview`.
- Object story or `StoryContext`.
- Actions taken and actions not taken.
- Object status or lifecycle/status summary.

If these are present, Minerva may route to `ADMIN_QUEUE_EXPLANATION_PIPELINE` in controlled mode. If the story is absent, the contract returns `CONTEXT_MISSING_OBJECT_STORY`.

CorrectionReview remains one representative subject, not the whole model.

## Required Evidence By Question Type

`WHAT_IS_THIS_FIELD` requires surface, subject, field metadata, and field catalogue or domain knowledge.

`WHAT_HAPPENS_IF_I_CHANGE_THIS` requires field context, domain knowledge, platform doctrine or slice knowledge, and validation/configuration impact knowledge. Missing doctrine may allow caveated readiness; missing field/domain evidence blocks.

`WHY_IS_THIS_IN_ADMIN_QUEUE` requires subject context, object story or story context, actions taken, actions not taken, and status or lifecycle summary.

`WHY_THIS_TREATMENT` requires object story, lifecycle context, treatment/routing summary, domain reasoning or platform doctrine, and actions not taken. CorrectionReview retro or supplementary questions also require treatment code, ProcessPeriod lifecycle context, and payment-window context when payment, banking, netting, or recovery is involved.

`WHAT_CHANGED` requires source-change summary and changed fields or before-after summary.

`WHAT_HAS_NOT_HAPPENED` requires actions-not-taken evidence.

`WHAT_EVIDENCE_IS_MISSING` and blocker questions require missing-evidence or blocker/validation context.

## Blocking And Caveats

Missing field metadata blocks field help. Missing object story blocks object-specific answers. Missing lifecycle blocks treatment explanation. Missing payment context blocks banking, netting, payment, or recovery treatment explanation. Missing source-change summary blocks "what changed" answers. Missing actions-not-taken blocks "what has not happened" answers.

Runtime truth requires runtime evidence. DB truth requires DB evidence. Production truth requires production evidence and explicit authorisation. Live operator response is blocked in this slice.

Some generic guidance can be ready with caveats when non-object-specific context exists but doctrine or slice knowledge is incomplete.

## Pipeline Position

The future pipeline is:

1. `MinervaExplanationContext`.
2. Evidence retrieval, metadata retrieval, and object story retrieval.
3. Answer preparation.
4. Citation/provenance packet.
5. Controlled answer rehearsal.
6. Controlled answer gate.
7. Future UI answer only if explicitly authorised.

This slice implements only the context contract and readiness review at step 1.

## No Live Integration Boundary

This contract does not expose chat, call a live LLM, connect to DB, read live Admin Queue, read live CorrectionReview, read live LeaveType, mutate corpus, add API/UI, integrate with Workforce runtime, integrate with Analytics runtime, persist answer attempts, or generate final live answers.

Every review preserves false boundary flags for live LLM, final answer, chat, DB read/write, runtime integration, corpus mutation, answer display, and persistence.

## Future Object Story Integration

Future Workforce/Admin Queue integration should provide object story packets that include lifecycle state, source-change summary, object status, actions taken, actions not taken, missing evidence, treatment/routing summary, and payment context where applicable. Minerva should refuse object-specific explanations when the object story is absent, even if a surface or object id is present.
