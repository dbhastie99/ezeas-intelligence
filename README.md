# Ezeas Intelligence

Minerva is the Ezeas knowledge and evidence intelligence layer. It reads, indexes, retrieves, explains and audits.

Minerva is not a payroll calculation engine. In Walking Skeleton v0.1 it is read-only and advisory. It does not calculate payroll, determine entitlements, interpret awards at runtime, approve exceptions, suppress warnings, override payroll outcomes, mutate configuration or finalise PayRuns.

## v0.1 Scope

- Ingest TXT and DOCX knowledge files.
- Extract text, calculate SHA256, prevent duplicate ingestion and store document chunks.
- Create chat sessions and answer from simple keyword retrieval.
- Return grounded source references.
- Audit every AI answer.
- Use a stub LLM client only.

Operational payroll JSON evidence intelligence is intentionally not implemented in this slice.

Code Evidence Index tooling is documented in [docs/CODE_EVIDENCE_INDEX.md](docs/CODE_EVIDENCE_INDEX.md). It is metadata-only: no code content capture, DB ingestion, LLM exposure, scanned code execution, or source repo mutation is implemented.

Worker Story evaluation is documented in [docs/WORKER_STORY_EVALUATION_RUNBOOK.md](docs/WORKER_STORY_EVALUATION_RUNBOOK.md), including benchmark, corpus coverage diagnostic, and answer gap report commands.

Annual Leave / Leave Management evaluation is documented in [docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md](docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md). The runbook records the existing Annual Leave benchmark and golden-question commands, and keeps Annual Leave baseline readiness outstanding until Annual Leave-specific corpus coverage and answer gap tooling exists.

Completed-domain baseline decisions are tracked in [docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md](docs/evaluation/worker_story_baselines/COMPLETED_DOMAIN_BASELINE_DECISION_LEDGER.md). The ledger is diagnostic/control documentation only and does not create v0.5 slices automatically.

Worker Story baseline capture policy and checked-in baseline packs are documented under [docs/evaluation/worker_story_baselines/](docs/evaluation/worker_story_baselines/), with the DB readiness check documented in [WORKER_STORY_BASELINE_DB_READINESS.md](docs/evaluation/worker_story_baselines/WORKER_STORY_BASELINE_DB_READINESS.md). The v0.3 captured baseline records READY database readiness, benchmark result 5 total / 4 passed / 1 failed, corpus coverage 10 STRONG / 0 WEAK / 0 MISSING and answer gap status GOOD with all groups KEEP. The four-domain batch close-out is recorded in [BASELINE_BATCH_CLOSEOUT_2026_05_13.md](docs/evaluation/worker_story_baselines/BASELINE_BATCH_CLOSEOUT_2026_05_13.md). These artefacts are comparison controls only; they do not mutate corpus, change routing, change answer generation, call a live LLM, ingest operational JSON, connect Code Evidence, or prove runtime platform truth.

Before retrying Worker Story baseline capture, run the read-only DB readiness check documented in [docs/evaluation/worker_story_baselines/WORKER_STORY_BASELINE_DB_READINESS.md](docs/evaluation/worker_story_baselines/WORKER_STORY_BASELINE_DB_READINESS.md).

## SQL Server Setup

1. Create the database manually:

```powershell
sqlcmd -S localhost -i scripts/create_db.sql
```

2. Create the tables:

```powershell
sqlcmd -S localhost -d ezeas-intelligence-db -i scripts/create_tables.sql
```

You can also run both scripts in SQL Server Management Studio. Copy `.env.example` to `.env` and adjust `MINERVA_DATABASE_URL` for your SQL Server and ODBC driver.

## Slice 1.2 - Local SQL Server Run Proof

This proof shows that Minerva can run locally against SQL Server database `ezeas-intelligence-db`. It does not use the operational payroll database. It does not ingest JSON, call an external LLM, use embeddings, or execute autonomous actions.

### A. Create The Database In SSMS

1. Open SQL Server Management Studio.
2. Connect to your local SQL Server instance.
3. Open and run:

```text
scripts/create_db.sql
```

4. Switch to database `ezeas-intelligence-db`.
5. Open and run:

```text
scripts/create_tables.sql
```

The scripts create the Minerva database and the five Slice 1.x tables if they do not already exist.

### B. Configure Environment

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Set `MINERVA_DATABASE_URL` for local SQL Server. Example for Windows Integrated auth with ODBC Driver 18:

```text
MINERVA_DATABASE_URL=mssql+pyodbc:///?odbc_connect=Driver%3D%7BODBC+Driver+18+for+SQL+Server%7D%3BServer%3Dlocalhost%3BDatabase%3Dezeas-intelligence-db%3BTrusted_Connection%3Dyes%3BEncrypt%3Dyes%3BTrustServerCertificate%3Dyes%3B
MINERVA_ENV=local
MINERVA_LLM_PROVIDER=stub
MINERVA_CHUNK_SIZE=1200
MINERVA_CHUNK_OVERLAP=150
```

`TrustServerCertificate=yes` is for local development. Keep the actual operational payroll database separate and do not point Minerva at it.

### C. Install And Run The Proof

From PowerShell or the PyCharm terminal:

```powershell
pip install -r requirements.txt
python scripts/check_sqlserver_tables.py
python scripts/local_smoke_test.py
uvicorn app.main:app --reload
```

If your Windows machine uses the Python launcher, use `py` instead of `python`:

