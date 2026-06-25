# Minerva Knowledge Artifact: Analytics Builder M7 Safety Regression Harness

M7 defines a static safety regression harness for future Analytics Builder Minerva answers.

It does not run live LLM evaluation, generate answers, create runtime ingestion, or promote any baseline. It creates the metadata and documentation needed to evaluate future answers after governed source import execution.

## Inputs

- M1 answer safety contract: `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
- M1 benchmark question plan: `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`
- M2 retrieval domain: `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`
- M5 governed import manifest: `metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json`
- M6 answer baseline stubs: `metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json`
- M6 planned eval file: `samples/eval/analytics_builder_benchmark.planned.v0_1.json`

## Harness

The primary artifact is `metadata/minerva/analytics_builder_safety_regression_harness.v0_1.json`.

It defines:

- 12 safety rules;
- prohibited claim patterns;
- required claim patterns;
- question-to-rule mappings;
- negative unsafe-answer snippets;
- positive required safe-answer snippets;
- a baseline promotion gate.

## Promotion Posture

Current gate result is blocked pending governed source ingestion and answer evaluation. Planned/pending baselines cannot become evaluated until governed source ingestion has executed and source lineage is preserved. Evaluated baselines cannot become production-passed until all safety checks pass and governed review authorizes production answer use.

## Safety Posture

The harness preserves these controls:

- Current Certified asset count is zero.
- Final-paid payroll truth remains UNPROVEN / Blocked.
- PayrollLedger does not prove bank-paid truth.
- CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth.
- ObjectTime is source-context evidence, not payment finality.
- PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth.
- Visual rendering is not certification proof.
- Blocked gaps are safety controls, not failures.
- Minerva must say not enough governed proof rather than inventing proof.
