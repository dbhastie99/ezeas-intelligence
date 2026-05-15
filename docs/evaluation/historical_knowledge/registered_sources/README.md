# Registered Historical Source Folders

Version: v0.1

Date: 15 May 2026

This folder is the registered source folder root for Minerva historical knowledge controls: `docs/evaluation/historical_knowledge/registered_sources/`.

Registration validation is governed by `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER_VALIDATION_RUNBOOK.md`.

Registered folders are a discovery and classification aid, not automatic truth. A file placed in a registered folder still requires a source register entry in `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` before it is treated as a registered historical source.

Filenames are metadata and hints only. Source classification remains register-driven through the source register, review status, implementation-state classification, supersession status, and relevant cross-checking.

No historical source is ingested merely by placing it in a folder. No corpus mutation, Code Evidence integration, live LLM call, runtime change, baseline promotion, ledger promotion, review approval, governed ingestion, historical ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, or generated artefact creation occurs from this folder structure.

## Controlled Folders

| Folder | Starting source type | Starting reliability |
| --- | --- | --- |
| `developer_logs/` | `DEVELOPER_LOG` | Tier 2 |
| `hardening_logs/` | `HARDENING_LOG` | Tier 2 |
| `platform_doctrine/` | `PLATFORM_DOCTRINE` | Tier 2 |
| `mixed_log_doctrine/` | `MIXED_LOG_DOCTRINE` | Tier 2 by default, or lower if mixed provenance creates unresolved uncertainty |
| `chat_continuance/` | `CHAT_OR_CONTINUANCE` | Tier 3 |
| `code_evidence/` | `CODE_EVIDENCE` | Tier 1 |
| `test_evidence/` | `TEST_EVIDENCE` | Tier 1 |
| `prompt_files/` | `PROMPT_FILE` | Requires review; tier depends on prompt/control role and provenance |
| `baseline_packs/` | `BASELINE_PACK` | Requires review; tier depends on generated artefact provenance and review status |
| `award_build_control/` | `AWARD_BUILD_CONTROL` | Requires review; tier depends on control role and implementation cross-checking |
| `other_requires_review/` | `OTHER_REQUIRES_REVIEW` | Requires review before tier assignment |
