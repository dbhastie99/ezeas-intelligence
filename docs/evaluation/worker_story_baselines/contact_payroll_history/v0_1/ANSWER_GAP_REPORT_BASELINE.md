# Contact Payroll History Answer Gap Report Baseline

This file records the captured answer gap report result for the Contact Payroll History baseline pack. It is diagnostic-only and not operational truth.

## Commands Executed

```powershell
.\.venv\Scripts\python.exe scripts\build_contact_payroll_history_answer_gap_report.py --coverage-report .\artifacts\eval\contact_payroll_history_corpus_coverage.json
.\.venv\Scripts\python.exe scripts\build_contact_payroll_history_answer_gap_report.py --coverage-report .\artifacts\eval\contact_payroll_history_corpus_coverage.json --json --output .\artifacts\eval\contact_payroll_history_answer_gap_report.json
```

## Scope

The answer gap report uses the captured Contact Payroll History corpus coverage JSON as transient input and summarizes answer-readiness gaps into this curated markdown baseline.

## Captured Result Summary

Result status: `COMPLETED_WITH_REFINEMENT_NEEDED`

- Report type: `CONTACT_PAYROLL_HISTORY_ANSWER_GAP_REPORT`
- Overall status: `NEEDS_REFINEMENT`
- Source coverage plan: `CONTACT_PAYROLL_HISTORY`
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Recommended actions:

- `KEEP`: 7
- `IMPROVE_SYNTHESIS`: 1
- `IMPROVE_RETRIEVAL_TERMS`: 2
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 1

Recommended next actions:

- Add formal source evidence later for missing Contact Payroll History groups before widening answer claims.
- Refine Contact Payroll History retrieval terms for weak supporting groups before adding new corpus.
- Tighten Contact Payroll History answer synthesis for weak core groups while keeping status caveats.

## Source References

- Runbook: `docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md`
- Gap service: `app/services/contact_payroll_history_answer_gap_report_service.py`
- Gap script: `scripts\build_contact_payroll_history_answer_gap_report.py`
- Required coverage JSON: `.\artifacts\eval\contact_payroll_history_corpus_coverage.json`

## Interpretation

Contact Payroll History is a captured baseline with refinement still required. The missing `gross_to_net_history` corpus group means answer claims should not be widened until formal source evidence exists. Weak retrieval and synthesis groups should be hardened while preserving status caveats.

## Diagnostic-Only Guardrails

This answer gap report baseline:

- does not mutate corpus;
- does not ingest operational JSON;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth.
