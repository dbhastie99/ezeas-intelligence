# Historical Developer Log and Doctrine Inventory Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template inventories developer logs, hardening logs, and doctrine documents as curated decision/rationale sources requiring review and implementation-state classification.

Source classification is register-driven, not filename-driven. Registered folders and source-register entries are the durable discovery mechanism. Original filename is metadata and may be a hint only. Hardcoded individual document names must not be used as the primary source classification mechanism.

Developer logs and doctrine may include planned, partial, superseded, or backlog work. They must not be treated as implemented runtime truth without cross-checking code, tests, commits, and current doctrine.

Inventory alone does not mutate corpus, does not ingest sources, does not connect Code Evidence, does not run live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

## 2. Control References

Use this template with:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

## 3. Source Tier Rules

Developer logs, hardening logs, and platform doctrine are Tier 2 curated decision/rationale sources requiring review and implementation-state classification.

Tier 2 material can explain rationale, accepted doctrine, or intended backlog, but it does not override Tier 1 code and tests for implemented state. Chats and continuance prompts remain Tier 3 raw historical source material, not final truth.

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
| Source title | Record the log or doctrine title. |
| Original filename | Record the original filename as metadata only; it may be a hint but must not drive classification. |
| Source folder | Record the registered source folder used for durable discovery. |
| Registered source type | Record `DEVELOPER_LOG`, `HARDENING_LOG`, `PLATFORM_DOCTRINE`, `MIXED_LOG_DOCTRINE`, or `OTHER_REQUIRES_REVIEW` as assigned by the register. |
| Source tier | Record the starting reliability tier assigned by the register; usually Tier 2 unless a reviewed exception is documented. |
| Domain tags | Record controlled domain tags relevant to the source. |
| Date or date range | Record log date, doctrine date, or best-known range. |
| Repository context | Record repository, product area, branch/context, and domain if known. |
| Related commits if known | Record commit hashes or leave `unknown`; commits require separate review. |
| Related control artefacts | Record related prompts, review gates, log, hardening log, doctrine, or inventory references. |
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
