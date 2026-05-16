# Minerva Controlled Evaluation Runbook / Batch Evaluation Harness v0.1

## Durable Prompt / Control Artefact

Date: 2026-05-17

Slice: Minerva Controlled Evaluation Runbook / Batch Evaluation Harness v0.1

## Objective

Create and execute a deterministic local batch evaluation harness for the checked-in Minerva controlled evaluation report fixtures under `tests/fixtures/controlled_evaluation_reports`.

The harness must run fixture metadata through the existing controlled evaluation chain and return structured internal pass/fail metadata for regression checks, developer handoff, controlled evaluation summaries, golden baseline drift detection, and next-slice readiness reporting.

## Required Posture

This slice is local deterministic harness/docs/tests only.

It must not:

- enable internal chat exposure;
- enable public, production, tenant, or customer chat exposure;
- add or register an API route;
- call a live LLM;
- generate final natural-language answers;
- connect to a database;
- read from a database;
- write to a database;
- create migrations;
- mutate corpus;
- ingest Code Evidence;
- alter live retrieval backend behaviour;
- add credentials or connection strings;
- change workforce-platform;
- change ezeas-analytics;
- change UI;
- claim production readiness;
- claim deployment readiness;
- claim runtime readiness.

## Implementation Scope

Create a focused service at `app/services/controlled_evaluation_batch_harness_service.py` unless repo conventions indicate a better explicit location.

The harness must accept supplied fixture payloads, fixture file paths, or an explicitly supplied fixture directory. It must not scan arbitrary repository paths unless a caller passes a directory.

The harness output must include batch-level counts, deterministic pass/fail status, category-specific failure lists, no-action attestation, and final-answer-generation safety flags.

Each fixture result must include fixture identity, purpose, expected and actual publication/safety values, failures, preserved boundaries, and violated boundaries.

## Required Behaviour

1. Running all existing controlled evaluation report fixtures produces deterministic results.
2. The harness reports fixture count, passed count, failed count, skipped count, and all_passed.
3. Safe fixture expected outputs pass.
4. Blocked overstatement fixture expected outputs pass when the overstatement is blocked.
5. A fixture whose expected publication decision does not match actual output fails.
6. A fixture that becomes safe for final answer generation fails.
7. A fixture that loses no-action/deferred boundary expectations fails.
8. A fixture that loses required caveats fails.
9. Batch output is deterministic for repeated runs.
10. The harness never marks the batch safe for final answer generation.
11. Fixture files are not mutated.
12. The harness does not write generated reports in this slice.

## Execution Plan

1. Inspect existing controlled readiness, classifier, publication gate, report assembler, and golden fixture tests.
2. Add the deterministic batch harness service.
3. Add focused tests for fixture loading, expected-pass behaviour, drift failures, deterministic output, no mutation, and no generated report writes.
4. Add `docs/evaluation/controlled_evaluation_runbook_batch_harness_v0_1.md`.
5. Run focused pytest, compile check for the new service, `git diff --check`, and confirm `.pytest_tmp` is absent.

## Completion Criteria

The slice is complete when the harness, tests, and documentation are checked into the working tree, focused verification passes, no generated reports are written, `.pytest_tmp` is absent, and the final status explicitly confirms no runtime, exposure, DB, corpus, Code Evidence, cross-repo, deployment, production, live LLM, or final answer generation action occurred.
