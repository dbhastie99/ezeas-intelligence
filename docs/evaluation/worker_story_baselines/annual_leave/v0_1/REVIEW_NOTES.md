# Annual Leave / Leave Management Baseline Review Notes

These notes define the manual review checklist for the Annual Leave / Leave Management captured baseline. They are diagnostic-only and not operational truth.

This review file does not mutate corpus, does not change routing, does not change answer generation, does not call live LLM, does not ingest operational JSON, and does not connect Code Evidence.

## Manual Review Checklist

- Confirm the baseline pack references `docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md`.
- Confirm the baseline pack references `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`.
- Confirm all required files exist: `BASELINE_SUMMARY.md`, `BENCHMARK_BASELINE.md`, `CORPUS_COVERAGE_BASELINE.md`, `ANSWER_GAP_REPORT_BASELINE.md` and `REVIEW_NOTES.md`.
- Confirm command completion status is explicit.
- Confirm this pack is labelled as captured, not as a blocked database capture.
- Confirm benchmark result is 1 total, 1 passed, 0 failed.
- Confirm corpus coverage is 7 `STRONG`, 0 `WEAK`, 0 `MISSING`.
- Confirm answer gap report status is `GOOD` with 7 `KEEP` actions.
- Confirm generated output is summarized into curated markdown and not required as a committed artefact.
- Confirm every file keeps diagnostic-only guardrails.
- Confirm no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Reviewer Questions

- Is the decision ledger clear that Annual Leave / Leave Management is now `BASELINE_ALREADY_EXISTS`?
- Is the recommended next action limited to benchmark watch rather than corpus mutation?
- Are generated JSON outputs treated as local evaluation artefacts rather than required committed baseline files?

## What Must Not Be Inferred

This baseline must not be read as proof that:

- runtime Annual Leave or payroll output is correct;
- Annual Leave / Leave Management runtime implementation is complete;
- the corpus is complete;
- Minerva calculated payroll or leave balances;
- Minerva mutated corpus;
- Minerva changed routing;
- Minerva changed answer generation;
- Minerva called a live LLM;
- Minerva ingested operational JSON;
- Minerva connected Code Evidence to answer generation.

## Explicitly Not Implemented

This baseline did not implement or authorize:

- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- corpus mutation;
- DB or schema migration;
- endpoints or UI;
- workforce-platform changes.
