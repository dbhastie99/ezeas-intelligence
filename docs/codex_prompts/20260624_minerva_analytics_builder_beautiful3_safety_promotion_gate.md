# Codex Prompt: 20260624 Minerva Analytics Builder Beautiful 3 Safety Promotion Gate

```text
cd C:\Projects\ezeas-intelligence
codex -a never -s workspace-write

You are working only in the `ezeas-intelligence` repository.

This is Beautiful Slice 3 of 10 for the Analytics Builder OMG productisation phase.

Beautiful Slice 1 is complete:

* Governed static source import package created.
* Compact imported corpus extracts created.
* Source lineage recorded to `ezeas-analytics`.
* Generated HTML was not copied and remains reference-only.
* Production answer use remained blocked pending evaluated baselines and safety promotion.

Beautiful Slice 2 is complete:

* Curated static evaluated answer baselines created.
* All 15 benchmark questions covered.
* Baseline status: `evaluated_non_production_pending_safety_promotion`.
* Production answer use: `not_allowed_pending_safety_promotion`.
* Production-passed: false.
* Runtime-enabled: false.
* Beautiful 3 safety promotion is required.
* No live LLM evaluation or runtime generation was used.

This task is:

Beautiful 3 — Minerva Safety Promotion Gate.

Goal:
Run a static safety promotion evaluation over the Beautiful 2 evaluated answer baselines using the M7 safety regression harness.

This slice should determine whether the evaluated non-production answer baselines pass the safety gate and can be marked as safety-promoted for controlled non-production/demo use.

Important:
This slice may promote evaluated baselines only to a controlled non-production safety-promoted status if all static safety rules pass.

This slice must not mark answers production-passed.
This slice must not enable production answer use.
This slice must not claim live Minerva runtime answers are production-ready.

Allowed outcome if all checks pass:

* `safety_promoted_non_production`
* `controlled_demo_answer_use_allowed`
* `production_answer_use_status: not_allowed_pending_runtime_ingestion_and_production_evaluation`

Not allowed:

* `production_passed`
* `runtime_enabled`
* `production_answer_use_allowed`
* `certified`
* any final-paid proof promotion.

Critical boundaries:

* Do not run live LLM evaluation unless repo has a safe mocked/static convention; prefer static evaluation of the curated Beautiful 2 answers.
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
4. Keep all modifications limited to safe docs/metadata/tests/static safety-promotion files.
5. Do not stage or commit.

Suggested prompt path:
`docs/codex_prompts/20260624_minerva_analytics_builder_beautiful3_safety_promotion_gate.md`

Suggested diagnostic artifacts:
`docs/diagnostics/20260624_minerva_analytics_builder_beautiful3_safety_promotion_gate.md`
`docs/diagnostics/20260624_minerva_analytics_builder_beautiful3_safety_promotion_gate.json`

Suggested knowledge artifact:
`docs/knowledge/20260624_minerva_analytics_builder_beautiful3_safety_promotion_gate.md`

First inspect:

* Beautiful 1 governed source import:
  `metadata/minerva/analytics_builder_governed_source_import.v0_1.json`
* Beautiful 1 imported corpus extracts:
  `docs/knowledge/minerva/analytics_builder/imported_corpus/`
* Beautiful 2 evaluated baselines:
  `metadata/minerva/analytics_builder_evaluated_answer_baselines.v0_1.json`
* Beautiful 2 evaluated sample/eval file:
  `samples/eval/analytics_builder_benchmark.evaluated_non_production.v0_1.json`
* M7 safety regression harness:
  `metadata/minerva/analytics_builder_safety_regression_harness.v0_1.json`
* M1 answer safety contract:
  `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
* M6 baseline stubs:
  `metadata/minerva/analytics_builder_answer_baseline_stubs.v0_1.json`
* M8 demo readiness pack:
  `metadata/minerva/analytics_builder_demo_readiness_pack.v0_1.json`
* existing safety/eval/verification test conventions.

Create metadata:
`metadata/minerva/analytics_builder_safety_promotion_gate.v0_1.json`

The metadata should include:

