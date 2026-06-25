# 20260624 Minerva Analytics Builder M5 Source Count Import Manifest Prompt

```text
cd C:\Projects\ezeas-intelligence
codex -a never -s workspace-write

You are working only in the `ezeas-intelligence` repository.

This is Step 5 of the post-v0.2 Analytics Builder OMG plan.

Important sequencing update:
Answer baselines remain blocked because M4 found source count/path reconciliation issues.

M4 findings:

* `C:\Projects\ezeas-analytics` exists locally.
* Expected tag exists:
  `analytics-builder-static-omg-v0.2-20260624`
* M1 expected paths under `docs/analytics_builder/...` were stale/wrong.
* Actual canonical source locations include:

  * `metadata/analytics_builder/`
  * `metadata/analytics_builder/dataset_cards/`
  * `metadata/analytics_builder/visual_recipes/`
  * `metadata/analytics_builder/certification_packets/`
  * `docs/analytics_builder_guide/`
  * `docs/analytics_builder_guide/demo_walkthroughs/`
  * `docs/generated/analytics_builder_guide/`
* Generated HTML exists under `docs/generated/analytics_builder_guide/` with 38 HTML files.
* Generated HTML is reference-only and must not be bulk-copied or treated as source truth.
* M1 expected 9 datasets, but M4 found 6 dataset card files.
* M1 expected 13 visual recipes, but M4 found 10 visual recipe files.
* M5 answer baselines are blocked until the count mismatch is reconciled and a governed import manifest is created/reviewed.

Completed so far:

M1 — Minerva Analytics Builder Ingestion Contract:

* source corpus manifest;
* answer safety contract;
* benchmark question plan;
* ingestion/readiness docs;
* diagnostics, knowledge artifact, saved prompt, tests.

M2 — Analytics Builder Retrieval Domain:

* metadata-only planned retrieval domain;
* domain key `analytics_builder_guide`;
* 15 retrieval term groups;
* routing examples and prohibited routing confusions;
* no runtime registry modification.

M3 — Corpus Knowledge Pack Registration:

* static knowledge-pack manifest;
* static corpus registration docs;
* static corpus index docs;
* safety summary;
* all 15 M1 artifact groups covered;
* status: `static_corpus_registered_metadata_only`;
* production answer use: `not_allowed_pending_governed_source_ingestion`;
* no source content copied.

M4 — Source Path Reconciliation and Governed Import Plan:

* confirmed canonical source paths;
* confirmed expected v0.2 tag;
* identified stale M1 source paths;
* identified dataset/recipe count mismatch;
* kept answer baselines blocked.

Known repo condition:
The `ezeas-intelligence` worktree has pre-existing dirty runtime/app files, including `app/core/config.py` and untracked Minerva runtime/service files. Do not modify, stage, clean, fix, or rely on those unrelated files in this slice. Full-suite status-sensitive failures from those dirty files are known and unrelated.

This task is:

M5 — Source Count Reconciliation and Governed Import Manifest.

Goal:
Resolve the dataset and visual recipe count mismatch by inspecting canonical `ezeas-analytics` metadata read-only, then create a governed import manifest that defines exactly which Analytics Builder source artifacts Minerva may use in later answer baselines.

This slice should answer:

* Why does M1 say 9 datasets while only 6 dataset card files were found?
* Why does M1 say 13 visual recipes while only 10 visual recipe files were found?
* Are some datasets/recipes represented in catalogue/library files but not separate card files?
* Are some packet/gap/candidate assets counted as datasets/recipes?
* Which canonical JSON files should Minerva import or reference?
* Which markdown docs should Minerva import or summarise?
* Which generated HTML files should remain reference-only?
* Is the corpus ready for M6 answer baselines after this slice?
* If not, exactly what remains blocked?

Critical boundaries:

* Do not modify `ezeas-analytics`.
* Do not modify `workforce-platform`.
* Do not modify `award-configurator-v1`.
* Do not modify runtime/app dirty files such as `app/core/config.py` or unrelated untracked Minerva runtime/service files.
* Do not bulk-copy generated HTML.
* Do not treat generated HTML as source truth.
* Do not create runtime ingestion behaviour.
* Do not modify retrieval runtime code.
* Do not create runtime UI.
* Do not create app routes.
* Do not create BI dashboards.
* Do not create SQL write paths.
* Do not create stored procedures.
* Do not modify payroll, payment, award, scheduling, or ObjectTime runtime behaviour.
* Do not create a second analytics truth path.
* Do not mark anything Certified.
* Do not change final-paid truth posture.
* Do not claim production answer use is allowed unless governed source import/readiness criteria are met.
* Do not fix unrelated pre-existing dirty worktree failures.
* Do not use `git add .`.
* Do not commit unless explicitly asked after review.

Critical answer doctrine for Minerva:

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
4. Keep all modifications limited to safe docs/metadata/tests/static planning files.
5. Do not stage or commit.

Suggested prompt path:
`docs/codex_prompts/20260624_minerva_analytics_builder_m5_source_count_import_manifest.md`

Suggested diagnostic artifacts:
`docs/diagnostics/20260624_minerva_analytics_builder_m5_source_count_import_manifest.md`
`docs/diagnostics/20260624_minerva_analytics_builder_m5_source_count_import_manifest.json`

Suggested knowledge artifact:
`docs/knowledge/20260624_minerva_analytics_builder_m5_source_count_import_manifest.md`

First inspect read-only in `C:\Projects\ezeas-analytics`:

* `metadata/analytics_builder/dataset_catalogue.v0_1.json`
* `metadata/analytics_builder/dataset_cards/`
* `metadata/analytics_builder/visual_recipe_library.v0_1.json`
* `metadata/analytics_builder/visual_recipes/`
* `metadata/analytics_builder/certification_evidence_packets.v0_1.json`
* `metadata/analytics_builder/certification_packets/`
* `metadata/analytics_builder/certification_readiness_report.v0_1.json`
* `metadata/analytics_builder/blocked_gap_roadmap.v0_1.json`
* `metadata/analytics_builder/blocked_gap_action_pack.v0_1.json`
* `metadata/analytics_builder/v0_2_closeout.v0_1.json`
* `metadata/analytics_builder/validation_manifest.v0_1.json`
* `docs/analytics_builder_guide/`
* `docs/analytics_builder_guide/demo_walkthroughs/`
* `docs/generated/analytics_builder_guide/`

Also inspect current M1-M4 metadata in `ezeas-intelligence`:

* `metadata/minerva/analytics_builder_source_manifest.v0_1.json`
* `metadata/minerva/analytics_builder_knowledge_pack.v0_1.json`
* `metadata/minerva/analytics_builder_source_path_reconciliation.v0_1.json`
* `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`
* `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`

Create metadata:
`metadata/minerva/analytics_builder_governed_import_manifest.v0_1.json`

The governed import manifest should include:

* import_manifest_version;
* source_repo;
* source_repo_path_checked;
* source_tag_checked;
* m1_source_manifest_ref;
* m3_knowledge_pack_ref;
* m4_reconciliation_ref;
* import_readiness_status;
* dataset_count_reconciliation;
* visual_recipe_count_reconciliation;
* source_artifacts_to_reference;
* source_artifacts_to_extract;
* source_artifacts_not_to_copy;
* source_artifacts_unresolved;
* canonical_import_units;
* required_safety_contract_ref;
* required_retrieval_domain_ref;
* answer_baseline_readiness;
* production_answer_use_status;
* no_source_repo_modification flag;
* no_runtime_behavior flag;
* no_trust_posture_change flag.

Dataset count reconciliation should include:

* expected_count_from_m1;
* catalogue_count;
* dataset_card_file_count;
* dataset_packet_count if relevant;
* exact dataset IDs from catalogue;
* exact dataset card IDs/files;
* IDs with card files;
* IDs without card files;
* explanation of discrepancy;
* import decision per dataset ID.

Visual recipe count reconciliation should include:

* expected_count_from_m1;
* visual_recipe_library_count;
* visual_recipe_file_count;
* recipe_packet_count if relevant;
* exact recipe IDs from library;
* exact recipe file IDs/files;
* IDs with recipe files;
* IDs without recipe files;
* explanation of discrepancy;
* import decision per recipe ID.

Canonical import units should include:

* unit_id;
* source_path;
* source_type: json_metadata, markdown_doc, generated_html_reference, test_reference, diagnostic_reference;
* import_method: reference_only, compact_extract, metadata_copy, do_not_copy_reference_only, unresolved;
* purpose_for_minerva;
* safety_requirements;
* required_before_answer_baselines;
* required_before_production_answer_use.

Create docs:

* `docs/minerva/analytics_builder/20260624_source_count_reconciliation.md`
* `docs/minerva/analytics_builder/20260624_governed_import_manifest.md`
* `docs/minerva/analytics_builder/20260624_m6_answer_baseline_readiness.md`

The source count reconciliation doc should explain:

1. Why counts differed.
2. Dataset reconciliation findings.
3. Visual recipe reconciliation findings.
4. Whether counts are now explainable.
5. Whether additional missing source files are a problem or expected design.

The governed import manifest doc should explain:

1. What Minerva may reference.
2. What Minerva may extract.
3. What Minerva must not copy.
4. Why generated HTML is reference-only.
5. How source lineage is preserved.
6. How final-paid/certification safety is preserved.
7. How this supports answer baselines.

The M6 answer baseline readiness doc should state:

1. Whether M6 can proceed.
2. If yes, under what restrictions.
3. If no, what remains unresolved.
4. Which benchmark questions are safe for baseline stubs.
5. Which benchmark questions must remain pending or heavily qualified.

Suggested tests:
`tests/test_minerva_analytics_builder_governed_import_manifest.py`

Tests should validate:

1. Governed import manifest parses.
2. Manifest references M1, M3, and M4 metadata.
3. Manifest includes dataset count reconciliation.
4. Manifest includes visual recipe count reconciliation.
5. Manifest explains any dataset count mismatch.
6. Manifest explains any recipe count mismatch.
7. Generated HTML is not marked as source truth or bulk-copy content.
8. All canonical import units have import methods.
9. Answer baseline readiness is explicit.
10. Production answer use remains blocked unless all required source import conditions are satisfied.
11. Final-paid/certification/trust posture remains unchanged.
12. No runtime/app/payroll/payment/write path files are modified.

Verification:
Run:

* JSON validation for governed import manifest and diagnostic JSON.
* New targeted governed import manifest test.
* M1 tests:
  `python -m pytest tests/test_minerva_analytics_builder_source_manifest.py tests/test_minerva_analytics_builder_answer_safety_contract.py tests/test_minerva_analytics_builder_benchmark_questions.py`
* M2 test:
  `python -m pytest tests/test_minerva_analytics_builder_retrieval_domain.py`
* M3 test:
  `python -m pytest tests/test_minerva_analytics_builder_knowledge_pack.py`
* M4 test:
  `python -m pytest tests/test_minerva_analytics_builder_source_path_reconciliation.py`
* Existing relevant knowledge/manifest tests:
  `python -m pytest tests/test_minerva_knowledge_artifact_inventory_service.py tests/test_manifest_ingestion.py`
* Existing retrieval plan tests:
  `python -m pytest tests/test_domain_retrieval_plans.py`
* Do not run full suite unless practical; if run, classify known unrelated pre-existing dirty-worktree failures and do not fix them.

Do not require a live database.
Do not run destructive commands.
Do not stage.
Do not commit.

Expected final response from Codex:

* Repo inspection summary.
* Dataset count reconciliation.
* Visual recipe count reconciliation.
* Explanation of count mismatches.
* Governed import manifest created.
* Canonical import units created.
* Whether M6 answer baselines can proceed.
* Files created/changed.
* Verification commands run and results.
* Full suite result if run, with classification of unrelated pre-existing failures.
* Git status summary.
* Clear statement that no runtime/application behaviour was implemented.
* Clear statement that no final-paid/certification/trust posture was changed.
* Clear statement that no `ezeas-analytics` files were modified.
* Do not run `git add .`.
* Do not commit.
```
