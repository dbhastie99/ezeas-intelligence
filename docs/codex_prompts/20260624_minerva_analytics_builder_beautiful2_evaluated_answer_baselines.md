# Codex Prompt: 20260624 Minerva Analytics Builder Beautiful 2 Evaluated Answer Baselines

```text
cd C:\Projects\ezeas-intelligence
codex -a never -s workspace-write

You are working only in the `ezeas-intelligence` repository.

This is Beautiful Slice 2 of 10 for the Analytics Builder OMG productisation phase.

Beautiful Slice 1 is complete:

* Created governed static source import metadata.
* Created compact imported corpus extracts.
* Recorded source lineage to `ezeas-analytics`.
* Confirmed source tag `analytics-builder-static-omg-v0.2-20260624`.
* Recorded inspected source HEAD.
* Did not copy generated HTML.
* Generated HTML remains reference-only, not source truth.
* Beautiful Slice 2 evaluated answer baselines may proceed in non-production scope.
* Production answer use remains blocked pending evaluated baselines and safety promotion.

This task is:

Beautiful 2 — Evaluated Minerva Answer Baselines.

Goal:
Convert the planned/pending Analytics Builder answer baseline stubs into evaluated non-production answer baselines using the governed imported corpus extracts from Beautiful Slice 1.

The output should create safe, source-grounded expected answers for the Analytics Builder benchmark questions, with explicit source references, safety assertions, prohibited-claim checks, and non-production status.

This slice should create evaluated baseline artifacts, but must not mark them production-passed.

Production answer use must remain blocked until Beautiful Slice 3 safety promotion gate passes.

Critical boundaries:

* Do not run live LLM evaluation unless the repo already has a safe mocked/static evaluation convention. Prefer curated/static evaluated baseline answers grounded in the imported corpus extracts.
* Do not mark baselines production-passed.
* Do not claim Minerva is production-ready.
* Do not create runtime answer generation.
* Do not create runtime ingestion behaviour.
* Do not modify retrieval runtime code.
* Do not modify unrelated dirty runtime/app files in `ezeas-intelligence`, including `app/core/config.py` and existing untracked Minerva runtime/service files.
* Do not modify `ezeas-analytics`.
* Do not modify `workforce-platform`.
* Do not modify `award-configurator-v1`.
* Do not modify `Ezeas-FastAPI`.
* Do not create app routes.
* Do not create APIs.
* Do not create runtime UI.
* Do not create SQL write paths.
* Do not create stored procedures.
* Do not create payroll/payment/award/scheduling/ObjectTime writes.
* Do not create a second analytics truth path.
* Do not mark anything Certified.
* Do not change final-paid truth posture.
* Do not use `git add .`.
* Do not commit unless explicitly asked after review.

Critical answer/proof doctrine:

* Current Certified asset count is zero.
* Final-paid payroll truth remains UNPROVEN / Blocked.
* PayrollLedger is not bank-paid proof.
* CalcInterpreterLine is calculation/detail evidence, not payment execution proof.
* ObjectTime is source-context evidence, not payment finality proof.
* PayRun finalisation or SUCCEEDED alone does not prove settlement, bank acceptance, remittance, or final-paid truth.
* Visual rendering is not certification proof.
* Validation passing is evidence, not automatic certification.
* Refresh/update is not certification.
* Export is not publishing unless a governed publishing workflow says so.
* Blocked gaps are safety controls, not failures.
* Minerva must preserve Diagnostic / Transitional / Blocked / Certified language.
* Minerva must preserve PROVEN / LIKELY / POSSIBLE / DISPROVEN / UNPROVEN language.
* Minerva must say “not enough governed proof” rather than inventing proof.
* Diagnostic/Transitional assets may be useful with warnings, but are not Certified.
* Blocked assets require upstream proof before promotion.

Mandatory prompt and knowledge preservation:

1. Save this exact prompt into the `ezeas-intelligence` repository.
2. Create a verbose Minerva-ready knowledge artifact for this slice.
3. Create a concise diagnostic artifact.
4. Keep all modifications limited to safe docs/metadata/tests/static evaluated-baseline files.
5. Do not stage or commit.

Suggested prompt path:
`docs/codex_prompts/20260624_minerva_analytics_builder_beautiful2_evaluated_answer_baselines.md`

Suggested diagnostic artifacts:
`docs/diagnostics/20260624_minerva_analytics_builder_beautiful2_evaluated_answer_baselines.md`
`docs/diagnostics/20260624_minerva_analytics_builder_beautiful2_evaluated_answer_baselines.json`

Suggested knowledge artifact:
`docs/knowledge/20260624_minerva_analytics_builder_beautiful2_evaluated_answer_baselines.md`

First inspect:

* Beautiful 1 governed source import:
  `metadata/minerva/analytics_builder_governed_source_import.v0_1.json`
* Beautiful 1 imported corpus extracts:
  `docs/knowledge/minerva/analytics_builder/imported_corpus/`
* M1 benchmark question plan:
  `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`
* M1 answer safety contract:
  `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
