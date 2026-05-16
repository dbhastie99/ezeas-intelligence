# Minerva Historical Read-Only Gated Retrieval Skeleton Contract Hardening v0.1

Date: 16 May 2026

## Purpose

Create and execute the durable control artefact for Minerva historical read-only gated retrieval skeleton contract hardening v0.1.

## Objective

Harden the read-only gated retrieval skeleton contract so the response shape, decision catalog, fixture catalog, guardrails, expected outcomes, and no-runtime assertions are complete enough to support a later answer-synthesis enforcement skeleton.

## Scope

This slice may strengthen `app/services/historical_read_only_gated_retrieval_skeleton_service.py` only for deterministic in-memory metadata evaluation and response consistency.

Create:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_CONTRACT_HARDENING.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_DECISION_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_GATED_RETRIEVAL_CONTRACT_CLOSEOUT.md`

Update the existing read-only gated retrieval skeleton docs, runtime expected outcomes, no-runtime assertions, retrieval gate design, historical knowledge control index, and focused tests in `tests/test_domain_baseline_capture_batch.py`.

## Required Posture

- Read-only skeleton contract hardening only.
- In-memory metadata evaluation only.
- No live retrieval backend.
- No vector search.
- No corpus query.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No live LLM calls.
- No database reads or writes.
- No schema migrations.
- No endpoint changes.
- No UI changes.
- No answer synthesis runtime.
- No citation rendering runtime.
- No chat exposure.
- No workforce-platform, award-configurator-v1, or ezeas-analytics changes.
- No current-truth promotion.
- No runtime answer-use activation.
- No runtime retrieval activation beyond supplied metadata evaluation.
- No historical source may become answerable current truth in this slice.

## Required Response Contract

The skeleton response must consistently expose:

- `RetrievalGateSkeletonImplemented`
- `LiveRetrievalPerformed`
- `LiveLLMCalled`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `EndpointUIPresent`
- `RetrievalDecision`
- `RetrievalMode`
- `ExpectedAnswerMode`
- `RefusalReason`
- `CitationRequired`
- `CaveatRequired`
- `RuntimeBoundaryAsserted`
- `Guardrails`
- `NonGoals`
- `Explanation`

Required defaults are true for `RetrievalGateSkeletonImplemented` and `RuntimeBoundaryAsserted`, and false for all live/runtime side-effect fields.

## Required Decisions

- `ELIGIBLE_CURRENT_TRUTH_RETRIEVAL`
- `ELIGIBLE_HISTORICAL_CONTEXT_RETRIEVAL`
- `ELIGIBLE_CAVEATED_RETRIEVAL`
- `REFUSE_MISSING_ANSWER_USE_PERMISSION`
- `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY`
- `REFUSE_MISSING_PROVENANCE`
- `REFUSE_CONFLICTED_EVIDENCE`
- `REFUSE_SUPERSEDED_EVIDENCE`
- `REFUSE_HISTORICAL_CONTEXT_NOT_CURRENT_TRUTH`
- `REFUSE_NOT_ANSWERABLE`
- `BLOCKED_RUNTIME_NOT_IMPLEMENTED`

`RuntimeActionPermitted` must remain No for all decisions.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
python -m py_compile app/services/historical_read_only_gated_retrieval_skeleton_service.py
git diff --check
```

Remove `.pytest_tmp` if present.

## Progress Target

After this slice, narrow safe internal chat pilot readiness should move to about 93%. The next recommended slice is the answer synthesis enforcement skeleton. This slice does not authorize live retrieval, backend, LLM, chat, database, corpus, endpoint/UI, answer synthesis, citation rendering, or current-truth promotion behaviour.
