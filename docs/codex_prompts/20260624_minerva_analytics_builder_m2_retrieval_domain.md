# 20260624 Minerva Analytics Builder M2 Retrieval Domain Prompt

```text
cd C:\Projects\ezeas-intelligence
codex -a never -s workspace-write

You are working only in the `ezeas-intelligence` repository.

This is Step 2 of the post-v0.2 Analytics Builder OMG plan.

Step 1 / M1 is complete:

* Created Analytics Builder source corpus manifest.
* Created answer safety contract.
* Created benchmark question plan.
* Created ingestion/readiness docs.
* Created diagnostics, Minerva-ready knowledge, saved prompt, and tests.
* Did not create runtime ingestion.
* Did not modify retrieval runtime code.
* Did not modify `ezeas-analytics`.
* Did not change final-paid, certification, or trust posture.
* Planned domain key `analytics_builder_guide` is currently metadata-only.
* Full suite currently has unrelated pre-existing dirty-runtime failures; do not attempt to fix those in this slice.

This task is Step 2 / M2 — Analytics Builder Retrieval Domain.

Goal:
Create a dedicated Minerva retrieval-domain planning layer for Analytics Builder Guide knowledge so Analytics Builder questions can be routed and retrieved separately from generic payroll, ObjectTime, payment, or source-truth domains.

This slice should make the Analytics Builder retrieval domain explicit, testable, and safety-aware.

This slice should not perform full corpus ingestion unless existing repo conventions make a metadata-only or planned-domain registration safe.
This slice should not modify runtime retrieval behaviour unless the existing repo pattern requires a static retrieval plan registry update and it can be done without touching unrelated dirty runtime files.

Critical boundaries:

* Do not modify `ezeas-analytics`.
* Do not modify `workforce-platform`.
* Do not modify `award-configurator-v1`.
* Do not modify runtime/app dirty files such as `app/core/config.py` or unrelated untracked Minerva runtime/service files.
* Do not create runtime UI.
* Do not create app routes.
* Do not create BI dashboards.
* Do not create SQL write paths.
* Do not create stored procedures.
* Do not modify payroll, payment, award, scheduling, or ObjectTime runtime behaviour.
* Do not create a second analytics truth path.
* Do not mark anything Certified.
* Do not change final-paid truth posture.
* Do not claim retrieval is production-enabled unless tests and repo conventions prove it.
* Do not fix unrelated pre-existing dirty worktree failures.
* Do not use `git add .`.
* Do not commit unless explicitly asked after review.

Critical answer doctrine for Minerva:

* Minerva must not claim any asset is Certified unless source metadata says it is Certified.
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
* Minerva must say “not enough governed proof” rather than inventing proof.

Mandatory prompt and knowledge preservation:

1. Save this exact prompt into the `ezeas-intelligence` repository.
2. Create a verbose Minerva-ready knowledge artifact for this slice.
3. Create a concise diagnostic artifact.
4. Keep all modifications limited to safe `ezeas-intelligence` metadata/docs/tests unless an existing retrieval-plan registry update is clearly conventional and safe.

Suggested prompt path:
`docs/codex_prompts/20260624_minerva_analytics_builder_m2_retrieval_domain.md`

Suggested diagnostic artifacts:
`docs/diagnostics/20260624_minerva_analytics_builder_m2_retrieval_domain.md`
`docs/diagnostics/20260624_minerva_analytics_builder_m2_retrieval_domain.json`

Suggested knowledge artifact:
`docs/knowledge/20260624_minerva_analytics_builder_m2_retrieval_domain_knowledge.md`

First inspect:

* `app/services/domain_retrieval_plan_service.py`
* existing tests for domain retrieval plans
* existing docs under `docs/minerva/domain_coverage/`
* existing metadata conventions under `metadata/minerva/`
* M1 files:

  * `metadata/minerva/analytics_builder_source_manifest.v0_1.json`
  * `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
  * `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`
  * `docs/minerva/analytics_builder/20260624_ingestion_plan.md`
  * `docs/minerva/analytics_builder/20260624_source_corpus_manifest.md`
  * `docs/minerva/analytics_builder/20260624_answer_safety_contract.md`
  * `docs/minerva/analytics_builder/20260624_benchmark_question_plan.md`
* existing retrieval domains for ObjectTime/source truth, payment execution/remittance, finalisation readiness, payroll output, payroll bases/totals, gross-to-net, process/payrun lifecycle.

Create a retrieval-domain plan for `analytics_builder_guide`.

Suggested docs:

* `docs/minerva/analytics_builder/20260624_retrieval_domain_plan.md`
* `docs/minerva/domain_coverage/analytics_builder_guide.md`

Suggested metadata:

* `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`

