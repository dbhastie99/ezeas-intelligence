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

## v0.3 Captured Baseline Review

The v0.3 captured baseline is now usable as a Worker Story comparison control because DB readiness returned `READY` and the benchmark, corpus coverage and answer gap report commands produced diagnostic baseline results.

Do not scale baseline capture to the 29 remaining `BASELINE_REQUIRED` domains until the Worker Story answer drift is fixed or formally accepted. The first failed benchmark, `worker-story-evidence-rich-answer`, should become the next hardening target because it exposes synthesis/routing/answer-mode drift rather than missing corpus evidence.

Generated JSON artefacts remain local/transient unless baseline policy changes. The curated markdown summary is the checked-in comparison artefact.

This baseline does not prove operational truth, runtime implementation, payroll correctness, corpus mutation, live LLM execution, operational JSON ingestion or Code Evidence answer integration.

## Post-Baseline Hardening Note v0.1

After Worker Story answer synthesis/routing drift hardening, the real DB-backed benchmark was rerun in the same environment after DB readiness returned `READY`.

Confirmed rerun result:

- Worker Story benchmark: 5 total, 5 passed, 0 failed.
- Annual Leave regression benchmark: 1 total, 1 passed, 0 failed.
- Audit/chat rows created: false.
- The v0.3 failed case is considered addressed by synthesis/routing hardening.
- Corpus coverage remains interpreted as sufficient; the prior failure is not considered a corpus coverage gap.

This note does not change the completed-domain ledger. Worker Story remains `BASELINE_ALREADY_EXISTS`; counts remain `BASELINE_REQUIRED`: 29, `BASELINE_ALREADY_EXISTS`: 1 and `RUNBOOK_OUTSTANDING`: 1.

The rerun note is diagnostic/control documentation only. It does not claim corpus mutation, routing changes in this baseline pack, answer generation changes in this baseline pack, live LLM calls, operational JSON ingestion, Code Evidence connection, runtime payroll truth, database schema changes, endpoints or UI changes.

## v0.2 Captured Baseline Review

The v0.2 captured baseline is complete enough to prove the artefact shape and command execution policy, but not complete enough to serve as a semantic Worker Story answer-quality comparison. The documented commands were executed, and the captured result is that the benchmark and coverage commands are blocked by the configured SQL Server connection in this environment.

The pack shape is ready to copy to other domains only after reviewers accept that a baseline pack can record blocked execution honestly. Before scaling to the remaining 29 `BASELINE_REQUIRED` domains, run Worker Story again in an environment with reachable configured corpus storage and capture actual benchmark, coverage and answer-gap summaries.

Recommended changes before scaling:

- run `py scripts/check_worker_story_baseline_db_readiness.py` before retrying Worker Story baseline capture;
- decide whether generated JSON should ever be checked in under domain baseline folders;
- keep curated markdown summaries as the default;
- require each baseline pack to distinguish environment blockers from product-domain failures;
- keep the completed-domain ledger stable until each domain has its own checked-in pack.
