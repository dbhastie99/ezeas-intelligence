# Minerva Historical Answer Synthesis Enforcement Skeleton v0.1

Date: 16 May 2026

## Objective

Create the first deterministic answer synthesis enforcement skeleton for Minerva historical knowledge.

This slice introduces an in-memory, metadata-only gate that consumes supplied retrieval gate output and decides which answer mode is allowed or whether refusal is required.

## Required Posture

- Answer synthesis enforcement skeleton only.
- In-memory metadata evaluation only.
- No live LLM calls.
- No final chat answer generation.
- No live retrieval backend.
- No vector search.
- No corpus query.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No database reads or writes.
- No schema migrations.
- No endpoint changes.
- No UI changes.
- No citation rendering runtime.
- No chat exposure.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.
- No current-truth promotion.
- No runtime answer-use permission activation.
- No runtime retrieval eligibility activation beyond supplied metadata evaluation.
- No historical source may become answerable current truth in this slice.

## Artefacts

Create, if consistent with package structure:

- `app/services/historical_answer_synthesis_enforcement_skeleton_service.py`

Create docs:

- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_SYNTHESIS_ENFORCEMENT_SKELETON.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_SYNTHESIS_ENFORCEMENT_RESPONSE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_SYNTHESIS_ENFORCEMENT_FIXTURE_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_SYNTHESIS_ENFORCEMENT_GUARDRAILS.md`

Update linked historical retrieval/runtime controls and `tests/test_domain_baseline_capture_batch.py`.

## Required Behaviour

The skeleton accepts an in-memory retrieval gate output object/dictionary and returns a response containing explicit false runtime flags, an `AnswerModeDecision`, an `AllowedAnswerMode`, refusal fields, citation/caveat requirements, guardrails, non-goals, and explanation.

Eligible retrieval decisions map to answer-mode allowance decisions only. Refusal retrieval decisions preserve refusal. Missing citation/provenance, conflicted evidence, superseded current-truth evidence, not-answerable evidence, and runtime-not-implemented conditions must refuse or block.

## Verification

Run:

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `python -m py_compile app/services/historical_answer_synthesis_enforcement_skeleton_service.py`
- `git diff --check`

Clean `.pytest_tmp` if present.
