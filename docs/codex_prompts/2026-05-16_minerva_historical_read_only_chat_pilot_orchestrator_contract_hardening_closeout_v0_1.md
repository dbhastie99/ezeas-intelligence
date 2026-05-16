# Minerva Historical Read-Only Chat Pilot Orchestrator Contract Hardening Closeout v0.1

Date: 16 May 2026

## Slice

Minerva historical read-only chat pilot orchestrator contract hardening and closeout v0.1.

## Objective

Harden and close out the read-only chat pilot orchestrator candidate contract so it is complete enough to support a future endpoint/UI planning gate.

## Required Posture

- Contract hardening and closeout only.
- In-memory metadata orchestration only.
- No live LLM calls.
- No final natural-language answer generation.
- No endpoint changes.
- No UI changes.
- No public or internal chat exposure.
- No live retrieval backend.
- No vector search.
- No corpus query.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No database reads or writes.
- No schema migrations.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.

## Current Truth

- The orchestrator candidate is in-memory metadata-only.
- No live retrieval backend is used.
- No corpus/vector/database stores are queried.
- No live LLM is called.
- No chat endpoint/UI is exposed.
- No final natural-language answer is generated.
- No DB read/write occurs.
- No corpus mutation occurs.

## Files In Scope

Potential service update:

- `app/services/historical_read_only_chat_pilot_orchestrator_candidate_service.py`

Create docs:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CONTRACT_HARDENING.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_DECISION_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_CLOSEOUT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ENDPOINT_UI_PLANNING_ENTRY_CRITERIA.md`

Update docs/tests:

- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_FIXTURE_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_GUARDRAILS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE_CLOSEOUT_ENTRY_CRITERIA.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `tests/test_domain_baseline_capture_batch.py`

## Contract Requirements

The orchestrator response must consistently expose:

- `ChatPilotOrchestratorCandidateImplemented`
- `LiveLLMCalled`
- `FinalAnswerGenerated`
- `ChatExposed`
- `EndpointUIPresent`
- `LiveRetrievalPerformed`
- `CorpusMutationPerformed`
- `DatabaseReadPerformed`
- `DatabaseWritePerformed`
- `RetrievalGateResult`
- `AnswerSynthesisGateResult`
- `CitationRefusalGateResult`
- `PilotResponseStatus`
- `PilotResponseMode`
- `RefusalRequired`
- `RefusalReason`
- `CitationReady`
- `CaveatRequired`
- `RuntimeBoundaryAsserted`
- `Guardrails`
- `NonGoals`
- `Explanation`

Required defaults:

- `ChatPilotOrchestratorCandidateImplemented`: true
- `LiveLLMCalled`: false
- `FinalAnswerGenerated`: false
- `ChatExposed`: false
- `EndpointUIPresent`: false
- `LiveRetrievalPerformed`: false
- `CorpusMutationPerformed`: false
- `DatabaseReadPerformed`: false
- `DatabaseWritePerformed`: false
- `RuntimeBoundaryAsserted`: true

## Decision Catalog Values

- `READY_CURRENT_TRUTH_ENVELOPE`
- `READY_HISTORICAL_CONTEXT_ENVELOPE`
- `READY_CAVEATED_ENVELOPE`
- `REFUSAL_ENVELOPE`
- `BLOCKED_NO_RUNTIME_ENVELOPE`
- `REFUSE_MISSING_ANSWER_USE`
- `REFUSE_MISSING_RETRIEVAL_ELIGIBILITY`
- `REFUSE_MISSING_PROVENANCE`
- `REFUSE_MISSING_CITATION`
- `REFUSE_CONFLICTED`
- `REFUSE_SUPERSEDED`
- `REFUSE_NOT_ANSWERABLE`

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
python -m py_compile app/services/historical_read_only_chat_pilot_orchestrator_candidate_service.py
git diff --check
```

Clean `.pytest_tmp` if present.

## Report

Report files changed, whether the service was modified, test results, py_compile result, git diff check result, `.pytest_tmp` status, progress after this slice, and explicit confirmation that no prohibited runtime, ingestion, DB, endpoint/UI, chat, LLM, corpus, schema, workforce-platform, award-configurator-v1, ezeas-analytics, current-truth promotion, runtime answer-use activation, or runtime retrieval activation was introduced.

Suggested commit message: `minerva-historical-read-only-chat-pilot-orchestrator-contract-hardening-closeout-v01`
