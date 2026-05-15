# Historical Source Register Validation Runbook

Version: v0.1

Date: 15 May 2026

## 1. Purpose

This runbook defines the validation rules for Minerva historical source registration before real historical documents are added.

It preserves the doctrine that folder placement alone is not registration. A file placed in `docs/evaluation/historical_knowledge/registered_sources/` does not become registered, reviewed, ingested, or true merely because of that placement.

## 2. Scope

This runbook validates registration controls for historical source material, registered source folders, and `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`.

It applies before any backfill draft, governed ingestion plan, source citation, implemented-state conclusion, or baseline-promotion path relies on historical source material.

## 3. Validation Principle

A source file must have a corresponding `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` entry before it is treated as registered.

Registered source type comes from the register entry, not the filename. Original filename is metadata only.

Folder placement alone is not registration. Folder placement may support discovery and expected classification checks, but the register entry is the controlling record.

## 4. Registered Source Definition

A source is registered only when `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` contains a corresponding register entry for that source.

The register entry must include source type, source tier, review status, implementation-state classification, ingestion permission, and provenance fields before any backfill draft can rely on the source.

Review status and implementation-state classification are required before any backfill draft can rely on the source.

## 5. Unregistered File Definition

Files in `docs/evaluation/historical_knowledge/registered_sources/` without corresponding register entries are `UNREGISTERED_SOURCE_MATERIAL`.

`UNREGISTERED_SOURCE_MATERIAL` must not be ingested, cited as final truth, used for baseline promotion, or used as implemented-state evidence.

Unregistered source material may be identified as candidate material for a later explicit registration/review slice, but it remains outside registered historical knowledge until the register is updated.

## 6. Required Register Entry Fields

Every source register entry must include:

- Source title
- Original filename
- Source folder
- Registered source type
- Source tier
- Domain tags
- Date or date range
- Repository context
- Implementation-state classification
- Review status
- Ingestion permitted
- Supersession status
- Evidence confidence
- Notes

The durable register may also include related commits and related control artefacts as provenance fields. Missing provenance must be recorded as `unknown` with a reason, not silently omitted.

`Ingestion permitted` defaults to `No` until a governed backfill/review path changes it in a later explicit slice.

## 7. Folder-to-Source-Type Expectations

Registered folders provide expected starting source types only:

| Folder | Expected registered source type |
| --- | --- |
| `developer_logs/` | `DEVELOPER_LOG` |
| `hardening_logs/` | `HARDENING_LOG` |
| `platform_doctrine/` | `PLATFORM_DOCTRINE` |
| `mixed_log_doctrine/` | `MIXED_LOG_DOCTRINE` |
| `chat_continuance/` | `CHAT_OR_CONTINUANCE` |
| `code_evidence/` | `CODE_EVIDENCE` |
| `test_evidence/` | `TEST_EVIDENCE` |
| `prompt_files/` | `PROMPT_FILE` |
| `baseline_packs/` | `BASELINE_PACK` |
| `award_build_control/` | `AWARD_BUILD_CONTROL` |
| `other_requires_review/` | `OTHER_REQUIRES_REVIEW` |

Allowed source types remain:

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

Source type and folder should be consistent, or the mismatch must be documented with `OTHER_REQUIRES_REVIEW` or an explicit rationale in the register notes.

## 8. Validation Rules

1. Confirm the source file has a corresponding register entry before treating it as registered.
2. Confirm source title, original filename, source folder, registered source type, source tier, domain tags, date or date range, repository context, implementation-state classification, review status, ingestion permitted, supersession status, evidence confidence, and notes are present.
3. Confirm registered source type is one controlled source type assigned by the register entry.
4. Confirm original filename is treated as metadata only.
5. Confirm source type and folder are consistent, or the mismatch is documented with `OTHER_REQUIRES_REVIEW` or an explicit rationale.
6. Confirm review status and implementation-state classification are present before any backfill draft relies on the source.
7. Confirm `Ingestion permitted` is `No` by default unless a later explicit governed ingestion slice changed it.
8. Confirm unregistered source material is not ingested, cited as final truth, used for baseline promotion, or used as implemented-state evidence.

Implementation-state classifications remain:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_TESTED`
- `DOCUMENTED_DOCTRINE`
- `DOCUMENTED_BACKLOG`
- `PLANNED_NOT_IMPLEMENTED`
- `SUPERSEDED`
- `UNCERTAIN_REQUIRES_REVIEW`

## 9. Allowed Exceptions

A folder/source-type mismatch is allowed only when the register documents `OTHER_REQUIRES_REVIEW` or an explicit rationale.

Candidate material may be staged in `registered_sources/` for later review, but until a corresponding register entry exists it remains `UNREGISTERED_SOURCE_MATERIAL`.

Unknown provenance may be recorded only when the register marks the field as `unknown` and explains the uncertainty in notes.

## 10. Failure Handling

If a file lacks a corresponding register entry, treat it as `UNREGISTERED_SOURCE_MATERIAL`.

If required fields are missing, do not rely on the source for any backfill draft, ingestion decision, implemented-state conclusion, citation as final truth, baseline promotion, or ledger promotion.

If source type and folder conflict without documented rationale, assign or preserve `OTHER_REQUIRES_REVIEW` until review resolves the mismatch.

If ingestion permission is absent or ambiguous, treat it as `No`.

## 11. Backfill Workflow Integration

Before a backfill draft relies on a historical source, validate the corresponding register entry against this runbook.

Backfill work may identify candidate source material, but reliance requires a register entry, review status, implementation-state classification, ingestion permission, supersession status, and provenance fields.

This runbook does not permit direct historical ingestion. Governed ingestion requires a later explicit review and ingestion slice.

## 12. Non-Goals

This slice does not ingest or parse real historical documents.

This slice does not perform historical ingestion, corpus mutation, Code Evidence integration, live LLM call, runtime change, endpoint change, UI change, workforce-platform change, award-configurator-v1 change, baseline promotion, ledger promotion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, DB write, migration, or generated artefact creation.

This slice does not promote any historical source, domain baseline, ledger count, or implemented-state claim.

## 13. Future Automation

Future automation may scan `docs/evaluation/historical_knowledge/registered_sources/` and compare files against `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`.

Future automation may report files without corresponding register entries as `UNREGISTERED_SOURCE_MATERIAL`, report folder/source-type mismatches, and report missing required fields.

Future automation must not ingest or parse real historical documents unless a later explicit governed ingestion slice permits that work.
