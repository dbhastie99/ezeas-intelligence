# Historical Developer Log Batch Intake Guidance

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This guidance defines how operators may safely add many historical developer logs, hardening logs, platform doctrine documents, and mixed log/doctrine sources to the historical developer-log batch register.

This is intake guidance only. It creates metadata-registration controls for future batch rows. It does not ingest, parse, review, or extract historical source content.

Adding a file to a registered folder is not ingestion. Adding a batch row is metadata registration only. Original filename is metadata only. Register entries drive classification, not filenames.

## 2. Scope

Use this guidance with `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md` and the historical batch model.

The intended path is ordinary batch registration and triage first. The Analytics Engine source has demonstrated the full deep-review path, but that path is not the default for ordinary developer-log-like materials.

Ordinary logs can remain batch-registered until needed. Full review chain is required only for high-value/high-risk sources.

Minerva must not treat batch-registered sources as current truth unless later reviewed/backfilled/governed.

## 3. Intake Inputs

Operators may use metadata available from controlled placement context, source register context, batch planning notes, repository context, date ranges, and stable source labels.

Operators must not parse or extract historical source content for claims during intake. If metadata is insufficient, classify the source conservatively as `OTHER_REQUIRES_REVIEW` or use `UNCERTAIN_REQUIRES_REVIEW` where the column requires implementation-state classification.

Do not rely on filenames as authority. A filename may be a discovery hint only.

## 4. Registered Folder Placement

Registered folders are discovery aids. Adding a file to a registered folder is not ingestion and does not make the source current truth.

Use the closest registered folder when metadata supports it:

| Folder | Usual source type |
| --- | --- |
| `registered_sources/developer_logs/` | `DEVELOPER_LOG` |
| `registered_sources/hardening_logs/` | `HARDENING_LOG` |
| `registered_sources/platform_doctrine/` | `PLATFORM_DOCTRINE` |
| `registered_sources/mixed_log_doctrine/` | `MIXED_LOG_DOCTRINE` |
| `registered_sources/other_requires_review/` | `OTHER_REQUIRES_REVIEW` |

Folder placement is not enough. Register entries drive classification, not filenames or folders.

## 5. Register ID Convention

Use stable IDs that preserve source family and date. The recommended patterns are:

- `HIST-DEVLOG-YYYY-MM-DD-NNN`
- `HIST-HARDENING-YYYY-MM-DD-NNN`
- `HIST-DOCTRINE-YYYY-MM-DD-NNN`
- `HIST-MIXED-YYYY-MM-DD-NNN`

Use `NNN` as a zero-padded sequence for that source family and date, such as `001`, `002`, or `003`.

When a precise source date is unknown, use the best controlled date range in the date column and choose a conservative register ID date from the batch context only when that convention has been approved by the operator.

## 6. Batch Row Creation

Adding a batch row is metadata registration only. A row must not include extracted implementation claims, quoted historical source content, or unreviewed doctrine as current truth.

Use one row per source unless grouping is safer and clearer. Developer logs can be grouped by domain/date range where appropriate, provided the row preserves enough metadata to locate the materials later and no high-value/high-risk escalation condition requires individual deep review.

Default row values:

- `Review status`: `NOT_REVIEWED`
- `Ingestion permitted`: `No`
- `Implementation-state classification`: `UNCERTAIN_REQUIRES_REVIEW` unless the operator has strong evidence from the document/register context
- `Full review chain required`: `No` or `Uncertain` for ordinary logs; `Yes` only when escalation criteria apply

## 7. Source Type Selection

Use the registered source type that best matches the source metadata:

| Source type | Use when |
| --- | --- |
| `DEVELOPER_LOG` | Developer-authored historical working notes, implementation logs, or engineering decision logs. |
| `HARDENING_LOG` | Historical hardening, remediation, reliability, control, or defect-prevention notes. |
| `PLATFORM_DOCTRINE` | Platform doctrine, operating model, durable design principle, or formal guidance source. |
| `MIXED_LOG_DOCTRINE` | A source combines log-like implementation history with doctrine or guidance. |
| `OTHER_REQUIRES_REVIEW` | Metadata is insufficient, conflicting, or outside the controlled source types. |

If a title or filename suggests one type but register context suggests another, follow the register context and record the uncertainty in metadata notes.

## 8. Domain Tagging Guidance

Assign one or more domain tags from controlled metadata context. Use `unknown` or `requires review` when the operator lacks reliable metadata.

Required domain tags include:

- Worker Story
- ObjectTime / Source Truth
- Process Periods / PayRun Lifecycle
- Payroll Buckets / Bases / Totals
- Deductions and Obligations
- Tax / PAYG
- Imports / Actuals
- Leave Workflow / Annual Leave
- Award Configurator
- Analytics
- Reconciliation
- Finalised Correction / ObjectTime Route Guard

Domain tags support grouping and future backfill planning. They do not make any historical source authoritative.

## 9. Implementation-State Classification Guidance

Implementation-state classification should default to `UNCERTAIN_REQUIRES_REVIEW` unless the operator has strong evidence from the document/register context.

Do not infer implemented state from a filename, folder, source title, or unreviewed historical note. Implementation claims that may affect current answers require later code/test/schema confirmation through the review chain.

## 10. Review Status and Ingestion Defaults

`Review status` defaults to `NOT_REVIEWED`.

`Ingestion permitted` defaults to `No`.

