# Controlled Evaluation Summary Export v0.1

## 1. Purpose

Define the deterministic in-memory export model for Minerva controlled evaluation batch summaries.

The export is for regression checks, developer handoff, controlled evaluation summaries, golden baseline drift detection, CI-style local command execution, and next-slice readiness reporting.

## 2. Scope

Scope is limited to converting structured in-memory batch summary metadata into structured in-memory export metadata.

The export service does not write files, call live systems, expose chat, register routes, connect to a DB, mutate corpus, ingest Code Evidence, or generate final user-facing natural-language answers.

## 3. Current Status

Minerva remains controlled-readiness only.

This slice adds internal deterministic export metadata only. It is not runtime readiness, deployment readiness, production readiness, chat exposure, endpoint exposure, live LLM use, DB access, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, or analytics runtime integration.

## 4. Relationship to Golden Baselines

Golden baselines remain the checked-in controlled evaluation report fixtures under `tests/fixtures/controlled_evaluation_reports`.

The export model does not read or update those fixtures. It only preserves summary metadata derived from deterministic golden-baseline regression checks.

## 5. Relationship to Batch Harness

The batch harness remains responsible for evaluating controlled evaluation fixtures and producing deterministic batch results.

The export model does not execute the harness. It consumes the structured summary that can be built from harness output.

## 6. Relationship to Batch Summary Model

The batch summary model remains responsible for aggregating harness results into summary metadata.

The export model preserves that summary metadata and adds an export contract for internal handoff and CI-style reporting.

## 7. Export Model

Export output includes `export_id`, `source_summary_id`, `export_type`, `phase_name`, `generated_from_controlled_inputs`, `overall_status`, `all_passed`, fixture counts, failure categories, remaining work, recommended next slice, progress before and after the slice, developer-handoff safety, final-answer-generation safety, no-action attestation, prohibited capability boundaries, export caveats, and explanation.

## 8. Export Types

Supported export types are:

- `CONTROLLED_INTERNAL_SUMMARY`
- `DEVELOPER_HANDOFF_SUMMARY`
- `CI_CHECK_SUMMARY`
- `PHASE_PROGRESS_SUMMARY`
- `UNKNOWN_REQUIRES_REVIEW`

Unknown export types become `UNKNOWN_REQUIRES_REVIEW` and fail export safety checks.

## 9. Developer Handoff Boundary

Developer handoff export is permitted only when source summary handoff safety is true, caveats are present, no-action boundaries are present, and no export policy failure is present.

Developer handoff means internal metadata handoff only.

## 10. CI Check Summary Boundary

CI check summary export is permitted only for deterministic controlled inputs.

If `generated_from_controlled_inputs` is false, the export fails with a controlled review requirement.

## 11. Phase Progress Summary Boundary

Phase progress summary export preserves caller-supplied progress metadata.

For this slice, progress before the slice is approximately 70%, and expected progress after the slice is approximately 95%.

## 12. Final Answer Generation Boundary

The export is never safe for final answer generation.

The export service does not generate final natural-language answers.

## 13. Runtime / Deployment / Production Boundary

The export must not claim runtime readiness, deployment readiness, production readiness, chat exposure, endpoint exposure, live LLM use, or final answer generation.

Any positive prohibited claim causes the export to fail controlled safety checks.

## 14. DB / Corpus / Code Evidence Boundary

The export service does not connect to a database, read from a database, write to a database, create migrations, mutate corpus, or ingest Code Evidence.

## 15. Cross-Repo Runtime Boundary

The export service does not integrate workforce-platform runtime behaviour or ezeas-analytics runtime behaviour.

No cross-repo runtime integration is authorised.

## 16. What This Slice Authorises

This slice authorises deterministic in-memory summary export metadata, focused tests, compile checks, and documentation.

## 17. What This Slice Does Not Authorise

This slice does not authorise chat exposure, final natural-language answer generation, live LLM calls, runtime retrieval, DB access, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, endpoint exposure, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, deployment readiness, production readiness, or runtime readiness.

## 18. Developer Handoff

Use `export_controlled_evaluation_summary` from `app/services/controlled_evaluation_summary_export_service.py`.

Keep output in memory. Treat failed exports as controlled regression or export metadata issues requiring review before phase closeout.
