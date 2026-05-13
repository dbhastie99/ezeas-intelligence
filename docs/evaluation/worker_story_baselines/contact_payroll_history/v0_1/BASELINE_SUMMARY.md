# Contact Payroll History Baseline Summary

Slice name: Minerva Next Baseline Batch v0.1 - Payroll Evidence Context Domains

Domain: Contact Payroll History

Source runbook: `docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This captured baseline pack is diagnostic-only and not operational truth. It records actual DB-backed benchmark, corpus coverage and answer gap command summaries after DB readiness returned `READY`.

## Execution Context

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

DB readiness result: `READY`.

- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Configuration source reported: `.env:MINERVA_DATABASE_URL`
- Dialect/driver reported: `mssql/pyodbc`
- Selected ODBC driver reported: `ODBC Driver 18 for SQL Server`

Contact Payroll History commands ran to actual result. ObjectTime / Source Truth, Process Periods / PayRun Lifecycle and Imports / Actuals remain blocked and are not updated by this pack.

Generated benchmark, corpus coverage and answer-gap JSON outputs were summarized into curated markdown only. Generated JSON files under `.\artifacts\eval\` are not required committed artefacts.

## Commands Executed

| Area | Command | Completed In v0.1 | Captured Result Summary |
|---|---|---:|---|
| DB readiness check | `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py` | yes | `READY`; ready: yes. |
| Contact Payroll History benchmark | `.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.contact_payroll_history.json` | yes | 7 total, 5 passed, 2 failed. |
| Corpus coverage diagnostic | `.\.venv\Scripts\python.exe scripts\scan_contact_payroll_history_corpus_coverage.py` | yes | 11 groups: 7 STRONG, 3 WEAK, 1 MISSING. |
| Corpus coverage diagnostic JSON | `.\.venv\Scripts\python.exe scripts\scan_contact_payroll_history_corpus_coverage.py --json --output .\artifacts\eval\contact_payroll_history_corpus_coverage.json` | yes | Generated transient JSON; not committed. |
| Answer gap report | `.\.venv\Scripts\python.exe scripts\build_contact_payroll_history_answer_gap_report.py --coverage-report .\artifacts\eval\contact_payroll_history_corpus_coverage.json` | yes | `NEEDS_REFINEMENT`. |
| Answer gap report JSON | `.\.venv\Scripts\python.exe scripts\build_contact_payroll_history_answer_gap_report.py --coverage-report .\artifacts\eval\contact_payroll_history_corpus_coverage.json --json --output .\artifacts\eval\contact_payroll_history_answer_gap_report.json` | yes | Generated transient JSON; not committed. |

## Captured High-Level Findings

- Readiness status: `READY`.
- Baseline pack created: captured DB-backed baseline.
- Benchmark result: 7 total, 5 passed, 2 failed.
- Failed benchmark cases: `contact-payroll-history-rich-answer`, `contact-payroll-history-retro-replay-correction`.
- Failure classification: combination of benchmark answer-term expectation gap and source-evidence/matched-phrase drift, with corpus gap present for `gross_to_net_history`; not purely benchmark drift.
- Corpus coverage result: `STRONG` = 7, `WEAK` = 3, `MISSING` = 1.
- Missing coverage group: `gross_to_net_history`.
- Weak coverage groups: `current_and_historical_payroll_output`, `retro_replay_and_correction_relationship`, `outstanding_hardening`.
- Answer gap report: `NEEDS_REFINEMENT`; 7 KEEP, 1 IMPROVE_SYNTHESIS, 2 IMPROVE_RETRIEVAL_TERMS, 1 ADD_FORMAL_SOURCE_EVIDENCE_LATER.
- Indexed corpus: 5 active documents, 4583 chunks.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Generated artefacts committed: no.
- Final ledger status is now `BASELINE_ALREADY_EXISTS`.

## Known Gaps

- Contact Payroll History has one missing corpus evidence group: `gross_to_net_history`.
- Weak supporting groups remain for `current_and_historical_payroll_output`, `retro_replay_and_correction_relationship` and `outstanding_hardening`.
- The two failed benchmark cases remain captured as baseline failures and should not be hidden by weakening expectations.
- Generated output files under `.\artifacts\eval\contact_payroll_history_*.json` are transient evaluation outputs and are not required committed artefacts.

## Guardrails

This captured pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Add formal source evidence later for missing Contact Payroll History groups before widening answer claims. Refine Contact Payroll History retrieval terms for weak supporting groups before adding new corpus. Tighten Contact Payroll History answer synthesis for weak core groups while keeping status caveats.
