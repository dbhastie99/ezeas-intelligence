# Controlled Evaluation Batch Harness v0.1

## 1. Purpose

Define the deterministic Minerva controlled evaluation batch harness for checked-in controlled evaluation report fixtures.

The harness supports regression checks, developer handoff, controlled evaluation summaries, golden baseline drift detection, and next-slice readiness reporting.

## 2. Scope

Scope is limited to local deterministic evaluation of supplied fixture payloads, supplied fixture file paths, or an explicitly supplied fixture directory.

The harness does not scan arbitrary repository paths unless a caller passes a fixture directory.

## 3. Current Status

Minerva remains controlled-readiness only.

This slice is a local deterministic batch harness, docs, and tests slice. It is not runtime, deployment, production, chat exposure, live LLM, DB validation, corpus mutation, Code Evidence ingestion, or final natural-language answer generation work.

## 4. Relationship to Status Guard

The Controlled-Readiness Status Answer Guard remains the source of posture: controlled-readiness is not runtime, deployment, production, exposure, DB validation, or final answer generation readiness.

The harness preserves that posture by failing fixtures that lose no-action or deferred-boundary expectations.

## 5. Relationship to Candidate Answer Classifier

The Candidate Answer Readiness Classifier remains deterministic controlled metadata classification.

The harness does not create candidate final answers and does not promote classifier output to user-facing text.

## 6. Relationship to Publication Gate

The Evaluation Output Publication Gate remains the deterministic decision point for controlled internal publication and blocked overstatement decisions.

The harness compares fixture expectations with actual publication gate outcomes.

## 7. Relationship to Controlled Evaluation Report Assembler

The Controlled Evaluation Report Assembler remains the deterministic producer of structured internal report metadata.

The harness runs fixture input metadata through the assembler and checks publication decision, controlled-report safety, final-answer-generation safety, required caveats, preserved boundaries, violated boundaries, no-action attestation, and block reasons.

## 8. Relationship to Golden Baselines

The checked-in fixtures under `tests/fixtures/controlled_evaluation_reports` are golden baselines.

The harness detects drift when actual deterministic outputs no longer match fixture expectations.

## 9. Batch Harness Model

Batch output includes `batch_id`, fixture counts, pass/fail counts, skipped count, `all_passed`, `fixture_results`, blocked-claim failures, missing-caveat failures, unexpected-publication-decision failures, final-answer-generation safety failures, runtime-or-exposure safety failures, deterministic-output flag, controlled-summary safety flag, final-answer-generation safety flag, no-action attestation, and explanation.

## 10. Fixture Result Model

Each fixture result includes `fixture_id`, `fixture_path`, `fixture_purpose`, `passed`, expected and actual publication decision, expected and actual controlled-report safety, expected and actual final-answer-generation safety, failures, preserved boundaries, and violated boundaries.

## 11. Pass / Fail Rules

A fixture passes only when actual deterministic output matches expected publication decision, expected controlled evaluation report safety, expected final answer generation safety, expected preserved boundaries, expected violated boundaries, expected block reasons, expected required caveats, and expected no-action attestation.

Any fixture that becomes safe for final answer generation fails.

The batch passes only when every supplied fixture passes.

## 12. Drift Detection Rules

Drift includes unexpected publication decision, missing required caveat, changed preserved boundary expectations, changed violated boundary expectations, changed blocked-claim expectations, changed no-action attestation, and any final-answer-generation safety change.

## 13. Safety Failure Categories

Safety failure categories include blocked claim failures, missing caveat failures, unexpected publication decision failures, final answer generation safety failures, and runtime or exposure safety failures.

## 14. Final Answer Generation Boundary

The harness never generates final user-facing natural-language answers.

The harness never marks the batch safe for final answer generation.

## 15. Chat / Endpoint Exposure Boundary

This is not a chat exposure slice.

The harness does not expose internal chat, public chat, production chat, tenant chat, or customer chat. It does not add an endpoint, register a route, or create an API surface.

## 16. Runtime Boundary

This is not a runtime readiness slice and not a runtime retrieval slice.

The harness does not alter live retrieval backend behaviour and does not enable runtime behaviour.

## 17. Deployment Boundary

This is not a deployment-readiness slice.

The harness does not claim deployment readiness and does not prepare deployment configuration.

## 18. Production Boundary

This is not a production-readiness slice.

The harness does not claim production readiness and does not authorise production use.

## 19. DB / Validation Boundary

This is not a DB validation slice.

The harness does not connect to, query, read from, or write to a database.

## 20. Corpus / Code Evidence Boundary

The harness does not mutate corpus and does not ingest Code Evidence.

It only reads supplied local JSON fixture files when a caller explicitly supplies paths or a directory.

## 21. Cross-Repo Runtime Boundary

The harness does not integrate workforce-platform or ezeas-analytics runtime behaviour.

No cross-repo runtime integration is authorised by this slice.

## 22. What This Slice Authorises

This slice authorises a local deterministic in-memory batch harness, focused tests, and documentation for controlled evaluation fixture regression checks.

## 23. What This Slice Does Not Authorise

This slice does not authorise chat exposure, final natural-language answer generation, live LLM calls, runtime retrieval, DB validation, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, endpoint exposure, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, deployment readiness, production readiness, or runtime readiness.

## 24. Recommended Next Slice

Recommended next slice: add a controlled evaluation summary consumer that can read the in-memory batch result and produce developer-facing next-slice readiness metadata without exposing chat, enabling runtime retrieval, connecting to a DB, or generating final user-facing natural-language answers.

## 25. Developer Handoff

Use `evaluate_controlled_evaluation_fixture_payloads`, `evaluate_controlled_evaluation_fixture_paths`, or `evaluate_controlled_evaluation_fixture_directory` from `app/services/controlled_evaluation_batch_harness_service.py`.

Keep output in memory. Do not write generated reports in this slice. Treat any failed fixture as golden baseline drift requiring review before further controlled evaluation summary work.
