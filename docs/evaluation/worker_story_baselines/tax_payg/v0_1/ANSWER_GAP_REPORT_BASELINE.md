# Tax / PAYG Answer Gap Report Baseline

This file records the manually captured answer gap report result for the Tax / PAYG baseline pack. It is diagnostic-only and not operational truth.

## Commands Executed

```powershell
python scripts\build_tax_payg_answer_gap_report.py --coverage-report .\artifacts\eval\tax_payg_corpus_coverage.json
python scripts\build_tax_payg_answer_gap_report.py --coverage-report .\artifacts\eval\tax_payg_corpus_coverage.json --json --output .\artifacts\eval\tax_payg_answer_gap_report.json
```

## Scope

The Tax / PAYG answer gap report consumes the captured corpus coverage JSON and recommends whether each evidence group should be kept, refined or deferred for formal source evidence.

## Captured Result Summary

Result status: `COMPLETED_WITH_REFINEMENT_NEEDED`

- Domain: Tax / PAYG
- Report type: `TAX_PAYG_ANSWER_GAP_REPORT`
- Source coverage plan: `TAX_PAYG`
- Overall status: `NEEDS_REFINEMENT`
- `LOW` / `KEEP` groups: 10
- `HIGH` / `ADD_FORMAL_SOURCE_EVIDENCE_LATER` groups: 1
- `MEDIUM` / `IMPROVE_RETRIEVAL_TERMS` groups: 1
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

- 10 groups.

`HIGH` / `ADD_FORMAL_SOURCE_EVIDENCE_LATER` group:

- `purpose_and_operator_meaning`

`MEDIUM` / `IMPROVE_RETRIEVAL_TERMS` group:

- `outstanding_hardening`

Recommended next actions:

- Add formal source evidence later for missing Tax / PAYG groups before widening answer claims.
- Refine Tax / PAYG retrieval terms for weak supporting groups before adding new corpus.

## Boundary Expectations

Answer gap refinement must preserve:

- Tax / PAYG as governed payroll-tax evidence and explanation context, not a generic calculator domain;
- Minerva explaining Tax / PAYG without calculating PAYG withholding;
- deterministic services and tax providers as the owners of withholding calculation;
- Tax/PAYG rates, thresholds, bands, offsets and formulas as governed data/rule-pack/configuration;
- TaxStory explanation for source truth, worker tax profile, payroll context, rule-pack selection, component selection, frequency conversion, band/formula calculation, rounding, net-pay effect, unsupported/skipped rules and audit provenance;
- PaymentDate and payroll context selection evidence;
- taxable basis, taxable earnings and Payroll Bases & Totals context;
- supplementary incremental PAYG context over same-period taxable earnings and prior PAYG withheld;
- Worker Story and PayRun Admin Queue tax readiness context.

## Source References

- Runbook: `docs/TAX_PAYG_EVALUATION_RUNBOOK.md`
- Answer gap service: `app/services/tax_payg_answer_gap_report_service.py`
- Answer gap script: `scripts\build_tax_payg_answer_gap_report.py`
- Required coverage JSON: `.\artifacts\eval\tax_payg_corpus_coverage.json`

## Interpretation

Tax / PAYG is a recaptured baseline result with refinement still required. The missing `purpose_and_operator_meaning` group is a formal source-evidence gap, not only synthesis or retrieval drift. The weak `outstanding_hardening` group requires retrieval-term refinement. Promotion should not be considered until the formal source-evidence gap is addressed or the coverage plan is revised with justification, and the benchmark failure set is resolved or deliberately accepted under a documented baseline policy.

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