* M2 retrieval domain:
  `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`
* M6 answer baseline stubs:
  `metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json`
* M6 planned eval file:
  `samples/eval/analytics_builder_benchmark.planned.v0_1.json`
* M7 safety regression harness:
  `metadata/minerva/analytics_builder_safety_regression_harness.v0_1.json`
* M8 demo readiness pack:
  `metadata/minerva/analytics_builder_demo_readiness_pack.v0_1.json`
* existing rich-answer benchmark/evaluation conventions under:
  `samples/eval/`
* existing tests for benchmark/eval and answer verification.

Create metadata:
`metadata/minerva/analytics_builder_evaluated_answer_baselines.v0_1.json`

The metadata should include:

* baseline_version;
* baseline_status: `evaluated_non_production_pending_safety_promotion`;
* production_answer_use_status: `not_allowed_pending_safety_promotion`;
* source_import_ref;
* source_benchmark_question_plan_ref;
* source_answer_safety_contract_ref;
* source_retrieval_domain_ref;
* source_answer_baseline_stubs_ref;
* source_safety_harness_ref;
* evaluated_baseline_entries;
* evaluation_method;
* source_grounding_summary;
* safety_assertion_summary;
* unresolved_answer_limitations;
* beautiful3_safety_promotion_required flag;
* no_runtime_behavior flag;
* no_trust_posture_change flag;
* no_source_repo_modification flag.

Create evaluated sample/eval artifact if consistent with repo conventions:
`samples/eval/analytics_builder_benchmark.evaluated_non_production.v0_1.json`

This file must clearly state:

* non-production;
* not production-passed;
* not runtime-enabled;
* pending Beautiful 3 safety promotion.

For each of the 15 benchmark questions, create an evaluated baseline entry with:

* question_id;
* question;
* evaluated_answer_status: `evaluated_non_production`;
* expected_answer;
* source_extract_refs;
* required_safety_terms_present;
* prohibited_claims_absent;
* proof_status_terms;
* certification_status_terms;
* blocked_status_terms;
* answer_limitations;
* allowed_confidence;
* not_allowed_claims;
* readiness_for_safety_promotion;
* reviewer_notes.

The 15 questions are:

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

Expected answers should be concise, grounded, and safe. They should not be overly long. They should include warnings where necessary.

Do not invent sources. Reference imported corpus extract files, not raw generated HTML.

Create docs:

* `docs/minerva/analytics_builder/20260624_evaluated_answer_baselines.md`
* `docs/minerva/analytics_builder/20260624_evaluated_answer_baseline_limitations.md`
* `docs/minerva/analytics_builder/20260624_beautiful3_safety_promotion_readiness.md`

The evaluated answer baselines doc should include:

1. Purpose.
2. Why these are non-production evaluated baselines.
3. Source corpus used.
4. Evaluation method.
5. Question coverage.
6. Safety posture.
7. Production answer use status.
8. What Beautiful 3 must do.

The limitations doc should include:

