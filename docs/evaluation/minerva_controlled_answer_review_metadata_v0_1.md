# Minerva Controlled Answer Review Metadata v0.1

## Review Model

Controlled answer review metadata consumes a controlled synthesis rehearsal output. It produces deterministic review readiness metadata for a human reviewer.

The ready status is `CONTROLLED_ANSWER_REVIEW_READY`. When ready, `answer_skeleton_ready_for_human_review` may be true, but `final_answer_generated`, `live_llm_performed`, and `chat_exposure_authorised` remain false.

## Required Review Checks

Required checks are:

- source references;
- caveats;
- prohibited claim scan;
- evidence/implementation boundary;
- no-runtime claim;
- still-to-do clarity.

Reviewer confirmation is always required. Review readiness does not authorise a final answer.

## No Live LLM or Chat Boundary

This metadata does not call a live LLM, does not expose chat, does not register an endpoint, and does not create a final user-facing answer.

## Blocked Claims

Final answer, live LLM, user-facing answer, or chat exposure claims produce `BLOCKED_FINAL_ANSWER_OR_CHAT_EXPOSURE_CLAIM`. Runtime, deployment, or production overstatement produces `BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT`.

## Developer Handoff

Use `build_controlled_answer_review_metadata(rehearsal_output)` after the controlled rehearsal returns ready. Missing review checks must remain explicit. Human confirmation is required before any later phase can consider answer exposure.
