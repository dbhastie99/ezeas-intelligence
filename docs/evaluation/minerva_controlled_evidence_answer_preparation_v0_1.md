# Minerva Controlled Evidence Answer Preparation v0.1

## Preparation Model

Controlled answer preparation consumes ready Developer Log retrieval metadata and produces metadata for later bounded synthesis. It does not generate a final answer.

The ready status is `CONTROLLED_ANSWER_PREPARATION_READY`. When ready, `answer_ready_for_controlled_synthesis` may be true, but `final_answer_generated`, `live_llm_performed`, and `chat_exposure_authorised` remain false.

## Required Caveats

Controlled answer preparation requires:

- evidence-boundary;
- implementation-status-boundary;
- no-runtime-claim;
- source-reference requirement.

Required source references are copied from retrieval metadata.

## Safe Answer Modes

The safe controlled answer modes are:

- status-summary;
- decision-summary;
- risk-summary;
- still-to-do-summary.

These are metadata modes only. They do not expose chat and do not create final natural-language answers in this slice.

## Blocked Claims

Final answer generation, live LLM use, chat exposure, runtime readiness, deployment readiness, production readiness, DB reads/writes, and live corpus mutation are prohibited. Claims of final answer generation or live LLM use produce `BLOCKED_FINAL_ANSWER_OR_LIVE_LLM_CLAIM`. Runtime, deployment, production, or chat overstatement produces `BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT`.

## Developer Handoff

Use `build_controlled_evidence_answer_preparation(retrieval_metadata)` only after retrieval metadata is ready. The output is suitable for controlled synthesis planning, not for user-facing chat or final answers.
