# Historical Register-Driven Source Classification

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This model locks in the Minerva historical knowledge rule that source classification is register-driven, not filename-driven.

Minerva follows registered source folders and source-register entries in `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` as the durable discovery mechanism. Individual filenames are metadata and may be hints only. Hardcoded individual document names must not be used as the primary source classification mechanism.

The registered source folder root is `docs/evaluation/historical_knowledge/registered_sources/`. These folders provide starting discovery and classification context only; source classification remains controlled by source-register entries.

Registered folders and source-register entries are the durable discovery mechanism.

Registered folders and source-register entries as the durable discovery mechanism are the stable way to discover historical sources.

A document does not need to be named Developer Log, Hardening Log, Doctrine, Continuance Prompt, or any other exact phrase to be treated as that source type. Registered folders and source-register entries determine source class and starting reliability tier.

## 2. Classification Rule

The register assigns source class and starting reliability tier. `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` is the durable register that controls those assignments. The filename is retained as provenance metadata, not as the governing classifier.

A document can be classified as one of the controlled source types even if the filename does not contain those exact words:

- `DEVELOPER_LOG`
- `HARDENING_LOG`
- `PLATFORM_DOCTRINE`
- `MIXED_LOG_DOCTRINE`
- `CHAT_OR_CONTINUANCE`
- `CODE_EVIDENCE`
- `TEST_EVIDENCE`
- `PROMPT_FILE`
- `BASELINE_PACK`
- `AWARD_BUILD_CONTROL`
- `OTHER_REQUIRES_REVIEW`

## 3. Register Fields

Every historical source register must include these fields before a source can be considered registered:

| Field | Required handling |
| --- | --- |
| Source title | Human-readable title or stable source identifier. |
| Original filename | Metadata only; may be a hint but must not drive source classification. |
| Source folder | Registered folder used for durable discovery and provenance. |
| Registered source type | One controlled source type assigned by the register. |
| Source tier | Starting reliability tier assigned by the register and tiering model. |
| Domain tags | Controlled domain tags relevant to the source. |
| Date or date range | Source date, commit date, prompt date, log date, or best-known range. |
| Repository context | Repository, product area, and branch/context if known. |
| Related commits if known | Commit hashes or `unknown`; commit references require review. |
| Related control artefacts | Linked prompts, control documents, review gates, inventories, or doctrine references. |
| Implementation-state classification | One controlled implementation-state classification. |
| Review status | Review state such as `NOT_REVIEWED`, `IN_REVIEW`, `REVIEWED_BLOCKED`, or `REVIEWED_READY_FOR_INGESTION`. |
| Ingestion permitted | `No` unless a later governed ingestion slice explicitly permits ingestion. |
| Supersession status | Current, superseded, partially superseded, or unknown. |
| Evidence confidence | High, medium, low, or unknown with reason. |
| Notes | Limited provenance notes only, not unreviewed historical claims as truth. |

## 4. Source Tier Rules

Code and tests are highest authority for implemented state. Code alone may prove what exists, but may not explain why a decision was made.

Developer logs, hardening logs, and platform doctrine are curated decision/rationale sources requiring review and implementation-state classification. Logs and doctrine may explain why, but may include planned, partial, superseded, or backlog work.

Historical chats and continuance prompts are raw historical source material, not final truth, and require cross-checking. Chats may contain valuable context, but must not be ingested directly as truth.

## 5. Implementation-State Classifications

Use exactly one current implementation-state classification unless a later review gate records why multiple states apply:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## 6. Review And Reliance Rule

A registered source does not become final truth until review status, implementation-state classification, supersession status, and relevant cross-checking have been completed.

Final reliance requires cross-checking against code/tests/commits/logs/doctrine where relevant. The required cross-check depends on source class and claim type: implemented-state claims require code/tests evidence; rationale claims require logs/doctrine/commits where available; chat or continuance claims require cross-checking before any candidate decision is promoted.

Example safe state:

| Registered | Registered source type | Review status | Implementation-state classification | Ingestion permitted |
| --- | --- | --- | --- | --- |
| Yes | `DEVELOPER_LOG` | `NOT_REVIEWED` | `UNCERTAIN_REQUIRES_REVIEW` | No |

This example is registered, but it is not platform truth and must not be ingested as truth.

## 7. Slice Boundaries

This slice does not ingest any historical documents, does not parse actual developer logs, does not parse doctrine documents, does not parse chats, does not ingest code, does not mutate corpus, does not connect Code Evidence, does not run live LLM, does not change runtime behaviour, does not promote baselines, and does not change ledger counts.

This slice does not implement DB writes, migrations, corpus mutation, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, ledger promotion, or generated artefact creation.
