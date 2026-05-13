# Gross-to-Net Baseline Review Notes

These notes define the manual review checklist for the Gross-to-Net captured baseline. They are diagnostic-only and not operational truth.

This review file does not mutate corpus, does not change routing, does not change answer generation, does not call live LLM, does not ingest operational JSON, and does not connect Code Evidence.

## Manual Review Checklist

- Confirm the baseline pack references `docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md`.
- Confirm the baseline pack references `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`.
- Confirm all required files exist: `BASELINE_SUMMARY.md`, `BENCHMARK_BASELINE.md`, `CORPUS_COVERAGE_BASELINE.md`, `ANSWER_GAP_REPORT_BASELINE.md` and `REVIEW_NOTES.md`.
- Confirm command completion status is explicit.
- Confirm this pack is labelled as captured, not as a blocked database capture.
- Confirm benchmark result is 6 total, 5 passed, 1 failed.
- Confirm failed benchmark case ID `gross-to-net-current-effective-worker-story` is recorded.
- Confirm the failure is classified as benchmark answer-term expectation drift, not a corpus gap.
- Confirm corpus coverage is 10 `STRONG`, 0 `WEAK`, 0 `MISSING`.
- Confirm answer gap report status is `GOOD` with 10 `KEEP` actions.
- Confirm generated output is summarized into curated markdown and not required as a committed artefact.
- Confirm every file keeps diagnostic-only guardrails.
- Confirm no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Reviewer Questions

- Is the decision ledger clear that Gross-to-Net is now `BASELINE_ALREADY_EXISTS`?
- Is the failed benchmark case preserved without weakening expectations?
- Is the recommended next action limited to benchmark watch rather than corpus mutation?
- Are generated JSON outputs treated as local evaluation artefacts rather than required committed baseline files?

## What Must Not Be Inferred

This baseline must not be read as proof that:

- runtime payroll output is correct;
- Gross-to-Net runtime implementation is complete;
- the corpus is complete;
- Minerva calculated payroll;
- Minerva mutated corpus;
- Minerva changed routing;
- Minerva changed answer generation;
- Minerva called a live LLM;
- Minerva ingested operational JSON;
- Minerva connected Code Evidence to answer generation.

## Expansion Notes

This completes the previously blocked Gross-to-Net pack from the small four-domain baseline batch. No domains from that batch remain blocked. Annual Leave / Leave Management remains `RUNBOOK_OUTSTANDING`.