1. No live runtime answer generation.
2. No production answer use yet.
3. No final-paid proof.
4. No Certified assets.
5. No generated HTML source truth.
6. No runtime ingestion or API.

The Beautiful 3 readiness doc should state:

* whether all 15 answers are ready for static safety promotion checks;
* what safety checks must run;
* what would block promotion.

Suggested tests:
`tests/test_minerva_analytics_builder_evaluated_answer_baselines.py`

Tests should validate:

1. Evaluated answer baseline metadata parses.
2. Baseline status is evaluated non-production pending safety promotion.
3. Production answer use remains blocked.
4. Metadata references Beautiful 1 source import.
5. Metadata references M1 benchmark plan.
6. Metadata references M1 safety contract.
7. Metadata references M6 baseline stubs.
8. Metadata references M7 safety harness.
9. All 15 benchmark questions have evaluated entries.
10. Every evaluated answer has source extract refs.
11. Every evaluated answer has required safety terms.
12. Every evaluated answer has prohibited claims absent.
13. Final-paid answer preserves UNPROVEN / Blocked posture.
14. PayrollLedger answer says not bank-paid proof.
15. CalcInterpreterLine answer says not payment execution proof.
16. ObjectTime answer says not payment finality proof.
17. Certified assets answer says current Certified count is zero.
18. Blocked gaps answer treats blocked gaps as safety controls.
19. Sample/eval evaluated file, if created, is non-production and not production-passed.
20. Beautiful 3 safety promotion required flag exists.
21. No runtime/app/payroll/payment/write path files are modified.

Verification:
Run:

* JSON validation for evaluated answer baseline metadata, optional sample/eval JSON, and diagnostic JSON.
* New targeted evaluated answer baseline test.
* Beautiful 1 test:
  `python -m pytest tests/test_minerva_analytics_builder_governed_source_import.py`
* M1 tests:
  `python -m pytest tests/test_minerva_analytics_builder_source_manifest.py tests/test_minerva_analytics_builder_answer_safety_contract.py tests/test_minerva_analytics_builder_benchmark_questions.py`
* M2 test:
  `python -m pytest tests/test_minerva_analytics_builder_retrieval_domain.py`
* M3 test:
  `python -m pytest tests/test_minerva_analytics_builder_knowledge_pack.py`
* M4 test:
  `python -m pytest tests/test_minerva_analytics_builder_source_path_reconciliation.py`
* M5 test:
  `python -m pytest tests/test_minerva_analytics_builder_governed_import_manifest.py`
* M6 test:
  `python -m pytest tests/test_minerva_analytics_builder_answer_baseline_stubs.py`
* M7 test:
  `python -m pytest tests/test_minerva_analytics_builder_safety_regression_harness.py`
* M8 test:
  `python -m pytest tests/test_minerva_analytics_builder_demo_readiness_pack.py`
* Existing relevant knowledge/manifest/retrieval tests:
  `python -m pytest tests/test_minerva_knowledge_artifact_inventory_service.py tests/test_manifest_ingestion.py tests/test_domain_retrieval_plans.py`
* Do not run full suite unless practical; if run, classify known unrelated pre-existing dirty-worktree failures and do not fix them.

Do not require a live database.
Do not run destructive commands.
Do not stage.
Do not commit.

Expected final response from Codex:

* Repo inspection summary.
* Evaluated baseline metadata created.
* Evaluated sample/eval file created or not, with reason.
* Number of evaluated questions.
* Baseline status.
* Production answer use status.
* Safety assertion summary.
* Beautiful 3 readiness summary.
* Files created/changed.
* Verification commands run and results.
* Full suite result if run, with classification of unrelated failures if any.
* Git status summary.
* Clear statement that no runtime/application behaviour was implemented.
* Clear statement that no final-paid/certification/trust posture changed.
* Clear statement that no `ezeas-analytics`, `workforce-platform`, `award-configurator-v1`, or `Ezeas-FastAPI` files were modified.
* Do not run `git add .`.
* Do not commit.
```
