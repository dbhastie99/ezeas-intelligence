# Minerva Historical Citation/Refusal Enforcement Skeleton v0.1

Date: 16 May 2026

## Objective

Create the first citation/refusal enforcement skeleton for Minerva historical knowledge.

This slice introduces a deterministic, in-memory, metadata-only citation/refusal gate skeleton that consumes answer synthesis skeleton output and decides whether a future answer can proceed to a citation-ready response envelope or must refuse because provenance, citation, or gate requirements are missing.

## Required Posture

- Citation/refusal enforcement skeleton only.
- In-memory metadata evaluation only.
- No live LLM calls.
- No final chat answer generation.
- No citation rendering runtime beyond metadata envelope validation.
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
- No chat exposure.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.
- No current-truth promotion.
- No runtime answer-use permission activation.
- No runtime retrieval eligibility activation beyond supplied metadata evaluation.
- No historical source may become answerable current truth in this slice.

## Artefacts

Create if consistent with existing package structure:

- `app/services/historical_citation_refusal_enforcement_skeleton_service.py`

Create docs:

- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_SKELETON.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_RESPONSE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_FIXTURE_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_REFUSAL_ENFORCEMENT_GUARDRAILS.md`

Update existing answer synthesis and runtime control docs so the citation/refusal enforcement skeleton is linked from the current governance chain.

## Required Behaviour

The service accepts supplied in-memory answer synthesis output metadata only. It returns a response containing no-runtime defaults, citation readiness fields, caveat readiness fields, guardrails, non-goals, and an explanation.

Required no-runtime defaults:

- `CitationRefusalSkeletonImplemented`: true
- `FinalAnswerGenerated`: false
- `LiveLLMCalled`: false
- `ChatExposed`: false
- `RetrievalRuntimeCalled`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `EndpointUIPresent`: false
- `RuntimeBoundaryAsserted`: true

Decision catalog:

- `CITATION_READY_CURRENT_TRUTH`
- `CITATION_READY_HISTORICAL_CONTEXT`
- `CITATION_READY_CAVEATED`
- `REFUSE_MISSING_SOURCE_ID`
- `REFUSE_MISSING_SOURCE_TITLE`
- `REFUSE_MISSING_SOURCE_DATE_OR_UNKNOWN_MARKER`
- `REFUSE_MISSING_GOVERNANCE_CHAIN`
- `REFUSE_CONFLICTED_EVIDENCE`
- `REFUSE_SUPERSEDED_EVIDENCE`
- `REFUSE_NOT_ANSWER_APPROVED`
- `REFUSE_PRIOR_GATE_REFUSAL`
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
python -m py_compile app/services/historical_citation_refusal_enforcement_skeleton_service.py
git diff --check
```

Clean `.pytest_tmp` if present.

## Execution Status

Executed in this slice. The implementation remains metadata-only and does not introduce retrieval runtime, answer synthesis runtime, citation rendering runtime, final answer generation, live LLM calls, chat exposure, endpoint/UI, database read/write, schema migration, source ingestion, corpus mutation, Code Evidence ingestion, or cross-repo changes.
