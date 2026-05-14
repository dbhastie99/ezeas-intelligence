# Process Periods / PayRun Lifecycle Answer Gap Report Baseline

This file records the manually captured answer gap report for the Process Periods / PayRun Lifecycle baseline pack. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
python scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json --json --output .\artifacts\eval\process_period_payrun_lifecycle_answer_gap_report.json
```

DB readiness was `READY` in normal PowerShell before capture. Codex did not rerun these DB-backed commands.

The generated JSON file `artifacts/eval/process_period_payrun_lifecycle_answer_gap_report.json` was produced as a transient evaluation artefact and must remain untracked.

## Scope

The answer gap report consumes `.\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json` after the coverage diagnostic has completed. The source coverage result has 10 STRONG, 3 WEAK and 0 MISSING evidence groups.

## Captured Result Summary

Result status: `NEEDS_REFINEMENT`

- Report type: `PROCESS_PERIOD_PAYRUN_LIFECYCLE_ANSWER_GAP_REPORT`
- Source coverage plan: `PROCESS_PERIOD_PAYRUN_LIFECYCLE`
- Overall status: `NEEDS_REFINEMENT`
- `LOW` / `KEEP` groups: 10
- `MEDIUM` refinement groups: 3
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Final ledger status remains `BASELINE_REQUIRED`; this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

## Refinement Groups

- `purpose_and_operator_meaning`: WEAK -> `IMPROVE_SYNTHESIS`
- `close_rolls_forward`: WEAK -> `IMPROVE_RETRIEVAL_TERMS`
- `outstanding_hardening`: WEAK -> `IMPROVE_RETRIEVAL_TERMS`

## Recommended Actions

- Refine Process Periods / PayRun Lifecycle retrieval terms for weak supporting groups before adding new corpus.
- Tighten Process Periods / PayRun Lifecycle answer synthesis for weak core groups while keeping status caveats.

## Interpretation

This is a recaptured baseline result requiring refinement, not a promoted baseline. The answer gap is driven by weak supporting groups and synthesis coverage, not missing corpus evidence, because the source coverage report has 0 MISSING groups.

Payment date and calendar policy remain governed context, dirty contacts require reprocessing before safe use, and finalised or protected runs require correction/review pathways rather than ordinary mutation.

## Source References

- Runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`
- Gap service: `app/services/process_period_payrun_lifecycle_answer_gap_report_service.py`
- Gap script: `scripts\build_process_period_payrun_lifecycle_answer_gap_report.py`
- Required coverage JSON: `.\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json`

## Diagnostic-Only Guardrails

This answer gap report baseline:

- does not mutate corpus;
- does not ingest operational JSON;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
