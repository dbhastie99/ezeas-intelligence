# Imports / Actuals Answer Gap Report Baseline

This file records the manually captured answer gap report result for the Imports / Actuals baseline pack. It is diagnostic-only and not operational truth.

## Commands Executed

```powershell
python scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json
python scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json --json --output .\artifacts\eval\imports_actuals_answer_gap_report.json
```

## Scope

The Imports / Actuals answer gap report consumes the captured corpus coverage JSON and recommends whether each evidence group should be kept, refined or deferred for formal source evidence.

## Captured Result Summary

Result status: `COMPLETED_WITH_REFINEMENT_NEEDED`

- Domain: Imports / Actuals
- Report type: `IMPORTS_ACTUALS_ANSWER_GAP_REPORT`
- Source coverage plan: `IMPORTS_ACTUALS`
- Overall status: `NEEDS_REFINEMENT`
- `LOW` / `KEEP` groups: 9
- `MEDIUM` / `IMPROVE_SYNTHESIS` groups: 1
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER` groups: 2
- Answer gap JSON generated: yes
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Answer gap report: recaptured and requires refinement.

Baseline pack state: recaptured result, not promoted.

Final ledger status remains `BASELINE_REQUIRED`; this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

## Recommended Actions

`LOW` / `KEEP` groups:

- 9 groups.

`MEDIUM` / `IMPROVE_SYNTHESIS` group:

- `pay_code_and_rate_type_mapping`

`ADD_FORMAL_SOURCE_EVIDENCE_LATER` groups:

- `purpose_and_operator_meaning`: HIGH
- `outstanding_hardening`: MEDIUM

Recommended next actions:

- Add formal source evidence later for missing Imports / Actuals groups before widening answer claims.
- Tighten Imports / Actuals answer synthesis for weak core groups while keeping status caveats.

## Boundary Expectations

Answer gap refinement must preserve:

- imported actuals as evidence for reconciliation, not calculated payroll truth;
- source truth provenance and evidence preservation;
- imported timesheet truth and imported external/payroll-system results;
- source-to-payroll comparison and actual-versus-calculated reconciliation;
- validation and error-resolution workflow;
- award-specific import template expectations;
- shift assessment and shift attribute import expectations;
- claim and claim amount import expectations;
- rate type/pay code mapping context, tenant overrides and mapping snapshots;
- worker story explanation context.

## Source References

- Runbook: `docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md`
- Answer gap service: `app/services/imports_actuals_answer_gap_report_service.py`
- Answer gap script: `scripts\build_imports_actuals_answer_gap_report.py`
- Required coverage JSON: `.\artifacts\eval\imports_actuals_corpus_coverage.json`

## Interpretation

Imports / Actuals is a recaptured baseline result with refinement still required. The missing `purpose_and_operator_meaning` and `outstanding_hardening` groups are formal source-evidence gaps, not only synthesis or retrieval drift. Promotion should not be considered until those gaps are addressed or the coverage plan is revised with justification, and the benchmark failure set is resolved or deliberately accepted under a documented baseline policy.

## Diagnostic-Only Guardrails

This answer gap baseline:

- does not mutate corpus;
- does not ingest documents;
- does not ingest operational JSON;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
