# Historical Code Evidence Inventory Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template inventories code, tests, and related code evidence as the highest authority for implemented state.

Code/tests can confirm implemented behaviour, but code alone may not explain why a decision was made. Rationale still requires cross-check against logs, doctrine, commits, and reviewed historical sources.

Inventory alone does not mutate corpus, does not ingest sources, does not connect Code Evidence, does not run live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

## 2. Control References

Use this template with:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

## 3. Source Tier Rules

Code and tests are Tier 1 and the highest authority for implemented state.

Tier 1 material does not automatically explain rationale. Developer logs, hardening logs, and platform doctrine are Tier 2 curated decision/rationale sources requiring review. Historical chats and continuance prompts are Tier 3 raw historical source material, not final truth.

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
| Source title | Record file, test, module, commit, or code evidence title. |
| Source type | Record code, test, commit, code-derived evidence, or related implementation source type. |
| Source tier | Record Tier 1 for code/tests unless a reviewed exception is documented. |
| Date or date range | Record file date, commit date, test date, or best-known range. |
| Repository/domain | Record repository, product area, and domain if known. |
| Related commits if known | Record commit hashes or leave `unknown`; commits require review for provenance. |
| Related developer log or doctrine reference | Record rationale references or leave `unknown`; code alone may not explain why. |
| Implementation-state classification | Use one of the classifications in this template after review. |
| Evidence confidence | Record high, medium, low, or unknown with reason. |
| Supersession risk | Record high, medium, low, or unknown with reason. |
| Backlog/doctrine/runtime distinction | Identify runtime implementation, test coverage state, doctrine/rationale gap, or uncertain state. |
| Review required | Always record `yes` unless a future approved review gate says otherwise. |
| Ingestion permitted | Record `no`; inventory does not permit ingestion. |
| Notes | Record limited provenance notes only, not extracted historical claims. |

## 6. Blank Inventory Table

| Source title | Source type | Source tier | Date or date range | Repository/domain | Related commits if known | Related developer log or doctrine reference | Implementation-state classification | Evidence confidence | Supersession risk | Backlog/doctrine/runtime distinction | Review required | Ingestion permitted | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 7. Boundaries

This template does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This template does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.
