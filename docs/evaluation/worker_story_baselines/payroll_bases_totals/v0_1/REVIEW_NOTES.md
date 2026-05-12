# Payroll Bases & Totals Baseline Review Notes

These notes define the manual review checklist for the Payroll Bases & Totals baseline capture. They are diagnostic-only and not operational truth.

This review file does not mutate corpus, does not change routing, does not change answer generation, does not call live LLM, does not ingest operational JSON, and does not connect Code Evidence.

## Manual Review Checklist

- Confirm the baseline pack references `docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md`.
- Confirm the baseline pack references `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`.
- Confirm all required files exist: `BASELINE_SUMMARY.md`, `BENCHMARK_BASELINE.md`, `CORPUS_COVERAGE_BASELINE.md`, `ANSWER_GAP_REPORT_BASELINE.md` and `REVIEW_NOTES.md`.
- Confirm command completion status is explicit.
- Confirm DB readiness is labelled `READY`.
- Confirm the benchmark result is 6 total, 6 passed and 0 failed.
- Confirm corpus coverage is 8 `STRONG`, 1 `WEAK` and 0 `MISSING`.
- Confirm the answer gap report status is `NEEDS_REFINEMENT`.
- Confirm `outstanding_hardening` is the weak group and maps to `IMPROVE_RETRIEVAL_TERMS`.
- Confirm generated JSON outputs are summarized into curated markdown and are not required committed artefacts.
- Confirm every file keeps diagnostic-only guardrails.
- Confirm no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Reviewer Questions

- Does this captured baseline pack provide enough detail for future before/after Payroll Bases & Totals comparison?
- Is the `outstanding_hardening` refinement clearly separated from new corpus ingestion?
- Is the decision ledger clear that only Worker Story and Payroll Bases & Totals are treated as `BASELINE_ALREADY_EXISTS`?
- Are PayRun Admin Queue, Movement Review and Gross-to-Net still blocked v0.1 capture packs?

## What Must Not Be Inferred

This baseline must not be read as proof that:

- runtime payroll output is correct;
- Payroll Bases & Totals runtime implementation is complete;
- the corpus is complete;
- Minerva calculated payroll;
- Minerva mutated corpus;
- Minerva changed routing;
- Minerva changed answer generation;
- Minerva called a live LLM;
- Minerva ingested operational JSON;
- Minerva connected Code Evidence to answer generation;
- Minerva changed DB schema or migrations;
- Minerva added endpoints or UI;
- Minerva changed workforce-platform.

## Expansion Notes

Do not expand this captured Payroll Bases & Totals baseline to PayRun Admin Queue, Movement Review or Gross-to-Net. Those packs remain blocked until their own DB-backed baseline commands are captured.
