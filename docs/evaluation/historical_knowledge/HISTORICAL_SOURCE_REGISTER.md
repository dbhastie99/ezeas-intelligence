# Historical Source Register

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This register is the durable Minerva control artefact for historical source discovery and classification.

It defines the source-register skeleton and the first controlled source inventory row. This slice registers one analytics developer log at metadata level only. It does not ingest actual historical chats, developer logs, hardening logs, doctrine documents, prompts, code evidence, test evidence, baseline packs, award build controls, or any other historical source content.

## 2. Scope

This skeleton covers the register schema, controlled source types, review statuses, implementation-state classifications, ingestion permission rules, and future population workflow.

This register now contains the first controlled inventory entry and first controlled registered-source placement placeholder. No historical source is ingested by this skeleton slice. No historical source is ingested by this inventory slice. No historical source is ingested by this placement slice.

## 3. Register-Driven Classification Rule

Source classification is register-driven, not filename-driven. The durable rule is that source classification is register-driven, not filename-driven.

Registration validation is controlled by `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`.

Registered folders/register entries are the durable discovery mechanism for historical source discovery and classification. Filenames are metadata and hints only.

The registered source folder root is `docs/evaluation/historical_knowledge/registered_sources/`. These folders are discovery and classification aids only; files placed there still require a row in this register before they are treated as registered historical sources.

Hardcoded individual document names must not be used as the primary classification mechanism.

The register assigns source class and starting reliability tier. A registered source does not become final truth until review status, implementation-state classification, supersession status, and relevant cross-checking against code/tests/commits/logs/doctrine where relevant have been completed.

Inventory/registering a source does not itself permit ingestion. Folder placement alone is not ingestion.

The register entry controls classification. Original filenames are metadata only. A placeholder path records registered placement; it does not mean the full historical document has been ingested.

## 4. Source Register Table

The first populated row is metadata-only. The source remains external/user-provided until a future controlled source-placement or backfill slice.

| Register ID | Source title | Original filename | Source folder | Registered source type | Source tier | Domain tags | Date or date range | Repository context | Related commits if known | Related control artefacts | Implementation-state classification | Review status | Ingestion permitted | Supersession status | Evidence confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HIST-ANALYTICS-2025-12-06-20 | Developer Log - Analytics Engine | Developer Log - Analytics Engine (5).docx | `docs/evaluation/historical_knowledge/registered_sources/developer_logs/HIST_ANALYTICS_2025_12_06_20_SOURCE_PLACEHOLDER.md` | `DEVELOPER_LOG` - developer-authored historical analytics working material requiring review and implementation-state confirmation | Tier 2 | Analytics; Workforce Analytics DB; Golden Slice; ObjectTime; ProcessedRule; CalcInterpreterLine Replatform Review; Power BI; Reconciliation Reporting | 6 December 2025 to 20 December 2025 | Historical analytics server / workforce analytics context | unknown | `HISTORICAL_SOURCE_TIERING_MODEL.md`; `HISTORICAL_BACKFILL_PROCESS.md`; `HISTORICAL_REGISTER_DRIVEN_SOURCE_CLASSIFICATION.md`; `HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md` | `UNCERTAIN_REQUIRES_REVIEW` - current implementation state requires code confirmation and is not fully current | `NOT_REVIEWED` | No | `PARTIALLY_SUPERSEDED_BY_CALCINTERPRETERLINE_MODEL` - supersession risk because `CalcInterpreterLine` is the current target calculation fact source | Medium/high for historical rationale; requires code confirmation for current implementation | Metadata-level registration and placeholder placement only. Folder placement alone is not ingestion. The full historical document has not been ingested. Register entry controls classification; original filename is metadata only. `ProcessedRule`-era analytics requires review before being treated as current; `CalcInterpreterLine` is the current target calculation fact source for processed payroll analytics. Future analytics backfill must cross-check against current code, tests, database views, schema/scripts, and commits. |

## 5. Required Register Fields

| Field | Required handling |
| --- | --- |
| Register ID | Stable register identifier assigned by a future explicit population slice. |
| Source title | Human-readable title or stable source identifier. |
| Original filename | Metadata only; may be a hint but must not drive source classification. |
| Source folder | Registered source folder used for durable discovery and provenance. |
| Registered source type | One controlled source type assigned by the register. |
| Source tier | Starting reliability tier assigned by this register and the source tiering model. |
| Domain tags | Controlled domain tags relevant to the source. |
| Date or date range | Source date, commit date, prompt date, log date, or best-known range. |
| Repository context | Repository, product area, branch/context, and domain if known. |
| Related commits if known | Commit hashes or `unknown`; commit references require review and cross-checking. |
| Related control artefacts | Linked prompts, control documents, review gates, inventories, doctrine, logs, or `unknown`. |
| Implementation-state classification | One controlled implementation-state classification from this register. |
| Review status | One controlled review status from this register. |
| Ingestion permitted | `No` unless a later explicit governed ingestion slice permits ingestion. |
| Supersession status | Current, superseded, partially superseded, or unknown with reason. |
| Evidence confidence | High, medium, low, or unknown with reason. |
| Notes | Limited provenance notes only, not extracted historical claims as truth. |

