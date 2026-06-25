# Analytics Builder Governed Import Manifest - M5

Machine-readable manifest: `metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json`

## What Minerva May Reference

Minerva may reference canonical JSON metadata under `metadata/analytics_builder/` and guide markdown under `docs/analytics_builder_guide/` after preserving source repo, source tag, source path, artifact group, and safety notes.

## What Minerva May Extract

Minerva may later create compact extracts from:

* dataset catalogue and dataset card JSON;
* candidate/gap dataset register JSON;
* visual recipe library and recipe JSON;
* blocked recipe register JSON;
* certification evidence packet JSON;
* certification readiness report JSON;
* prohibited claims JSON;
* guide markdown and demo walkthrough markdown.

## What Minerva Must Not Copy

Generated HTML under `docs/generated/analytics_builder_guide/` must not be bulk-copied and must not be treated as source truth.

SQL artifacts must not be imported into this Minerva static answer corpus and must not create write paths.

## Source Lineage

Every import unit must retain:

* source repo: `ezeas-analytics`;
* source tag: `analytics-builder-static-omg-v0.2-20260624`;
* canonical source path;
* import method;
* safety requirements;
* baseline and production-use gates.

## Safety Preservation

Current Certified asset count remains zero. Final-paid payroll truth remains `UNPROVEN / Blocked`. PayrollLedger does not prove bank-paid truth. CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth. ObjectTime is source-context evidence, not payment finality. Visual rendering is not certification proof.

## Baseline Support

The manifest supports M6 restricted baseline stubs. It does not allow production-passed baselines or production answer use.
