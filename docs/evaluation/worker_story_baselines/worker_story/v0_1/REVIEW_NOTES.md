# Worker Story Baseline Review Notes

These notes define the manual review checklist for Worker Story baseline captures. They are diagnostic-only and not operational truth.

This review file does not mutate corpus, does not change routing, does not change answer generation, does not call live LLM, does not ingest operational JSON, and does not connect Code Evidence.

## Manual Review Checklist

- Confirm the baseline pack references `docs/WORKER_STORY_EVALUATION_RUNBOOK.md`.
- Confirm the baseline pack references `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`.
- Confirm all required files exist: `BASELINE_SUMMARY.md`, `BENCHMARK_BASELINE.md`, `CORPUS_COVERAGE_BASELINE.md`, `ANSWER_GAP_REPORT_BASELINE.md` and `REVIEW_NOTES.md`.
- Confirm command completion status is explicit.
- Confirm generated output is either intentionally absent or clearly labelled.
- Confirm every file keeps diagnostic-only guardrails.
- Confirm no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Reviewer Questions

- Does the benchmark baseline show a stable comparison point or only the capture shape?
- Does the coverage baseline identify evidence groups without overstating corpus readiness?
- Does the gap report baseline distinguish retrieval, synthesis and corpus-evidence improvements?
- Are known gaps explicit enough for the next reviewer to understand what was not captured?
- Is the decision ledger updated only for domains with a checked-in baseline pack?

## What Would Justify Retrieval Improvement

Improve retrieval terms when formal corpus evidence exists but the coverage diagnostic or benchmark cannot find it reliably. The review should point to formal evidence that should have been retrieved and explain why the current terms miss it.

## What Would Justify Synthesis Improvement

Improve synthesis when retrieved evidence is strong but the answer does not express the needed Worker Story relationship, limitation or guardrail clearly enough. The review should identify the evidence group and the missing answer concept.

## What Would Justify Formal Source Evidence Later

Add formal source evidence later when the corpus genuinely lacks support for a Worker Story evidence group. Do not use operational JSON or Code Evidence as a shortcut for missing formal corpus evidence.

## What Must Not Be Inferred

This baseline must not be read as proof that:

- runtime payroll output is correct;
- Worker Story runtime implementation is complete;
- the corpus is complete;
- Minerva calculated payroll;
- Minerva mutated corpus;
- Minerva changed routing;
- Minerva changed answer generation;
- Minerva called a live LLM;
- Minerva ingested operational JSON;
- Minerva connected Code Evidence to answer generation.

## Expansion Notes

Future baseline packs for other `BASELINE_REQUIRED` domains should copy this structure, use the target domain runbook commands and preserve the same diagnostic-only boundary. Do not expand to all domains in one slice. Apply the pattern domain by domain after the Worker Story pilot is reviewed.
