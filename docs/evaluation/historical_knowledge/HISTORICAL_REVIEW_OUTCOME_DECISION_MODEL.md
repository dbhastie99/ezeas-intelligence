# Historical Review Outcome Decision Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed outcome decision model for classified Minerva historical deep-review findings.

Outcome decisions summarize the result of findings classification and identify whether a later governed ingestion, answer-use, current-truth, backlog, rejection, duplicate, supersession, or cross-check decision path may be considered.

## 2. Scope

This model applies only after findings have been captured and classified through `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDINGS_CLASSIFICATION_MODEL.md`.

It does not ingest source content, mutate operational corpus, create Code Evidence, write databases, call live LLMs, change endpoints, change UI, change external repositories, promote current truth, or permit answer use.

## 3. Outcome Decision Status Model

| Outcome decision status | Meaning |
| --- | --- |
| `OUTCOME_NOT_DECIDED` | No governed outcome decision has been recorded. |
| `OUTCOME_REQUIRES_CROSS_CHECK` | Required cross-checks remain incomplete before any further decision can be considered. |
| `OUTCOME_HISTORICAL_ONLY` | The classified finding is retained as historical context only. |
| `OUTCOME_SUPERSEDED` | The classified finding is superseded by newer or more authoritative truth. |
| `OUTCOME_DUPLICATE` | The classified finding duplicates existing evidence and should link to that evidence. |
| `OUTCOME_REJECTED` | The classified finding or source path is rejected under current controls. |
| `OUTCOME_BACKLOG_CAPTURE_REQUIRED` | The classified finding should be captured in a later governed backlog/follow-up path. |
| `OUTCOME_CURRENT_TRUTH_CANDIDATE` | The classified finding may be considered for current-truth approval later, but is not current truth. |
| `OUTCOME_READY_FOR_INGESTION_DECISION` | A later ingestion decision may be considered, but ingestion is not approved. |
| `OUTCOME_READY_FOR_ANSWER_USE_DECISION` | A later answer-use decision may be considered, but answer use is not approved. |

## 4. Decision Boundaries

Outcome decision does not ingest.

Outcome decision does not permit answer use unless a later answer-use decision explicitly approves it.

Outcome decision does not promote current truth unless a later current-truth decision explicitly approves it.

`OUTCOME_READY_FOR_INGESTION_DECISION` only means a later ingestion decision may be considered.

`OUTCOME_READY_FOR_ANSWER_USE_DECISION` only means a later answer-use decision may be considered.

Outcome decision does not mutate operational corpus, create Code Evidence, write to a database, call a live LLM, create migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, or change runtime behaviour.

## 5. Required Inputs

Before recording an outcome decision, the decision path must have:

- `FindingClassificationId`
- `FindingsRecordId`
- `DecisionRecordId`
- `SourceId`
- `FindingId`
- classification status
- finding classification type
- cross-check requirement and status
- conflict assessment
- supersession assessment
- duplicate assessment
- reviewer
- classified timestamp

## 6. Developer Handoff

Future developers must treat outcome decisions as control-state summaries only. They may point to later ingestion/backfill/current-truth/answer-use decision work, but they do not approve that work.

Any future ingestion, backfill, current-truth promotion, or Minerva chat exposure requires a separate governed slice.