```powershell
py -m pip install -r requirements.txt
py scripts/check_sqlserver_tables.py
py scripts/local_smoke_test.py
py -m uvicorn app.main:app --reload
```

### D. Expected Smoke Result

`scripts/check_sqlserver_tables.py` should report that all expected tables exist and print row counts for:

- `KnowledgeDocument`
- `KnowledgeChunk`
- `KnowledgeChatSession`
- `KnowledgeChatMessage`
- `AIInteractionAudit`

`scripts/local_smoke_test.py` should print:

- health result with `status=ok`;
- sample document ingestion result;
- `duplicate=true` on repeat runs for the same sample document;
- a chat answer from the stub LLM;
- source reference count greater than zero;
- an audit id.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload
```

Health check:

```powershell
curl http://127.0.0.1:8000/health
```

## Ingest Sample Knowledge

```powershell
python scripts/ingest_folder.py samples/knowledge --source-type PLATFORM_DOCTRINE --capability-status DOCTRINE
```

Or use the API:

```powershell
curl -F "file=@samples/knowledge/sample_platform_doctrine.txt" -F "source_type=PLATFORM_DOCTRINE" http://127.0.0.1:8000/api/v1/ingest/file
```

## Loading The First Minerva Knowledge Corpus

Use manifest ingestion when loading the first repeatable platform knowledge corpus. This is for TXT and DOCX platform knowledge only, such as Platform Doctrine, hardening logs, developer logs, requirements, and planning documents. Do not place live customer payroll JSON or operational payroll evidence in this corpus.

Place TXT and DOCX files under a local folder such as:

```text
samples/knowledge/
```

Create or edit a manifest JSON file. Start from:

```text
samples/knowledge/manifest.example.json
```

Manifest example:

```json
{
  "default_source_type": "OTHER",
  "default_capability_status": "UNKNOWN",
  "default_tenant_id": null,
  "documents": [
    {
      "path": "samples/knowledge/sample_platform_doctrine.txt",
      "source_type": "SAMPLE",
      "capability_status": "UNKNOWN",
      "title": "Sample Platform Doctrine"
    }
  ]
}
```

Document-level fields override manifest defaults. `path` is required. `tenant_id` and `title` are optional. If `title` is missing, Minerva uses the filename without extension.

Run manifest ingestion:

```powershell
py scripts/ingest_manifest.py samples/knowledge/manifest.example.json
```

Rerunning the same manifest is safe. Existing files are reported as duplicates instead of being ingested again.

Verify SQL Server row counts:

```powershell
py scripts/check_sqlserver_tables.py
```

Allowed `source_type` values:

- `PLATFORM_DOCTRINE`
- `HARDENING_LOG`
- `DEVELOPER_LOG`
- `REQUIREMENTS`
- `CHAT_HISTORY`
- `OTHER`
- `SAMPLE`

Allowed `capability_status` values:

- `IMPLEMENTED`
- `PHASE_ONE`
- `DOCTRINE`
- `OUTSTANDING_HARDENING`
- `FUTURE_ROADMAP`
- `DESIGN_DISCUSSION`
- `UNKNOWN`

## Chat

Create a session:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/chat/session -H "Content-Type: application/json" -d "{\"title\":\"Minerva doctrine\"}"
```

Ask a question using the returned session id:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/chat/message -H "Content-Type: application/json" -d "{\"session_id\":\"YOUR_SESSION_ID\",\"message\":\"What is Minerva allowed to do?\"}"
```

For local SQL Server corpus investigation, use the operator ask script:

```powershell
py scripts/ask_minerva.py "What is Minerva not allowed to do?"
py scripts/ask_minerva.py "What is Minerva not allowed to do?" --source-type PLATFORM_DOCTRINE --top-k 5
py scripts/ask_minerva.py "What is Minerva not allowed to do?" --include-samples
```

The script creates a new chat session per invocation, uses the stub LLM only, prints source scores and matched tokens, and writes an audit row.

## Corpus Hygiene

Sample/test documents are for smoke tests and local debugging only. They should use `source_type=SAMPLE`, not `PLATFORM_DOCTRINE`, so normal Minerva queries prefer the real doctrine/log corpus.

Normal `ask_minerva.py` queries exclude `SAMPLE` documents by default. Include them only when debugging:

```powershell
py scripts/ask_minerva.py "What is Minerva allowed to do?" --include-samples
```

List current documents:

```powershell
py scripts/list_documents.py
py scripts/list_documents.py --source-type SAMPLE
py scripts/list_documents.py --status ACTIVE --title-contains "Smoke"
```

Supersede a document without deleting chunks:

```powershell
py scripts/set_document_status.py <document_id> SUPERSEDED
```

Reactivate a document if needed:

```powershell
py scripts/set_document_status.py <document_id> ACTIVE
```

## Golden Question Evaluation

Golden questions are deterministic retrieval and answer regression checks for the current Minerva corpus. They are not a true external LLM quality evaluation, and they do not call an external LLM provider. They use Minerva's current keyword retrieval and stub answer generator.

Run the default pack:

```powershell
py scripts/run_golden_questions.py
```

Run with full per-question output:

```powershell
py scripts/run_golden_questions.py --verbose
```

Run a specific manifest and write JSON results:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/golden_questions.minerva.json --json-output .\golden-results.json
```

By default, evaluation does not create chat messages or audit rows. To create an audit trail for a run:

```powershell
py scripts/run_golden_questions.py --create-audit
```

Add new golden questions by editing:

```text
samples/eval/golden_questions.minerva.json
```

