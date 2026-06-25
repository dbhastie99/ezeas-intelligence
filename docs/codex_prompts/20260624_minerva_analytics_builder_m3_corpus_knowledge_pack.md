# 20260624 Minerva Analytics Builder M3 Corpus Knowledge Pack Prompt

```text
cd C:\Projects\ezeas-intelligence
codex -a never -s workspace-write

You are working only in the `ezeas-intelligence` repository.

This is Step 3 of the post-v0.2 Analytics Builder OMG plan.

Step 1 / M1 is complete:

* Created Analytics Builder source corpus manifest.
* Created answer safety contract.
* Created benchmark question plan.
* Created ingestion/readiness docs, diagnostics, Minerva-ready knowledge, saved prompt, and tests.
* Did not create runtime ingestion.
* Did not modify retrieval runtime code.
* Did not modify `ezeas-analytics`.
* Did not change final-paid, certification, or trust posture.

Step 2 / M2 is complete:

* Created metadata-only Analytics Builder retrieval-domain plan.
* Created `analytics_builder_guide` planned domain metadata.
* Created 15 retrieval term groups.
* Created routing examples and prohibited routing confusions.
* Did not modify runtime retrieval registry code because the repo has unrelated dirty runtime/app files.
* Did not change final-paid, certification, or trust posture.

Known repo condition:
The `ezeas-intelligence` worktree has pre-existing dirty runtime/app files, including `app/core/config.py` and untracked Minerva runtime/service files. Do not modify, stage, clean, fix, or rely on those unrelated files in this slice. Full-suite status-sensitive failures from those dirty files are known and unrelated.

This task is Step 3 / M3 — Analytics Builder Corpus Ingestion / Knowledge Pack.

Goal:
Create a static Analytics Builder knowledge-pack layer in `ezeas-intelligence` that registers the completed `ezeas-analytics` static OMG v0.2 corpus as Minerva-ingestable knowledge.

This slice should bridge M1/M2 metadata to actual knowledge-pack source structure without creating runtime ingestion behaviour.

The result should make it clear:

* which Analytics Builder source artifacts are expected;
* which source artifacts have been registered as a static knowledge pack;
* whether source content has actually been copied, referenced, or remains pending;
* what is safe for Minerva to use in later answer baselines;
* what remains pending before production answer use.

Critical boundaries:

* Do not modify `ezeas-analytics`.
* Do not copy large/generated content blindly.
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
* Do not claim production ingestion is complete unless repo evidence proves it.
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
4. Keep all modifications limited to safe docs/metadata/tests/static knowledge-pack files.
5. Do not stage or commit.

Suggested prompt path:
`docs/codex_prompts/20260624_minerva_analytics_builder_m3_corpus_knowledge_pack.md`

Suggested diagnostic artifacts:
`docs/diagnostics/20260624_minerva_analytics_builder_m3_corpus_knowledge_pack.md`
`docs/diagnostics/20260624_minerva_analytics_builder_m3_corpus_knowledge_pack.json`

Suggested knowledge artifact:
`docs/knowledge/20260624_minerva_analytics_builder_m3_corpus_knowledge_pack.md`

First inspect:

* M1 metadata:

  * `metadata/minerva/analytics_builder_source_manifest.v0_1.json`
  * `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
  * `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`
* M2 metadata:

  * `metadata/minerva/analytics_builder_retrieval_domain.v0_1.json`
* M1/M2 docs under:

  * `docs/minerva/analytics_builder/`
  * `docs/minerva/domain_coverage/analytics_builder_guide.md`
* Existing knowledge artifact conventions:

  * `docs/knowledge/`
  * `docs/knowledge/minerva/` if present
* Existing manifest ingestion conventions:

  * tests around manifest ingestion
  * any existing corpus/knowledge pack metadata
* Existing evaluation/baseline conventions:

  * `docs/evaluation/worker_story_baselines/`
  * `samples/eval/`
