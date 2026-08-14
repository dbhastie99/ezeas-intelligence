# Implementation summary

The live V1 instruction prohibited invented worker outcomes but did not define three propositions precisely enough for model composition: absence of a criterion is not proof of a universal opposite; recognised service commencement is not entitlement access; and a first-person question is not certified worker context.

This Intelligence-only refinement advances the audited prompt to `LEAVE_STUDIO_LIVE_CONVERSATION_V2` while preserving `LEAVE_STUDIO_LLM_CONTEXT_V3`. It adds the same precision constraints to the provider payload and strict schema descriptions, treats question/history assertions as ungoverned, and retains all four persona styles.

Post-provider validation now fails closed with stable reasons for:

- `validation_negative_inference_claim`;
- `validation_service_entitlement_conflation`;
- `validation_personal_outcome_claim`;
- `validation_worker_context_boundary`.

The existing grounding, persona, URL/markup, action, capability, numerical, tool/secret-envelope, history, audit and mutation validation remains in force. No OpenAI client, schema, configuration, Workforce, UI, policy, worker, payroll or financial code changed.

Implementation files:

- `app/services/leave_studio_conversation_service.py`
- `tests/test_leave_studio_live_conversation.py`

Immutable implementation commit: `99976986967333bda74e14a0dc426a1b970d4d05`.
