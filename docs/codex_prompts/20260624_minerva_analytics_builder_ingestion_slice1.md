# 20260624 Minerva Analytics Builder Ingestion Slice 1 Prompt

```text
cd C:\Projects\ezeas-intelligence
codex -a never -s workspace-write

You are working only in the `ezeas-intelligence` repository.

We have just completed the `ezeas-analytics` Analytics Builder Guide static OMG v0.2 milestone.

Recommended analytics repo tag:
`analytics-builder-static-omg-v0.2-20260624`

Before beginning, do not modify `ezeas-analytics`, `workforce-platform`, `award-configurator-v1`, or any runtime/application repo. This slice is only for Minerva ingestion/readiness inside `ezeas-intelligence`.

This task is Minerva Analytics Builder Ingestion - Slice 1.

Goal:
Create the first Minerva ingestion/readiness layer for the Analytics Builder Guide corpus so Minerva can answer analytics-builder questions safely, with proof-status honesty and without overclaiming certification or final-paid truth.

The source corpus comes from the completed `ezeas-analytics` static Analytics Builder OMG v0.2 milestone. If local cross-repo access is unavailable, create the ingestion plan and expected source manifest without copying source content blindly.

Important source artifacts from `ezeas-analytics` include:

* Analytics Builder Guide spine.
* Dataset catalogue and dataset cards.
* Visual recipe library and recipe cards.
* Certification rules.
* Prohibited claims.
* Validation manifest.
* Certification evidence packets.
* Certification readiness report.
* Internal review/demo walkthrough pack.
* Blocked-gap roadmap.
* Blocked-gap action pack.
* v0.2 closeout package.
* Generated static guide.

Known v0.2 portfolio status:

* 9 datasets.
* 13 visual recipes.
* 6 validation assets.
* 4 validation gaps.
* 22 certification evidence packets.
* 0 certified assets.
* Certification statuses: Transitional 10, Diagnostic 4, Blocked 8.
* Proof statuses: LIKELY 14, UNPROVEN 8.
* Blocked gaps remain:

  * review/exception analytics;
  * roster-vs-actual/ObjectTime scheduling coverage;
  * standalone CalcInterpreterLine detail;
  * final bank-paid payroll truth.

Critical doctrine:

* Minerva must not claim any asset is Certified unless the source metadata says it is Certified.
* Current Certified asset count is zero.
* Final-paid payroll truth remains UNPROVEN / Blocked.
* PayrollLedger does not prove bank-paid truth.
* CalcInterpreterLine is calculation/detail evidence, not payment execution or final-paid truth.
* ObjectTime is source-context evidence, not payment finality.
* PayRun finalisation or SUCCEEDED status alone does not prove settlement, bank acceptance, remittance, or final-paid truth.
* Visual rendering is not certification proof.
* Blocked gaps are safety controls, not failures.
* Minerva must preserve proof statuses: PROVEN / LIKELY / POSSIBLE / DISPROVEN / UNPROVEN.
* Minerva must distinguish Diagnostic, Transitional, Blocked, and Certified.
* Minerva must say "not enough governed proof" rather than inventing proof.
* Do not create runtime UI.
* Do not create app routes.
* Do not create BI dashboards.
* Do not create SQL write paths.
* Do not create stored procedures.
* Do not modify payroll, payment, award, or scheduling runtime behaviour.
* Do not create a second analytics truth path.

Mandatory prompt and knowledge preservation:

1. Save this exact prompt into the `ezeas-intelligence` repository.
2. Create a verbose Minerva-ready knowledge artifact for this slice.
3. Create a concise diagnostic artifact.
4. Do not use `git add .`.
5. Do not commit unless explicitly asked after review.

Suggested prompt path:
`docs/codex_prompts/20260624_minerva_analytics_builder_ingestion_slice1.md`

Suggested diagnostic artifact:
`docs/diagnostics/20260624_minerva_analytics_builder_ingestion_slice1.md`
`docs/diagnostics/20260624_minerva_analytics_builder_ingestion_slice1.json`

Suggested knowledge artifact:
`docs/knowledge/20260624_minerva_analytics_builder_ingestion_slice1_knowledge.md`

First inspect the `ezeas-intelligence` repo structure:

* retrieval plan services;
* domain retrieval plans;
* worker story baselines;
* domain baselines;
* benchmark/evaluation structure;
* existing Minerva corpus/index conventions;
* existing tests for retrieval plans, knowledge packs, baseline capture, and safety wording;
* existing docs/knowledge conventions;
* any analytics, payroll, ObjectTime, source-truth, finality, or certification-related retrieval domains.

Then create a Minerva Analytics Builder ingestion/readiness plan.

Suggested docs:

* `docs/minerva/analytics_builder/20260624_ingestion_plan.md`
* `docs/minerva/analytics_builder/20260624_source_corpus_manifest.md`
* `docs/minerva/analytics_builder/20260624_answer_safety_contract.md`
* `docs/minerva/analytics_builder/20260624_benchmark_question_plan.md`

Suggested metadata:

* `metadata/minerva/analytics_builder_source_manifest.v0_1.json`
* `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
* `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`

