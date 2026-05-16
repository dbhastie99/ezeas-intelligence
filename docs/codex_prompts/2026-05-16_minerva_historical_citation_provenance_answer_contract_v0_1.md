# Minerva Historical Citation / Provenance Answer Contract v0.1 Prompt

Date: 16 May 2026

## Objective

Create the first governed citation/provenance answer contract for Minerva historical knowledge.

This slice defines what provenance must be attached to future Minerva answers across current-truth, historical-context, caveated, backlog/context, doctrine/context, hardening/context, developer-log/context, and refusal modes.

## Required Posture

Documentation/control/test hardening only.

Do not implement chat, retrieval runtime, answer synthesis runtime, citation rendering runtime, live LLM calls, source ingestion, corpus mutation, current-truth promotion, runtime answer-use activation, runtime retrieval eligibility activation, endpoint changes, UI changes, schema migrations, database writes, workforce-platform changes, award-configurator-v1 changes, or ezeas-analytics changes.

Historical sources are not answerable current truth by default. Answer-use permission does not automatically implement retrieval. Retrieval eligibility does not automatically expose chat. Answer-mode contract does not implement answer synthesis runtime. Minerva is not exposed for chat in this slice.

Boundary checklist:

- No source content ingestion
- No operational corpus mutation
- No Code Evidence ingestion
- No live LLM calls
- No database writes
- No schema migrations
- No endpoint changes
- No UI changes
- No retrieval runtime changes
- No answer synthesis runtime changes
- No citation rendering runtime changes
- No chat exposure
- No workforce-platform changes
- No award-configurator-v1 changes
- No ezeas-analytics changes
- No current-truth promotion
- No runtime answer-use permission activation
- No runtime retrieval eligibility activation

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_ANSWER_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CITATION_PROVENANCE_REFUSAL_RULES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_EVIDENCE_CHAIN_REQUIREMENTS.md`

## Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_CONTRACT.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_REFUSAL_POLICY.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_MODE_CITATION_REQUIREMENTS.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_PERMISSION_GATE.md`
- `tests/test_domain_baseline_capture_batch.py`

## Required Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Suggested Commit Message

`minerva-historical-citation-provenance-answer-contract-v01`
