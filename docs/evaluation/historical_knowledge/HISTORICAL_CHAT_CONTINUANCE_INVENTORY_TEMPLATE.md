# Historical Chat and Continuance Inventory Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template inventories historical chats, continuance prompts, and related prompts as raw historical source material, not final truth.

Chats and prompts require cross-check against code/tests/logs/doctrine/commits before any candidate decision can be classified. They must not be ingested directly as truth.

Inventory alone does not mutate corpus, does not ingest sources, does not connect Code Evidence, does not run live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

## 2. Control References

Use this template with:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

## 3. Source Tier Rules

Historical chats and continuance prompts are Tier 3 raw historical source material, not final truth.

Tier 3 material must be cross-check against code/tests/logs/doctrine/commits before implementation-state classification. Tier 1 code and tests remain the highest authority for implemented state. Tier 2 developer logs, hardening logs, and platform doctrine remain curated decision/rationale sources requiring review.

## 4. Implementation-State Classifications

Use exactly one current implementation-state classification unless a later review gate records why multiple states apply:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## 5. Inventory Fields

| Field | Required handling |
| --- | --- |
| Source title | Record the chat, continuance, or prompt title. |
| Source type | Record historical chat, continuance prompt, prompt, or related raw source type. |
| Source tier | Record Tier 3 unless a reviewed exception is documented. |
| Date or date range | Record chat date, prompt date, or best-known range. |
| Repository/domain | Record repository, product area, and domain if known. |
| Related commits if known | Record commit hashes or leave `unknown`; do not infer implementation from chat claims. |
| Related developer log or doctrine reference | Record linked logs/doctrine or leave `unknown`. |
| Implementation-state classification | Use one of the classifications in this template after cross-check. |
| Evidence confidence | Record high, medium, low, or unknown with reason. |
| Supersession risk | Record high, medium, low, or unknown with reason. |
| Backlog/doctrine/runtime distinction | Identify backlog intent, doctrine/rationale, runtime implementation claim, or uncertain state. |
| Review required | Always record `yes` unless a future approved review gate says otherwise. |
| Ingestion permitted | Record `no`; inventory does not permit ingestion. |
| Notes | Record limited provenance notes only, not extracted historical claims. |

## 6. Blank Inventory Table

| Source title | Source type | Source tier | Date or date range | Repository/domain | Related commits if known | Related developer log or doctrine reference | Implementation-state classification | Evidence confidence | Supersession risk | Backlog/doctrine/runtime distinction | Review required | Ingestion permitted | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 7. Boundaries

This template does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This template does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.
