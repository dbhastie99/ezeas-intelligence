# Historical Code Evidence Inventory Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template inventories code, tests, and related code evidence as the highest authority for implemented state.

Source classification is register-driven, not filename-driven. Registered folders and source-register entries are the durable discovery mechanism. Original filename is metadata and may be a hint only. Hardcoded individual document names must not be used as the primary source classification mechanism.

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
| Original filename | Record the original filename as metadata only; it may be a hint but must not drive classification. |
| Source folder | Record the registered source folder used for durable discovery. |
| Registered source type | Record `CODE_EVIDENCE`, `TEST_EVIDENCE`, or `OTHER_REQUIRES_REVIEW` as assigned by the register. |
| Source tier | Record the starting reliability tier assigned by the register; usually Tier 1 for code/tests unless a reviewed exception is documented. |
| Domain tags | Record controlled domain tags relevant to the source. |
| Date or date range | Record file date, commit date, test date, or best-known range. |
| Repository context | Record repository, product area, branch/context, and domain if known. |
| Related commits if known | Record commit hashes or leave `unknown`; commits require review for provenance. |
| Related control artefacts | Record rationale references, prompts, review gates, inventories, or leave `unknown`; code alone may not explain why. |
| Implementation-state classification | Use one of the classifications in this template after review. |
| Review status | Record review status. A registered source can remain `NOT_REVIEWED` and must not be relied on as platform truth. |
| Ingestion permitted | Record `No`; inventory does not permit ingestion. |
| Supersession status | Record current, superseded, partially superseded, or unknown with reason. |
| Evidence confidence | Record high, medium, low, or unknown with reason. |
| Notes | Record limited provenance notes only, not extracted historical claims. |

## 6. Blank Inventory Table

| Source title | Original filename | Source folder | Registered source type | Source tier | Domain tags | Date or date range | Repository context | Related commits if known | Related control artefacts | Implementation-state classification | Review status | Ingestion permitted | Supersession status | Evidence confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 7. Boundaries

This template does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This template does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

This template does not ingest any historical documents, does not parse actual developer logs, does not parse doctrine documents, does not parse chats, does not connect Code Evidence, does not promote baselines, and does not perform ledger promotion.
