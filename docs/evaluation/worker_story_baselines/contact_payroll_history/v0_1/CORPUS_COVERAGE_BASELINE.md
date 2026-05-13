# Contact Payroll History Corpus Coverage Baseline

This file records the captured corpus coverage result for the Contact Payroll History baseline pack. It is diagnostic-only and not operational truth.

## Commands Executed

```powershell
.\.venv\Scripts\python.exe scripts\scan_contact_payroll_history_corpus_coverage.py
.\.venv\Scripts\python.exe scripts\scan_contact_payroll_history_corpus_coverage.py --json --output .\artifacts\eval\contact_payroll_history_corpus_coverage.json
```

## Scope

The Contact Payroll History corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. DB readiness returned `READY`.

## Captured Result Summary

Result status: `COMPLETED_WITH_GAPS`

- Domain: Contact Payroll History
- Plan id: `CONTACT_PAYROLL_HISTORY`
- Evidence groups: 11
- `STRONG`: 7
- `WEAK`: 3
- `MISSING`: 1
- Coverage JSON generated: yes
- Generated artefact committed: no
- Indexed corpus: 5 active documents, 4583 chunks
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Missing group:

- `gross_to_net_history`

Weak groups:

- `current_and_historical_payroll_output`
- `retro_replay_and_correction_relationship`
- `outstanding_hardening`

## Source References

- Runbook: `docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/contact_payroll_history_corpus_coverage_service.py`
- Coverage script: `scripts\scan_contact_payroll_history_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Interpretation

Contact Payroll History has broad coverage but not full coverage. The `gross_to_net_history` group is missing and should be treated as a corpus gap before widening answer claims. The weak groups require retrieval-term or synthesis hardening, not operational JSON ingestion.

## Diagnostic-Only Guardrails

This corpus coverage baseline:

- does not mutate corpus;
- does not ingest documents;
- does not ingest operational JSON;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth.
