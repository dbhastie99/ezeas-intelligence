# Historical Current-Truth Promotion Blocker Model

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This document defines blocker codes for future Minerva historical current-truth promotion review.

Blocker resolution does not itself promote current truth, permit answer use, ingest source content, mutate corpus, write a database, call a live LLM, expose chat, create Code Evidence, add endpoints, add UI, or modify runtime answer behaviour.

## 2. Required Blocker Codes

| Blocker code | Meaning | Required resolution |
| --- | --- | --- |
| `SOURCE_NOT_REVIEWED` | Source review is missing or incomplete. | Complete governed source review before promotion review proceeds. |
| `BACKFILL_NOT_COMPLETED` | Required backfill execution has not completed. | Complete future governed backfill execution or document why backfill is not required. |
| `BACKFILL_VALIDATION_NOT_COMPLETED` | Required post-backfill validation has not completed. | Complete validation before promotion review proceeds. |
| `FINDING_CLASSIFICATION_NOT_PROMOTABLE` | Finding classification does not support current-truth assessment. | Reclassify through governed review or reject/defer promotion. |
| `HISTORICAL_ONLY_CONTEXT` | Evidence is historical-only. | Retain historical-only unless a later explicit slice approves a different status. |
| `SUPERSEDED_BY_CURRENT_REPOSITORY_TRUTH` | Current repository truth supersedes the historical finding. | Link controlling current truth and reject or retain as historical-only. |
| `CONFLICT_REQUIRES_RESOLUTION` | Evidence conflicts with current truth or reviewed evidence. | Resolve conflict before promotion can proceed. |
| `DUPLICATE_REQUIRES_LINKING` | Finding duplicates existing governed evidence. | Link duplicate evidence instead of creating duplicate truth. |
| `REPOSITORY_CROSS_CHECK_REQUIRED` | Current repository truth has not been checked. | Complete code/test/schema/docs/log cross-check. |
| `FORMAL_EVIDENCE_GAP` | Required formal evidence is missing. | Create or link formal evidence through the appropriate governed process. |
| `IMPLEMENTATION_STATE_UNCERTAIN` | Implemented/planned/partial/removed state is unclear. | Resolve implementation state against repository evidence. |
| `SOURCE_AUTHORITY_TOO_LOW` | Source authority is insufficient for current-truth promotion. | Obtain higher-authority evidence or reject/defer promotion. |
| `SENSITIVE_OR_TENANT_DATA_RISK` | Sensitive, personal, tenant, credential, secret, or customer-specific data risk exists. | Exclude, redact, quarantine, or block promotion. |
| `PROMOTION_SCOPE_NOT_DEFINED` | Proposed truth scope is missing or too broad. | Define narrow current-truth scope before review proceeds. |
| `REVIEWER_APPROVAL_MISSING` | Required reviewer approval is missing. | Capture explicit reviewer approval in a future promotion slice. |
| `ANSWER_USE_NOT_APPROVED` | Answer-use permission is not separately approved. | Keep answer use blocked unless a separate answer-use gate approves it. |

## 3. Blocker Handling Rules

Promotion blockers must be recorded on the future promotion candidate record.

Resolving a blocker only permits reassessment.

Resolving a blocker does not promote current truth.

Resolving a blocker does not permit answer use.

Resolving a blocker does not mutate corpus.

Resolving a blocker does not write a database.

Resolving a blocker does not expose chat.

`ANSWER_USE_NOT_APPROVED` may remain present even after a future current-truth approval because answer-use permission is separate.

## 4. Explicit Non-Goals

- No source content ingestion.
- No operational corpus mutation.
- No Code Evidence ingestion.
- No live LLM calls.
- No database writes.
- No schema migrations.
- No endpoint changes.
- No UI changes.
- No current-truth promotion.
- No answer-use permission.
- No chat exposure.
- No runtime answer behaviour changes.
