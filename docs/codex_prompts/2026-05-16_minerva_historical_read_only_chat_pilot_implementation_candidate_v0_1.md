# Minerva Historical Read-Only Chat Pilot Implementation Candidate v0.1

Date: 16 May 2026

## Objective

Create a narrow read-only chat pilot implementation candidate for Minerva historical knowledge.

The slice introduces a deterministic in-memory pilot orchestration helper that chains the existing read-only gated retrieval skeleton, answer synthesis enforcement skeleton, and citation/refusal enforcement skeleton using supplied metadata only.

## Required Posture

- Read-only pilot implementation candidate only.
- In-memory metadata orchestration only.
- No live LLM calls.
- No final natural-language chat answer generation beyond deterministic envelope/status output.
- No public chat exposure.
- No endpoint/UI creation.
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
- No current-truth promotion.
- No runtime answer-use permission activation beyond supplied metadata evaluation.
- No runtime retrieval eligibility activation beyond supplied metadata evaluation.
- No historical source may become answerable current truth in this slice.

## Expected Artefacts

- `app/services/historical_read_only_chat_pilot_orchestrator_candidate_service.py`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_RESPONSE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_FIXTURE_CATALOG.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_ORCHESTRATOR_GUARDRAILS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_READ_ONLY_CHAT_PILOT_IMPLEMENTATION_CANDIDATE_CLOSEOUT_ENTRY_CRITERIA.md`

Update the existing go/no-go closeout, implementation candidate entry criteria, closeout decision record, remaining runtime boundaries, safety test pack, historical knowledge control index, and baseline capture batch test file.

## Orchestrator Contract

The helper accepts supplied in-memory metadata only and returns an orchestration envelope with conservative runtime flags:

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

Allowed envelope modes are `READY_CURRENT_TRUTH_ENVELOPE`, `READY_HISTORICAL_CONTEXT_ENVELOPE`, `READY_CAVEATED_ENVELOPE`, `REFUSAL_ENVELOPE`, and `BLOCKED_NO_RUNTIME_ENVELOPE`.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
python -m py_compile app/services/historical_read_only_chat_pilot_orchestrator_candidate_service.py
git diff --check
```

Clean `.pytest_tmp` if present.
