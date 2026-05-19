# Minerva Controlled Multi-Source Evidence Onboarding v0.1

Implement controlled multi-source evidence onboarding for Minerva over local fixture evidence only. Extend or wrap the existing controlled durable Developer Log retrieval harness so Minerva can deterministically retrieve across controlled fixtures for Developer Log, Hardening Log, and Platform Doctrine while preserving source authority, source type, source status, implementation status, current-truth status, answer-use boundaries, caveats, and non-action boundaries.

This slice follows `minerva-controlled-retrieval-harness-v01`, which proved deterministic retrieval over Developer Log durable evidence fixtures without live LLM, chat exposure, DB access, live corpus mutation, Code Evidence ingestion, runtime integration, or final answer generation.

## Source Scope

In scope:

- Existing Developer Log durable fixture/evidence path.
- Controlled Hardening Log fixture/evidence path.
- Controlled Platform Doctrine fixture/evidence path.
- Source authority metadata.
- Multi-source retrieval envelope.
- Focused tests.
- Saved Codex prompt artefact.
- Slice knowledge artefact.

Out of scope:

- Live document ingestion.
- Live DB retrieval.
- Chat history ingestion.
- Code Evidence ingestion.
- Live corpus mutation.
- External files outside repo fixtures.
- Final natural-language answer generation.
- Live LLM call.
- Endpoint/UI exposure.
- Runtime integration.

## Source Authority

Use deterministic source-aware ranking. Suggested authority order:

1. `PLATFORM_DOCTRINE`
2. `HARDENING_LOG`
3. `DEVELOPER_LOG`
4. `THREAD_CONTINUANCE_PROMPT`, if later modelled
5. `GENERAL_HISTORICAL_NOTE` or future lower-authority sources

Source authority is not the same as query relevance. Ranking should combine matched terms, simple deterministic query intent, source authority, source/status boundary, and answer-use safety. Do not use live LLMs, embeddings, vector search, external calls, or nondeterministic ranking.

## Retrieval Envelope Requirements

The result envelope must include query text, normalized query terms, retrieval mode, evidence universe, evidence types searched, evidence types out of scope, authority policy applied, result count, results, boundary flags, caveats, next step, unsupported evidence types, and final-answer prohibition.

Each result must include evidence type, source title, source status, authority level, implementation status, current-truth status, answer-use status, matched terms, match reasons, rank/score, can-prove statements, cannot-prove statements, required caveats, and `FinalAnswerPermitted = false`.

Every envelope must keep these flags false:

- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposureEnabled`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `LiveCorpusMutationPerformed`
- `CodeEvidenceIngestionPerformed`
- `RetrievalBackendChanged`
- `RuntimeIntegrationPerformed`
- `ProductionReadinessClaimed`

## Required Behaviours

- Platform Doctrine query should return and rank Platform Doctrine evidence highly, with caveats that doctrine is not execution proof.
- Hardening query should return and rank Hardening Log evidence highly, with caveats that hardening/prohibition evidence is not implementation proof.
- Developer Log durable evidence path query should return and rank Developer Log evidence highly, with caveats that controlled-readiness/work records are not production readiness.
- Prohibited-actions query should include/rank Hardening Log and/or Platform Doctrine highly while keeping all runtime/live boundary flags false.
- Unsupported source queries such as Code Evidence, live DB state, or Analytics Readiness Summary must not fabricate evidence and must return unsupported/out-of-scope status.
- Repeated identical queries must return the same ordered result identifiers.

## Required Artefacts

- `app/services/controlled_multi_source_evidence_retrieval_service.py`
- `tests/test_controlled_multi_source_evidence_retrieval.py`
- `docs/codex_prompts/2026-05-19_minerva_controlled_multi_source_evidence_onboarding_v0_1.md`
- `docs/slice_knowledge/2026-05-19_minerva_controlled_multi_source_evidence_onboarding_v0_1.md`

Preserve backward compatibility with existing controlled durable retrieval harness tests.

## Verification

Run appropriate repo commands, including:

- `py -m py_compile app/services/controlled_multi_source_evidence_retrieval_service.py`
- `py -m pytest tests/test_controlled_multi_source_evidence_retrieval.py -q`
- `py -m pytest tests/test_controlled_durable_evidence_retrieval_harness.py -q`
- `py -m pytest -q -k "developer_log and durable"` if relevant
- `git diff --check`
- `Test-Path .pytest_tmp`
- `Test-Path docs/codex_prompts/2026-05-19_minerva_controlled_multi_source_evidence_onboarding_v0_1.md`
- `Test-Path docs/slice_knowledge/2026-05-19_minerva_controlled_multi_source_evidence_onboarding_v0_1.md`

Suggested commit message:

`minerva-controlled-multi-source-evidence-v01`