Suggested tests:

* `tests/test_minerva_analytics_builder_source_manifest.py`
* `tests/test_minerva_analytics_builder_answer_safety_contract.py`
* `tests/test_minerva_analytics_builder_benchmark_questions.py`

If the repo has an existing retrieval plan registry, add a new planned retrieval domain only if it fits repo conventions:

* domain key suggestion: `analytics_builder_guide`
* status: planned / ingestion_ready / static_corpus_pending, depending on existing vocabulary.
  Do not overstate runtime ingestion if no actual indexing path exists yet.

Source corpus manifest should list expected source artifacts from `ezeas-analytics`, including:

* dataset catalogue;
* dataset cards;
* visual recipe library;
* visual recipe cards;
* certification rules;
* prohibited claims;
* validation manifest;
* certification evidence packets;
* certification readiness report;
* internal review/demo walkthrough pack;
* blocked-gap roadmap;
* blocked-gap action pack;
* v0.2 closeout;
* generated guide.

For each source artifact include:

* source_repo;
* source_path;
* expected purpose;
* expected Minerva use;
* trust/finality warning requirement;
* ingestion status;
* required before production answer use.

Answer safety contract must include:

* allowed answer patterns;
* prohibited claims;
* required disclaimers;
* required status wording;
* required blocked-gap wording;
* final-paid safety rules;
* CalcInterpreterLine safety rules;
* ObjectTime safety rules;
* PayrollLedger bridge safety rules;
* certification safety rules;
* visual rendering safety rules.

Benchmark question plan should include at least these questions:

1. Which dataset should I use for payroll cost by worksite?
2. Which visual recipe should I use for payroll cost by rate type?
3. Why is final-paid payroll truth blocked?
4. Can I use PayrollLedger as bank-paid proof?
5. Does CalcInterpreterLine prove payment execution?
6. Does ObjectTime prove payment finality?
7. Why are there zero Certified assets?
8. What is the difference between Diagnostic, Transitional, Blocked, and Certified?
9. What validations exist for payroll outcome analytics?
10. What validation gaps remain?
11. What should a reviewer look at first?
12. What blocked gaps need upstream proof?
13. How should Minerva explain blocked gaps?
14. What claims are prohibited for final-paid truth?
15. What is the recommended next stream after static v0.2?

For each benchmark question define:

* expected answer intent;
* required source artifact types;
* required safety wording;
* prohibited wording;
* expected status terms;
* whether the answer may be definitive or must be qualified.

Do not create actual answer baselines unless repo conventions make that safe and easy. If you do create baseline stubs, mark them as planned/pending source ingestion, not production-passed.

Create tests that validate:

1. Source manifest parses.
2. Source manifest includes required `ezeas-analytics` artifact groups.
3. Answer safety contract parses.
4. Safety contract blocks final-paid overclaims.
5. Safety contract blocks PayrollLedger-as-bank-paid proof.
6. Safety contract blocks CalcInterpreterLine-as-payment-execution proof.
7. Safety contract blocks ObjectTime-as-payment-finality proof.
8. Safety contract says zero Certified assets unless source says otherwise.
9. Benchmark question plan parses.
10. Benchmark question plan includes all required benchmark questions.
11. Benchmark entries contain required safety/prohibited wording fields.
12. Any retrieval-plan registry update, if made, follows existing repo conventions.
13. No runtime/app/payroll/payment/write path files are modified.

Verification:
Run targeted tests for the new files.
Run existing relevant retrieval/domain/baseline tests.
Run full pytest if practical.

Expected final response from Codex:

* Repo inspection summary.
* Whether actual ingestion path exists or only an ingestion/readiness plan was created.
* Files created/changed.
* Source manifest summary.
* Answer safety contract summary.
* Benchmark question plan summary.
* Retrieval plan registry changes, if any.
* Verification commands and results.
* Full suite result if run.
* Git status summary.
* Clear statement that no runtime/application behaviour was implemented.
* Clear statement that no final-paid/certification/trust posture was changed.
* Clear statement that no `ezeas-analytics` files were modified.
* Do not run `git add .`.
* Do not commit.
```
