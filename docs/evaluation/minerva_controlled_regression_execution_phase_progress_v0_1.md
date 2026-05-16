# Minerva Controlled Regression Execution Phase Progress v0.1

## 1. Current Goal

Advance Minerva controlled regression execution and internal evaluation summary readiness using deterministic local batch evaluation over checked-in controlled evaluation report fixtures.

## 2. Current Phase

Controlled regression execution and internal evaluation summary readiness.

## 3. Current Estimated Progress Before Slice

Approximately 35% complete before this slice.

## 4. Expected Progress After Slice

Approximately 70% complete after this slice.

This increase is limited to controlled regression execution readiness because the slice adds deterministic batch evaluation, fixture-level pass/fail metadata, summary metadata, drift categories, safety categories, and focused regression tests.

## 5. Completed Work

Completed prior controlled evaluation-output governance work:

- Controlled-Readiness Status Answer Guard / Retrieval Preference Pack v0.1.
- Candidate Answer Readiness Classifier v0.1.
- Evaluation Output Publication Gate v0.1.
- Controlled Evaluation Report Assembler v0.1.
- Controlled Evaluation Report Fixture Pack / Golden Report Baselines v0.1.

Completed in this slice:

- Deterministic controlled evaluation batch harness.
- Fixture-level pass/fail model.
- Batch-level failure categories for drift and safety issues.
- Deterministic controlled evaluation batch summary model.
- Focused regression tests for batch harness and summary behavior.
- Documentation and durable prompt/control artefact.

## 6. Work Remaining

Remaining work:

- Add a controlled evaluation summary consumer for developer handoff metadata.
- Add a controlled regression execution closeout record once the consumer is in place.
- Decide whether additional golden fixtures are required for edge-case drift scenarios.
- Keep runtime, exposure, DB, live LLM, corpus, Code Evidence, and cross-repo integration boundaries deferred until separately authorised.

## 7. Why This Larger Slice Is Safe

This slice is safe to group because all work is local, deterministic, in-memory, and testable.

It does not add runtime surfaces, routes, APIs, UI, DB access, live retrieval, live LLM calls, final answer generation, corpus writes, Code Evidence ingestion, migrations, credentials, deployment configuration, production claims, workforce-platform runtime integration, or ezeas-analytics runtime integration.

## 8. Quality Guardrails

Quality guardrails:

- deterministic repeated output;
- focused fixture regression tests;
- no fixture mutation;
- no generated report writes;
- explicit final-answer-generation false flags;
- explicit no-action attestation;
- failure categories for publication drift, missing caveats, blocked claims, final-answer-generation safety, and runtime or exposure safety.

## 9. What Must Still Remain Prohibited

Still prohibited:

- internal chat exposure;
- public, production, tenant, or customer chat exposure;
- API endpoints or route registration;
- live LLM calls;
- final natural-language answer generation;
- DB connection, reads, writes, or validation;
- migrations;
- corpus mutation;
- Code Evidence ingestion;
- live retrieval backend changes;
- credentials or connection strings;
- workforce-platform changes;
- ezeas-analytics changes;
- UI changes;
- production readiness claims;
- deployment readiness claims;
- runtime readiness claims.

## 10. Recommended Next Slice

Recommended next slice: add a controlled evaluation summary consumer and closeout record that reads in-memory batch summary metadata for developer handoff only.

The next slice must preserve all runtime, exposure, final answer generation, live LLM, DB, corpus, Code Evidence, cross-repo, deployment, and production boundaries unless separately authorised.

## 11. Developer Handoff

Use the batch harness service to evaluate checked-in golden fixtures and the summary service to convert the result into internal developer-handoff metadata.

Treat failures as controlled regression drift requiring review. Do not use these outputs as final user-facing answers.