A batch row does not authorize governed ingestion, historical ingestion, review approval, backfill evidence reliance, Code Evidence connection, current-truth answering, or corpus mutation.

## 11. Triage Priority Guidance

Use priority to organize future work, not to promote truth:

| Priority | Use when |
| --- | --- |
| `high` | Metadata indicates high-risk domain impact, current-answer risk, or likely architecture significance. |
| `medium` | Source may support future backfill but has no immediate current-answer risk. |
| `low` | Source appears useful as context but can wait. |
| `monitor` | Source may be superseded, duplicated, or dependent on later platform changes. |
| `none` | Source is registered for completeness only. |

Ordinary developer logs can remain batch-registered until needed by domain backfill, current-answer risk review, supersession review, or review-readiness planning.

## 12. Full Review Chain Escalation Guidance

Escalate to full review-readiness, decision-gate, code/test/schema cross-check, findings, and decision-record controls when any of these apply:

- Source contains a major architecture decision.
- Source may affect current Minerva answers.
- Source contains implementation claims that need code/test/schema confirmation.
- Source may be superseded by later platform changes.
- Source contains conflicting claims.
- Source covers high-risk payroll/source-truth/tax/imports/reconciliation/deduction/leave/worker-story/analytics/award-configurator/finalised-correction domains.

Full review chain is required only for high-value/high-risk sources. Batch registration remains acceptable for ordinary logs until a later controlled slice needs them.

## 13. Quality Checks Before Commit

Before committing intake guidance or future batch-row additions:

- Confirm no historical source content was ingested, parsed, reviewed, or extracted.
- Confirm every new row keeps `Ingestion permitted` as `No` unless a separate governed ingestion slice explicitly changed it.
- Confirm every new row keeps `Review status` as `NOT_REVIEWED` unless a separate review decision changed it.
- Confirm uncertain implementation state remains `UNCERTAIN_REQUIRES_REVIEW`.
- Confirm original filename is metadata only.
- Confirm register entries drive classification, not filenames.
- Confirm ordinary logs are not escalated to the full review chain without a high-value/high-risk reason.
- Confirm Minerva is not permitted to treat batch-registered sources as current truth unless later reviewed/backfilled/governed.

## 14. Non-Goals

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
- change ledger counts
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

For audit searchability: no corpus mutation, no ingestion, no Code Evidence integration, no live LLM, no runtime change, no baseline promotion, no ledger promotion, and no ledger update occur in this slice.

## 15. Example Rows

These examples are metadata-only examples. They do not contain real source content and must not be treated as evidence.

| Batch ID | Register ID | Source title | Original filename | Source folder | Registered source type | Source tier | Domain tags | Date or date range | Repository context | Related commits if known | Related control artefacts | Implementation-state classification | Review status | Ingestion permitted | Supersession risk | Evidence confidence | Backfill priority | Full review chain required | Full review chain reason | Suggested next action | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HIST-DEVLOG-BATCH-2026-05-15` | `HIST-DEVLOG-2026-05-15-001` | Example developer log group | `example-devlog-title.md` | `registered_sources/developer_logs/` | `DEVELOPER_LOG` | Tier 2 | Worker Story; ObjectTime / Source Truth | 2026-05-15 | example repository context | unknown | batch intake guidance | `UNCERTAIN_REQUIRES_REVIEW` | `NOT_REVIEWED` | No | unknown | metadata only | medium | Uncertain | grouped ordinary logs; review only if needed | REGISTER_AND_MONITOR | Metadata-only example; no source content extracted. |
| `HIST-DEVLOG-BATCH-2026-05-15` | `HIST-HARDENING-2026-05-15-001` | Example hardening note | `example-hardening-note.md` | `registered_sources/hardening_logs/` | `HARDENING_LOG` | Tier 2 | Reconciliation; Finalised Correction / ObjectTime Route Guard | 2026-05-15 | example repository context | unknown | batch intake guidance | `UNCERTAIN_REQUIRES_REVIEW` | `NOT_REVIEWED` | No | possible later change | metadata only | high | Yes | high-risk domain metadata; requires review before reliance | NEEDS_FULL_REVIEW_CHAIN | Metadata-only example; no source content extracted. |
| `HIST-DEVLOG-BATCH-2026-05-15` | `HIST-DOCTRINE-2026-05-15-001` | Example doctrine source | `example-platform-doctrine.md` | `registered_sources/platform_doctrine/` | `PLATFORM_DOCTRINE` | Tier 2 | Analytics; Award Configurator | 2026-05-15 | example repository context | unknown | batch intake guidance | `UNCERTAIN_REQUIRES_REVIEW` | `NOT_REVIEWED` | No | unknown | metadata only | medium | Uncertain | doctrine requires review before current-answer use | NEEDS_DOMAIN_REVIEW | Metadata-only example; no source content extracted. |
| `HIST-DEVLOG-BATCH-2026-05-15` | `HIST-MIXED-2026-05-15-001` | Example mixed log/doctrine source | `example-mixed-source.md` | `registered_sources/mixed_log_doctrine/` | `MIXED_LOG_DOCTRINE` | Tier 2 | Payroll Buckets / Bases / Totals; Tax / PAYG | 2026-05-15 | example repository context | unknown | batch intake guidance | `UNCERTAIN_REQUIRES_REVIEW` | `NOT_REVIEWED` | No | unknown | metadata only | high | Yes | high-risk payroll/tax metadata; requires review before reliance | NEEDS_FULL_REVIEW_CHAIN | Metadata-only example; no source content extracted. |
