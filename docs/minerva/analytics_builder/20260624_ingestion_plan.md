# Minerva Analytics Builder Ingestion Plan - Slice 1

This slice creates ingestion/readiness planning for the Analytics Builder Guide static OMG v0.2 corpus. It does not ingest source content, mutate the operational corpus, create runtime routes, create BI dashboards, create SQL write paths, or change payroll, payment, award, scheduling, or analytics runtime behavior.

## Scope

The intended source corpus is `ezeas-analytics` at tag `analytics-builder-static-omg-v0.2-20260624`. Local source content was not copied into this repository by this slice. The source manifest therefore records expected artifact groups, expected paths, and required review gates before production answer use.

The planned Minerva domain key is `analytics_builder_guide`. No application retrieval-plan registry was changed because the current registry is implemented in `app/services/domain_retrieval_plan_service.py` as runtime routing code. This slice keeps the domain as planned/static-corpus-pending metadata only.

## Repository Inspection Summary

The repository already contains:

* deterministic retrieval plans in `app/services/domain_retrieval_plan_service.py`;
* domain-specific corpus coverage and answer gap report services;
* worker-story baseline packs under `docs/evaluation/worker_story_baselines/`;
* rich-answer benchmark manifests under `samples/eval/`;
* Minerva knowledge artifacts under `docs/knowledge/minerva/`;
* Minerva domain coverage records under `docs/minerva/domain_coverage/`;
* tests for retrieval plans, rich answer manifests, corpus coverage, answer gap reports, knowledge artifacts, and safety wording.

Relevant existing domains include payroll output, payment execution/remittance, process periods/payrun lifecycle, ObjectTime/source truth, finalisation readiness, payroll bases/totals, gross-to-net, and costing/GL consequence. Those domains are useful safety context but are not a substitute for Analytics Builder source ingestion.

## Ingestion Readiness Gates

1. Confirm `ezeas-analytics` source at `analytics-builder-static-omg-v0.2-20260624`.
2. Verify expected source artifact paths and counts.
3. Review every dataset card and visual recipe card for proof status and certification status.
4. Load prohibited claims and certification rules into answer-safety checks before any answer baseline is marked production-passed.
5. Preserve the current v0.2 posture: 9 datasets, 13 visual recipes, 6 validation assets, 4 validation gaps, 22 certification evidence packets, 0 Certified assets.
6. Treat final-paid payroll truth as `UNPROVEN / Blocked`.
7. Create answer baselines only after governed source ingestion and review.

## Non-Goals

This slice does not:

* index source documents;
* create runtime UI or app routes;
* create BI dashboards;
* create SQL write paths or stored procedures;
* modify payroll, payment, award, or scheduling behavior;
* create a second analytics truth path;
* promote any asset to Certified;
* prove final-paid payroll truth.

## Created Readiness Artifacts

* `metadata/minerva/analytics_builder_source_manifest.v0_1.json`
* `metadata/minerva/analytics_builder_answer_safety_contract.v0_1.json`
* `metadata/minerva/analytics_builder_benchmark_questions.v0_1.json`
* `docs/minerva/analytics_builder/20260624_source_corpus_manifest.md`
* `docs/minerva/analytics_builder/20260624_answer_safety_contract.md`
* `docs/minerva/analytics_builder/20260624_benchmark_question_plan.md`

