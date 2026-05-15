# Historical Batch Register Template

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This template defines the required columns for metadata-level historical batch registration.

Batch registration does not ingest source content, does not mutate corpus, does not connect Code Evidence, does not call live LLM, does not change runtime behaviour, does not promote baselines, does not change ledger counts, and does not perform ledger promotion.

Minerva must not treat batch-registered sources as current truth unless later reviewed, backfilled, and governed.

## 2. Required Columns

| Column | Required handling |
| --- | --- |
| Batch ID | Stable identifier for the batch registration run. |
| Register ID | Stable source register identifier or proposed identifier pending register update. |
| Source title | Human-readable title or stable source label. |
| Original filename | Metadata only; may be a discovery hint but does not control classification. |
| Source folder | Registered source folder or proposed folder for durable discovery. |
| Registered source type | Controlled source type assigned by the register. |
| Source tier | Starting source tier assigned by the register and tiering model. |
| Domain tags | Domain tags used for grouping and future backfill planning. |
| Date or date range | Source date, prompt date, log date, commit date, or best-known range. |
| Repository context | Repository, product area, branch, service, or domain context if known. |
| Related commits if known | Commit hashes or `unknown`; commit references require later review. |
| Related control artefacts | Related prompts, logs, templates, registers, gates, plans, or `unknown`. |
| Implementation-state classification | Current metadata classification, usually `UNCERTAIN_REQUIRES_REVIEW` until reviewed. |
| Review status | Current review status such as `NOT_REVIEWED`, `NEEDS_REVIEW`, or `SUPERSEDED`. |
| Ingestion permitted | Defaults to `No`; only a later explicit governed ingestion slice may change it. |
| Supersession risk | Known or suspected supersession risk, or `unknown`. |
| Evidence confidence | Confidence in provenance and metadata, not source-content truth. |
| Backfill priority | Priority for future domain backfill, such as high, medium, low, monitor, or none. |
| Full review chain required | `Yes`, `No`, or `Uncertain` based on batch triage. |
| Full review chain reason | Rationale for requiring or deferring the full review chain. |
| Suggested next action | Batch outcome or next control action. |
| Notes | Metadata notes only; do not extract historical claims as truth. |

## 3. Blank Template

| Batch ID | Register ID | Source title | Original filename | Source folder | Registered source type | Source tier | Domain tags | Date or date range | Repository context | Related commits if known | Related control artefacts | Implementation-state classification | Review status | Ingestion permitted | Supersession risk | Evidence confidence | Backfill priority | Full review chain required | Full review chain reason | Suggested next action | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  | No |  |  |  |  |  |  |  |

## 4. Boundary Notes

This template is for registration metadata only. It does not permit parsing developer logs, doctrine documents, historical chats, continuance prompts, hardening logs, code, tests, or prompt files for source-content claims.