Each question can specify expected source types, a preferred top source type, source phrases that should appear in snippets or matched phrases, and answer phrases that should appear in the deterministic answer. Run the pack before and after large corpus ingestion or retrieval scoring changes.

## Domain Golden Question Packs

The foundation golden pack checks Minerva doctrine, boundaries and architecture:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/golden_questions.minerva.json --verbose
```

The Annual Leave pack checks whether the formal corpus already answers key leave-management questions before bulk raw chat-history ingestion:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/golden_questions.annual_leave.json --verbose
```

Domain packs are deterministic retrieval and answer regression checks, not external LLM evaluation. A failure usually means either retrieval needs tuning or the formal Developer Logs/doctrine corpus does not yet contain enough clear evidence for that product question.

## Rich Answer Standard

Snippet stitching is not acceptable as Minerva's final answer standard for serious platform-domain questions. Rich answers should be structured, source-grounded and honest about implementation status and uncertainty.

The answer modes are:

- `DOCTRINE`
- `PRODUCT_DOMAIN`
- `TECHNICAL_SUPPORT`
- `WORKER_FACING`
- `DEVELOPER_PLATFORM`
- `GENERAL`

For product/domain questions, the target sections are:

- Direct summary
- How the system works
- Current implementation status
- What remains outstanding
- Evidence basis / source references

The full contract is documented in:

```text
docs/RICH_ANSWER_STANDARD.md
```

Run the Annual Leave rich-answer benchmark:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.annual_leave.json --verbose --allow-failures
```

Run the Worker Story rich-answer benchmark:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures
```

Rich benchmarks are source-grounded answer-quality checks over the loaded Minerva corpus. They use deterministic retrieval and the stub answer generator; they are not live LLM calls. Use `--allow-failures` for benchmark tracking when the target formal corpus has not yet been loaded.

## Domain Retrieval Plans

Complex product-domain questions should not rely on one generic keyword search. Minerva can use deterministic domain retrieval plans that split a question into evidence groups, run targeted retrieval for each group, and keep the answer grounded in the retrieved formal corpus.

Annual Leave / Leave Management is the first implemented plan. It searches evidence groups for:

- Configuration and rule setup
- Accrual basis and ledger posting
- TAKEN leave and deduction rules
- Valuation and ordinary rate evidence
- PayRun leave orchestration
- Worker Story leave evidence
- Outstanding hardening and future work

This is not a hardcoded Annual Leave answer. The plan only decides what evidence to look for. If a group has weak or missing evidence, Minerva should say the loaded formal corpus does not yet contain enough retrieved evidence for that group.

Run the Annual Leave rich-answer benchmark after corpus changes:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.annual_leave.json --verbose --allow-failures
```

Worker Story / Worker Calculation Story is also implemented as a domain retrieval plan. It searches evidence groups for source truth and inclusion, interpreted worked hours, calculated payroll outcome, Decision Story and Rate Story, leave/accrual outcome, Payroll Bases & Totals, Movement Review, PayRun Admin Queue, current-effective truth and outstanding hardening.

Run the Worker Story rich-answer benchmark after corpus changes:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/rich_answer_benchmark.worker_story.json --verbose --allow-failures
```

Run the Payroll Bases & Totals rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_bases_and_totals.json
```

Payroll Bases & Totals evaluation is documented in [docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md](docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md), including benchmark, corpus coverage diagnostic, answer gap report commands and diagnostic-only guardrails.

Run the PayRun Admin Queue rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payrun_admin_queue.json
```

PayRun Admin Queue evaluation is documented in [docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md](docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md), including benchmark, corpus coverage diagnostic, answer gap report commands and diagnostic-only guardrails.

Run the Movement Review rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.movement_review.json
```

Movement Review evaluation is documented in [docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md](docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md), including benchmark, corpus coverage diagnostic, answer gap report commands and diagnostic-only guardrails.

Run the Comparison / Remediation rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.comparison_remediation.json
```

Run the Tax / PAYG rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.tax_payg.json
```

Run the Deductions / Obligations rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.deductions_obligations.json
```

Run the Retro / Replay rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.retro_replay.json
```

Run the Payment Execution / Remittance rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payment_execution_remittance.json
```

Run the Leave Accrual / Processing rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.leave_accrual_processing.json
```

Run the Finalisation Readiness rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.finalisation_readiness.json
```

Run the Leave Source Model rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.leave_source_model.json
```

Run the On-costs / Employer Liabilities rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.oncosts_employer_liabilities.json
```

Run the Award Build / Award Evidence rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.award_build_evidence.json
```

Run the Imports / Actuals rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.imports_actuals.json
```

Run the ObjectTime / Source Truth rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.objecttime_source_truth.json
```

Run the Contacts / Employee Appointments rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.contacts_employee_appointments.json
```

For the repeatable Contacts / Employee Appointments evaluation workflow and interpretation guidance, see [docs/CONTACTS_EMPLOYEE_APPOINTMENTS_EVALUATION_RUNBOOK.md](docs/CONTACTS_EMPLOYEE_APPOINTMENTS_EVALUATION_RUNBOOK.md).

Run the Process Periods / PayRun Lifecycle rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.process_period_payrun_lifecycle.json
```

Run the Costing / GL Consequence Evidence rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.costing_gl_consequence.json
```

Run the Worker Attention / Issue Resolution rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.worker_attention_issue_resolution.json
```

Run the Gross-to-Net rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.gross_to_net.json
```

