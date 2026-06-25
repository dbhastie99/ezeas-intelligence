# 20260624 Minerva Analytics Builder M4 Source Path Reconciliation Prompt

```text
cd C:\Projects\ezeas-intelligence
codex -a never -s workspace-write

You are working only in the `ezeas-intelligence` repository.

This is Step 4 of the post-v0.2 Analytics Builder OMG plan.

Important sequencing update:
The original Step 4 was intended to be Answer Baselines. However, M3 found that `C:\Projects\ezeas-analytics` exists locally but the expected M1 source paths were not found at the exact registered paths. No source content was copied, and production answer use remains `not_allowed_pending_governed_source_ingestion`.

Therefore, this Step 4 is now:

M4 — Source Path Reconciliation and Governed Corpus Import Plan.

Answer baselines must wait until the Analytics Builder source corpus paths are reconciled and the ingestion/import boundary is governed.

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
* expected M1 source paths not found at exact registered paths;
* no source content copied.

Known repo condition:
The `ezeas-intelligence` worktree has pre-existing dirty runtime/app files, including `app/core/config.py` and untracked Minerva runtime/service files. Do not modify, stage, clean, fix, or rely on those unrelated files in this slice. Full-suite status-sensitive failures from those dirty files are known and unrelated.

Goal:
Reconcile the expected Analytics Builder source corpus paths against the actual local `ezeas-analytics` repository structure, without modifying `ezeas-analytics`, and create a governed import plan that identifies exactly which source artifacts can be imported or referenced in a later slice.

This slice should answer:

* Which M1 expected source paths are wrong, stale, or incomplete?
* What are the actual source paths in `ezeas-analytics`?
* Which artifacts are safe to register by path?
* Which artifacts are safe to copy as compact knowledge extracts?
* Which generated artifacts should not be copied?
* What should the governed import method be?
* What must happen before M5 answer baselines?

Critical boundaries:

* Do not modify `ezeas-analytics`.
* Do not modify `workforce-platform`.
* Do not modify `award-configurator-v1`.
* Do not modify runtime/app dirty files such as `app/core/config.py` or unrelated untracked Minerva runtime/service files.
* Do not copy large/generated HTML blindly.
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
* Do not claim production answer use is allowed until governed source import exists.
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
`docs/codex_prompts/20260624_minerva_analytics_builder_m4_source_path_reconciliation.md`

Suggested diagnostic artifacts:
`docs/diagnostics/20260624_minerva_analytics_builder_m4_source_path_reconciliation.md`
`docs/diagnostics/20260624_minerva_analytics_builder_m4_source_path_reconciliation.json`

Suggested knowledge artifact:
`docs/knowledge/20260624_minerva_analytics_builder_m4_source_path_reconciliation.md`

First inspect:

* M1 source manifest:
  `metadata/minerva/analytics_builder_source_manifest.v0_1.json`
* M3 knowledge-pack manifest:
  `metadata/minerva/analytics_builder_knowledge_pack.v0_1.json`
* M2 retrieval-domain metadata:
  `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`
* M1 answer safety contract:
  `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
* local `C:\Projects\ezeas-analytics` file tree, read-only only.
* likely source locations in `ezeas-analytics`, including:

  * `metadata/analytics_builder/`
  * `docs/analytics_builder_guide/`
  * `docs/generated/analytics_builder_guide/`
  * `docs/codex_prompts/`
  * `docs/diagnostics/`
  * `docs/knowledge/`
  * `tests/`

Do not modify any files under `C:\Projects\ezeas-analytics`.

Create metadata:
`metadata/minerva/analytics_builder_source_path_reconciliation.v0_1.json`

The reconciliation metadata should include:

* reconciliation_version;
* source_repo: `ezeas-analytics`;
* source_repo_path_checked;
* analytics_tag_expected: `analytics-builder-static-omg-v0.2-20260624`;
* m1_manifest_ref;
* m3_knowledge_pack_ref;
* reconciliation_status;
* expected_artifact_groups;
* expected_path_results;
* discovered_actual_paths;
* recommended_import_manifest_updates;
* import_method_recommendations;
* artifacts_safe_to_copy_as_extracts;
* artifacts_safe_to_reference_by_path;
* artifacts_not_safe_to_copy;
* missing_or_unresolved_artifacts;
* readiness_for_answer_baselines;
* no_source_repo_modification flag;
* no_runtime_behavior flag;
* no_trust_posture_change flag.

For each M1 artifact group, record:

* artifact_group_id;
* expected_paths;
* found_exact_paths;
* discovered_alternative_paths;
* recommended_canonical_source_paths;
* import_recommendation:

  * reference_only;
  * compact_extract;
  * metadata_copy;
  * do_not_copy_generated_artifact;
  * unresolved;
* reason;
* required_before_m5_answer_baselines.

Create docs:

* `docs/minerva/analytics_builder/20260624_source_path_reconciliation.md`
* `docs/minerva/analytics_builder/20260624_governed_corpus_import_plan.md`

The source path reconciliation doc should explain:

1. Why M4 was inserted before answer baselines.
2. What M3 found.
3. Which source paths were expected.
4. Which actual paths were discovered.
5. Which artifacts are safe to use for Minerva.
6. Which artifacts remain unresolved.
7. What must happen before M5.

The governed corpus import plan should define:

1. Import method options.
2. Recommended import approach.
3. What not to copy.
4. How to preserve source lineage.
5. How to avoid stale generated HTML becoming source truth.
6. How to update M1/M3 manifests later.
7. Acceptance criteria for proceeding to M5 answer baselines.

Suggested tests:
`tests/test_minerva_analytics_builder_source_path_reconciliation.py`

Tests should validate:

1. Reconciliation metadata parses.
2. Reconciliation references M1 source manifest.
3. Reconciliation references M3 knowledge-pack manifest.
4. Reconciliation includes all M1 artifact groups.
5. Each artifact group has expected path results.
6. Each artifact group has an import recommendation.
7. Generated HTML is not marked as bulk-copy source truth.
8. Production answer use remains blocked unless all required source groups are resolved.
9. Readiness for M5 is explicitly stated.
10. No runtime/app/payroll/payment/write path files are modified.

Verification:
Run:

* JSON validation for reconciliation metadata and diagnostic JSON.
* New targeted reconciliation test.
* M1 tests:
  `python -m pytest tests/test_minerva_analytics_builder_source_manifest.py tests/test_minerva_analytics_builder_answer_safety_contract.py tests/test_minerva_analytics_builder_benchmark_questions.py`
* M2 test:
  `python -m pytest tests/test_minerva_analytics_builder_retrieval_domain.py`
* M3 test:
  `python -m pytest tests/test_minerva_analytics_builder_knowledge_pack.py`
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
* Source path reconciliation summary.
* Exact source path mismatch findings.
* Discovered canonical source paths, if any.
* Import recommendations.
* Whether M5 answer baselines are now safe or still blocked.
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
