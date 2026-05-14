# ObjectTime / Source Truth Answer Gap Report Baseline

This file records manually captured answer gap output for the ObjectTime / Source Truth promoted baseline. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json
python scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json --json --output .\artifacts\eval\objecttime_source_truth_answer_gap_report.json
```

The answer gap report consumed the transient coverage JSON produced by the corpus coverage diagnostic. Generated JSON remains an untracked evaluation artefact and is not a committed baseline artefact.

## Scope

The answer gap report consumes `.\artifacts\eval\objecttime_source_truth_corpus_coverage.json` after the coverage diagnostic completes. It classifies whether existing retrieval terms and answer synthesis are sufficient for a durable comparison control.

## Captured Result Summary

Result status: `PROMOTED_BASELINE_CAPTURED`

- Report type: `OBJECTTIME_SOURCE_TRUTH_ANSWER_GAP_REPORT`
- Overall status: `GOOD`
- Source coverage plan: `OBJECTTIME_SOURCE_TRUTH`
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

- `outstanding_hardening` -> `KEEP`

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Recommendation

Recommended next action: Keep current ObjectTime / Source Truth retrieval terms and answer synthesis under benchmark watch.

The answer gap result confirms the previous promotion blocker is resolved without adding corpus.

## Source References

- Runbook: `docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md`
- Gap service: `app/services/objecttime_source_truth_answer_gap_report_service.py`
- Gap script: `scripts\build_objecttime_source_truth_answer_gap_report.py`
- Required coverage JSON: `.\artifacts\eval\objecttime_source_truth_corpus_coverage.json`

## Interpretation

ObjectTime / Source Truth is now `BASELINE_ALREADY_EXISTS` because the benchmark passed 12 of 12, corpus coverage is STRONG=12, WEAK=0, MISSING=0, and the answer gap status is `GOOD`.

Any next answer gap review must preserve that SourceTruth is not WorkedHours, raw span hours are not user-facing payroll worked hours, and v5.56 is runtime intake readiness only, not runtime intake implementation.

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