* Current git status, only to avoid touching unrelated dirty runtime/app files.

Create a static Analytics Builder knowledge-pack manifest.

Suggested metadata:
`metadata/minerva/analytics_builder_knowledge_pack.v0_1.json`

Suggested docs:

* `docs/minerva/analytics_builder/20260624_knowledge_pack.md`
* `docs/minerva/analytics_builder/20260624_static_corpus_registration.md`

Suggested static corpus index:

* `docs/knowledge/minerva/analytics_builder/README.md`
* `docs/knowledge/minerva/analytics_builder/static_corpus_index.md`
* `docs/knowledge/minerva/analytics_builder/source_artifact_groups.md`
* `docs/knowledge/minerva/analytics_builder/safety_summary.md`

If `docs/knowledge/minerva/analytics_builder/` does not match repo convention, use the closest existing convention and document why.

The knowledge-pack manifest should include:

* pack_version
* domain_key: `analytics_builder_guide`
* source_manifest_ref
* answer_safety_contract_ref
* retrieval_domain_ref
* benchmark_question_plan_ref
* analytics_source_tag: `analytics-builder-static-omg-v0.2-20260624`
* source_repo: `ezeas-analytics`
* pack_status: static_corpus_registered or static_corpus_pending, depending on what is actually created
* source_artifact_groups
* registered_static_knowledge_files
* missing_source_artifacts
* production_answer_use_status
* ingestion_method: metadata_registration_only, copied_static_docs, or pending_manual_import
* safety_requirements
* no_runtime_behavior flag
* no_trust_posture_change flag
* no_source_repo_modification flag

For each source artifact group, include:

* artifact_group_id
* source_paths_expected
* knowledge_pack_status
* minerva_use
* safety_notes
* required_before_baseline_answers
* required_before_production_answer_use

If local `ezeas-analytics` files are accessible and small enough to inspect safely, you may record discovered path existence in the manifest. Do not modify `ezeas-analytics`. Do not copy generated HTML or large generated files blindly. Prefer registration and summary over bulk copy.

Create static knowledge-pack docs that summarise:

1. What the Analytics Builder corpus is.
2. What has been registered.
3. What has not been ingested yet.
4. Why source lineage matters.
5. How Minerva should use the pack.
6. How Minerva must avoid overclaims.
7. What benchmark answers can be created in M4.
8. What remains blocked.

Create tests:
`tests/test_minerva_analytics_builder_knowledge_pack.py`

Tests should validate:

1. Knowledge-pack manifest parses.
2. Domain key is `analytics_builder_guide`.
3. Manifest references M1 source manifest.
4. Manifest references M1 answer safety contract.
5. Manifest references M1 benchmark question plan.
6. Manifest references M2 retrieval domain metadata.
7. Manifest includes all required source artifact groups from M1.
8. Manifest includes pack status and ingestion method.
9. Manifest does not claim production answer use unless actual ingestion evidence exists.
10. Manifest includes safety requirements for final-paid truth, PayrollLedger, CalcInterpreterLine, ObjectTime, certification, and visual rendering.
11. Static knowledge-pack docs exist.
12. No runtime/app/payroll/payment/write path files are modified.

Verification:
Run:

* JSON validation for knowledge-pack manifest and diagnostic JSON.
* New targeted knowledge-pack test.
* M1 tests:
  `python -m pytest tests/test_minerva_analytics_builder_source_manifest.py tests/test_minerva_analytics_builder_answer_safety_contract.py tests/test_minerva_analytics_builder_benchmark_questions.py`
* M2 test:
  `python -m pytest tests/test_minerva_analytics_builder_retrieval_domain.py`
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
* Whether source corpus was copied, registered, or left pending.
* Knowledge-pack manifest created.
* Static knowledge-pack docs created.
* Source artifact groups covered.
* Missing source artifacts, if any.
* Production answer use status.
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
