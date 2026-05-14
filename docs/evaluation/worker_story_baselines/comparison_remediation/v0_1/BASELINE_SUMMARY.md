# Comparison / Remediation Baseline Summary

Slice name: Comparison / Remediation Baseline Capture Result Update and Promotion v0.1

Domain: Comparison / Remediation

Source runbook: `docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This pack is diagnostic-only and not operational truth. It records manually captured PowerShell command outputs for the Comparison / Remediation baseline. Promotion is now allowed because the benchmark passes, corpus coverage is all STRONG, and the answer gap report is `GOOD`.

Comparison / Remediation is now `BASELINE_ALREADY_EXISTS`.

## Execution Context

Captured on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY` in normal PowerShell before capture.

- Readiness status: `READY`
- Ready: yes.
- Configuration source: `.env:MINERVA_DATABASE_URL`
- Selected ODBC driver: `ODBC Driver 17 for SQL Server`
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none.
- Read-only guardrails remained in place.

## Commands

| Area | Command | Completed | Captured Result Summary |
|---|---|---:|---|
| Comparison / Remediation benchmark | `python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.comparison_remediation.json` | yes | 9 total / 9 passed / 0 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `python scripts\scan_comparison_remediation_corpus_coverage.py` | yes | 12 evidence groups; STRONG=12, WEAK=0, MISSING=0; indexed corpus 5 active documents, 4583 chunks. |
| Corpus coverage JSON | `python scripts\scan_comparison_remediation_corpus_coverage.py --json --output .\artifacts\eval\comparison_remediation_corpus_coverage.json` | yes | Generated transient JSON; committed: no. |
| Answer gap report | `python scripts\build_comparison_remediation_answer_gap_report.py --coverage-report .\artifacts\eval\comparison_remediation_corpus_coverage.json` | yes | `GOOD`; 12 LOW / KEEP groups. |
| Answer gap report JSON | `python scripts\build_comparison_remediation_answer_gap_report.py --coverage-report .\artifacts\eval\comparison_remediation_corpus_coverage.json --json --output .\artifacts\eval\comparison_remediation_answer_gap_report.json` | yes | Generated transient JSON; committed: no. |

## Captured Finding

- DB readiness result: `READY`.
- Result status: `PROMOTED_BASELINE_CAPTURED`.
- Baseline pack state: captured evidence and promoted.
- Benchmark result: 9 total, 9 passed, 0 failed.
- Corpus coverage result: STRONG=12, WEAK=0, MISSING=0.
- Answer gap report: `GOOD`.
- Answer gap actions: 12 KEEP, 0 IMPROVE_RETRIEVAL_TERMS, 0 IMPROVE_SYNTHESIS, 0 ADD_FORMAL_SOURCE_EVIDENCE_LATER.
- Generated artefact committed: no.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Domain Boundary To Preserve

Comparison / Remediation is payroll evidence and review/remediation context, not generic diffing. It explains governed comparison evidence for operators and downstream review surfaces.

- The model supports three lanes: primary calculated, comparator calculated, and actual imported / actuals lane.
- The primary award path remains operational payroll truth.
- Imported actuals are external outcome truth and must not be collapsed into calculated interpreter output.
- Comparison policy governs comparator selection, active lanes, offset policy, output mode, variance treatment, review requirements, and evidence/story obligations.
- Comparison run and line evidence must be preserved.
- Variance/top-up is a governed consequence of comparison, not an invisible calculation side effect.
- Position/classification mapping must be explicit and evidence-backed.
- Worker Story, Admin Queue, and Movement Review consume comparison evidence.
- Outstanding hardening and non-goals remain visible.
- Baseline capture does not implement runtime comparison/remediation behaviour.

## Not Implemented

This pack does not implement or claim:

- DB writes;
- migrations;
- corpus mutation;
- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- endpoint/UI/runtime changes;
- workforce-platform changes;
- payroll runtime changes;
- comparison/remediation runtime changes;
- correction execution;
- payment/remittance execution;
- finalisation execution;
- generated artefacts committed.

## Guardrails

This promoted baseline pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not prove payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Keep current Comparison / Remediation retrieval terms and answer synthesis under benchmark watch.
