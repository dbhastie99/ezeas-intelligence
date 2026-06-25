# Dataset Catalogue Extract

Source files:

- `metadata/analytics_builder/dataset_catalogue.v0_1.json`
- `metadata/analytics_builder/dataset_cards/*.json`
- `docs/analytics_builder_guide/dataset_cards/*.md`

## Count

Total dataset count: 9.

The count reconciles as 5 governed active dataset cards plus 4 blocked/gap dataset assets in `candidate_gap_datasets_v0_1.json`.

## Governed Active Datasets

- `payroll_outcome_line_v0_1`
- `payroll_context_dimensions_v0_1`
- `worker_worksite_context_dimensions_v0_1`
- `payroll_ledger_calcinterpreterline_bridge_v0_2`
- `objecttime_enriched_payroll_outcome_line_v0_2`

## Blocked/Gap Datasets

- `standalone_calc_interpreter_line_detail`
- `review_exception_required_review`
- `roster_vs_actual_objecttime_scheduling`
- `final_bank_paid_payroll_truth`

## Minerva Use

Minerva may use this extract for dataset-selection baseline evaluation in Beautiful Slice 2. It must preserve Diagnostic / Transitional / Blocked / Certified language and PROVEN / LIKELY / POSSIBLE / DISPROVEN / UNPROVEN language.

## Safety Notes

- Current Certified asset count is zero.
- Dataset availability is not certification.
- PayrollLedger is not bank-paid proof.
- CalcInterpreterLine is calculation/detail evidence, not payment execution proof.
- ObjectTime is source-context evidence, not payment finality proof.
- Final bank-paid payroll truth remains UNPROVEN / Blocked.
