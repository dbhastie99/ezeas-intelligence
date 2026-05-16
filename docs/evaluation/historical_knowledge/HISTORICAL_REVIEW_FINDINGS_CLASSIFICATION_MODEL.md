# Historical Review Findings Classification Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines the governed findings classification model for Minerva historical deep review.

Findings classification happens after future governed deep-review findings have been captured. It classifies each finding for downstream outcome decision control without ingesting source content, mutating corpus, promoting current truth, or permitting answer use.

## 2. Scope

This model applies to findings produced from `docs/evaluation/historical_knowledge/HISTORICAL_DEEP_REVIEW_FINDINGS_OUTPUT_TEMPLATE.md` or a governed successor.

It is documentation/control guidance only. It does not perform deep review, ingest source content, backfill corpus, mutate operational evidence, promote current truth, or change answer synthesis.

## 3. Classification Status Model

| Classification status | Meaning |
| --- | --- |
| `CLASSIFICATION_NOT_STARTED` | Findings exist or are expected, but classification has not started. |
| `CLASSIFICATION_IN_PROGRESS` | A reviewer is assigning classifications and recording required cross-check state. |
| `CLASSIFICATION_BLOCKED` | Classification cannot proceed because source identity, findings linkage, repository context, cross-check access, or decision record linkage is missing. |
| `CLASSIFICATION_COMPLETED_FINDINGS_ONLY` | Findings have been classified, but no outcome, ingestion, answer-use, or current-truth decision has been approved. |
| `CLASSIFICATION_REQUIRES_CROSS_CHECK` | Classification indicates repository or cross-repository checks are required before outcome decision. |
| `CLASSIFICATION_READY_FOR_OUTCOME_DECISION` | Classification is complete enough for a separate governed outcome decision to be considered. |
| `CLASSIFICATION_REJECTED` | The finding is rejected under current controls. |
| `CLASSIFICATION_SUPERSEDED` | The finding is superseded by newer or more authoritative repository/source truth. |

## 4. Finding Classification Types

| Finding classification type | Meaning |
| --- | --- |
| `CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL` | The finding may be relevant to current truth, but is not current truth and requires later governed approval. |
| `HISTORICAL_ONLY_CONTEXT` | The finding is useful for project narrative, audit history, or source chronology only. |
| `SUPERSEDED_BY_CURRENT_REPOSITORY_TRUTH` | The finding is superseded by current repository files, current platform doctrine, latest committed logs, or newer approved evidence. |
| `DUPLICATE_OF_EXISTING_EVIDENCE` | The finding duplicates existing evidence and should link to that evidence rather than create new current truth. |
| `CONFLICTS_WITH_CURRENT_TRUTH` | The finding conflicts with current repository truth or approved evidence and must not be promoted or used for answers. |
| `BACKLOG_OR_FOLLOW_UP_ITEM` | The finding records work that may need later backlog or follow-up handling. |
| `PLATFORM_DOCTRINE_CANDIDATE` | The finding may affect workforce/platform/runtime doctrine and requires relevant cross-checking. |
| `HARDENING_REQUIREMENT_CANDIDATE` | The finding may become a hardening requirement after later governed decision. |
| `DEVELOPER_LOG_CONTEXT` | The finding provides developer-log context but does not establish current truth. |
| `NOT_RELEVANT` | The finding is not relevant to the active review scope. |
| `REQUIRES_REPOSITORY_CROSS_CHECK` | The finding cannot be classified for outcome until current repository evidence is checked. |

## 5. Classification Requirements

Every finding must link to `FindingsRecordId`, `DecisionRecordId`, `SourceId`, source reference, reviewer, review date, repository context, and domain context.

Every finding must receive a classification type.

Every finding must record whether cross-check is required.

Every finding must record whether it conflicts with current repository truth.

Every finding must record whether it appears superseded or duplicate.

Every finding must record recommended next decision.

Every finding must preserve ingestion No, answer use No, and current truth No unless a later decision changes them.

## 6. Cross-Check Requirements

Cross-checking must be identified and completed where relevant before a finding can advance to outcome decision:

- `workforce-platform` cross-check where source affects workforce/platform/runtime doctrine.
- `award-configurator-v1` cross-check where source affects award build/configuration/parser/interpreter truth.
- `ezeas-analytics` cross-check where source affects analytics/reporting schema/view/readiness truth.
- `ezeas-intelligence` cross-check where source affects Minerva retrieval/evidence/answering doctrine.

Cross-checks must compare against current repository files, latest committed logs, current platform doctrine, hardening logs, and completed-domain baseline evidence where applicable.

## 7. Conflict Handling

Conflicting evidence must not be promoted.

Conflicting evidence must not be answerable current truth.

Conflict requires decision-record update before ingestion or answer use can be considered.

Historical source must not override newer repository/source truth without explicit decision rationale.

## 8. Supersession Handling

Superseded findings remain historical context only unless separately preserved.

Superseded findings must not be used as current answer truth.

Duplicate findings should link to existing evidence rather than create new current truth.

## 9. Current-Truth Candidate Boundary

`CURRENT_TRUTH_CANDIDATE_REQUIRES_APPROVAL` is not current truth.

Approval requires separate outcome decision, ingestion/backfill decision, and answer-use decision.

Candidate status does not permit Minerva answer use.

## 10. Historical-Only Boundary

Historical-only findings may be useful for project narrative and audit history.

Historical-only findings must not override current truth.

Historical-only findings must be labelled historical in any future retrieval use.

## 11. Answer-Use Boundary

Answer-use remains No for all classifications in this slice.

Answer-use requires explicit future governed approval.

Minerva chat exposure must respect answer-use permission.

## 12. Ingestion Boundary

Classification does not ingest source content.

Classification does not mutate corpus.

Classification may recommend future ingestion consideration but does not approve it.

Classification is a prerequisite for ingestion/backfill decision control through `docs/evaluation/historical_knowledge/HISTORICAL_INGESTION_BACKFILL_DECISION_CONTROL.md`, but classification is not permission to ingest, backfill, mutate corpus, promote current truth, or permit answer use.

## 13. What Findings Classification Does Not Mean

Creating classification docs does not perform deep review.

Classification does not ingest source content.

Classification does not promote current truth.

Classification does not permit answer use.

Classification does not mutate operational corpus.

Classification does not create Code Evidence.

Classification does not write to a database.

Classification does not call a live LLM.

## 14. Developer Handoff

Future developers must classify completed findings before any outcome decision, ingestion/backfill decision, current-truth decision, or answer-use decision can be considered.

Use `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_FINDING_CLASSIFICATION_TEMPLATE.md` for individual finding classification records and `docs/evaluation/historical_knowledge/HISTORICAL_REVIEW_OUTCOME_DECISION_MODEL.md` for the later outcome decision path.

Do not ingest source content, mutate operational corpus, create Code Evidence, call live LLM, write databases, create migrations, change endpoints, change UI, change workforce-platform, change award-configurator-v1, change ezeas-analytics, promote current truth, permit answer use, or execute deep review merely because findings classification exists.
