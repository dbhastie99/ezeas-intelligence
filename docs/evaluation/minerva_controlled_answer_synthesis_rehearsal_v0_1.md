# Minerva Controlled Answer Synthesis Rehearsal v0.1

## Rehearsal Model

Controlled answer synthesis rehearsal consumes controlled answer-preparation metadata and Developer Log retrieval metadata. It produces a deterministic answer skeleton readiness record for later human review.

The ready status is `CONTROLLED_ANSWER_SYNTHESIS_REHEARSAL_READY`. When ready, `answer_skeleton_prepared` may be true, but `final_answer_generated`, `live_llm_performed`, and `chat_exposure_authorised` remain false.

## Answer Skeleton vs Final Answer

The answer skeleton is structured metadata for safe sections and supported modes. It is not a final natural-language answer and is not exposed to chat.

Safe answer sections are:

- status summary;
- decisions captured;
- risks;
- still-to-do;
- evidence boundaries.

Supported answer modes are:

- status-summary;
- decision-summary;
- risk-summary;
- still-to-do-summary.

## Required Caveats

The rehearsal includes:

- evidence-boundary;
- implementation-status-boundary;
- no-runtime-claim;
- source-reference requirement.

Evidence references are preserved from answer-preparation metadata or retrieval metadata.

## Blocked Claims

The rehearsal blocks final answer generation, live LLM use, chat exposure, implementation completion overstatement, runtime readiness, deployment readiness, production readiness, DB or corpus mutation, and user-facing claims unless directly evidenced.

## Developer Handoff

Use `build_controlled_answer_synthesis_rehearsal(answer_preparation_metadata, retrieval_metadata)` only after answer preparation and retrieval metadata are ready. The output is for controlled rehearsal and review metadata only, not for chat, endpoint exposure, final answers, runtime integration, deployment, or production use.
