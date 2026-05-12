# PayRun Admin Queue Baseline Review Notes

These notes define the manual review checklist for the PayRun Admin Queue captured baseline. They are diagnostic-only and not operational truth.

This review file does not mutate corpus, does not change routing, does not change answer generation, does not call live LLM, does not ingest operational JSON, and does not connect Code Evidence.

## Manual Review Checklist

- Confirm the baseline pack references `docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md`.
- Confirm the baseline pack references `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`.
- Confirm all required files exist: `BASELINE_SUMMARY.md`, `BENCHMARK_BASELINE.md`, `CORPUS_COVERAGE_BASELINE.md`, `ANSWER_GAP_REPORT_BASELINE.md` and `REVIEW_NOTES.md`.
- Confirm command completion status is explicit.
- Confirm this pack is labelled as captured with failures, not as a blocked database capture.
- Confirm benchmark result is 8 total, 6 passed, 2 failed.
- Confirm failed case IDs are recorded: `payrun-admin-queue-rich-answer`; `payrun-admin-queue-cleanliness-assurance`.
- Confirm failure classification is benchmark/source-evidence check or retrieval/source-matched-phrase drift, not corpus gap.
- Confirm corpus coverage is 11 `STRONG`, 0 `WEAK`, 0 `MISSING`.
- Confirm answer gap report status is `GOOD` with 11 `KEEP` actions.
- Confirm generated output is summarized into curated markdown and not required as a committed artefact.
- Confirm every file keeps diagnostic-only guardrails.
- Confirm no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Reviewer Questions

- Are the two benchmark failures clearly separated from corpus coverage, which reported all groups as `STRONG`?
- Is the decision ledger clear that PayRun Admin Queue is now `BASELINE_ALREADY_EXISTS` while Movement Review and Gross-to-Net remain `BASELINE_REQUIRED`?
- Is the recommended next action limited to benchmark watch rather than corpus mutation?

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

Do not update Movement Review or Gross-to-Net to captured state in this slice. They remain blocked v0.1 capture packs until their own DB-backed commands are captured.
