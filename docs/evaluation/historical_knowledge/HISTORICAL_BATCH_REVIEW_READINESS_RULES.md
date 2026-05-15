# Historical Batch Review Readiness Rules

Version: v0.1

Date: 16 May 2026

## 1. Purpose

These rules define when a metadata-only historical batch source may move to `READY_FOR_DEEP_REVIEW` in `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE.md`.

Readiness is a queue-control state only. It does not perform deep review, ingestion, backfill, corpus mutation, current-truth promotion, or answer-use approval.

## 2. Required Readiness Rules

A source may become `READY_FOR_DEEP_REVIEW` only when all rules are satisfied:

| Rule | Requirement |
| --- | --- |
| `SOURCE_ID_EXISTS` | A stable source id exists in the source register or batch register. |
| `SOURCE_LOCATION_OR_ATTACHMENT_REFERENCE_EXISTS` | A controlled source location or attachment reference exists so a future reviewer can locate the source without ingesting it. |
| `SOURCE_TYPE_IDENTIFIED` | The source type is identified through register-driven classification. |
| `REPOSITORY_DOMAIN_RELEVANCE_IDENTIFIED` | Repository relevance and domain relevance are identified. |
| `DATE_OR_APPROXIMATE_DATE_RECORDED` | A source date, date range, or approximate controlled date is recorded. |
| `CURRENT_TRUTH_RISK_ASSESSED` | The risk that the source could be mistaken for current truth is assessed. |
| `DUPLICATE_SUPERSESSION_RISK_ASSESSED` | Duplicate and supersession risk is assessed. |
| `CROSS_CHECK_REPOSITORIES_IDENTIFIED` | Required cross-check repositories, code areas, tests, schemas, commits, or doctrine surfaces are identified. |
| `EXPECTED_REVIEW_OUTPUTS_IDENTIFIED` | Expected review outputs are identified, including review pack, cross-check findings, decision gate update, or decision record as applicable. |
| `INGESTION_REMAINS_NO_BEFORE_REVIEW` | Ingestion remains `No` before review. |
| `ANSWERABILITY_REMAINS_NO_BEFORE_REVIEW` | Answerability remains `No` before review. |

## 3. Readiness Boundary

`READY_FOR_DEEP_REVIEW` does not mean ingested.

`READY_FOR_DEEP_REVIEW` does not mean current truth.

`READY_FOR_DEEP_REVIEW` does not mean Minerva may answer from it.

`READY_FOR_DEEP_REVIEW` does not mean source content has been parsed, extracted, summarized, cross-checked, backfilled, or promoted.

`REVIEW_COMPLETE_NOT_INGESTED` still does not permit answer use until a separate governed ingestion/backfill decision exists.

## 4. Candidate Selection Eligibility

`READY_FOR_DEEP_REVIEW` only makes a source eligible for candidate selection under `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_CANDIDATE_SELECTION.md`.

`READY_FOR_DEEP_REVIEW` does not start review, ingestion, answer use, or current-truth promotion.

Candidate selection remains a separate governed control stage. It may identify a future review candidate, but it does not perform deep review, ingest source content, mutate operational corpus, create Code Evidence, write databases, call live LLM, or permit Minerva to answer from historical material.

## 5. Decision Record Authorization Before Review Execution

`READY_FOR_DEEP_REVIEW` and `CANDIDATE_SELECTED_FOR_REVIEW` do not authorise review execution until a decision record permits review start.

The decision record must follow `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_DECISION_RECORD.md` and explicitly set `ReviewStartPermitted: Yes` before any future deep review begins.

Until that explicit decision exists, ingestion remains `No`, answer use remains `No`, current truth remains `No`, operational corpus mutation remains `No`, Code Evidence ingestion remains `No`, and live LLM use remains `No`.

## 6. Status Transition Controls

Only a future explicit review-control slice may move a source into `READY_FOR_DEEP_REVIEW`, `REVIEW_IN_PROGRESS`, or `REVIEW_COMPLETE_NOT_INGESTED`.

Any transition must preserve:

- `IngestionPermitted: No` unless a separate governed ingestion slice explicitly changes it
- `AnswerUsePermitted: No` before governed ingestion/backfill approval
- source register authority over classification
- repository separation from workforce-platform, award-configurator-v1, and ezeas-analytics
- the rule that historical sources are not current truth unless reviewed, cross-checked, backfilled, and governed

## 7. Non-Goals

These rules do not ingest source content, mutate corpus, connect Code Evidence, call live LLM, write databases, create schema migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, promote current truth, or permit Minerva answer use from historical material.
