# Analytics Builder Source Count Reconciliation - M5

M5 resolves the M4 count mismatch without modifying `ezeas-analytics` or copying source content.

## Dataset Count

M1 expected 9 datasets. The active dataset catalogue lists 5 governed dataset card paths:

* `payroll_outcome_line_v0_1`
* `payroll_context_dimensions_v0_1`
* `worker_worksite_context_dimensions_v0_1`
* `payroll_ledger_calcinterpreterline_bridge_v0_2`
* `objecttime_enriched_payroll_outcome_line_v0_2`

The `dataset_cards` directory contains 6 JSON files because the sixth file is `candidate_gap_datasets_v0_1.json`, a register for 4 blocked/gap dataset assets:

* `standalone_calc_interpreter_line_detail`
* `review_exception_required_review`
* `roster_vs_actual_objecttime_scheduling`
* `final_bank_paid_payroll_truth`

Certification readiness and certification packets count 5 governed datasets plus 4 blocked/gap datasets, for 9 total.

## Visual Recipe Count

M1 expected 13 visual recipes. The active visual recipe library lists 9 governed recipe card paths:

* `payroll_cost_by_rate_type`
* `payroll_cost_by_worksite`
* `rate_type_mix`
* `objecttime_source_context_coverage`
* `worker_pay_story`
* `award_outcome_breakdown`
* `payroll_ledger_to_calculation_detail_reconciliation`
* `process_period_payroll_review_summary`
* `payroll_outcome_line_drillthrough`

The `visual_recipes` directory contains 10 JSON files because the tenth file is `blocked_visual_recipes_v0_1.json`, a register for 4 blocked recipe assets:

* `review_required_lines`
* `correction_retro_impact`
* `final_bank_paid_payroll_truth`
* `roster_vs_actual_scheduling_coverage`

Certification readiness and certification packets count 9 governed recipes plus 4 blocked recipes, for 13 total.

## Are Missing Files A Problem?

The missing individual files are expected design, not a file-loss problem. Blocked/gap datasets and recipes are represented as register entries and certification packets rather than individual card files.

M6 may proceed only as restricted baseline stubs. Production-passed answer baselines remain blocked until governed import execution and answer evaluation exist.
