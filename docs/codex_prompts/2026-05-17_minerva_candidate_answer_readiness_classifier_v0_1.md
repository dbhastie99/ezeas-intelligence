# Minerva Candidate Answer Readiness Classifier v0.1 Prompt

Date: 17 May 2026

## Objective

Create and execute the Minerva Candidate Answer Readiness Classifier v0.1 slice.

This slice adds a deterministic safety/evaluation classifier for proposed Minerva answer/status text or structured candidate output. The classifier decides whether a candidate preserves controlled-readiness caveats and whether it is safe for controlled evaluation or developer handoff. It must not generate final user-facing answers.

## Required Posture

- Local deterministic service, tests, and documentation only.
- No live LLM calls.
- No final natural-language answer generation.
- No chat exposure.
- No API endpoint.
- No route registration.
- No DB connection.
- No DB reads.
- No DB writes.
- No migrations.
- No corpus mutation.
- No Code Evidence ingestion.
- No live retrieval backend changes.
- No workforce-platform changes.
- No ezeas-analytics changes.
- No UI changes.
- No production readiness claim.
- No deployment readiness claim.
- No runtime readiness claim.

## Create

- `app/services/candidate_answer_readiness_classifier_service.py`
- `docs/evaluation/candidate_answer_readiness_classifier_v0_1.md`
- `tests/test_candidate_answer_readiness_classifier_service.py`

## Required Service Behaviour

The service must expose deterministic functions/classes that evaluate candidate answer/status text or structured candidate output and return metadata equivalent to:

- `readiness_classification`
- `safe_for_controlled_evaluation`
- `safe_for_developer_handoff`
- `safe_for_final_answer_generation`
- `overstatement_detected`
- `prohibited_claims_detected`
- `required_caveats`
- `missing_caveats`
- `preserved_boundaries`
- `violated_boundaries`
- `final_answer_generation_claim_detected`
- `live_llm_claim_detected`
- `chat_exposure_claim_detected`
- `endpoint_exposure_claim_detected`
- `db_access_claim_detected`
- `db_validation_claim_detected`
- `corpus_mutation_claim_detected`
- `code_evidence_ingestion_claim_detected`
- `workforce_runtime_integration_claim_detected`
- `analytics_runtime_integration_claim_detected`
- `explanation`

Classification values should include:

- `SAFE_CONTROLLED_EVALUATION_ONLY`
- `NEEDS_CAVEAT`
- `BLOCKED_OVERSTATED_RUNTIME`
- `BLOCKED_OVERSTATED_DEPLOYMENT`
- `BLOCKED_OVERSTATED_PRODUCTION`
- `BLOCKED_OVERSTATED_EXPOSURE`
- `BLOCKED_FINAL_ANSWER_GENERATION_CLAIM`
- `BLOCKED_LIVE_LLM_CLAIM`
- `BLOCKED_DB_ACCESS_CLAIM`
- `BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM`
- `BLOCKED_CROSS_REPO_RUNTIME_CLAIM`
- `UNKNOWN_REQUIRES_REVIEW`

## Required Test Coverage

Tests must prove:

1. controlled-readiness/no-action text is safe for controlled evaluation only;
2. production-ready claim is blocked;
3. deployed claim is blocked;
4. runtime-enabled claim is blocked;
5. chat exposure enabled claim is blocked;
6. endpoint exposure enabled claim is blocked;
7. final answer generation enabled claim is blocked;
8. live LLM enabled claim is blocked;
9. DB access occurred claim is blocked;
10. DB validation occurred claim is blocked unless framed as pending/not performed;
11. corpus mutation occurred claim is blocked;
12. Code Evidence ingestion occurred claim is blocked;
13. workforce-platform runtime integration occurred claim is blocked;
14. analytics runtime integration occurred claim is blocked;
15. ambiguous status without caveat requires review;
16. final artefact preference plus controlled-readiness caveat is safe for developer handoff only.

## Documentation Requirements

Create `docs/evaluation/candidate_answer_readiness_classifier_v0_1.md` with sections covering purpose, scope, current status, classification need, controlled evaluation, developer handoff, final answer generation, exposure, runtime, deployment, production, DB/validation, corpus/Code Evidence, cross-repo runtime, classification model, blocked claims, caveat behaviour, authorisations, non-authorisations, recommended next slice, and developer handoff.

The document must clearly state that this is deterministic classifier only and does not expose chat, generate final answers, call live LLMs, enable runtime retrieval, validate against a DB, query/write a DB, mutate corpus, ingest Code Evidence, expose endpoints, or integrate workforce-platform/ezeas-analytics runtime behaviour.

## Verification

Run:

```powershell
python -m pytest tests/test_candidate_answer_readiness_classifier_service.py -q
python -m py_compile app/services/candidate_answer_readiness_classifier_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

Remove `.pytest_tmp` if present.

## Expected Report

Report files changed, behaviour implemented, explicit no-action confirmation, exact tests run and results, warnings or limitations, and current `git status --short`.

Suggested commit message: `minerva-candidate-answer-readiness-classifier-v01`
