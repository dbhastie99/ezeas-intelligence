# Process Periods / PayRun Lifecycle Answer Gap Report Baseline

This file records manually captured answer gap report output for the Process Periods / PayRun Lifecycle promoted baseline. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
python scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json --json --output .\artifacts\eval\process_period_payrun_lifecycle_answer_gap_report.json
```

The generated JSON file `artifacts/eval/process_period_payrun_lifecycle_answer_gap_report.json` was produced as a transient evaluation artefact and must remain untracked.

## Scope

The answer gap report consumes `.\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json` after the coverage diagnostic has completed. The source coverage result has 13 STRONG, 0 WEAK and 0 MISSING evidence groups.

## Captured Result Summary

Result status: `COMPLETED`

- Report type: `PROCESS_PERIOD_PAYRUN_LIFECYCLE_ANSWER_GAP_REPORT`
- Source coverage plan: `PROCESS_PERIOD_PAYRUN_LIFECYCLE`
- Overall status: `GOOD`
- `LOW` / `KEEP` groups: 13
- `MEDIUM` refinement groups: 0
- `IMPROVE_RETRIEVAL_TERMS`: 0
- `IMPROVE_SYNTHESIS`: 0
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 0
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Group Findings

- `purpose_and_operator_meaning`: STRONG -> `KEEP`
- `process_period_and_group_context`: STRONG -> `KEEP`
- `open_not_open_closed_lifecycle`: STRONG -> `KEEP`
- `close_rolls_forward`: STRONG -> `KEEP`
- `payment_date_and_calendar_policy`: STRONG -> `KEEP`
- `payrun_creation_and_admission`: STRONG -> `KEEP`
- `run_type_and_run_purpose`: STRONG -> `KEEP`
- `regular_supplementary_retro_distinction`: STRONG -> `KEEP`
- `payrun_contact_lifecycle`: STRONG -> `KEEP`
- `current_effective_output_and_finalisation`: STRONG -> `KEEP`
- `payment_execution_and_period_close`: STRONG -> `KEEP`
- `worker_story_admin_queue_and_movement_review_connection`: STRONG -> `KEEP`
- `outstanding_hardening`: STRONG -> `KEEP`

## Recommended Actions

- Keep current Process Periods / PayRun Lifecycle retrieval terms and answer synthesis under benchmark watch.

## Interpretation

This is a promoted baseline result after answer-synthesis and retrieval-term hardening. Payment date and calendar policy remain governed context, dirty contacts require reprocessing before safe use, and finalised or protected runs require correction/review pathways rather than ordinary mutation.

## Source References

- Runbook: `docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md`
- Gap service: `app/services/process_period_payrun_lifecycle_answer_gap_report_service.py`
- Gap script: `scripts\build_process_period_payrun_lifecycle_answer_gap_report.py`
- Required coverage JSON: `.\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json`

## Diagnostic-Only Guardrails

This answer gap report baseline:

- does not mutate corpus;
- does not ingest operational JSON;
- does not change endpoint/UI/runtime behavior;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
