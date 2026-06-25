# Minerva Knowledge Artifact: Analytics Builder M6 Answer Baseline Stubs

This knowledge artifact records the M6 planning layer for Analytics Builder Guide answer evaluation.

M6 creates planned/pending answer baseline stubs only. It does not create production-passed baselines and does not enable production Minerva answers from the Analytics Builder corpus.

## Inputs

- M1 benchmark question plan: `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`
- M1 answer safety contract: `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
- M2 retrieval domain: `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`
- M5 governed import manifest: `metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json`

## Created Layer

The primary M6 artifact is `metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json`.

It defines 15 baseline entries. Each entry records:

- question ID and question text;
- expected answer intent;
- required source artifact groups;
- required retrieval term groups;
- required safety wording;
- prohibited wording;
- required status terms;
- qualification limits;
- expected outline;
- safety assertions;
- readiness blockers;
- evaluation notes.

The optional sample/eval file `samples/eval/analytics_builder_benchmark.planned.v0_1.json` mirrors the question list for future evaluation harness work, but it is explicitly planned/pending and not production-passed.

## Safety Controls

Future Analytics Builder answers must preserve these controls:

- Current Certified asset count is zero.
- Final-paid payroll truth remains UNPROVEN / Blocked.
- PayrollLedger does not prove bank-paid truth.
- CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth.
- ObjectTime is source-context evidence, not payment finality.
- PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth.
- Visual rendering is not certification proof.
- Blocked gaps are safety controls, not failures.
- Minerva must say not enough governed proof rather than inventing proof.

## Readiness

M6 makes M7-style answer evaluation easier, but it does not make answer use production-ready. The next required step is governed source import execution from the M5 manifest followed by answer candidate generation and evaluation.
