# Historical Backfill Execution Safety Checklist

Version: v0.1

Date: 16 May 2026

This checklist is required before any future Minerva historical backfill dry-run or apply step is considered.

This slice is design/control only. It does not execute backfill, ingest source content, mutate corpus, create Code Evidence, write to a database, call a live LLM, promote current truth, permit answer use, or expose chat.

| Check | Required state | Status |
| --- | --- | --- |
| Source reviewed | Source reviewed through governed historical review. | Not completed in this slice. |
| Ingestion/backfill decision approved | Decision-control record approves planning only. | Not completed in this slice. |
| No unresolved blockers | Blockers cleared or safely deferred with rationale. | Not completed in this slice. |
| Source scope frozen | Included and excluded sources/findings recorded. | Not completed in this slice. |
| Source authority confirmed | Authority tier and governing source status recorded. | Not completed in this slice. |
| Supersession checked | Superseded material excluded or historical-only labelled. | Not completed in this slice. |
| Conflict checked | Conflicting finding handling recorded. | Not completed in this slice. |
| Duplicate checked | Duplicate evidence linked or not-duplicate rationale recorded. | Not completed in this slice. |
| Sensitive data checked | Sensitive data excluded, controlled, or blocked. | Not completed in this slice. |
| Tenant data checked | Tenant data excluded, controlled, or blocked. | Not completed in this slice. |
| Extraction plan reviewed | Evidence extraction boundaries reviewed. | Not completed in this slice. |
| Dry-run completed in future slice | Dry-run result exists from a later explicit dry-run slice. | Not completed in this slice. |
| Reviewer approval captured | Reviewer approval recorded before apply. | Not completed in this slice. |
| No answer-use permission implied | Answer-use permission remains separate and No. | Required. |
| No current-truth promotion implied | Current-truth promotion remains separate and No. | Required. |

## Required Defaults

| Permission | Required value |
| --- | --- |
| `BackfillExecutionPermitted` | No |
| `BackfillDryRunPermitted` | No, unless a later explicit dry-run slice approves it |
| `CorpusMutationPermitted` | No |
| `DatabaseWritePermitted` | No |
| `CurrentTruthPromotionPermitted` | No |
| `AnswerUsePermitted` | No |
| `ChatExposurePermitted` | No |
| `CodeEvidenceIngestionPermitted` | No |
| `LiveLLMUsePermitted` | No |

## Explicit Non-Goals

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
