# Minerva Historical Developer Log Batch Intake Guidance v0.1

Date: 15 May 2026

## Purpose

Create the durable operator guidance for safely adding many historical developer logs, hardening logs, platform doctrine documents, and mixed log/doctrine sources into the existing developer-log batch register.

This slice creates intake guidance only. It must not ingest, parse, review, or extract historical source content.

## Create

- `docs/evaluation/historical_knowledge/HISTORICAL_DEVELOPER_LOG_BATCH_INTAKE_GUIDANCE.md`

## Update If Needed

- `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTRATION_AND_TRIAGE_MODEL.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_REGISTER_TEMPLATE.md`
- `docs/evaluation/historical_knowledge/HISTORICAL_BATCH_TRIAGE_PROCESS.md`
- `docs/evaluation/historical_knowledge/batch_registers/HISTORICAL_DEVELOPER_LOG_BATCH_REGISTER_2026_05_15.md`

## Controls

The guidance must state:

- Adding a file to a registered folder is not ingestion.
- Adding a batch row is metadata registration only.
- Original filename is metadata only.
- Register entries drive classification, not filenames.
- Ingestion permitted defaults to No.
- Review status defaults to NOT_REVIEWED.
- Implementation-state classification should default to UNCERTAIN_REQUIRES_REVIEW unless the operator has strong evidence from the document/register context.
- Developer logs can be grouped by domain/date range where appropriate.
- Full review chain is required only for high-value/high-risk sources.
- Ordinary logs can remain batch-registered until needed.
- Minerva must not treat batch-registered sources as current truth unless later reviewed/backfilled/governed.

The guidance must define register ID conventions:

- `HIST-DEVLOG-YYYY-MM-DD-NNN`
- `HIST-HARDENING-YYYY-MM-DD-NNN`
- `HIST-DOCTRINE-YYYY-MM-DD-NNN`
- `HIST-MIXED-YYYY-MM-DD-NNN`

The guidance must include source type selection for:

- `DEVELOPER_LOG`
- `HARDENING_LOG`
- `PLATFORM_DOCTRINE`
- `MIXED_LOG_DOCTRINE`
- `OTHER_REQUIRES_REVIEW`

The guidance must include domain tagging guidance for Worker Story, ObjectTime / Source Truth, Process Periods / PayRun Lifecycle, Payroll Buckets / Bases / Totals, Deductions and Obligations, Tax / PAYG, Imports / Actuals, Leave Workflow / Annual Leave, Award Configurator, Analytics, Reconciliation, and Finalised Correction / ObjectTime Route Guard.

Full review chain escalation guidance must cover major architecture decisions, possible effect on current Minerva answers, implementation claims requiring code/test/schema confirmation, supersession risk, conflicting claims, and high-risk payroll/source-truth/tax/imports/reconciliation/deduction/leave/worker-story/analytics/award-configurator/finalised-correction domains.

Example rows must be metadata-only examples and must not contain real source content.

## Non-Goals

This slice does not ingest historical chats, ingest developer logs, ingest doctrine documents, ingest code, parse or extract historical source content, review historical sources, mutate corpus, connect Code Evidence, call live LLM, change runtime behaviour, change ledger counts, or promote baselines.

This slice does not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, ezeas-analytics changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, ledger update, ledger promotion, or generated artefact creation.

## Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Suggested commit message: `minerva-historical-developer-log-batch-intake-guidance-v01`
