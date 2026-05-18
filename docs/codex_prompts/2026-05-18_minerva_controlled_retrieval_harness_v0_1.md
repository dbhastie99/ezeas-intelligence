# Minerva Controlled Retrieval Harness Over Durable Evidence Fixtures v0.1

## Objective

Implement a controlled local retrieval harness over existing durable evidence fixtures so Minerva can deterministically retrieve relevant Developer Log durable evidence records and return a structured retrieval envelope preserving source/status boundaries.

The harness answers in structured retrieval form only: what matched, why it matched, what the evidence can prove, what it cannot prove, whether final answer generation is permitted, whether live LLM/chat/DB/corpus mutation occurred, and the next safe step.

## Scope

- Add a controlled retrieval harness service over existing controlled durable Developer Log fixtures.
- Use deterministic keyword/metadata matching. This slice proves retrieval contract quality, not semantic/vector search quality.
- Return `QueryText`, `NormalizedQueryTerms`, `RetrievalMode`, `FixtureUniverse`, `EvidenceTypesInScope`, `EvidenceTypesOutOfScope`, `ResultCount`, `Results`, `BoundaryFlags`, `NextStep`, and `Caveats`.
- Each result must preserve record id, source type/title/status, implementation status where available, answer-use/boundary status where available, matched terms, match reasons, rank/score, can-prove and cannot-prove claims, caveat requirement, and final-answer permission.
- Add focused tests for positive retrieval, unsupported future evidence types, deterministic ordering, boundary flags, source/status preservation, and no final answer generation.
- Add this saved prompt artefact and a slice knowledge artefact.

## Non-Goals And Prohibited Actions

Do not call a live LLM, generate final user-facing natural-language answers, expose or register chat, add UI, connect to a DB, read from a DB, write to a DB, mutate live corpus, ingest Code Evidence, change retrieval backend, add vector/embedding search, change `workforce-platform`, change `ezeas-analytics`, change `award-configurator-v1`, add new evidence families beyond existing controlled Developer Log fixtures, claim runtime readiness, or claim production readiness.

Boundary flags must remain false for live LLM, final answer generation, chat exposure, DB read/write, live corpus mutation, Code Evidence ingestion, retrieval backend change, runtime integration, and production readiness.

## Expected Query Behaviours

Positive Developer Log retrieval examples:

- `Developer Log durable evidence path status`
- `What evidence says Minerva did not call a live LLM?`
- `Developer Log controlled answer path closeout`
- `What remains prohibited for Minerva Developer Log evidence?`

Unsupported future evidence examples:

- `What does the Hardening Log say?`
- `What does Platform Doctrine say?`

These unsupported queries must not fabricate evidence. They should return zero results or a clear unsupported/out-of-scope explanation.

## Expected Output Bundle

- `app/services/controlled_durable_evidence_retrieval_harness_service.py`
- `tests/test_controlled_durable_evidence_retrieval_harness.py`
- `docs/codex_prompts/2026-05-18_minerva_controlled_retrieval_harness_v0_1.md`
- `docs/slice_knowledge/2026-05-18_minerva_controlled_retrieval_harness_v0_1.md`

## Verification Commands

- `python -m py_compile app/services/controlled_durable_evidence_retrieval_harness_service.py`
- `pytest tests/test_controlled_durable_evidence_retrieval_harness.py -q`
- Run directly related existing focused Developer Log durable evidence path tests.
- `git diff --check`
- `Test-Path .pytest_tmp`

## Commit Message Suggestion

`minerva-controlled-retrieval-harness-v01`
