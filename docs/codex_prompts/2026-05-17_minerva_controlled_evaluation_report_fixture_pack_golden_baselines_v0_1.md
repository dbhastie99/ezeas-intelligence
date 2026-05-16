# Codex Prompt - Minerva Controlled Evaluation Report Fixture Pack / Golden Report Baselines v0.1

## Slice

Minerva Controlled Evaluation Report Fixture Pack / Golden Report Baselines v0.1.

## Context

This slice follows the first full Minerva controlled evaluation-output chain:

1. Minerva Controlled-Readiness Status Answer Guard / Retrieval Preference Pack v0.1.
2. Minerva Candidate Answer Readiness Classifier v0.1.
3. Minerva Evaluation Output Publication Gate v0.1.
4. Minerva Controlled Evaluation Report Assembler v0.1.

Minerva remains controlled-readiness only. Internal chat exposure, public/production/tenant/customer chat exposure, final natural-language answer generation, live LLM use, live retrieval backend use, DB access, DB writes, corpus mutation, Code Evidence ingestion, workforce-platform runtime integration, and ezeas-analytics runtime integration remain deferred.

## Objective

Create a deterministic checked-in fixture and golden baseline layer for the controlled evaluation report chain. The fixture pack must detect drift, overstatement, missing caveats, unsafe publication decisions, and accidental final-answer/runtime/deployment/production claims in future changes.

## Required Scope

This slice is local deterministic fixtures/tests/docs only.

It must not:

- enable internal chat exposure;
- enable public, production, tenant, or customer chat exposure;
- add or register an API route;
- call a live LLM;
- generate final natural-language answers;
- connect to a database;
- read from a database;
- write to a database;
- create migrations;
- mutate corpus;
- ingest Code Evidence;
- alter live retrieval backend behaviour;
- add credentials or connection strings;
- change workforce-platform;
- change ezeas-analytics;
- change UI;
- claim production readiness;
- claim deployment readiness;
- claim runtime readiness.

## Fixture Pack

Create deterministic JSON fixtures under `tests/fixtures/controlled_evaluation_reports/`:

- `safe_controlled_evaluation_report.json`
- `safe_developer_handoff.json`
- `safe_progress_summary.json`
- `safe_next_slice_recommendation.json`
- `ambiguous_requires_review.json`
- `blocked_production_overstatement.json`
- `blocked_deployment_overstatement.json`
- `blocked_runtime_overstatement.json`
- `blocked_exposure_overstatement.json`
- `blocked_final_answer_generation_overstatement.json`
- `blocked_live_llm_overstatement.json`
- `blocked_db_access_validation_overstatement.json`
- `blocked_corpus_code_evidence_overstatement.json`
- `blocked_workforce_runtime_integration_overstatement.json`
- `blocked_analytics_runtime_integration_overstatement.json`

Each fixture must include:

- `fixture_id`
- `fixture_purpose`
- `input_metadata`
- `expected_publication_decision`
- `expected_safe_for_controlled_evaluation_report`
- `expected_safe_for_developer_handoff`
- `expected_safe_for_progress_summary`
- `expected_safe_for_final_answer_generation`
- `expected_required_caveats`
- `expected_block_reasons`
- `expected_preserved_boundaries`
- `expected_violated_boundaries`
- `expected_no_action_attestation`
- `expected_recommended_next_slice`
- `expected_summary_terms`

## Tests

Create `tests/test_controlled_evaluation_report_golden_baselines.py`.

The tests must load every fixture and run `input_metadata` through the existing controlled evaluation report assembler and publication gate as appropriate.

The tests must assert:

1. All fixture files are valid JSON.
2. All fixture IDs are unique.
3. Fixture output is deterministic for repeated runs.
4. Safe controlled evaluation report fixture remains safe for controlled evaluation report only.
5. Safe developer handoff fixture remains safe for developer handoff.
6. Safe progress summary fixture remains safe for progress summary.
7. Safe next-slice recommendation fixture preserves next-slice recommendation output.
8. Ambiguous fixture requires caveat or human review.
9. Production overstatement fixture is blocked.
10. Deployment overstatement fixture is blocked.
11. Runtime overstatement fixture is blocked.
12. Exposure overstatement fixture is blocked.
13. Final answer generation overstatement fixture is blocked.
14. Live LLM overstatement fixture is blocked.
15. DB access/validation overstatement fixture is blocked unless framed as pending/not performed.
16. Corpus mutation / Code Evidence overstatement fixture is blocked.
17. Workforce runtime integration overstatement fixture is blocked.
18. Analytics runtime integration overstatement fixture is blocked.
19. No fixture is safe for final answer generation.
20. No fixture introduces runtime, deployment, production, chat exposure, endpoint exposure, live LLM, DB, corpus, Code Evidence, workforce runtime, or analytics runtime approval unless it is explicitly a blocked/violated-boundary example.

## Documentation

Create `docs/evaluation/controlled_evaluation_report_fixture_pack_golden_baselines_v0_1.md`.

The documentation must include:

1. Purpose
2. Scope
3. Current Status
4. Relationship to Status Guard
5. Relationship to Candidate Answer Classifier
6. Relationship to Publication Gate
7. Relationship to Controlled Evaluation Report Assembler
8. Fixture Categories
9. Golden Baseline Expectations
10. Drift Risks Prevented
11. Overstatement Risks Prevented
12. Final Answer Generation Boundary
13. Chat / Endpoint Exposure Boundary
14. Runtime Boundary
15. Deployment Boundary
16. Production Boundary
17. DB / Validation Boundary
18. Corpus / Code Evidence Boundary
19. Cross-Repo Runtime Boundary
20. What This Slice Authorises
21. What This Slice Does Not Authorise
22. Recommended Next Slice
23. Developer Handoff

The documentation must clearly state that this is a deterministic fixture/golden-baseline pack only and not a chat exposure, final answer generation, live LLM, runtime retrieval, DB validation, production-readiness, corpus mutation, Code Evidence ingestion, endpoint exposure, workforce-platform runtime, analytics runtime, or UI slice.

## Verification

Use Windows PowerShell syntax only:

- `python -m pytest tests\test_controlled_evaluation_report_golden_baselines.py`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `git status --short`

Run `python -m py_compile` only if a new Python helper/service is added.