## 6. Source Type Definitions

| Source type | Definition |
| --- | --- |
| `DEVELOPER_LOG` | Developer-authored historical log or working note requiring review. |
| `HARDENING_LOG` | Historical hardening, remediation, or quality-control log requiring review. |
| `PLATFORM_DOCTRINE` | Durable platform doctrine or design rule requiring implementation-state classification. |
| `MIXED_LOG_DOCTRINE` | Source combining logs, decisions, doctrine, or backlog notes requiring careful separation. |
| `CHAT_OR_CONTINUANCE` | Historical chat, continuance prompt, or conversation-derived source; raw material, not final truth. |
| `CODE_EVIDENCE` | Code-derived source used to confirm implemented state, not rationale by itself. |
| `TEST_EVIDENCE` | Test-derived source used to confirm expected or covered behaviour. |
| `PROMPT_FILE` | Prompt/control artefact source requiring review before reliance. |
| `BASELINE_PACK` | Baseline, benchmark, coverage, or answer-gap pack requiring provenance review. |
| `AWARD_BUILD_CONTROL` | Award build or award configurator control source requiring domain review. |
| `OTHER_REQUIRES_REVIEW` | Any source that does not fit the controlled types and requires explicit review. |

## 7. Source Tier Defaults

| Source type | Default tier |
| --- | --- |
| `CODE_EVIDENCE` | Tier 1 |
| `TEST_EVIDENCE` | Tier 1 |
| `DEVELOPER_LOG` | Tier 2 |
| `HARDENING_LOG` | Tier 2 |
| `PLATFORM_DOCTRINE` | Tier 2 |
| `MIXED_LOG_DOCTRINE` | Tier 2 by default, or lower if mixed provenance creates unresolved uncertainty. |
| `CHAT_OR_CONTINUANCE` | Tier 3 |
| `PROMPT_FILE` | Requires review; tier depends on prompt/control role and provenance. |
| `BASELINE_PACK` | Requires review; tier depends on generated artefact provenance and review status. |
| `AWARD_BUILD_CONTROL` | Requires review; tier depends on control role and implementation cross-checking. |
| `OTHER_REQUIRES_REVIEW` | Requires review before tier assignment. |

## 8. Review Status Definitions

| Review status | Definition |
| --- | --- |
| `NOT_REVIEWED` | Registered or placeholder source has not been reviewed. |
| `NEEDS_REVIEW` | Source requires review before it can be used for a backfill draft. |
| `REVIEWED_READY_FOR_BACKFILL_DRAFT` | Source has been reviewed enough to support a curated backfill draft, not ingestion. |
| `REVIEWED_READY_FOR_GOVERNED_INGESTION` | Source has completed required review and may be considered by a separate governed ingestion slice. |
| `SUPERSEDED` | Source has been replaced or invalidated by later source material, code, tests, commits, or doctrine. |

## 9. Implementation-State Classifications

Use exactly one current implementation-state classification unless a later review gate records why multiple states apply:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## 10. Ingestion Permission Rules

Inventory/registering a source does not itself permit ingestion.

`Ingestion permitted` must remain `No` for all sources until a separate explicit governed ingestion slice changes that state after review status, implementation-state classification, supersession status, and relevant cross-checking are complete.

No historical source is ingested by this skeleton slice. No historical source is ingested by this inventory slice. No historical source is ingested by this placement slice.

## 11. Non-Goals

This skeleton, first inventory row, and first placement placeholder do not ingest historical chats, do not ingest developer logs, do not ingest doctrine documents, do not ingest code, do not mutate corpus, do not connect Code Evidence, do not run live LLM, do not change runtime behaviour, do not promote baselines, and do not change ledger counts.

This skeleton and placement slice do not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, ledger promotion, or generated artefact creation.

The Analytics Engine developer log registered as `HIST-ANALYTICS-2025-12-06-20` is source material, not current final truth. It is intended to support later analytics replatform planning and must not be used for direct Minerva ingestion without a separate governed slice.

## 12. Future Population Workflow

Future population requires a separate explicit slice.

1. Read the historical knowledge control index, this source register, the source tiering model, the register-driven classification model, the source inventory templates, and the backfill process.
2. Identify source folders/register entries for one domain without using filenames as the primary classifier.
3. Add placeholder or reviewed register rows only within the approved source scope.
4. Assign registered source type, source tier, review status, implementation-state classification, supersession status, evidence confidence, and ingestion permission.
5. Cross-check source claims against code/tests/commits/logs/doctrine where relevant.
6. Keep ingestion permission as `No` unless a later explicit governed ingestion slice permits ingestion.