If the repo has a safe existing retrieval plan registry pattern, add a planned/static retrieval domain entry for `analytics_builder_guide`.
If that would require modifying dirty runtime files or production retrieval behaviour, do not modify runtime code. Instead record the proposed registry entry in metadata and documentation only.

The retrieval-domain metadata should include:

* domain_key: `analytics_builder_guide`
* domain_status: planned_static_corpus_pending or equivalent
* source_manifest_ref
* answer_safety_contract_ref
* benchmark_question_plan_ref
* retrieval_intent
* source_artifact_groups
* retrieval_term_groups
* routing_examples
* safety_critical_terms
* prohibited_routing_confusions
* related_domains
* escalation_rules
* not_production_enabled flag if applicable
* no_runtime_behavior flag
* no_trust_posture_change flag

Retrieval term groups should include at least:

1. Dataset selection.
2. Visual recipe selection.
3. Certification status.
4. Validation manifest.
5. Certification evidence packets.
6. Certification readiness.
7. Internal review/demo walkthroughs.
8. Blocked-gap roadmap.
9. Blocked-gap action pack.
10. Final-paid truth safety.
11. PayrollLedger bridge safety.
12. CalcInterpreterLine safety.
13. ObjectTime safety.
14. Prohibited claims.
15. Next-stream decision.

For each retrieval term group define:

* group_id;
* purpose;
* positive_terms;
* negative_or_confusion_terms;
* required_source_artifact_groups;
* required_safety_rules;
* benchmark_question_ids supported.

Routing examples should include:

* “Which dataset should I use for payroll cost by worksite?”
* “Why is final-paid truth blocked?”
* “Can PayrollLedger prove bank-paid truth?”
* “What validations exist?”
* “Why are there zero Certified assets?”
* “What should a reviewer look at first?”
* “What blocked gaps need upstream proof?”

Prohibited routing confusions should include:

* Do not route final-paid proof questions only to generic payroll lifecycle material.
* Do not route payment execution questions as if Analytics Builder has certified final-paid proof.
* Do not route ObjectTime scheduling questions as if roster-vs-actual is proven.
* Do not route CalcInterpreterLine questions as if it is final-paid proof.
* Do not route rendered visual questions as certification proof.
* Do not route blocked-gap questions as defects/failures.

Create tests such as:
`tests/test_minerva_analytics_builder_retrieval_domain.py`

Tests should validate:

1. Retrieval-domain metadata parses.
2. Domain key is `analytics_builder_guide`.
3. Domain status does not claim production-enabled unless a real registry update was safely made.
4. Metadata references the M1 source manifest.
5. Metadata references the M1 answer safety contract.
6. Metadata references the M1 benchmark question plan.
7. Required retrieval term groups exist.
8. Final-paid retrieval terms include blocked/UNPROVEN/finality safety wording.
9. PayrollLedger retrieval terms include not-bank-paid-proof warning.
10. CalcInterpreterLine retrieval terms include calculation/detail warning.
11. ObjectTime retrieval terms include source-context/not-payment-finality warning.
12. Prohibited routing confusions are present.
13. Routing examples cover key M1 benchmark questions.
14. If a registry update is made, existing retrieval-domain tests still pass.
15. No unrelated runtime/app/payroll/payment/write path files are modified.

Verification:
Run:

* JSON validation for new retrieval-domain metadata and diagnostic JSON.
* New targeted retrieval-domain test.
* M1 tests:
  `python -m pytest tests/test_minerva_analytics_builder_source_manifest.py tests/test_minerva_analytics_builder_answer_safety_contract.py tests/test_minerva_analytics_builder_benchmark_questions.py`
* Existing retrieval plan tests:
  `python -m pytest tests/test_domain_retrieval_plans.py`
* Existing relevant knowledge/manifest tests:
  `python -m pytest tests/test_minerva_knowledge_artifact_inventory_service.py tests/test_manifest_ingestion.py`
* Do not run full suite unless practical; if run, classify the known pre-existing dirty-worktree failures and do not fix them.

Do not require a live database.
Do not run destructive commands.
Do not stage.
Do not commit.

Expected final response from Codex:

* Repo inspection summary.
* Whether runtime retrieval registry was changed or left metadata-only.
* Retrieval-domain metadata created.
* Retrieval term groups created.
* Routing examples created.
* Safety/prohibited routing rules created.
* Files created/changed.
* Verification commands run and results.
* Full suite result if run, with classification of unrelated pre-existing failures.
* Git status summary.
* Clear statement that no runtime/application behaviour was implemented unless a safe registry-only change was intentionally made.
* Clear statement that no final-paid/certification/trust posture was changed.
* Clear statement that no `ezeas-analytics` files were modified.
* Do not run `git add .`.
* Do not commit.
```
