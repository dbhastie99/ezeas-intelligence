# Prompt Instruction Contract

Instruction version: `LEAVE_STUDIO_LIVE_CONVERSATION_V1`.

The system instruction says that `LEAVE_STUDIO_LLM_CONTEXT_V3` is the sole factual authority; history is continuity/coreference only; model memory, browsing, URLs, tools, retrieval, database queries, legal invention, worker/payroll calculations, persistence claims and mutation are forbidden. It defines the four persona styles and requires strict JSON.

`SUPPORTED_GUIDANCE_ONLY` is explicitly treated as no persistence. The model may not say a setting can be changed, adjusted, customised, edited, saved or persisted unless the packet contains an explicit supported Change action.
