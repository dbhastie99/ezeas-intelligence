# Minerva Controlled Answer Preparation Over Multi-Source Retrieval Results v0.1

Implement deterministic controlled answer preparation over existing controlled multi-source retrieval results.

This slice consumes the prior local fixture retrieval envelope for Developer Log, Hardening Log, and Platform Doctrine evidence, then produces a structured answer-preparation packet. It is not final answer generation, chat exposure, live LLM use, DB-backed retrieval, corpus mutation, Code Evidence ingestion, runtime integration, or production-readiness proof.

## Objective

Given a query and a multi-source retrieval envelope, produce an `AnswerPreparationEnvelope` that identifies evidence used, evidence excluded, source authority, supported claims, caveated claims, prohibited claims, missing current/runtime/DB/deployment evidence, answer outline sections, citation/provenance requirements, boundary flags, and why final answer generation remains prohibited.

## Source Boundaries

- Platform Doctrine can establish platform rules, principles, and source/status boundaries.
- Hardening Log can establish risks, prohibitions, deferred work, and required boundaries.
- Developer Log can establish work completed, tests run, implementation status, and decisions captured.
- Thread Continuance Prompt, if onboarded later, is planning/continuity evidence only.
- Historical evidence is not current truth by default.
- Controlled-readiness is not runtime readiness.
- Runtime readiness is not production readiness.
- Doctrine does not prove implementation.
- Hardening does not prove completed runtime behaviour.
- Developer Log does not prove production deployment unless deployment evidence exists.

## Required Implementation

- Add `app/services/controlled_multi_source_answer_preparation_service.py`.
- Add `tests/test_controlled_multi_source_answer_preparation.py`.
- Add this saved Codex prompt artefact.
- Add the matching slice knowledge record.
- Reuse existing controlled multi-source retrieval envelopes and boundary flags.
- Do not rewrite existing retrieval harnesses unless absolutely necessary.

## Envelope Requirements

The preparation packet should include query text, answer mode, preparation status, evidence used, evidence excluded, evidence grouped by source type, source authority summary, current-truth assessment, implementation-status assessment, required caveats, supported claims, unsupported claims, prohibited claims, claims requiring additional evidence, answer outline, citation requirements, boundary flags, final-answer prohibition, and next safe step.

Preparation status values include `PREPARED`, `PREPARED_WITH_CAVEATS`, `INSUFFICIENT_EVIDENCE`, `BLOCKED_PROHIBITED_CLAIM`, and `OUT_OF_SCOPE`.

Claim status values include `SUPPORTED`, `SUPPORTED_WITH_CAVEAT`, `UNSUPPORTED`, `PROHIBITED`, `REQUIRES_CURRENT_RUNTIME_EVIDENCE`, `REQUIRES_CODE_EVIDENCE`, `REQUIRES_DB_EVIDENCE`, and `REQUIRES_DEPLOYMENT_EVIDENCE`.

## Required Tests

Cover:

- Preparing an answer packet from multi-source retrieval.
- Separating source authority for Developer Log work-completed claims.
- Handling doctrine claims without treating doctrine as execution proof.
- Blocking prohibited overclaims such as live chat and production readiness.
- Returning insufficient evidence for current live DB state.
- Source-specific citation/provenance rules.
- Boundary flags on every output.
- Regression tests for existing retrieval services.

## Boundary Flags

Every preparation envelope must keep these false:

- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposureEnabled`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `LiveCorpusMutationPerformed`
- `CodeEvidenceIngestionPerformed`
- `RuntimeIntegrationPerformed`
- `ProductionReadinessClaimed`

`FinalAnswerPermitted` must remain false for this slice.

## Verification

Run:

- `python -m py_compile app/services/controlled_multi_source_answer_preparation_service.py`
- `python -m pytest tests/test_controlled_multi_source_answer_preparation.py -q`
- `python -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `python -m pytest tests/test_controlled_durable_evidence_retrieval_harness.py -q`
- `python -m pytest -q -k "developer_log and durable"`
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_controlled_multi_source_answer_preparation_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_controlled_multi_source_answer_preparation_v0_1.md`

Suggested commit message:

`minerva-controlled-multi-source-answer-prep-v01`
