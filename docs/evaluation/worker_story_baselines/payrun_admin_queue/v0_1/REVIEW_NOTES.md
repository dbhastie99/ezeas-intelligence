# PayRun Admin Queue Baseline Review Notes

These notes define the manual review checklist for the PayRun Admin Queue baseline capture attempt. They are diagnostic-only and not operational truth.

This review file does not mutate corpus, does not change routing, does not change answer generation, does not call live LLM, does not ingest operational JSON, and does not connect Code Evidence.

## Manual Review Checklist

- Confirm the baseline pack references `docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md`.
- Confirm the baseline pack references `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`.
- Confirm all required files exist: `BASELINE_SUMMARY.md`, `BENCHMARK_BASELINE.md`, `CORPUS_COVERAGE_BASELINE.md`, `ANSWER_GAP_REPORT_BASELINE.md` and `REVIEW_NOTES.md`.
- Confirm command completion status is explicit.
- Confirm blocked execution is labelled `BLOCKED_DATABASE_CONNECTION`.
- Confirm generated output is either intentionally absent or clearly labelled.
- Confirm every file keeps diagnostic-only guardrails.
- Confirm no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Reviewer Questions

- Does this blocked capture pack help the next reviewer rerun the canonical commands?
- Is the database blocker clearly separated from product-domain evidence quality?
- Is the decision ledger clear that PayRun Admin Queue is not yet treated as `BASELINE_ALREADY_EXISTS`?

## What Must Not Be Inferred

This baseline must not be read as proof that:

- runtime payroll output is correct;
- PayRun Admin Queue runtime implementation is complete;
- the corpus is complete;
- Minerva calculated payroll;
- Minerva mutated corpus;
- Minerva changed routing;
- Minerva changed answer generation;
- Minerva called a live LLM;
- Minerva ingested operational JSON;
- Minerva connected Code Evidence to answer generation.

## Expansion Notes

Do not expand this blocked capture to all remaining domains. Restore DB connectivity and capture actual command results for this domain before moving it to `BASELINE_ALREADY_EXISTS`.
