# Comparison / Remediation Answer Gap Report Baseline

This file records manually captured answer gap output for the Comparison / Remediation promoted baseline. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\build_comparison_remediation_answer_gap_report.py --coverage-report .\artifacts\eval\comparison_remediation_corpus_coverage.json
python scripts\build_comparison_remediation_answer_gap_report.py --coverage-report .\artifacts\eval\comparison_remediation_corpus_coverage.json --json --output .\artifacts\eval\comparison_remediation_answer_gap_report.json
```

The answer gap report consumed the transient coverage JSON produced by the corpus coverage diagnostic. Generated JSON remains an untracked evaluation artefact and is not a committed baseline artefact.

## Scope

The answer gap report consumes `.\artifacts\eval\comparison_remediation_corpus_coverage.json` after the coverage diagnostic completes. It classifies whether existing retrieval terms and answer synthesis are sufficient for a durable comparison control.

## Captured Result Summary

Result status: `PROMOTED_BASELINE_CAPTURED`

- Report type: `COMPARISON_REMEDIATION_ANSWER_GAP_REPORT`
- Overall status: `GOOD`
- Source coverage plan: `COMPARISON_REMEDIATION`
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Answer gap report: completed and acceptable for promotion.

Baseline pack state: captured evidence and promoted.

Recommended actions:

- `KEEP`: 12
- `IMPROVE_RETRIEVAL_TERMS`: 0
- `IMPROVE_SYNTHESIS`: 0
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 0

Action detail:

- `LOW` / `KEEP` groups: 12
- `MEDIUM` refinement groups: 0
- `purpose_and_operator_meaning`: STRONG -> `KEEP`
- `three_lane_comparison_model`: STRONG -> `KEEP`
- `primary_award_path_preservation`: STRONG -> `KEEP`
- `actuals_as_external_outcome_truth`: STRONG -> `KEEP`
- `comparison_policy`: STRONG -> `KEEP`
- `comparison_run_and_line_evidence`: STRONG -> `KEEP`
- `variance_generation_and_governance`: STRONG -> `KEEP`
- `position_classification_mapping`: STRONG -> `KEEP`
- `worker_story_connection`: STRONG -> `KEEP`
- `admin_queue_connection`: STRONG -> `KEEP`
- `movement_review_connection`: STRONG -> `KEEP`
- `outstanding_hardening`: STRONG -> `KEEP`

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Recommendation

Recommended next action: Keep current Comparison / Remediation retrieval terms and answer synthesis under benchmark watch.

The answer gap result confirms there is no current retrieval-term, synthesis or formal-source evidence action for the covered groups.

## Source References

- Runbook: `docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md`
- Gap service: `app/services/comparison_remediation_answer_gap_report_service.py`
- Gap script: `scripts\build_comparison_remediation_answer_gap_report.py`
- Required coverage JSON: `.\artifacts\eval\comparison_remediation_corpus_coverage.json`

## Interpretation

Comparison / Remediation is now `BASELINE_ALREADY_EXISTS` because the benchmark passed 9 of 9, corpus coverage is STRONG=12, WEAK=0, MISSING=0, and the answer gap status is `GOOD`.

Any next answer gap review must preserve that comparison evidence does not replace primary payroll truth, imported actuals remain external outcome truth, and variance/top-up remains a governed consequence rather than an invisible calculation side effect.

## Diagnostic-Only Guardrails

This answer gap report baseline:

- does not mutate corpus;
- does not ingest operational JSON;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
