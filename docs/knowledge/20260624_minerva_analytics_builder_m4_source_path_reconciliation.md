# Minerva Analytics Builder M4 Source Path Reconciliation

This Minerva-ready knowledge artifact records Step 4 / M4 of the post-v0.2 Analytics Builder OMG plan.

## Why M4 Exists

The original M4 was answer baselines, but M3 found that the local `ezeas-analytics` repository did not contain the M1 expected source paths at the exact registered locations. Answer baselines must wait until the source corpus paths are reconciled and governed import boundaries are defined.

## Reconciliation Result

The expected tag `analytics-builder-static-omg-v0.2-20260624` exists in `C:/Projects/ezeas-analytics`.

The M1 expected `docs/analytics_builder/...` source layout is stale. The actual source layout is:

* `metadata/analytics_builder/` for canonical JSON metadata;
* `metadata/analytics_builder/dataset_cards/` for dataset card JSON;
* `metadata/analytics_builder/visual_recipes/` for visual recipe JSON;
* `metadata/analytics_builder/certification_packets/` for certification evidence packet JSON;
* `docs/analytics_builder_guide/` for guide markdown;
* `docs/analytics_builder_guide/demo_walkthroughs/` for demo walkthrough markdown;
* `docs/generated/analytics_builder_guide/` for generated HTML presentation output.

## Import Posture

The recommended later import approach is path reference plus compact extracts. Canonical JSON metadata can be referenced or copied as reviewed metadata extracts. Guide markdown and demo walkthrough markdown can become compact extracts. Generated HTML must remain reference-only and must not become source truth.

## Remaining M5 Blockers

M5 answer baselines remain blocked until a governed import manifest is created and reviewed.

Dataset count needs reconciliation: M1 says 9 datasets, while `metadata/analytics_builder/dataset_cards/` contains 6 files. Candidate/gap dataset metadata and dataset certification packets appear to cover the remaining blocked/gap datasets, but this must be verified.

Visual recipe count needs reconciliation: M1 says 13 visual recipes, while `metadata/analytics_builder/visual_recipes/` contains 10 files. `blocked_visual_recipes_v0_1.json` appears to cover blocked recipes, but this must be verified.

## Safety Posture

Current Certified asset count is zero. Final-paid payroll truth remains `UNPROVEN / Blocked`. PayrollLedger does not prove bank-paid truth. CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth. ObjectTime is source-context evidence, not payment finality. PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth. Visual rendering is not certification proof. Blocked gaps are safety controls, not failures.

Minerva must preserve proof statuses `PROVEN`, `LIKELY`, `POSSIBLE`, `DISPROVEN`, and `UNPROVEN`, and distinguish `Diagnostic`, `Transitional`, `Blocked`, and `Certified`.

When proof is missing, Minerva must say "not enough governed proof".

