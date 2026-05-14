# Comparison / Remediation Corpus Coverage Baseline

This file records manually captured corpus coverage output for the Comparison / Remediation promoted baseline. It is diagnostic-only and not operational truth.

## Commands

```powershell
python scripts\scan_comparison_remediation_corpus_coverage.py
python scripts\scan_comparison_remediation_corpus_coverage.py --json --output .\artifacts\eval\comparison_remediation_corpus_coverage.json
```

The generated JSON file `artifacts/eval/comparison_remediation_corpus_coverage.json` was produced as a transient evaluation artefact and must remain untracked.

## Scope

The Comparison / Remediation corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage preserves evidence for purpose and operator meaning, the three-lane comparison model, primary award path preservation, actuals as external outcome truth, comparison policy, comparison run and line evidence, variance generation and governance, position/classification mapping, Worker Story, Admin Queue, Movement Review and outstanding hardening.

## Captured Result Summary

Result status: `COMPLETED`

- Plan/domain: `COMPARISON_REMEDIATION` / Comparison / Remediation
- Evidence groups: 12
- `STRONG`: 12
- `WEAK`: 0
- `MISSING`: 0
- Indexed corpus: 5 active documents, 4583 chunks
- Coverage JSON generated: yes
- Generated artefact committed: no
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Final ledger status is `BASELINE_ALREADY_EXISTS`.

## Coverage Groups

- `purpose_and_operator_meaning`: STRONG
- `three_lane_comparison_model`: STRONG
- `primary_award_path_preservation`: STRONG
- `actuals_as_external_outcome_truth`: STRONG
- `comparison_policy`: STRONG
- `comparison_run_and_line_evidence`: STRONG
- `variance_generation_and_governance`: STRONG
- `position_classification_mapping`: STRONG
- `worker_story_connection`: STRONG
- `admin_queue_connection`: STRONG
- `movement_review_connection`: STRONG
- `outstanding_hardening`: STRONG

## Source References

- Runbook: `docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/comparison_remediation_corpus_coverage_service.py`
- Coverage script: `scripts\scan_comparison_remediation_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`

## Diagnostic-Only Guardrails

This corpus coverage baseline:

- does not mutate corpus;
- does not ingest documents;
- does not ingest operational JSON;
- does not change endpoint/UI/runtime behavior;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