Run the RateSource / Rate Story rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.rate_source_rate_story.json
```

Run the Decision Story rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.decision_story.json
```

Run the Payroll Output rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_output.json
```

Run the Contact Payroll History rich-answer benchmark, including broad and focused follow-up coverage, after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.contact_payroll_history.json
```

Run the Leave Requests / Leave Workflow rich-answer benchmark after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.leave_requests_workflow.json
```

Run the Public Holidays rich-answer benchmark after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.public_holidays.json
```

Run the Rosters / Patterns / Scheduling rich-answer benchmark after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.rosters_patterns_scheduling.json
```

Run the Award Positions / Classifications rich-answer benchmark after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.award_positions_classifications.json
```

Run the Payroll Tax / WorkCover / WIC Liability Detail rich-answer benchmark after corpus changes:

```powershell
.\.venv\Scripts\python.exe scripts\run_golden_questions.py --manifest samples\eval\rich_answer_benchmark.payroll_tax_workcover_wic_liability_detail.json
```

Run the diagnostic-only Payroll Tax / WorkCover / WIC Liability Detail corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py --json --output .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_corpus_coverage.json
```

Build the diagnostic-only Payroll Tax / WorkCover / WIC Liability Detail answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_corpus_coverage.json --output .\artifacts\eval\payroll_tax_workcover_wic_liability_detail_answer_gap_report.json
```

These Payroll Tax / WorkCover / WIC Liability Detail diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, connect Code Evidence Index to answer generation, and do not prove runtime operational truth. They do not calculate payroll tax, do not calculate WorkCover or WIC liability, do not lodge or remit statutory returns, do not decide statutory liability, do not change employer-liability configuration, do not change Worksite, State or jurisdiction truth, do not calculate payroll, do not mutate payroll output, do not determine or finalise readiness, and do not mutate operational workforce/payroll/liability truth.

