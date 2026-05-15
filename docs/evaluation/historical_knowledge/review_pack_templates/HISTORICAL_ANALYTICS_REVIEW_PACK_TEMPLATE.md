# Historical Analytics Review Pack Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template records a controlled review/backfill pack for a historical analytics source.

Historical source review pack creation does not ingest the source. It does not make any historical analytics source current truth. Minerva must not answer from a historical analytics source as current truth until the source has been reviewed, backfilled, and governed by a later explicit ingestion decision.

## 2. Source Register Details

| Field | Value |
| --- | --- |
| Register ID |  |
| Source title |  |
| Original filename |  |
| Registered source type |  |
| Source tier |  |
| Review status |  |
| Ingestion permitted |  |
| Reviewer |  |
| Review date |  |
| Historical domain tags |  |
| Source summary |  |

## 3. Source Material Boundary

| Field | Value |
| --- | --- |
| Historical implemented-state claims |  |
| Historical doctrine claims |  |
| Historical backlog/future-state claims |  |

Record only reviewed claims in this section. Do not extract, parse, or summarize unreviewed source content as current truth.

## 4. Review Preconditions

| Field | Value |
| --- | --- |
| Supersession risk |  |
| Code/test/schema cross-check required |  |

The reviewer must confirm source registration, source tier, review status, ingestion permission, supersession risk, and required cross-check scope before any evidence pack is treated as ready for backfill drafting.

## 5. Historical Architecture Summary

Use this section only after source review. Separate historical implementation descriptions from durable analytics doctrine and future-state/backlog notes.

## 6. Still-Valid Decisions

List only decisions confirmed as still valid by review and cross-checking. Include reviewer rationale for each retained decision.

## 7. Superseded or At-Risk Decisions

List decisions, schema/view assumptions, implementation paths, or reporting facts that are superseded, partially superseded, at risk, or uncertain. Include the evidence that drives the classification.

## 8. Current Code/Test/Schema Cross-Check

| Field | Value |
| --- | --- |
| Code/test/schema cross-check result |  |

Record current code, tests, schema, SQL views, and commit evidence checked by the reviewer. If no cross-check has been performed, state that explicitly.

## 9. Current Truth Classification

| Field | Value |
| --- | --- |
| Current implementation classification |  |
| Current doctrine classification |  |
| Current backlog classification |  |

Use the historical backfill implementation-state classifications. Do not classify a source as current truth merely because it is registered or historically useful.

## 10. Analytics Replatform Implications

Record implications for analytics replatform work, including any separation between historical `ProcessedRule`-era implementation assumptions and current `CalcInterpreterLine` target modelling.

## 11. Minerva Answering Implications

| Field | Value |
| --- | --- |
| Minerva-safe answer boundaries |  |

State exactly what Minerva may and may not answer from the reviewed pack. If the source is not reviewed/backfilled/governed, Minerva must not answer from it as current truth.

## 12. Backfill Evidence Pack Recommendation

| Field | Value |
| --- | --- |
| Backfill recommendation |  |
| Reviewer rationale |  |

Record whether a curated backfill evidence pack should be created, deferred, or blocked.

## 13. Ingestion Decision

Record the ingestion decision. Default is `No` unless a later explicit governed ingestion slice permits ingestion after review, cross-checking, and approval.

## 14. Non-Goals

Review pack draft readiness does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, does not perform ledger promotion, and does not perform historical ingestion.

This template does not implement DB writes, migrations, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, or generated artefact creation.

## 15. Required Follow-Up Actions

| Field | Value |
| --- | --- |
| Follow-up actions |  |

List required follow-up actions before backfill evidence pack creation, governed ingestion, or Minerva answer use can be considered.
