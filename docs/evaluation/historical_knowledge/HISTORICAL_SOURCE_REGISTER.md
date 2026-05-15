# Historical Source Register

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This register is the durable Minerva control artefact for historical source discovery and classification.

It defines the empty source-register skeleton that future domain-scoped historical backfill slices may populate after explicit approval. It does not register actual historical chats, developer logs, hardening logs, doctrine documents, prompts, code evidence, test evidence, baseline packs, award build controls, or any other historical source in this slice.

## 2. Scope

This skeleton covers the register schema, controlled source types, review statuses, implementation-state classifications, ingestion permission rules, and future population workflow.

The register is placeholder-only. No historical source is ingested by this skeleton slice.

## 3. Register-Driven Classification Rule

Source classification is register-driven, not filename-driven. The durable rule is that source classification is register-driven, not filename-driven.

Registration validation is controlled by `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`.

Registered folders/register entries are the durable discovery mechanism for historical source discovery and classification. Filenames are metadata and hints only.

The registered source folder root is `docs/evaluation/historical_knowledge/registered_sources/`. These folders are discovery and classification aids only; files placed there still require a row in this register before they are treated as registered historical sources.

Hardcoded individual document names must not be used as the primary classification mechanism.

The register assigns source class and starting reliability tier. A registered source does not become final truth until review status, implementation-state classification, supersession status, and relevant cross-checking against code/tests/commits/logs/doctrine where relevant have been completed.

Inventory/registering a source does not itself permit ingestion.

## 4. Source Register Table

No source rows are populated in this skeleton slice.

| Register ID | Source title | Original filename | Source folder | Registered source type | Source tier | Domain tags | Date or date range | Repository context | Related commits if known | Related control artefacts | Implementation-state classification | Review status | Ingestion permitted | Supersession status | Evidence confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

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

No historical source is ingested by this skeleton slice.

## 11. Non-Goals

This skeleton does not populate real historical source rows, does not ingest historical chats, does not ingest developer logs, does not ingest doctrine documents, does not ingest code, does not mutate corpus, does not connect Code Evidence, does not run live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This skeleton does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, ledger promotion, or generated artefact creation.

## 12. Future Population Workflow

Future population requires a separate explicit slice.

1. Read the historical knowledge control index, this source register, the source tiering model, the register-driven classification model, the source inventory templates, and the backfill process.
2. Identify source folders/register entries for one domain without using filenames as the primary classifier.
3. Add placeholder or reviewed register rows only within the approved source scope.
4. Assign registered source type, source tier, review status, implementation-state classification, supersession status, evidence confidence, and ingestion permission.
5. Cross-check source claims against code/tests/commits/logs/doctrine where relevant.
6. Keep ingestion permission as `No` unless a later explicit governed ingestion slice permits ingestion.
