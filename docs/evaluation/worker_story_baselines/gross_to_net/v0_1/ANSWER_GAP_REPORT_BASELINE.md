# Gross-to-Net Answer Gap Report Baseline

This file records the Gross-to-Net answer gap report baseline execution result for comparison control. It is diagnostic-only and not operational truth.

## Commands Executed

Human-readable mode:

```powershell
.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json
```

JSON mode with output file:

```powershell
.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json --json --output .\artifacts\eval\gross_to_net_answer_gap_report.json
```

Captured on 2026-05-13 from `C:\Projects\ezeas-intelligence`.

## Captured Result Summary

Result status: `COMPLETED`

Report type: `GROSS_TO_NET_ANSWER_GAP_REPORT`

Source coverage plan: `GROSS_TO_NET`

Overall status: `GOOD`

Recommended action counts:

- `KEEP`: 10
- `IMPROVE_RETRIEVAL_TERMS`: 0
- `IMPROVE_SYNTHESIS`: 0
- `ADD_FORMAL_SOURCE_EVIDENCE_LATER`: 0

Recommended next action: Keep current Gross-to-Net retrieval terms and answer synthesis under benchmark watch.

Generated artefact committed: no. The JSON output command created `.\artifacts\eval\gross_to_net_answer_gap_report.json` locally for summarization, but the file is not a required committed artefact.

Live LLM calls: no.

Corpus mutation: no.

Operational JSON ingestion: no.

## Action Mapping

Each reported Gross-to-Net evidence group was `STRONG` -> `KEEP`.

## Status Interpretation

- `GOOD`: core evidence is strong enough for the current answer path.
- `NEEDS_REFINEMENT`: evidence exists, but retrieval terms or synthesis may need refinement.
- `INSUFFICIENT_CORPUS`: important evidence is missing from the indexed formal corpus.

Answer gap status is an evaluation signal. It is not operational truth and does not prove runtime implementation.

## Diagnostic Interpretation

The answer gap report recommended keeping current Gross-to-Net retrieval terms and answer synthesis under benchmark watch. It did not recommend formal corpus additions.

## Diagnostic-Only Guardrails

This answer gap report baseline:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth.
