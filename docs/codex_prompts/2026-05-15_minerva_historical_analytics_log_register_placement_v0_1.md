# Minerva Historical Analytics Log Register Placement v0.1

Date: 15 May 2026

## 1. Purpose

Create the first controlled registered-source placement placeholder for the historical Analytics Engine developer log.

This slice uses the registered source folder model and `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md`. It does not ingest the full historical document content.

## 2. Source Context

The user provided a historical analytics developer log titled `Developer Log - Analytics Engine (5).docx`.

The log covers Golden Slice Analytics, `workforce_analytics_local` / `workforce_analytics_dev`, `vw_FactObjectTime`, `vw_FactProcessedRule`, `vw_GS_RosterVsActual`, Power BI handover, `ProcessedRule.Quantity` based hours, `AwardRateType` behaviour flags, ObjectTime Work/Schedule mapping, and dev analytics seeding.

This is historical source material. It is valuable for rationale and historical architecture, but it is not automatically current truth because current platform direction has moved toward `CalcInterpreterLine` as the canonical processed payroll result source.

## 3. Required Outputs

Ensure `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` contains a register entry for the Analytics Engine developer log.

Create a lightweight placeholder/metadata file under the correct registered source folder:

`docs/evaluation/historical_knowledge/registered_sources/developer_logs/HIST_ANALYTICS_2025_12_06_20_SOURCE_PLACEHOLDER.md`

The existing register classifies this source as `DEVELOPER_LOG`, so this slice uses `developer_logs` rather than `mixed_log_doctrine`. Register entries control classification; folder placement follows the register.

Update `docs/evaluation/historical_knowledge/HISTORICAL_SOURCE_REGISTER.md` to reference the registered source folder placeholder path.

Update `docs/evaluation/historical_knowledge/HISTORICAL_KNOWLEDGE_CONTROL_INDEX.md` if needed to mention that the first historical source placement placeholder exists.

Do not copy the full developer log content into the placeholder. The placeholder must contain metadata and handling instructions only.

## 4. Placeholder Requirements

The placeholder must include:

- Register ID: `HIST-ANALYTICS-2025-12-06-20`
- Source title: `Developer Log - Analytics Engine`
- Original filename: `Developer Log - Analytics Engine (5).docx`
- Registered source type: `DEVELOPER_LOG`, matching the register
- Source tier: Tier 2
- Domain tags: Analytics, Workforce Analytics DB, Golden Slice, ObjectTime, ProcessedRule, CalcInterpreterLine Replatform Review, Power BI, Reconciliation Reporting
- Date or date range: 6 December 2025 to 20 December 2025
- Review status: `NOT_REVIEWED`
- Ingestion permitted: No
- Implementation-state classification: `UNCERTAIN_REQUIRES_REVIEW`
- Supersession risk: `ProcessedRule`-era analytics is partially superseded by the `CalcInterpreterLine` model
- Handling instruction: source is registered historical source material only; do not ingest or treat as current truth until reviewed and cross-checked
- Future use: analytics replatform planning input

## 5. Required Control Statements

The placeholder and register must state:

- folder placement alone is not ingestion;
- register entry controls classification;
- original filename is metadata only;
- the full historical document has not been ingested;
- `ProcessedRule`-era analytics requires review before being treated as current;
- `CalcInterpreterLine` is the current target calculation fact source;
- future analytics backfill must cross-check against current code, tests, database views, schema/scripts, and commits;
- no corpus mutation, Code Evidence integration, live LLM call, runtime change, baseline promotion, ledger promotion, or historical ingestion occurs in this slice.

## 6. Test Requirements

Add or update tests in `tests/test_domain_baseline_capture_batch.py` or a focused historical knowledge test file. Tests must assert:

1. The analytics source placeholder exists under `registered_sources`.
2. The placeholder contains the Register ID.
3. The placeholder references `Developer Log - Analytics Engine`.
4. The placeholder records the original filename `Developer Log - Analytics Engine (5).docx`.
5. The placeholder records Tier 2.
6. The placeholder records `NOT_REVIEWED`.
7. The placeholder records ingestion permitted No.
8. The placeholder records Analytics, ProcessedRule, CalcInterpreterLine, and Power BI domain tags.
9. The placeholder states folder placement alone is not ingestion.
10. The placeholder states the full historical document has not been ingested.
11. The placeholder states `ProcessedRule`-era analytics requires review.
12. The placeholder states `CalcInterpreterLine` is the current target calculation fact source.
13. `HISTORICAL_SOURCE_REGISTER.md` references the placeholder path.
14. `HISTORICAL_SOURCE_REGISTER.md` keeps the source `NOT_REVIEWED` and ingestion permitted No.
15. The documents state no corpus mutation, no Code Evidence integration, no live LLM call, no runtime change, no baseline promotion, no ledger promotion, and no historical ingestion occur.

## 7. Boundaries

Do not ingest historical chats. Do not ingest the full developer log. Do not ingest doctrine documents. Do not ingest code. Do not mutate corpus. Do not implement DB writes, migrations, Code Evidence integration, live LLM calls, endpoint changes, UI changes, workforce-platform changes, award-configurator-v1 changes, runtime changes, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, promotion, or ledger update.

Do not perform historical ingestion, review approval, governed ingestion, recapture, benchmark execution, corpus coverage execution, answer-gap execution, generated-artefact promotion, baseline promotion, ledger update, or ledger promotion.

## 8. Verification

Run:

```powershell
python -m pytest tests/test_domain_baseline_capture_batch.py -q
git diff --check
```

Clean `.pytest_tmp` if present.

Report files changed, analytics placeholder created, tests, `.pytest_tmp` status, and confirmation of no DB/corpus/runtime/LLM/endpoint/UI/ledger-promotion/review-approval/governed-ingestion/historical-ingestion/recapture/benchmark/corpus-coverage/answer-gap/generated-artefact changes.

Suggested commit message: `minerva-historical-analytics-log-register-placement-v01`
