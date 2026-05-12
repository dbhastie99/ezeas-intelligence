# Movement Review Baseline Review Notes

These notes define the manual review checklist for the Movement Review captured baseline. They are diagnostic-only and not operational truth.

This review file does not mutate corpus, does not change routing, does not change answer generation, does not call live LLM, does not ingest operational JSON, and does not connect Code Evidence.

## Manual Review Checklist

- Confirm the baseline pack references `docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md`.
- Confirm the baseline pack references `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`.
- Confirm all required files exist: `BASELINE_SUMMARY.md`, `BENCHMARK_BASELINE.md`, `CORPUS_COVERAGE_BASELINE.md`, `ANSWER_GAP_REPORT_BASELINE.md` and `REVIEW_NOTES.md`.
- Confirm command completion status is explicit.
- Confirm this pack is labelled as captured, not as a blocked database capture.
- Confirm benchmark result is 8 total, 8 passed, 0 failed.
- Confirm corpus coverage is 11 `STRONG`, 0 `WEAK`, 0 `MISSING`.
- Confirm answer gap report status is `GOOD` with 11 `KEEP` actions.
- Confirm generated output is summarized into curated markdown and not required as a committed artefact.
- Confirm every file keeps diagnostic-only guardrails.
- Confirm no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Reviewer Questions

- Is the decision ledger clear that Movement Review is now `BASELINE_ALREADY_EXISTS` while Gross-to-Net remains `BASELINE_REQUIRED`?
- Is the recommended next action limited to benchmark watch rather than corpus mutation?
- Are generated JSON outputs treated as local evaluation artefacts rather than required committed baseline files?

## What Must Not Be Inferred

This baseline must not be read as proof that:

- runtime payroll output is correct;
- Movement Review runtime implementation is complete;
- the corpus is complete;
- Minerva calculated payroll;
- Minerva mutated corpus;
- Minerva changed routing;
- Minerva changed answer generation;
- Minerva called a live LLM;
- Minerva ingested operational JSON;
- Minerva connected Code Evidence to answer generation.

## Expansion Notes

Do not update Gross-to-Net to captured state in this slice. It remains a blocked v0.1 capture pack until its own DB-backed commands are captured.