* promotion_version;
* promotion_status: `safety_promoted_non_production` if all checks pass, otherwise `safety_promotion_blocked`;
* controlled_demo_answer_use_status;
* production_answer_use_status: `not_allowed_pending_runtime_ingestion_and_production_evaluation`;
* source_evaluated_baselines_ref;
* source_safety_harness_ref;
* source_answer_safety_contract_ref;
* source_import_ref;
* safety_rule_results;
* negative_case_results;
* positive_requirement_results;
* answer_level_results;
* prohibited_claim_scan_results;
* required_wording_scan_results;
* promotion_decision;
* promotion_limitations;
* production_blockers_remaining;
* no_runtime_behavior flag;
* no_trust_posture_change flag;
* no_source_repo_modification flag.

For each safety rule record:

* rule_id;
* result: pass/fail;
* evaluated_questions;
* evidence;
* notes.

For each answer record:

* question_id;
* safety_gate_result;
* required_terms_present;
* prohibited_claims_absent;
* proof_status_preserved;
* certification_status_preserved;
* final_paid_safety_preserved;
* promotion_allowed_for_non_production_demo;
* production_promotion_allowed: false;
* notes.

Create sample/eval promotion artifact if consistent with repo conventions:
`samples/eval/analytics_builder_benchmark.safety_promoted_non_production.v0_1.json`

This file must clearly state:

* non-production;
* not runtime-enabled;
* not production-passed;
* not production answer use;
* controlled demo only.

Create docs:

* `docs/minerva/analytics_builder/20260624_safety_promotion_gate.md`
* `docs/minerva/analytics_builder/20260624_safety_promotion_results.md`
* `docs/minerva/analytics_builder/20260624_production_answer_use_blockers.md`

The safety promotion gate doc should include:

1. Purpose.
2. Inputs.
3. Safety rules evaluated.
4. Promotion decision.
5. Why this is still non-production.
6. What controlled demo use means.
7. What remains blocked for production.

The safety promotion results doc should include:

1. Question-level results.
2. Safety-rule results.
3. Negative case results.
4. Positive requirement results.
5. Prohibited claim scan summary.
6. Required wording scan summary.

The production blockers doc should include:

1. No runtime ingestion.
2. No live LLM production evaluation.
3. No production answer serving.
4. No authentication/entitlement enforcement.
5. No final-paid proof.
6. No Certified assets.
7. No runtime audit.

Suggested tests:
`tests/test_minerva_analytics_builder_safety_promotion_gate.py`

Tests should validate:

1. Safety promotion metadata parses.
2. Promotion status is either safety_promoted_non_production or safety_promotion_blocked.
3. If promoted, controlled demo answer use is allowed.
4. Production answer use remains blocked.
5. Metadata references Beautiful 2 evaluated baselines.
6. Metadata references M7 safety harness.
7. Metadata references M1 answer safety contract.
8. Metadata references Beautiful 1 source import.
9. All 15 questions have answer-level safety results.
10. All M7 safety rules have results.
11. Prohibited claim scan includes final-paid overclaims.
12. Prohibited claim scan includes PayrollLedger bank-paid overclaims.
13. Prohibited claim scan includes CalcInterpreterLine payment execution overclaims.
14. Prohibited claim scan includes ObjectTime payment finality overclaims.
15. Required wording scan includes final-paid UNPROVEN / Blocked wording.
16. Required wording scan includes zero Certified assets wording.
17. If sample/eval promotion file exists, it is non-production and not production-passed.
18. Production blockers include runtime ingestion/evaluation/auth/audit blockers.
19. No runtime/app/payroll/payment/write path files are modified.

Verification:
Run:

* JSON validation for safety promotion metadata, optional sample/eval JSON, and diagnostic JSON.
* New targeted safety promotion gate test.
* Beautiful 2 test:
  `python -m pytest tests/test_minerva_analytics_builder_evaluated_answer_baselines.py`
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
* Safety promotion metadata created.
* Sample/eval promotion file created or not, with reason.
* Promotion status.
* Controlled demo answer use status.
* Production answer use status.
* Safety rule results summary.
* Question-level results summary.
* Prohibited claim scan summary.
* Required wording scan summary.
* Production blockers remaining.
* Whether Beautiful 4 can proceed.
* Files created/changed.
* Verification commands run and results.
* Full suite result if run, with classification of unrelated failures if any.
* Git status summary.
* Clear statement that no runtime/application behaviour was implemented.
* Clear statement that no final-paid/certification/trust posture changed.
* Clear statement that no `ezeas-analytics`, `workforce-platform`, `award-configurator-v1`, or Ezeas-FastAPI files were modified.
* Do not run `git add .`.
* Do not commit.
```
