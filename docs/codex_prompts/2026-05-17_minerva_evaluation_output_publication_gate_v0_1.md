# Minerva Evaluation Output Publication Gate v0.1 Prompt

Date: 17 May 2026

## Objective

Create and execute the Minerva Evaluation Output Publication Gate v0.1 slice.

This slice adds a deterministic local publication gate for proposed Minerva evaluation/status output before that output is published into controlled internal artefacts such as developer handoff notes, evaluation reports, progress summaries, controlled-readiness documentation, and next-slice recommendations.

The gate must not publish, generate, or expose final user-facing answers. It only classifies whether supplied evaluation/status content is safe for controlled internal publication.

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

- `app/services/evaluation_output_publication_gate_service.py`
- `docs/evaluation/evaluation_output_publication_gate_v0_1.md`
- `tests/test_evaluation_output_publication_gate_service.py`

## Required Service Behaviour

The service must expose deterministic functions/classes that evaluate candidate evaluation output text or structured candidate metadata and return metadata equivalent to:

- `publication_decision`
- `safe_for_controlled_evaluation_report`
- `safe_for_developer_handoff`
- `safe_for_progress_summary`
- `safe_for_final_answer_generation`
- `publication_blocked`
- `block_reasons`
- `required_caveats`
- `missing_caveats`
- `preserved_boundaries`
- `violated_boundaries`
- `overstatement_detected`
- `human_review_required`
- `final_answer_generation_claim_detected`
- `live_llm_claim_detected`
- `chat_exposure_claim_detected`
- `endpoint_exposure_claim_detected`
- `runtime_readiness_claim_detected`
- `deployment_readiness_claim_detected`
- `production_readiness_claim_detected`
- `db_access_claim_detected`
- `db_validation_claim_detected`
- `corpus_mutation_claim_detected`
- `code_evidence_ingestion_claim_detected`
- `workforce_runtime_integration_claim_detected`
- `analytics_runtime_integration_claim_detected`
- `explanation`

Publication decisions must include:

- `PUBLISH_CONTROLLED_EVALUATION_REPORT`
- `PUBLISH_DEVELOPER_HANDOFF`
- `PUBLISH_PROGRESS_SUMMARY`
- `NEEDS_CAVEAT_BEFORE_PUBLICATION`
- `BLOCKED_OVERSTATED_RUNTIME`
- `BLOCKED_OVERSTATED_DEPLOYMENT`
- `BLOCKED_OVERSTATED_PRODUCTION`
- `BLOCKED_OVERSTATED_EXPOSURE`
- `BLOCKED_FINAL_ANSWER_GENERATION_CLAIM`
- `BLOCKED_LIVE_LLM_CLAIM`
- `BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM`
- `BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM`
- `BLOCKED_CROSS_REPO_RUNTIME_CLAIM`
- `UNKNOWN_REQUIRES_HUMAN_REVIEW`

## Required Test Coverage

Tests must prove:

1. controlled-readiness/no-action output is publishable as controlled evaluation report only;
2. developer handoff output with caveats is publishable as developer handoff;
3. progress summary output with caveats is publishable as progress summary;
4. ambiguous status without caveat requires caveat or human review;
5. production-ready claim is blocked;
6. deployed/deployment-ready claim is blocked;
7. runtime-enabled claim is blocked;
8. chat exposure enabled claim is blocked;
9. endpoint exposure enabled claim is blocked;
10. final answer generation enabled claim is blocked;
11. live LLM enabled claim is blocked;
12. DB access/DB validation claim is blocked unless framed as pending/not performed;
13. corpus mutation claim is blocked;
14. Code Evidence ingestion claim is blocked;
15. workforce-platform runtime integration claim is blocked;
16. analytics runtime integration claim is blocked;
17. nothing is safe for final answer generation in this slice;
18. output is deterministic for repeated input.

## Documentation Requirements

Create `docs/evaluation/evaluation_output_publication_gate_v0_1.md` with sections covering purpose, scope, current status, why publication gating is needed, controlled evaluation report boundary, developer handoff boundary, progress summary boundary, final answer generation boundary, chat/endpoint exposure, runtime, deployment, production, DB/validation, corpus/Code Evidence, cross-repo runtime, publication decision model, blocked claim categories, caveat behaviour, authorisations, non-authorisations, recommended next slice, and developer handoff.

The document must clearly state this is deterministic publication gate only and does not expose chat, generate final answers, call live LLMs, enable runtime retrieval, validate against or query/write a DB, mutate corpus, ingest Code Evidence, expose endpoints, or integrate workforce-platform/ezeas-analytics runtime behaviour.

## Verification

Run:

```powershell
python -m pytest tests/test_evaluation_output_publication_gate_service.py -q
python -m py_compile app/services/evaluation_output_publication_gate_service.py
git diff --check
Test-Path .pytest_tmp
git status --short
```

Remove `.pytest_tmp` if present after confirming it is the repo-local path.

## Expected Report

Report files changed, behaviour implemented, publication decisions implemented, explicit no-action confirmation, exact tests run and results, warnings or limitations, and current `git status --short`.

Suggested commit message: `minerva-evaluation-output-publication-gate-v01`
