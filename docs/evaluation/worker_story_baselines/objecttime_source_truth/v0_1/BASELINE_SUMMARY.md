# ObjectTime / Source Truth Baseline Summary

Slice name: ObjectTime / Source Truth Baseline Recapture Result Update v0.1

Domain: ObjectTime / Source Truth

Source runbook: `docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md`

Source decision ledger: `docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md`

Baseline policy: `docs/evaluation/worker_story_baselines/BASELINE_CAPTURE_POLICY.md`

This pack is diagnostic-only and not operational truth. It records manually captured PowerShell command outputs for an ObjectTime / Source Truth recapture attempt. Promotion is withheld because the benchmark failed 4 of 12 questions and the answer gap report is `NEEDS_REFINEMENT`.

ObjectTime / Source Truth remains `BASELINE_REQUIRED`. This pack must not be counted as `BASELINE_ALREADY_EXISTS`.

## Execution Context

Recapture attempted on 2026-05-14 from `C:\Projects\ezeas-intelligence`.

DB readiness returned `READY`.

- Readiness command: `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py`
- Ready: yes.
- Configuration source: `.env:MINERVA_DATABASE_URL`
- Selected ODBC driver: `ODBC Driver 17 for SQL Server`
- Required tables checked: `KnowledgeDocument`, `KnowledgeChunk`
- Missing tables: none.
- Read-only guardrails remained in place.

The benchmark, corpus coverage diagnostic and answer gap report were then captured manually from PowerShell output. Codex did not rerun DB-backed commands for this documentation update.

## Commands

| Area | Command | Completed In Recapture | Captured Result Summary |
|---|---|---:|---|
| DB readiness check | `.\.venv\Scripts\python.exe scripts\check_worker_story_baseline_db_readiness.py` | yes | `READY`; ready: yes. |
| ObjectTime / Source Truth benchmark | `python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.objecttime_source_truth.json` | yes | 12 total / 8 passed / 4 failed; audit/chat rows created: false. |
| Corpus coverage diagnostic | `python scripts\scan_objecttime_source_truth_corpus_coverage.py` | yes | 12 evidence groups; STRONG=11, WEAK=1, MISSING=0; indexed corpus 5 active documents, 4583 chunks. |
| Answer gap report | `python scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json` | yes | `NEEDS_REFINEMENT`; 11 LOW / KEEP groups; 1 MEDIUM / IMPROVE_RETRIEVAL_TERMS group. |
| Answer gap report JSON | `python scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json --json --output .\artifacts\eval\objecttime_source_truth_answer_gap_report.json` | yes | Generated transient JSON; committed: no. |

## Recapture Finding

- DB readiness result: `READY`.
- Result status: `RECAPTURED_REQUIRES_REFINEMENT`.
- Baseline pack state: captured evidence with promotion withheld.
- Benchmark result: 12 total, 8 passed, 4 failed.
- Corpus coverage result: STRONG=11, WEAK=1, MISSING=0.
- Answer gap report: `NEEDS_REFINEMENT`.
- Generated artefact committed: no.
- Live LLM calls: no.
- Corpus mutation: no.
- Operational JSON ingestion: no.
- Code Evidence answer integration: no.
- Final ledger status remains `BASELINE_REQUIRED`.
- This recaptured result does not count as `BASELINE_ALREADY_EXISTS`.

The benchmark failures are answer-synthesis and term-coverage issues, not corpus absence issues. Corpus coverage reported no missing groups.

## Failed Benchmark Cases

1. `objecttime-payrun-inclusion`
   - Question: How does ObjectTime explain PayRun inclusion?
   - Missing expected terms: `ObjectTime`, `PayRun inclusion`, `source row`, `belongs in a PayRun`, `source inclusion`, `SourceTruth`
2. `objecttime-sourcetruth-vs-workedhours`
   - Question: What is the difference between SourceTruth and WorkedHours?
   - Missing expected terms: `SourceTruth`, `WorkedHours`, `separate concepts`, `source inclusion`, `worked hours`, `raw span hours`