For the repeatable Payroll Tax / WorkCover / WIC Liability Detail evaluation workflow and interpretation guidance, see [docs/PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_EVALUATION_RUNBOOK.md](docs/PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Award Positions / Classifications corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_award_positions_classifications_corpus_coverage.py --json --output .\artifacts\eval\award_positions_classifications_corpus_coverage.json
```

Build the diagnostic-only Award Positions / Classifications answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_award_positions_classifications_answer_gap_report.py --coverage-report .\artifacts\eval\award_positions_classifications_corpus_coverage.json --output .\artifacts\eval\award_positions_classifications_answer_gap_report.json
```

These Award Positions / Classifications diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, connect Code Evidence Index to answer generation, and do not prove runtime operational truth. They do not classify workers, do not change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records, do not select award classes at runtime, do not interpret awards at runtime, do not calculate payroll, do not decide entitlements, do not mutate payroll output, do not determine or finalise readiness, and do not mutate operational workforce/payroll/award truth.

For the repeatable Award Positions / Classifications evaluation workflow and interpretation guidance, see [docs/AWARD_POSITIONS_CLASSIFICATIONS_EVALUATION_RUNBOOK.md](docs/AWARD_POSITIONS_CLASSIFICATIONS_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Rosters / Patterns / Scheduling corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_rosters_patterns_scheduling_corpus_coverage.py --json --output .\artifacts\eval\rosters_patterns_scheduling_corpus_coverage.json
```

Build the diagnostic-only Rosters / Patterns / Scheduling answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_rosters_patterns_scheduling_answer_gap_report.py --coverage-report .\artifacts\eval\rosters_patterns_scheduling_corpus_coverage.json --output .\artifacts\eval\rosters_patterns_scheduling_answer_gap_report.json
```

These Rosters / Patterns / Scheduling diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, connect Code Evidence Index to answer generation, and do not prove runtime operational truth. They do not create rosters, do not change worker schedules, do not mutate Pattern, PatternDay or EmployeeAppointmentPattern truth, do not mutate ObjectTime, do not calculate payroll, do not decide entitlements, do not calculate or approve leave, do not determine or finalise readiness, and do not mutate operational workforce/payroll/leave truth.

For the repeatable Rosters / Patterns / Scheduling evaluation workflow and interpretation guidance, see [docs/ROSTERS_PATTERNS_SCHEDULING_EVALUATION_RUNBOOK.md](docs/ROSTERS_PATTERNS_SCHEDULING_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Public Holidays corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_public_holidays_corpus_coverage.py --json --output .\artifacts\eval\public_holidays_corpus_coverage.json
```

Build the diagnostic-only Public Holidays answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_public_holidays_answer_gap_report.py --coverage-report .\artifacts\eval\public_holidays_corpus_coverage.json --output .\artifacts\eval\public_holidays_answer_gap_report.json
```

These Public Holidays diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, connect Code Evidence Index to answer generation, and do not prove runtime operational truth. They do not calculate public holiday entitlements, do not decide payroll treatment, do not calculate or approve leave, do not post LeaveLedger rows, do not mutate Worksite/PublicHolidayGroup/EmployeeAppointment/PayRun/LeaveRequest truth, and do not determine or finalise readiness.

For the repeatable Public Holidays evaluation workflow and interpretation guidance, see [docs/PUBLIC_HOLIDAYS_EVALUATION_RUNBOOK.md](docs/PUBLIC_HOLIDAYS_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Leave Requests / Leave Workflow corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_requests_workflow_corpus_coverage.py --json --output .\artifacts\eval\leave_requests_workflow_corpus_coverage.json
```

Build the diagnostic-only Leave Requests / Leave Workflow answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_requests_workflow_answer_gap_report.py --coverage-report .\artifacts\eval\leave_requests_workflow_corpus_coverage.json --output .\artifacts\eval\leave_requests_workflow_answer_gap_report.json
```

These Leave Requests / Leave Workflow diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, connect Code Evidence Index to answer generation, and do not prove runtime operational truth.

For the repeatable Leave Requests / Leave Workflow evaluation workflow and interpretation guidance, see [docs/LEAVE_REQUESTS_WORKFLOW_EVALUATION_RUNBOOK.md](docs/LEAVE_REQUESTS_WORKFLOW_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Contact Payroll History corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_contact_payroll_history_corpus_coverage.py --json --output .\artifacts\eval\contact_payroll_history_corpus_coverage.json
```

Build the diagnostic-only Contact Payroll History answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_contact_payroll_history_answer_gap_report.py --coverage-report .\artifacts\eval\contact_payroll_history_corpus_coverage.json --output .\artifacts\eval\contact_payroll_history_answer_gap_report.json
```

These Contact Payroll History diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

For the repeatable Contact Payroll History evaluation workflow and interpretation guidance, see [docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md](docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Payroll Output corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_output_corpus_coverage.py --json --output .\artifacts\eval\payroll_output_corpus_coverage.json
```

Build the diagnostic-only Payroll Output answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_output_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_output_corpus_coverage.json --output .\artifacts\eval\payroll_output_answer_gap_report.json
```

These Payroll Output diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

For the repeatable Payroll Output evaluation workflow and interpretation guidance, see [docs/PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md](docs/PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Decision Story corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_decision_story_corpus_coverage.py --json --output .\artifacts\eval\decision_story_corpus_coverage.json
```

Build the diagnostic-only Decision Story answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_decision_story_answer_gap_report.py --coverage-report .\artifacts\eval\decision_story_corpus_coverage.json --output .\artifacts\eval\decision_story_answer_gap_report.json
```

These Decision Story diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

For the repeatable Decision Story evaluation workflow and interpretation guidance, see [docs/DECISION_STORY_EVALUATION_RUNBOOK.md](docs/DECISION_STORY_EVALUATION_RUNBOOK.md).

Run the diagnostic-only RateSource / Rate Story corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_rate_source_rate_story_corpus_coverage.py --json --output .\artifacts\eval\rate_source_rate_story_corpus_coverage.json
```

Build the diagnostic-only RateSource / Rate Story answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_rate_source_rate_story_answer_gap_report.py --coverage-report .\artifacts\eval\rate_source_rate_story_corpus_coverage.json --output .\artifacts\eval\rate_source_rate_story_answer_gap_report.json
```

These RateSource / Rate Story diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

For the repeatable RateSource / Rate Story evaluation workflow and interpretation guidance, see [docs/RATE_SOURCE_RATE_STORY_EVALUATION_RUNBOOK.md](docs/RATE_SOURCE_RATE_STORY_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Gross-to-Net corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_gross_to_net_corpus_coverage.py --json --output .\artifacts\eval\gross_to_net_corpus_coverage.json
```

Build the diagnostic-only Gross-to-Net answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_gross_to_net_answer_gap_report.py --coverage-report .\artifacts\eval\gross_to_net_corpus_coverage.json --output .\artifacts\eval\gross_to_net_answer_gap_report.json
```

These Gross-to-Net diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

For the repeatable Gross-to-Net evaluation workflow and interpretation guidance, see [docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md](docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Worker Attention / Issue Resolution corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_worker_attention_issue_resolution_corpus_coverage.py --json --output .\artifacts\eval\worker_attention_issue_resolution_corpus_coverage.json
```

Build the diagnostic-only Worker Attention / Issue Resolution answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_worker_attention_issue_resolution_answer_gap_report.py --coverage-report .\artifacts\eval\worker_attention_issue_resolution_corpus_coverage.json --output .\artifacts\eval\worker_attention_issue_resolution_answer_gap_report.json
```

These Worker Attention / Issue Resolution diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

For the repeatable Worker Attention / Issue Resolution evaluation workflow and interpretation guidance, see [docs/WORKER_ATTENTION_ISSUE_RESOLUTION_EVALUATION_RUNBOOK.md](docs/WORKER_ATTENTION_ISSUE_RESOLUTION_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Costing / GL Consequence Evidence corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_costing_gl_consequence_corpus_coverage.py --json --output .\artifacts\eval\costing_gl_consequence_corpus_coverage.json
```

Build the diagnostic-only Costing / GL Consequence Evidence answer gap report from coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_costing_gl_consequence_answer_gap_report.py --coverage-report .\artifacts\eval\costing_gl_consequence_corpus_coverage.json --output .\artifacts\eval\costing_gl_consequence_answer_gap_report.json
```

For the repeatable Costing / GL Consequence Evidence evaluation workflow and interpretation guidance, see [docs/COSTING_GL_CONSEQUENCE_EVALUATION_RUNBOOK.md](docs/COSTING_GL_CONSEQUENCE_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Process Periods / PayRun Lifecycle corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_process_period_payrun_lifecycle_corpus_coverage.py --json --output .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json
```

Build a diagnostic-only Process Periods / PayRun Lifecycle answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_process_period_payrun_lifecycle_answer_gap_report.py --coverage-report .\artifacts\eval\process_period_payrun_lifecycle_corpus_coverage.json --output .\artifacts\eval\process_period_payrun_lifecycle_answer_gap_report.json
```

These Process Periods / PayRun Lifecycle diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

For the repeatable Process Periods / PayRun Lifecycle evaluation workflow and interpretation guidance, see [docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md](docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md).

Run the diagnostic-only ObjectTime / Source Truth corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_objecttime_source_truth_corpus_coverage.py --json --output .\artifacts\eval\objecttime_source_truth_corpus_coverage.json
```

Build a diagnostic-only ObjectTime / Source Truth answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_objecttime_source_truth_answer_gap_report.py --coverage-report .\artifacts\eval\objecttime_source_truth_corpus_coverage.json --output .\artifacts\eval\objecttime_source_truth_answer_gap_report.json
```

These ObjectTime / Source Truth diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable ObjectTime / Source Truth evaluation workflow and interpretation guidance, see [docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md](docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Imports / Actuals corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_imports_actuals_corpus_coverage.py --json --output .\artifacts\eval\imports_actuals_corpus_coverage.json
```

Build a diagnostic-only Imports / Actuals answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_imports_actuals_answer_gap_report.py --coverage-report .\artifacts\eval\imports_actuals_corpus_coverage.json --output .\artifacts\eval\imports_actuals_answer_gap_report.json
```

These Imports / Actuals diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable Imports / Actuals evaluation workflow and interpretation guidance, see [docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md](docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Award Build / Award Evidence corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_award_build_evidence_corpus_coverage.py --json --output .\artifacts\eval\award_build_evidence_corpus_coverage.json
```

Build a diagnostic-only Award Build / Award Evidence answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_award_build_evidence_answer_gap_report.py --coverage-report .\artifacts\eval\award_build_evidence_corpus_coverage.json --output .\artifacts\eval\award_build_evidence_answer_gap_report.json
```

These Award Build / Award Evidence diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable Award Build / Award Evidence evaluation workflow and interpretation guidance, see [docs/AWARD_BUILD_EVIDENCE_EVALUATION_RUNBOOK.md](docs/AWARD_BUILD_EVIDENCE_EVALUATION_RUNBOOK.md).

Run the diagnostic-only On-costs / Employer Liabilities corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_oncosts_employer_liabilities_corpus_coverage.py --json --output .\artifacts\eval\oncosts_employer_liabilities_corpus_coverage.json
```

Build a diagnostic-only On-costs / Employer Liabilities answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_oncosts_employer_liabilities_answer_gap_report.py --coverage-report .\artifacts\eval\oncosts_employer_liabilities_corpus_coverage.json --output .\artifacts\eval\oncosts_employer_liabilities_answer_gap_report.json
```

These On-costs / Employer Liabilities diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable On-costs / Employer Liabilities evaluation workflow and interpretation guidance, see [docs/ONCOSTS_EMPLOYER_LIABILITIES_EVALUATION_RUNBOOK.md](docs/ONCOSTS_EMPLOYER_LIABILITIES_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Leave Source Model corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_source_model_corpus_coverage.py --json --output .\artifacts\eval\leave_source_model_corpus_coverage.json
```

Build a diagnostic-only Leave Source Model answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_source_model_answer_gap_report.py --coverage-report .\artifacts\eval\leave_source_model_corpus_coverage.json --output .\artifacts\eval\leave_source_model_answer_gap_report.json
```

These Leave Source Model diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable Leave Source Model evaluation workflow and interpretation guidance, see [docs/LEAVE_SOURCE_MODEL_EVALUATION_RUNBOOK.md](docs/LEAVE_SOURCE_MODEL_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Finalisation Readiness corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_finalisation_readiness_corpus_coverage.py --json --output .\artifacts\eval\finalisation_readiness_corpus_coverage.json
```

Build a diagnostic-only Finalisation Readiness answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_finalisation_readiness_answer_gap_report.py --coverage-report .\artifacts\eval\finalisation_readiness_corpus_coverage.json --output .\artifacts\eval\finalisation_readiness_answer_gap_report.json
```

These Finalisation Readiness diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable Finalisation Readiness evaluation workflow and interpretation guidance, see [docs/FINALISATION_READINESS_EVALUATION_RUNBOOK.md](docs/FINALISATION_READINESS_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Leave Accrual / Processing corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_leave_accrual_processing_corpus_coverage.py --json --output .\artifacts\eval\leave_accrual_processing_corpus_coverage.json
```

Build a diagnostic-only Leave Accrual / Processing answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_leave_accrual_processing_answer_gap_report.py --coverage-report .\artifacts\eval\leave_accrual_processing_corpus_coverage.json --output .\artifacts\eval\leave_accrual_processing_answer_gap_report.json
```

These Leave Accrual / Processing diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable Leave Accrual / Processing evaluation workflow and interpretation guidance, see [docs/LEAVE_ACCRUAL_PROCESSING_EVALUATION_RUNBOOK.md](docs/LEAVE_ACCRUAL_PROCESSING_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Payment Execution / Remittance corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payment_execution_remittance_corpus_coverage.py --json --output .\artifacts\eval\payment_execution_remittance_corpus_coverage.json
```

Build a diagnostic-only Payment Execution / Remittance answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_payment_execution_remittance_answer_gap_report.py --coverage-report .\artifacts\eval\payment_execution_remittance_corpus_coverage.json --output .\artifacts\eval\payment_execution_remittance_answer_gap_report.json
```

These Payment Execution / Remittance diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable Payment Execution / Remittance evaluation workflow and interpretation guidance, see [docs/PAYMENT_EXECUTION_REMITTANCE_EVALUATION_RUNBOOK.md](docs/PAYMENT_EXECUTION_REMITTANCE_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Retro / Replay corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_retro_replay_corpus_coverage.py --json --output .\artifacts\eval\retro_replay_corpus_coverage.json
```

Build a diagnostic-only Retro / Replay answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_retro_replay_answer_gap_report.py --coverage-report .\artifacts\eval\retro_replay_corpus_coverage.json --output .\artifacts\eval\retro_replay_answer_gap_report.json
```

These Retro / Replay diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

For the repeatable Retro / Replay evaluation workflow and interpretation guidance, see [docs/RETRO_REPLAY_EVALUATION_RUNBOOK.md](docs/RETRO_REPLAY_EVALUATION_RUNBOOK.md).

Run the diagnostic-only Deductions / Obligations corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_deductions_obligations_corpus_coverage.py --json --output .\artifacts\eval\deductions_obligations_corpus_coverage.json
```

Build a diagnostic-only Deductions / Obligations answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_deductions_obligations_answer_gap_report.py --coverage-report .\artifacts\eval\deductions_obligations_corpus_coverage.json --output .\artifacts\eval\deductions_obligations_answer_gap_report.json
```

These Deductions / Obligations diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

Deductions / Obligations evaluation is documented in [docs/DEDUCTIONS_OBLIGATIONS_EVALUATION_RUNBOOK.md](docs/DEDUCTIONS_OBLIGATIONS_EVALUATION_RUNBOOK.md), including benchmark, corpus coverage diagnostic, answer gap report commands and diagnostic-only guardrails.

Run the diagnostic-only Tax / PAYG corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_tax_payg_corpus_coverage.py --json --output .\artifacts\eval\tax_payg_corpus_coverage.json
```

Build a diagnostic-only Tax / PAYG answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_tax_payg_answer_gap_report.py --coverage-report .\artifacts\eval\tax_payg_corpus_coverage.json --output .\artifacts\eval\tax_payg_answer_gap_report.json
```

These Tax / PAYG diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

Tax / PAYG evaluation is documented in [docs/TAX_PAYG_EVALUATION_RUNBOOK.md](docs/TAX_PAYG_EVALUATION_RUNBOOK.md), including benchmark, corpus coverage diagnostic, answer gap report commands and diagnostic-only guardrails.

Run the diagnostic-only Comparison / Remediation corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_comparison_remediation_corpus_coverage.py --json --output .\artifacts\eval\comparison_remediation_corpus_coverage.json
```

Build a diagnostic-only Comparison / Remediation answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_comparison_remediation_answer_gap_report.py --coverage-report .\artifacts\eval\comparison_remediation_corpus_coverage.json --output .\artifacts\eval\comparison_remediation_answer_gap_report.json
```

These Comparison / Remediation diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

Comparison / Remediation evaluation is documented in [docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md](docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md), including benchmark, corpus coverage diagnostic, answer gap report commands and diagnostic-only guardrails.

Run the diagnostic-only Movement Review corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_movement_review_corpus_coverage.py --json --output .\artifacts\eval\movement_review_corpus_coverage.json
```

Build a diagnostic-only Movement Review answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_movement_review_answer_gap_report.py --coverage-report .\artifacts\eval\movement_review_corpus_coverage.json --output .\artifacts\eval\movement_review_answer_gap_report.json
```

These Movement Review diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

Run the diagnostic-only PayRun Admin Queue corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payrun_admin_queue_corpus_coverage.py --json --output .\artifacts\eval\payrun_admin_queue_corpus_coverage.json
```

Build a diagnostic-only PayRun Admin Queue answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_payrun_admin_queue_answer_gap_report.py --coverage-report .\artifacts\eval\payrun_admin_queue_corpus_coverage.json --output .\artifacts\eval\payrun_admin_queue_answer_gap_report.json
```

These PayRun Admin Queue diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

Run the diagnostic-only Contacts / Employee Appointments corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_contacts_employee_appointments_corpus_coverage.py --json --output .\artifacts\eval\contacts_employee_appointments_corpus_coverage.json
```

Build a diagnostic-only Contacts / Employee Appointments answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_contacts_employee_appointments_answer_gap_report.py --coverage-report .\artifacts\eval\contacts_employee_appointments_corpus_coverage.json --output .\artifacts\eval\contacts_employee_appointments_answer_gap_report.json
```

These Contacts / Employee Appointments diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, read source code as Minerva evidence, or connect Code Evidence Index to answer generation.

Run the diagnostic-only Payroll Bases & Totals corpus coverage scan:

```powershell
.\.venv\Scripts\python.exe scripts\scan_payroll_bases_corpus_coverage.py --json --output .\artifacts\eval\payroll_bases_corpus_coverage.json
```

Build a diagnostic-only Payroll Bases & Totals answer gap report from the coverage JSON:

```powershell
.\.venv\Scripts\python.exe scripts\build_payroll_bases_answer_gap_report.py --coverage-report .\artifacts\eval\payroll_bases_corpus_coverage.json --output .\artifacts\eval\payroll_bases_answer_gap_report.json
```

These Payroll Bases diagnostics read the already indexed formal corpus and saved diagnostic JSON only. They do not mutate corpus records, run migrations, ingest operational JSON, call a live LLM, or connect Code Evidence Index to answer generation.

Run the Worker Story corpus coverage diagnostic:

```powershell
py scripts/scan_worker_story_corpus_coverage.py
py scripts/scan_worker_story_corpus_coverage.py --json --output reports/worker_story_corpus_coverage.json
```

Build a coverage-driven Worker Story answer gap report:

```powershell
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json
py scripts/build_worker_story_answer_gap_report.py --coverage-report reports/worker_story_corpus_coverage.json --json --output reports/worker_story_answer_gap_report.json
```

The coverage diagnostic and gap report are not benchmarks and do not call a live LLM. The coverage diagnostic reads the already indexed formal corpus and reports whether each Worker Story evidence group is `STRONG`, `WEAK` or `MISSING`. The gap report consumes that JSON and recommends whether to keep the current path, refine retrieval terms, improve synthesis, or add formal source evidence later. Neither script ingests files or mutates corpus records.

## Targeted Annual Leave Corpus Supplement

If the Annual Leave golden pack fails against SQL Server, the loaded foundation corpus likely does not yet include enough leave-specific formal logs. Before bulk raw chat-history ingestion, load targeted formal leave documents only.

1. Put candidate formal leave documents in a local folder, such as:

```text
samples/knowledge/annual_leave_seed/
```

Use Developer Logs, Hardening Logs, Platform Doctrine or formal requirements. Do not put raw chat-history exports in this seed folder.

2. Scan candidate docs for likely Annual Leave relevance:

```powershell
py scripts/scan_leave_corpus_candidates.py samples/knowledge/annual_leave_seed
py scripts/scan_leave_corpus_candidates.py C:\path\to\candidate\docs --top 20
```

3. Build a draft manifest, then review and edit titles/source types if needed:

```powershell
py scripts/build_leave_manifest_from_candidates.py samples/knowledge/annual_leave_seed --output samples/knowledge/annual_leave_seed_manifest.generated.json --min-score 3
```

4. Ingest the reviewed manifest:

```powershell
py scripts/ingest_manifest.py samples/knowledge/annual_leave_seed_manifest.generated.json
```

5. Backfill SourceSection from that manifest if needed:

```powershell
py scripts/backfill_source_sections.py --manifest samples/knowledge/annual_leave_seed_manifest.generated.json
```

6. Check chunk quality:

```powershell
py scripts/chunk_quality_report.py
```

7. Re-run the Annual Leave golden pack:

```powershell
py scripts/run_golden_questions.py --manifest samples/eval/golden_questions.annual_leave.json --verbose
```

Raw chat history remains lower-authority supporting material. Do not bulk-load it until formal leave logs and doctrine have been tested first.

## Chunk And Metadata Inspection

Before bulk chat-history ingestion, inspect chunk boundaries and metadata quality so retrieval problems are easier to diagnose. Source sections help show which heading or section a chunk came from, which makes bad matches and poor chunk boundaries easier to spot.

List documents:

```powershell
py scripts/list_documents.py
py scripts/list_documents.py --source-type DEVELOPER_LOG --show-metadata
py scripts/list_documents.py --title-contains "Platform Doctrine" --show-metadata
```

Inspect chunks:

```powershell
py scripts/inspect_chunks.py --document-id <document_id>
py scripts/inspect_chunks.py --title-contains "Platform Doctrine"
py scripts/inspect_chunks.py --source-type DEVELOPER_LOG --limit 20
py scripts/inspect_chunks.py --document-id <document_id> --start-index 10 --limit 5
```

Run a corpus quality summary:

```powershell
py scripts/chunk_quality_report.py
py scripts/chunk_quality_report.py --source-type DEVELOPER_LOG
py scripts/chunk_quality_report.py --title-contains "Hardening"
```

Slice 1.8 does not add database columns for inferred metadata. Metadata extraction is diagnostic-only and is computed from the source text or filename when available. Existing SQL Server databases do not need manual `ALTER TABLE` statements for this slice.

## Backfilling SourceSection

If a corpus was loaded before SourceSection detection existed, existing chunks may show `Chunks missing SourceSection` in the quality report. Backfill re-extracts the original TXT/DOCX files, replaces only the document's chunks, and preserves the existing `KnowledgeDocument` row, document id, hash, source type, tenant id, title and status.

Dry-run the seed manifest first:

```powershell
py scripts/backfill_source_sections.py --manifest samples/knowledge/minerva_seed_manifest.json --dry-run
```

Run the real backfill:

```powershell
py scripts/backfill_source_sections.py --manifest samples/knowledge/minerva_seed_manifest.json
```

You can also backfill one document when you know the source file path:

```powershell
py scripts/backfill_source_sections.py --document-id <document_id> --file-path samples/knowledge/minerva_seed/platform_doctrine.docx
```

Backfill skips `SUPERSEDED` documents by default. Use `--include-superseded` only when intentionally repairing historical documents. Verify progress with:

```powershell
py scripts/chunk_quality_report.py
```

Slice 1.8.1 does not add database columns, so existing SQL Server databases do not need manual schema changes.

## Tests

Tests use SQLite in memory so normal pytest runs do not require SQL Server.

```powershell
pytest
```

## Guardrails

- No external LLM calls are made in v0.1.
- No JSON evidence ingestion is implemented.
- Retrieved document content is treated as evidence, not instructions.
- Minerva does not execute actions based on retrieved text.
- Tenant fields and tenant-aware retrieval structure are present for later RBAC hardening.
