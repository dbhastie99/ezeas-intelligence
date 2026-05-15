# Codex Prompt - Minerva Historical Analytics Cross-Check Findings Template v0.1

Mode: Documentation/control artefact only

Date: 15 May 2026

## Slice

Create the durable findings template and draft placeholder for the future code/test/schema cross-check of the registered Analytics Engine historical source.

Registered source: `HIST-ANALYTICS-2025-12-06-20`

Source title: Developer Log - Analytics Engine

Original filename: Developer Log - Analytics Engine (5).docx

## Required Outputs

- `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HISTORICAL_ANALYTICS_CROSSCHECK_FINDINGS_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/crosscheck_findings_templates/HIST_ANALYTICS_2025_12_06_20_CROSSCHECK_FINDINGS_DRAFT_PLACEHOLDER.md`

Update existing historical knowledge control artefacts only as needed to link the findings template and placeholder.

## Required Boundaries

This slice must not perform the cross-check, ingest the source, parse the source, extract historical source content, or treat the source as current truth.

The source remains `NOT_REVIEWED`, ingestion permitted No, and historical source material only.

ProcessedRule-era analytics claims require current code/test/schema confirmation before being treated as current.

`CalcInterpreterLine` is the current target canonical processed payroll calculation fact.

Minerva must not answer from the analytics source as current truth until reviewed, backfilled, and governed.

## Tests

Add focused assertions that the findings template and draft placeholder exist, include required sections, fields, classifications, source boundaries, and no-ingestion/no-runtime-change rules.

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Suggested commit message: minerva-historical-analytics-crosscheck-findings-template-v01
