# Tax / PAYG Corpus Coverage Baseline

This file records the manually captured corpus coverage result for the Tax / PAYG baseline pack. It is diagnostic-only and not operational truth.

## Commands Executed

```powershell
python scripts\scan_tax_payg_corpus_coverage.py
python scripts\scan_tax_payg_corpus_coverage.py --json --output .\artifacts\eval\tax_payg_corpus_coverage.json
```

## Scope

The Tax / PAYG corpus coverage diagnostic reads the already indexed formal corpus and reports evidence group coverage. It does not ingest files, mutate corpus records, call a live LLM or change schema.

Coverage preserves evidence for:

- governed withholding calculation evidence;
- deterministic services and tax providers;
- TaxStory and explainability;
- taxable basis and Payroll Bases & Totals;
- worker tax declarations and withholding inputs;
- ProcessPeriod PaymentDate and payment date context;
- pay frequency and provider support;
- gross-to-net and finalised totals;
- supplementary incremental PAYG;
- Worker Story and PayRun Admin Queue connection;
- unsupported and review states;
- outstanding hardening.

## Captured Result Summary

Result status: `COMPLETED_WITH_CORPUS_GAPS`

- Plan/domain: `TAX_PAYG` / Tax / PAYG
- Evidence groups: 12
- `STRONG`: 10
- `WEAK`: 1
- `MISSING`: 1
- Coverage JSON generated: yes
- Generated artefact committed: no
- Indexed corpus: 5 active documents, 4583 chunks
- Live LLM calls: no
- Corpus mutation: no
- Operational JSON ingestion: no
- Code Evidence answer integration: no

Corpus coverage result: recaptured with a real formal source-evidence gap.

Baseline pack state: recaptured result, not promoted.

Final ledger status remains `BASELINE_REQUIRED`; this recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

## Evidence Groups

- `purpose_and_operator_meaning`: MISSING
- `deterministic_tax_boundary`: STRONG
- `tax_story_and_explainability`: STRONG
- `taxable_basis_and_payroll_bases`: STRONG
- `worker_tax_declaration_and_withholding_inputs`: STRONG
- `payment_date_and_process_period_context`: STRONG
- `pay_frequency_and_provider_support`: STRONG
- `gross_to_net_and_finalised_totals`: STRONG
- `supplementary_incremental_payg`: STRONG
- `worker_story_and_admin_queue_connection`: STRONG
- `unsupported_and_review_states`: STRONG
- `outstanding_hardening`: WEAK

Important details:

- `purpose_and_operator_meaning` matched 0 chunks across 0 documents.
- `outstanding_hardening` matched 4 chunks across 1 document.
- `deterministic_tax_boundary` matched 4 chunks across 3 documents and includes tax providers / withholding calculation support.
- `tax_story_and_explainability` matched 10 chunks across 3 documents.
- `worker_story_and_admin_queue_connection` matched 7 chunks across 3 documents.
- The benchmark failure for `tax-payg-minerva-not-calculate` is a source-evidence/matched-phrase retrieval issue even though `deterministic_tax_boundary` is STRONG.

## Source References

- Runbook: `docs/TAX_PAYG_EVALUATION_RUNBOOK.md`
- Coverage service: `app/services/tax_payg_corpus_coverage_service.py`
- Coverage script: `scripts\scan_tax_payg_corpus_coverage.py`
- Readiness check: `scripts/check_worker_story_baseline_db_readiness.py`
- Transient JSON: `.\artifacts\eval\tax_payg_corpus_coverage.json`

## Interpretation

Tax / PAYG has genuine formal-corpus coverage gaps: 10 STRONG, 1 WEAK and 1 MISSING coverage groups. The missing `purpose_and_operator_meaning` group means this domain cannot be promoted solely through synthesis hardening unless formal source evidence is added or the coverage plan is legitimately revised with justification.

## Diagnostic-Only Guardrails

This corpus coverage baseline:

- does not mutate corpus;
- does not ingest documents;
- does not ingest operational JSON;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not change workforce-platform.
