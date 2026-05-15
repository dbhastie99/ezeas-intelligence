# Formal Evidence Current State Summary

Version: v0.1

Date: 15 May 2026

## Purpose

This is the operator-facing current-state summary for Minerva formal evidence control.

For the full control model, start with:

- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_INDEX.md`
- `docs/evaluation/source_evidence_drafts/FORMAL_EVIDENCE_CONTROL_MODEL_CLOSEOUT_2026_05_15.md`

## Current Controlled Domains

| Domain | Baseline status | Review status | Governed ingestion permitted | Recapture permitted | Promotion permitted | Promotion execution permitted |
| --- | --- | --- | --- | --- | --- | --- |
| Tax / PAYG | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |
| Imports / Actuals | `BASELINE_REQUIRED` | `NOT_REVIEWED` | No | No | No | No |

Tax / PAYG remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Imports / Actuals remains `BASELINE_REQUIRED` and `NOT_REVIEWED`.

Governed ingestion permitted: No.

Recapture permitted: No.

Promotion permitted: No.

Promotion execution permitted: No.

## Minerva Answer Boundaries

Minerva may explain Tax / PAYG doctrine, evidence, implementation state, and current gaps, but must not calculate PAYG withholding.

Imports / Actuals is not merely file upload or CSV parsing. It includes evidence-bearing import batches, rows, validation, errors, warnings, provenance, mapping, comparison, and remediation context.

## No Operational Change

No review approval occurred.

No governed ingestion occurred.

No corpus mutation occurred.

No recapture occurred.

No benchmark run occurred.

No corpus coverage run occurred.

No answer-gap run occurred.

No promotion occurred.

No ledger update occurred.

No runtime change occurred.

No endpoint change occurred.

No UI change occurred.

No workforce-platform change occurred.

No award-configurator-v1 change occurred.

No DB write, migration, Code Evidence integration, live LLM call, generated artefact creation, ledger promotion, or baseline promotion was performed.

## Next Allowed Actions

Future work may assign a reviewer.

Future work may perform an explicit review slice.

Future work may create `NEEDS_REVISION` or `REVIEWED_READY_FOR_INGESTION` decision records.

Future work may plan governed ingestion only after review readiness and the required review decision state exist.

Future work must not skip gates.

## Blocked Actions

Corpus ingestion remains blocked for Tax / PAYG and Imports / Actuals.

Recapture remains blocked for Tax / PAYG and Imports / Actuals.

Promotion remains blocked for Tax / PAYG and Imports / Actuals.

Ledger changes remain blocked for Tax / PAYG and Imports / Actuals.

This slice prompt is preserved at `docs/codex_prompts/2026-05-15_minerva_formal_evidence_current_state_summary_v0_1.md`.
