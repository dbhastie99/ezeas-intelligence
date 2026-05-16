# Minerva Historical Read-Only Gated Retrieval Skeleton Candidate v0.1

Date: 16 May 2026

## Durable Control Prompt

Create the first read-only gated retrieval skeleton candidate for Minerva historical knowledge after the historical runtime implementation test matrix v0.1.

The skeleton must be deterministic, in-memory, and metadata-only. It may evaluate supplied metadata against answer-use permission, retrieval eligibility, answer-mode, citation/provenance, conflict/supersession, current-truth, historical-context, caveat, and refusal rules.

It must not perform live retrieval, vector search, corpus query, database read/write, source content ingestion, operational corpus mutation, Code Evidence ingestion, live LLM calls, schema migrations, endpoint changes, UI changes, answer synthesis runtime, citation rendering runtime, chat exposure, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, current-truth promotion, runtime answer-use activation, or runtime retrieval activation beyond in-memory metadata evaluation.

Create if consistent with the repo:

- `app/services/historical_read_only_gated_retrieval_skeleton_service.py`

Create docs:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_SKELETON_CANDIDATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_RESPONSE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_FIXTURE_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_GUARDRAILS.md`

Update runtime matrix, expected outcomes, no-runtime assertions, retrieval gate design, chat pilot implementation entry criteria, historical knowledge control index, and focused tests in `tests/test_domain_baseline_capture_batch.py`.

Required service defaults:

- `RetrievalGateSkeletonImplemented`: true
- `LiveRetrievalPerformed`: false
- `LiveLLMCalled`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `EndpointUIPresent`: false
- `RuntimeBoundaryAsserted`: true

Required decision behavior:

- Missing, blocked, revoked, rejected, or superseded answer-use permission refuses.
- Missing, blocked, revoked, rejected, or excluded retrieval eligibility refuses.
- Missing or incomplete provenance refuses.
- Unresolved/conflicted evidence without approved caveat refuses.
- Superseded evidence refuses current-truth answers.
- Historical-context-only evidence does not become current truth.
- Fully approved current-truth metadata returns eligible current-truth retrieval decision.
- Historical-context approved metadata returns historical-context eligible decision.
- Caveat-required metadata preserves `CaveatRequired: true`.

Verification required:

- `python -m pytest tests/test_domain_baseline_capture_batch.py -q`
- `python -m py_compile app/services/historical_read_only_gated_retrieval_skeleton_service.py`
- `git diff --check`
- clean `.pytest_tmp` if present

Suggested commit message:

`minerva-historical-read-only-gated-retrieval-skeleton-candidate-v01`
