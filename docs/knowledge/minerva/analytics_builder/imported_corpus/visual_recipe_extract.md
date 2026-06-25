# Visual Recipe Extract

Source files:

- `metadata/analytics_builder/visual_recipe_library.v0_1.json`
- `metadata/analytics_builder/visual_recipes/*.json`
- `docs/analytics_builder_guide/visual_recipes/*.md`

## Count

Total visual recipe count: 13.

The count reconciles as 9 governed active visual recipe cards plus 4 blocked recipe assets in `blocked_visual_recipes_v0_1.json`.

## Governed Active Recipes

- `payroll_cost_by_rate_type`
- `payroll_cost_by_worksite`
- `rate_type_mix`
- `objecttime_source_context_coverage`
- `worker_pay_story`
- `award_outcome_breakdown`
- `payroll_ledger_to_calculation_detail_reconciliation`
- `process_period_payroll_review_summary`
- `payroll_outcome_line_drillthrough`

## Blocked Recipes

- `review_required_lines`
- `correction_retro_impact`
- `final_bank_paid_payroll_truth`
- `roster_vs_actual_scheduling_coverage`

## Minerva Use

Minerva may use this extract for visual recipe-selection baseline evaluation in Beautiful Slice 2. It must describe recipes as planned/evaluated answer targets until answer evaluation passes.

## Safety Notes

- Visual rendering is not certification proof.
- Generated HTML is reference-only and not source truth.
- Validation passing is evidence, not automatic certification.
- Blocked recipes require upstream proof before promotion.
