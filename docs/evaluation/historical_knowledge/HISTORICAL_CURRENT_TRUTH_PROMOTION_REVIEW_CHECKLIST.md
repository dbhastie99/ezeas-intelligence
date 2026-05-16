# Historical Current-Truth Promotion Review Checklist

Version: v0.1

Date: 16 May 2026

## 1. Purpose

This checklist defines the review controls required before a future explicit slice may consider promoting reviewed/backfilled historical evidence to current truth.

This checklist is documentation/control only. It does not promote current truth, permit answer use, ingest source content, mutate corpus, write a database, call a live LLM, expose chat, create Code Evidence, add endpoints, add UI, or modify runtime answer behaviour.

## 2. Checklist

| Check | Required state |
| --- | --- |
| Source reviewed | Confirmed before promotion review proceeds. |
| Finding classified as promotable | Confirmed or blocked with `FINDING_CLASSIFICATION_NOT_PROMOTABLE`. |
| Ingestion/backfill decision exists where required | Linked or documented as not required with rationale. |
| Backfill completed where required | Linked or blocked with `BACKFILL_NOT_COMPLETED`. |
| Backfill validation completed where required | Linked or blocked with `BACKFILL_VALIDATION_NOT_COMPLETED`. |
| Source authority confirmed | Confirmed against source tier and review outcome. |
| Current repository truth cross-checked | Code, tests, schema, docs, and committed logs checked where relevant. |
| Supersession checked | Newer controlling repository truth identified or ruled out. |
| Conflict checked | Conflicts resolved, rejected, or blocked. |
| Duplicate checked | Existing evidence linked before any new truth is proposed. |
| Implementation state checked | Implemented/planned/partial/removed/uncertain state recorded. |
| Formal evidence gaps checked | Missing formal evidence recorded or resolved. |
| Sensitive/tenant data checked | Sensitive, personal, tenant, credential, secret, and customer-specific risks checked. |
| Proposed truth scope documented | Scope is explicit and narrow. |
| Reviewer approval captured | Required only in a future explicit promotion slice. |
| Answer-use remains separate | `AnswerUsePermitted` remains No unless separately approved. |
| No chat exposure implied | Chat exposure remains No. |

## 3. Conservative Permission Defaults

| Permission | Default |
| --- | --- |
| `CurrentTruthPromotionPermitted` | No |
| `CurrentTruthPromotionApplied` | No |
| `AnswerUsePermitted` | No |
| `CorpusMutationPermitted` | No |
| `DatabaseWritePermitted` | No |
| `ChatExposurePermitted` | No |
| `LiveLLMUsePermitted` | No |
| `CodeEvidenceIngestionPermitted` | No |

## 4. Explicit Non-Goals

- Do not ingest source content.
- Do not mutate operational corpus.
- Do not create Code Evidence.
- Do not write to database.
- Do not call live LLM.
- Do not promote current truth.
- Do not permit answer use.
- Do not expose chat.
- Do not add endpoints.
- Do not add UI.
- Do not modify runtime answer behaviour.
