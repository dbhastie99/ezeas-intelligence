# Controlled Evaluation Batch Summary Model v0.1

## 1. Purpose

Define the deterministic internal summary model for Minerva controlled evaluation batch results.

The summary model supports developer handoff, controlled regression execution summaries, golden baseline drift reporting, and next-slice readiness reporting.

## 2. Scope

Scope is limited to converting an in-memory batch harness result into structured deterministic internal metadata.

The model does not read fixture files, write reports, call live systems, or generate final user-facing answers.

## 3. Summary Model

Summary output includes `summary_id`, `source_batch_id`, `phase_name`, progress before and after the slice, `overall_status`, fixture counts, safety failures, drift failures, blocked claim failures, remaining phase work, recommended next slice, developer-handoff safety, final-answer-generation safety, no-action attestation, and explanation.

## 4. Phase Progress Metadata

The model preserves caller-supplied phase progress metadata.

For this slice, the recorded current phase progress before the slice is approximately 35%, and expected progress after the slice is approximately 70%.

## 5. Overall Status Rules

Passing batch results produce `PASS` when no prohibited summary metadata claims are present.

Failed batch results produce `FAIL`.

Any summary metadata that positively claims runtime, deployment, production, chat exposure, live LLM use, DB access, corpus mutation, Code Evidence ingestion, cross-repo runtime integration, or final answer generation produces `FAIL`.

## 6. Remaining Work Model

Remaining work is represented as deterministic structured text supplied by the caller or defaulted by the service.

Remaining work must preserve deferred boundaries and must not imply runtime, deployment, production, chat exposure, DB access, live LLM use, corpus mutation, Code Evidence ingestion, or cross-repo runtime integration has occurred.

## 7. Recommended Next Slice

Recommended next slice: add a controlled evaluation summary consumer for developer handoff metadata while keeping runtime, chat exposure, DB access, live LLM use, and final answer generation deferred.

## 8. Developer Handoff Boundary

The summary is safe for developer handoff only when the batch passes, no-action boundaries are present, controlled-summary safety is true, and no summary metadata contains prohibited positive claims.

Developer handoff means internal metadata handoff only.

## 9. Final Answer Generation Boundary

The summary model never marks output safe for final answer generation.

The summary model does not generate final natural-language answers.

## 10. No-Action Attestation

The model attests that no runtime, exposure, endpoint, DB, corpus, Code Evidence, live LLM, final answer generation, UI, deployment, production, migration, credential, or cross-repo runtime action was performed.

## 11. What This Slice Authorises

This slice authorises deterministic in-memory batch summary metadata, focused regression tests, and documentation.

## 12. What This Slice Does Not Authorise

This slice does not authorise chat exposure, final natural-language answer generation, live LLM calls, runtime retrieval, DB validation, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, endpoint exposure, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, deployment readiness, production readiness, or runtime readiness.

## 13. Developer Handoff

Use `summarize_controlled_evaluation_batch_result` from `app/services/controlled_evaluation_batch_summary_service.py`.

Keep output in memory for this slice. Treat a `FAIL` summary as a controlled regression or summary metadata issue requiring review before the next controlled regression execution slice.
