# Minerva Historical Retrieval Eligibility Gate v0.1 Prompt

Date: 16 May 2026

## Objective

Create the first governed retrieval eligibility gate for Minerva historical knowledge.

This slice defines how future Minerva retrieval must decide whether evidence can be retrieved for current-truth answer mode, historical-context mode, caveated answer mode, backlog/context mode, doctrine/context mode, or must be excluded/refused.

## Required Posture

- Documentation/control/test hardening only.
- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No live LLM calls.
- No database writes.
- No schema migrations.
- No endpoint changes.
- No UI changes.
- No retrieval runtime changes.
- No chat exposure.
- No workforce-platform changes.
- No award-configurator-v1 changes.
- No ezeas-analytics changes.
- No current-truth promotion.
- No runtime answer-use permission activation.
- No runtime retrieval eligibility activation.
- No historical source may become answerable current truth in this slice.

## Current Truth

Historical sources are not answerable current truth by default.

Current-truth promotion does not automatically permit answer use.

Answer-use permission does not automatically implement retrieval.

Answer-use permission does not expose chat.

Retrieval eligibility must remain separate from answer-use permission and chat exposure.

Minerva is not exposed for chat yet.

This slice must not mutate operational corpus content or live evidence stores.

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ELIGIBILITY_BLOCKER_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_ANSWER_MODE_MAPPING.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_RETRIEVAL_EXCLUSION_RULES.md`

## Update

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_PERMISSION_GATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_PERMISSION_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_ANSWER_USE_SCOPE_RULES.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_CURRENT_TRUTH_PROMOTION_CONTROL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`
- `tests/test_domain_baseline_capture_batch.py`

## Required Controls

The gate must define retrieval eligibility statuses, preconditions, answer-use dependency, current-truth dependency, evidence-scope to retrieval-mode mapping, retrieval mode rules, exclusion rules, conflict/supersession handling, citation/provenance requirements, insufficient-evidence/refusal boundary, chat exposure boundary, runtime boundary, blocker handling, non-goals, and developer handoff.

The template must include conservative defaults: `CurrentTruthPermitted` No, `HistoricalContextPermitted` No, `RetrievalEligible` No, `ChatEligible` No, `CaveatRequired` Yes, and `CitationRequired` Yes.

The blocker model, answer-mode mapping, and exclusion rules must remain control documents only and must not implement retrieval runtime or chat behaviour.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

## Progress Note

After this slice, narrow safe internal chat pilot readiness should move from about 59% to about 64%.

Remaining major phases: answer-mode contract, insufficient-evidence/refusal policy, citation/provenance answer contract, retrieval runtime implementation planning, and pilot read-only chat surface.