3. `objecttime-current-effective-output`
   - Question: How does ObjectTime / Source Truth connect to current-effective payroll output?
   - Missing expected terms: `ObjectTime / Source Truth`, `current-effective payroll output`, `processed source truth`, `payroll outcome`, `current-effective truth`
4. `objecttime-worker-story-source-truth`
   - Question: How should Worker Story use Source Truth?
   - Missing expected terms: `Worker Story`, `Source Truth`, `source inclusion`, `calculated payroll outcome`, `before`, `Decision Story`

## Domain Boundary To Preserve

ObjectTime / Source Truth is source evidence and PayRun inclusion context. It is not merely a timesheet or shift domain, and it is not payroll calculation truth by itself.

The next refinement slice must preserve these boundaries:

- ObjectTime, ObjectTimeAttribute, ObjectTimeAssessment and ObjectTimeAssessmentResponse are ObjectTime-family source evidence surfaces.
- SourceTruth is not WorkedHours.
- Raw span hours are not user-facing payroll worked hours.
- Worked hours must come from interpreted payroll truth or governed payroll bucket results where supported.
- ObjectTime source changes can affect payroll causality, dirty state, finalised correction review and evidence preservation.
- Minerva baseline packs are diagnostic comparison controls, not operational payroll truth.

## Source-Change Status To Preserve

Current known source-change status is recorded here as a review guardrail only. It is not benchmark output.

ObjectTime-family guarded dry-run route wiring is complete for:

- `OBJECT_TIME`
- `OBJECT_TIME_ATTRIBUTE`
- `OBJECT_TIME_ASSESSMENT`
- `OBJECT_TIME_ASSESSMENT_RESPONSE`

Known workforce-platform source-change milestones to preserve:

- v5.41 dry-run adapter exists.
- v5.42 dry-run orchestrator exists.
- v5.43 rollout inventory exists.
- v5.44 ObjectTime dry-run probe exists.
- v5.45 ObjectTime route-adjacent contract probe exists.
- v5.46 ObjectTime request builder exists.
- v5.47 test-only route harness exists.
- v5.48 integration plan/readiness gate exists.
- v5.49 OBJECT_TIME guarded dry-run route wiring exists.
- v5.51 OBJECT_TIME edge hardening exists.
- v5.52 OBJECT_TIME_ATTRIBUTE guarded dry-run route wiring exists.
- v5.53 OBJECT_TIME_ASSESSMENT guarded dry-run route wiring exists.
- v5.54 OBJECT_TIME_ASSESSMENT_RESPONSE guarded dry-run route wiring exists.
- v5.55 ObjectTime-family guarded dry-run close-out exists.
- v5.56 source-change runtime intake readiness contract exists.

Do not overclaim v5.56. It is a readiness contract only. It is not runtime intake.

## Not Implemented

This pack does not implement or claim:

- DB writes;
- migrations;
- corpus mutation;
- operational JSON ingestion;
- Code Evidence answer integration;
- live LLM calls;
- endpoint/UI/workforce-platform/runtime changes;
- dirty runtime calls;
- correction/review/payment/finalisation execution;
- runtime source-change hook or intake;
- Finalised correction intake creation from hooks;
- review request creation from hooks;
- correction execution;
- retro or replay execution;
- supplementary execution;
- adjustment execution;
- payment or remittance execution;
- finalisation mutation;
- production enablement.

## Guardrails

This recaptured-result pack:

- does not mutate corpus;
- does not change routing;
- does not change answer generation;
- does not call live LLM;
- does not ingest operational JSON;
- does not connect Code Evidence;
- does not connect Code Evidence to answer generation;
- does not prove runtime platform truth;
- does not create payroll/runtime truth;
- does not create DB schema or migrations;
- does not add endpoints or UI;
- does not change workforce-platform;
- does not create v0.5 slices automatically.

## Recommended Next Slice

Refine ObjectTime / Source Truth retrieval terms and answer synthesis for the failed benchmark terms and the weak `outstanding_hardening` supporting group before promoting this domain. Do not add new corpus merely to address the four benchmark failures unless a later diagnostic shows a real source-evidence gap.
