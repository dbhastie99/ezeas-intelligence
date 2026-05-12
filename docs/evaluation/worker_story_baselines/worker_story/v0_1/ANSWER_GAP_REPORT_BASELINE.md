# Worker Story Answer Gap Report Baseline

This file records the Worker Story answer gap report baseline shape for comparison control. It is diagnostic-only and not operational truth.

## Command

Human-readable mode:

```powershell
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json
```

JSON mode with output file:

```powershell
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json --json --output reports/worker_story_answer_gap_report.json
```

## Status Interpretation

- `GOOD`: core evidence is strong enough for the current answer path.
- `NEEDS_REFINEMENT`: evidence exists, but retrieval terms or synthesis may need refinement.
- `INSUFFICIENT_CORPUS`: important evidence is missing from the indexed formal corpus.

Answer gap status is an evaluation signal. It is not operational truth and does not prove runtime implementation.

## Recommended Actions

The Worker Story answer gap report can recommend:

- `KEEP`: leave the current retrieval and synthesis behavior unchanged for the group.
- `IMPROVE_RETRIEVAL_TERMS`: refine deterministic search terms or group targeting so existing corpus evidence is found more reliably.
- `IMPROVE_SYNTHESIS`: adjust answer synthesis so retrieved evidence is explained more clearly and completely.
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: defer code changes and add or author formal source evidence in a later corpus slice.

## Current Baseline Finding

The answer gap report was not executed as a baseline-capture command in this v0.1 slice. This file defines the checked-in answer gap report baseline capture shape and must be populated by a future rerun if generated gap-report output is intentionally versioned.

No `GOOD`, `NEEDS_REFINEMENT` or `INSUFFICIENT_CORPUS` result is claimed by this file.

## Diagnostic-Only Guardrails

This answer gap report baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.
