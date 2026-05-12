# Baseline Capture Policy

Worker Story Baseline-Capture Pilot v0.1 defines the reusable baseline artefact shape for Minerva product-domain evaluation controls.

Baseline capture exists to preserve a checked-in comparison point for deterministic evaluation outputs after a domain has completed its v0.4 runbook. It helps reviewers compare future benchmark, corpus coverage and answer gap report changes against an agreed control summary.

This policy is diagnostic/control documentation only. Baseline artefacts are comparison controls only. They are not operational truth, do not prove runtime implementation and do not prove payroll correctness.

## Diagnostic Boundary

Baseline artefacts:

- do not mutate corpus;
- do not change routing;
- do not change answer generation;
- do not call live LLM;
- do not ingest operational JSON;
- do not connect Code Evidence;
- do not prove runtime platform truth;
- do not create or update runtime payroll, leave, workforce or evidence records.

## Standard Folder Shape

Each domain baseline pack should live under:

```text
docs/evaluation/worker_story_baselines/<domain_slug>/<version>/
```

The Worker Story pilot uses:

```text
docs/evaluation/worker_story_baselines/worker_story/v0_1/
```

Future domains should reuse the same folder shape unless a later policy supersedes it.

## Required Files

Each baseline pack must include:

- `BASELINE_SUMMARY.md`: the slice summary, source references, command completion state, high-level finding, known gaps, guardrails and next slice.
- `BENCHMARK_BASELINE.md`: the benchmark command, benchmark scope, pass/fail summary or intentional non-execution note, source references and guardrails.
- `CORPUS_COVERAGE_BASELINE.md`: the coverage diagnostic command, evidence group coverage summary, `STRONG` / `WEAK` / `MISSING` interpretation and guardrails.
- `ANSWER_GAP_REPORT_BASELINE.md`: the gap report command, overall status interpretation, recommended action categories and guardrails.
- `REVIEW_NOTES.md`: manual review checklist, reviewer questions, improvement triggers and expansion notes.

## Command Output Policy

Baseline packs may reference commands from the relevant v0.4 runbook, but command output should be checked in only when it is stable, useful for future comparison and free of runtime, tenant, secret or operational-data content.

Generated command output should not be pasted wholesale into a curated markdown summary unless the output is intentionally short and deterministic. Prefer a concise manually curated summary that records:

- command path and arguments;
- whether the command completed during the capture slice;
- whether the result was generated, manually summarized, or intentionally deferred;
- why any output was not embedded.

If a command was not run during the capture slice, the baseline file must say so plainly and must not invent pass/fail or coverage results.

## Generated Output And Curated Summary Policy

Generated outputs are transient evaluation materials unless explicitly checked in as part of a baseline pack. Curated summaries are allowed when they preserve the decision-relevant result without carrying volatile timestamps, local paths, database counts, or non-deterministic source ordering.

A curated summary must not overstate evidence. It can summarize deterministic test results and documented runbook commands, but it must not claim live corpus truth, operational truth or payroll correctness.

## Review Policy

Reviewers should check:

- the baseline pack references the correct domain runbook, benchmark manifest, diagnostic script and gap-report script;
- command completion status is explicit;
- manually summarized output is labelled as manually summarized;
- guardrails are present in every baseline file;
- known gaps are not hidden;
- no operational JSON, secrets, tenant data, source-code evidence content or runtime payroll truth is included.

## Future Domain Reuse

For each future `BASELINE_REQUIRED` domain:

1. Copy this folder shape.
2. Replace Worker Story domain references with the target domain references.
3. Use the target domain v0.4 runbook commands.
4. Keep the diagnostic-only boundary unchanged.
5. Update the completed-domain decision ledger only after the baseline pack exists.

Do not use operational JSON or Code Evidence as a shortcut for missing formal corpus evidence.

## Updating Or Superseding Baselines

Baseline packs should be immutable comparison points. Do not edit an old baseline to match new behavior unless correcting a documentation error. For a new capture, add a new version folder such as `v0_2/` and update the ledger or README pointer as needed.

If a baseline is superseded, record why in the new `BASELINE_SUMMARY.md` and keep the old pack available for comparison unless a separate approved cleanup slice removes it.
