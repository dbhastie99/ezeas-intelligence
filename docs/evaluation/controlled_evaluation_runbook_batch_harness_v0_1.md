# Controlled Evaluation Runbook / Batch Evaluation Harness v0.1

## 1. Purpose

This document defines the deterministic Minerva controlled evaluation runbook and batch evaluation harness for checked-in controlled evaluation report fixtures.

The harness is for internal regression checks, developer handoff, controlled evaluation summaries, golden baseline drift detection, and next-slice readiness reporting.

## 2. Scope

Scope is limited to local deterministic evaluation of supplied fixture payloads, supplied fixture file paths, or an explicitly supplied fixture directory.

The harness does not scan arbitrary repository paths unless a caller passes a fixture directory.

## 3. Current Status

Minerva remains controlled-readiness only.

This is a deterministic batch evaluation harness only. It is not a chat exposure slice, not a final answer generation slice, not a live LLM slice, not a runtime retrieval slice, not a DB validation slice, and not a production-readiness slice.

## 4. Relationship To Status Guard

The status guard remains the source of controlled-readiness posture: controlled-readiness is not runtime, deployment, production, exposure, DB validation, or final natural-language answer generation readiness.

This harness preserves that posture by validating fixture outputs against no-action and deferred-boundary expectations.

## 5. Relationship To Candidate Answer Classifier

The candidate answer classifier remains the deterministic classifier for candidate controlled-readiness metadata. This harness does not create candidate final answers and does not promote classifier output to user-facing text.

## 6. Relationship To Publication Gate

The publication gate remains the deterministic decision point for controlled internal artefact publication decisions and blocked overstatement decisions.

This harness compares fixture expectations with actual publication gate and report assembler outcomes.

## 7. Relationship To Controlled Evaluation Report Assembler

The report assembler remains the deterministic producer of structured internal controlled evaluation report metadata.

This harness runs fixture input metadata through the assembler and checks publication decision, controlled-report safety, final-answer-generation safety, required caveats, preserved boundaries, violated boundaries, no-action attestation, and block reasons.

## 8. Relationship To Golden Baselines

The checked-in fixtures under `tests/fixtures/controlled_evaluation_reports` are the golden baselines for this slice.

The harness detects drift when actual deterministic outputs no longer match fixture expectations.

## 9. Batch Harness Model

Batch output includes:

- `batch_id`
- `fixture_count`
- `passed_count`
- `failed_count`
- `skipped_count`
- `all_passed`
- `fixture_results`
- `blocked_claim_failures`
- `missing_caveat_failures`
- `unexpected_publication_decision_failures`
- `final_answer_generation_safety_failures`
- `runtime_or_exposure_safety_failures`
- `deterministic_output`
- `safe_for_controlled_evaluation_summary`
- `safe_for_final_answer_generation`
- `no_action_attestation`
- `explanation`

## 10. Fixture Result Model

Each fixture result includes:

- `fixture_id`
- `fixture_path`
- `fixture_purpose`
- `passed`
- `expected_publication_decision`
- `actual_publication_decision`
- `expected_safe_for_controlled_evaluation_report`
- `actual_safe_for_controlled_evaluation_report`
- `expected_safe_for_final_answer_generation`
- `actual_safe_for_final_answer_generation`
- `failures`
- `preserved_boundaries`
- `violated_boundaries`

## 11. Pass / Fail Rules

A fixture passes only when actual deterministic output matches expected publication decision, expected controlled evaluation report safety, expected final answer generation safety, expected preserved boundaries, expected violated boundaries, expected block reasons, expected required caveats, and expected no-action attestation.

Any fixture that becomes safe for final answer generation fails.

The batch passes only when every supplied fixture passes.

## 12. Drift Detection Rules

The harness treats these as drift:

- unexpected publication decision;
- missing required caveat;
- changed preserved boundary expectations;
- changed violated boundary expectations;
- changed blocked-claim expectations;
- changed no-action attestation;
- any final answer generation safety change.

## 13. Final Answer Generation Boundary

The harness never generates final user-facing natural-language answers.

The harness never marks the batch safe for final answer generation.

## 14. Chat / Endpoint Exposure Boundary

This is not a chat exposure slice.

The harness does not expose internal chat, public chat, production chat, tenant chat, or customer chat. It does not add an endpoint, register a route, or create an API surface.

## 15. Runtime Boundary

This is not a runtime readiness slice and not a runtime retrieval slice.

The harness does not alter live retrieval backend behaviour and does not enable runtime behaviour.

## 16. Deployment Boundary

This is not a deployment-readiness slice.

The harness does not claim deployment readiness and does not prepare deployment configuration.

## 17. Production Boundary

This is not a production-readiness slice.

The harness does not claim production readiness and does not authorise production use.

## 18. DB / Validation Boundary

This is not a DB validation slice.

The harness does not connect to or query a database. It does not read from a database and does not write to a database.

## 19. Corpus / Code Evidence Boundary

The harness does not mutate corpus and does not ingest Code Evidence.

It only reads supplied local JSON fixture files when a caller explicitly supplies paths or a directory.

## 20. Cross-Repo Runtime Boundary

The harness does not integrate workforce-platform or ezeas-analytics runtime behaviour.

No cross-repo runtime integration is authorised by this slice.

## 21. What This Slice Authorises

This slice authorises a local deterministic in-memory batch harness, focused tests, and documentation for controlled evaluation fixture regression checks.

## 22. What This Slice Does Not Authorise

This slice does not authorise chat exposure, final natural-language answer generation, live LLM calls, runtime retrieval, DB validation, DB reads, DB writes, migrations, corpus mutation, Code Evidence ingestion, endpoint exposure, UI changes, workforce-platform runtime integration, ezeas-analytics runtime integration, deployment readiness, production readiness, or runtime readiness.

## 23. Recommended Next Slice

Recommended next slice: add a controlled evaluation summary consumer that can read the in-memory batch result and produce developer-facing next-slice readiness metadata without exposing chat, enabling runtime retrieval, connecting to a DB, or generating final user-facing natural-language answers.

## 24. Developer Handoff

Use `evaluate_controlled_evaluation_fixture_payloads`, `evaluate_controlled_evaluation_fixture_paths`, or `evaluate_controlled_evaluation_fixture_directory` from `app/services/controlled_evaluation_batch_harness_service.py`.

Keep output in memory. Do not write generated reports in this slice. Treat any failed fixture as golden baseline drift requiring review before further controlled evaluation summary work.
