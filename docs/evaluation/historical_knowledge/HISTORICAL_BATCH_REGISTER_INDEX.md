# Historical Batch Register Index

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This index is the master discovery and governance index for Minerva historical batch registers.

The batch register index is discovery/governance metadata only. Listing a batch does not ingest source content. Listing a batch does not make sources current truth.

Future developer-log, hardening-log, doctrine, chat/continuance, code-evidence, test-evidence, award build control, baseline-pack, and mixed-source batch registers must be added here so their status, review boundary, ingestion permission, and corpus mutation state are visible before any future backfill work.

## 2. Scope

This index covers historical batch registers under `docs/evaluation/historical_knowledge/`.

It indexes batch register files and batch-level governance state. It does not index individual historical source content, does not parse source documents, does not review historical sources, and does not approve governed ingestion.

Ingestion permitted defaults to No for every listed batch unless a separate explicit governed ingestion slice changes that state.

## 3. Batch Register Index Table

| Batch ID | Batch register path | Source family | Source types covered | Date or date range | Batch status | Row count | Review status | Ingestion permitted | Corpus mutation status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIST-DEVLOG-BATCH-2026-05-15 | `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md` | Developer logs / hardening logs / platform doctrine / mixed log-doctrine sources | `DEVELOPER_LOG`, `HARDENING_LOG`, `PLATFORM_DOCTRINE`, `MIXED_LOG_DOCTRINE`, `OTHER_REQUIRES_REVIEW` | 6 December 2025 to 20 December 2025 for the initial Analytics row; future rows may use their own source dates or ranges | `ACTIVE_METADATA_ONLY` | 1 | `NOT_REVIEWED` | No | No | Metadata-only first developer-log-like batch. The listed Analytics Engine row remains unreviewed, non-ingested, not current truth, and governed by the source register and existing review controls. |

## 4. Registration Navigation Versus Review Control

This batch register index is a registration/navigation surface. It helps Minerva and developers discover which batch registers exist, how many metadata rows they contain, and the batch-level governance boundary.

`docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REVIEW_QUEUE.md` is the review-control surface. It records which registered historical sources are eligible for future deep review, which are blocked, and why.

Listing a batch here does not place a source into review. Queueing a source in the review queue does not ingest source content, make the source current truth, or permit answer use.

## 5. Batch Status Definitions

| Batch status | Meaning |
| --- | --- |
| `EMPTY_PLACEHOLDER` | Batch register exists for future use but has no source rows. It is discovery/governance metadata only. |
| `ACTIVE_METADATA_ONLY` | Batch register has one or more metadata rows, but source content has not been ingested, parsed, extracted, reviewed, or promoted. |
| `TRIAGE_IN_PROGRESS` | Batch rows are being classified or checked at metadata level. This does not permit ingestion or current-truth use. |
| `TRIAGE_COMPLETE` | Metadata triage is complete, but review, backfill, governed ingestion, and current-truth use still require separate approval. |
| `CLOSED_SUPERSEDED` | Batch register is closed because another register or control artefact supersedes it. Historical trace remains. |
| `CLOSED_MIGRATED` | Batch register is closed because its metadata has migrated to a newer governed register or index. Historical trace remains. |

## 6. Source Family Coverage

Planned future batch families include:

- developer logs / hardening logs / doctrine / mixed log-doctrine
- chat and continuance prompts
- code evidence summaries
- test evidence summaries
- award build control sources
- baseline packs
- other requires review

Each family still requires register-driven source classification. Batch family labels, source folders, and filenames are discovery aids only.

## 7. Discovery Rules

Minerva and Codex should use this index to find historical batch registers before proposing historical review, backfill, or ingestion work.

Source classification remains register-driven, not filename-driven. `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` remains the governing source classification register.

Batch register paths, source family labels, source folders, original filenames, and batch filenames may provide discovery hints. They do not determine source type, source tier, review status, implementation-state classification, ingestion permission, or current-truth authority.

Future batch registers must be added to this index with batch status, row count, review status, ingestion permission, corpus mutation status, and notes before they are used by a backfill workflow.

## 8. Review and Ingestion Boundaries

Listing a batch does not ingest source content.

Listing a batch does not make sources current truth.

Ingestion permitted defaults to No.

Minerva must not treat batch-listed sources as current truth unless later reviewed/backfilled/governed through the applicable historical knowledge control path.

Batch-listed sources remain non-authoritative until review status, implementation-state classification, supersession status, and relevant cross-checking against code/tests/commits/logs/doctrine where relevant have been completed and governed.

This index does not perform or approve review approval, governed ingestion, historical ingestion, corpus mutation, Code Evidence integration, live LLM calls, runtime changes, endpoint changes, UI changes, baseline promotion, ledger promotion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, or generated artefact creation.

For audit searchability: no corpus mutation, no ingestion, no Code Evidence integration, no live LLM, no runtime change, no baseline promotion, no ledger promotion, no review approval, no governed ingestion, no historical ingestion, no recapture, no benchmark execution, no corpus coverage execution, no answer-gap execution, and no generated artefact changes occur in this slice.

## 9. Non-Goals

This slice does not:

- ingest historical chats
- ingest developer logs
- ingest doctrine documents
- ingest code
- parse or extract historical source content
- review historical sources
- mutate corpus
- connect Code Evidence
- call live LLM
- change runtime behaviour
- promote baselines
- implement DB writes
- implement migrations
- add endpoint changes
- add UI changes
- change workforce-platform
- change award-configurator-v1
- change ezeas-analytics
- approve review
- permit governed ingestion
- perform historical ingestion
- recapture baselines
- run benchmark execution
- run corpus coverage execution
- run answer-gap execution
- perform promotion
- update ledgers
- perform ledger promotion
- create generated artefacts

## 10. Future Batch Workflow

Future batch-register creation or population requires a separate explicit slice.

1. Read `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`, this index, the source register, the register-driven classification model, the batch registration and triage model, the batch register template, and the relevant intake guidance.
2. Create or update the batch register with metadata only.
3. Add or update this index row with the batch path, source family, source types covered, date or date range, batch status, row count, review status, ingestion permission, corpus mutation status, and notes.
4. Keep `Ingestion permitted` as No unless a later explicit governed ingestion slice changes it.
5. Keep unreviewed sources as `NOT_REVIEWED` unless a later explicit review decision changes them.
6. Do not treat any batch-listed source as current truth unless later reviewed, backfilled, and governed.
7. Escalate high-value/high-risk sources to the full review chain only when a separate review/backfill slice requires it.

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_historical_batch_register_index_v0_1.md`.
