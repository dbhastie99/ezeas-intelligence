# Historical Source Inventory Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template defines the safe inventory fields for historical source documents before any future domain-scoped historical backfill review.

Inventory alone does not mutate corpus, does not ingest sources, does not connect Code Evidence, does not run live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This template must not be filled with historical material until a separate explicit slice permits source inventory work.

## 2. Control References

Use this template with:

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_GAP_REGISTER.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_TIERING_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BACKFILL_PROCESS.md`

## 3. Source Tier Rules

Preserve the source tier rules from `HISTORICAL_SOURCE_TIERING_MODEL.md`:

- Tier 1 code and tests are the highest authority for implemented state, while code alone may not explain why.
- Tier 2 developer logs, hardening logs, and platform doctrine are curated decision/rationale sources requiring review and implementation-state classification.
- Tier 3 historical chats and continuance prompts are raw historical source material, not final truth, and require cross-check against code/tests/logs/doctrine/commits.

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
| Source title | Record the document title or stable source identifier. |
| Source type | Record code, test, commit, developer log, hardening log, doctrine, chat, continuance prompt, or other controlled source type. |
| Source tier | Record Tier 1, Tier 2, or Tier 3 under `HISTORICAL_SOURCE_TIERING_MODEL.md`. |
| Date or date range | Record the source date, commit date, prompt date, log date, or best-known range. |
| Repository/domain | Record repository, product area, and domain if known. |
| Related commits if known | Record commit hashes or leave `unknown`; do not infer implementation from commit references alone. |
| Related developer log or doctrine reference | Record known linked log/doctrine references or leave `unknown`. |
| Implementation-state classification | Use one of the classifications in this template. |
| Evidence confidence | Record high, medium, low, or unknown with reason. |
| Supersession risk | Record high, medium, low, or unknown with reason. |
| Backlog/doctrine/runtime distinction | Identify whether the source appears to describe backlog intent, doctrine/rationale, runtime implementation, or uncertain state. |
| Review required | Always record `yes` unless a future approved review gate says otherwise. |
| Ingestion permitted | Record `no`; inventory does not permit ingestion. |
| Notes | Record limited provenance notes only, not extracted historical claims. |

## 6. Blank Inventory Table

| Source title | Source type | Source tier | Date or date range | Repository/domain | Related commits if known | Related developer log or doctrine reference | Implementation-state classification | Evidence confidence | Supersession risk | Backlog/doctrine/runtime distinction | Review required | Ingestion permitted | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 7. Boundaries

This template does not consume historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not run live LLM, does not connect Code Evidence, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This template does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

Tax / PAYG and Imports / Actuals remain `BASELINE_REQUIRED` and `NOT_REVIEWED` until their separate formal review path changes.
