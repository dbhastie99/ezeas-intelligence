from pathlib import Path


def test_worker_story_evaluation_runbook_exists_and_lists_required_commands():
    runbook_path = Path("docs/WORKER_STORY_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "run_golden_questions.py" in runbook
    assert "scan_worker_story_corpus_coverage.py" in runbook
    assert "build_worker_story_answer_gap_report.py" in runbook


def test_payroll_bases_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PAYROLL_BASES_AND_TOTALS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.payroll_bases_and_totals.json" in runbook
    assert "scan_payroll_bases_corpus_coverage.py" in runbook
    assert "build_payroll_bases_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook


def test_payrun_admin_queue_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PAYRUN_ADMIN_QUEUE_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.payrun_admin_queue.json" in runbook
    assert "scan_payrun_admin_queue_corpus_coverage.py" in runbook
    assert "build_payrun_admin_queue_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "queue cleanliness is not assurance" in runbook


def test_movement_review_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/MOVEMENT_REVIEW_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.movement_review.json" in runbook
    assert "scan_movement_review_corpus_coverage.py" in runbook
    assert "build_movement_review_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "variance is not automatic proof of error" in runbook
    assert "not every movement creates a fix action" in runbook


def test_comparison_remediation_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/COMPARISON_REMEDIATION_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.comparison_remediation.json" in runbook
    assert "scan_comparison_remediation_corpus_coverage.py" in runbook
    assert "build_comparison_remediation_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "comparison evidence before variance" in runbook
    assert "actuals as external outcome truth" in runbook
    assert "comparator classification can be guessed" in runbook


def test_tax_payg_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/TAX_PAYG_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.tax_payg.json" in runbook
    assert "scan_tax_payg_corpus_coverage.py" in runbook
    assert "build_tax_payg_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Minerva does not calculate tax" in runbook
    assert "TaxStory" in runbook
    assert "unsupported frequencies must be explicit" in runbook
    assert "supplementary incremental PAYG" in runbook


def test_deductions_obligations_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/DEDUCTIONS_OBLIGATIONS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.deductions_obligations.json" in runbook
    assert "scan_deductions_obligations_corpus_coverage.py" in runbook
    assert "build_deductions_obligations_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "LibraryDeductionTemplate -> AccountDeductionTemplate -> ContactPayrollDeduction -> PayRunDeductionApplication" in runbook
    assert "PayRunDeductionApplication is event/outcome memory" in runbook
    assert "applicability before affordability" in runbook
    assert "obligations are durable balance-bearing recovery records" in runbook
    assert "reducing-balance recovery" in runbook
    assert "negative net pay is a governed policy outcome" in runbook


def test_retro_replay_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/RETRO_REPLAY_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.retro_replay.json" in runbook
    assert "scan_retro_replay_corpus_coverage.py" in runbook
    assert "build_retro_replay_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "attributed-period truth" in runbook
    assert "paid-period truth" in runbook
    assert "finalised payroll truth must not be silently overwritten" in runbook
    assert "retro PayRuns" in runbook
    assert "supplementary PayRuns" in runbook
    assert "dependency detection" in runbook
    assert "governed historical bucket rebuilds" in runbook


def test_payment_execution_remittance_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PAYMENT_EXECUTION_REMITTANCE_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.payment_execution_remittance.json" in runbook
    assert "scan_payment_execution_remittance_corpus_coverage.py" in runbook
    assert "build_payment_execution_remittance_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "payment execution is not payroll calculation truth" in runbook
    assert "gross-to-net readiness is not payment execution readiness" in runbook
    assert "missing payment destination can block payment execution without invalidating gross-to-net" in runbook
    assert "bank file generation" in runbook
    assert "remittance reconciliation" in runbook
    assert "negative net pay handling" in runbook


def test_leave_accrual_processing_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/LEAVE_ACCRUAL_PROCESSING_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.leave_accrual_processing.json" in runbook
    assert "scan_leave_accrual_processing_corpus_coverage.py" in runbook
    assert "build_leave_accrual_processing_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Minerva does not calculate leave" in runbook
    assert "LeaveTypeRule alone is final applicability truth" in runbook
    assert "Leave Source Model" in runbook
    assert "TAKEN leave valuation hard-fail/no silent fallback" in runbook
    assert "CalcInterpreterLine/current-effective payroll output" in runbook
    assert "LeaveLedger" in runbook
    assert "Worker Story" in runbook
    assert "Payroll Bases & Totals" in runbook


def test_annual_leave_evaluation_runbook_exists_and_documents_foundation_status():
    runbook_path = Path("docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/ANNUAL_LEAVE_EVALUATION_RUNBOOK.md" in readme
    assert "samples\\eval\\rich_answer_benchmark.annual_leave.json" in runbook
    assert "samples\\eval\\golden_questions.annual_leave.json" in runbook
    assert "scripts\\scan_leave_corpus_candidates.py" in runbook
    assert "scripts\\build_leave_manifest_from_candidates.py" in runbook
    assert "app/services/domain_retrieval_plan_service.py" in runbook
    assert "ANNUAL_LEAVE_MANAGEMENT" in runbook
    assert "configuration" in runbook
    assert "accrual" in runbook
    assert "taken" in runbook
    assert "valuation" in runbook
    assert "payrun" in runbook
    assert "worker_story" in runbook
    assert "outstanding" in runbook
    assert "Leave Accrual / Processing is narrower and deeper" in runbook
    assert "Leave Source Model evaluates source truth and applicability boundaries" in runbook
    assert "Leave Requests / Leave Workflow evaluates request lifecycle" in runbook
    assert "Public Holidays evaluates public-holiday source/calendar evidence" in runbook
    assert "Adjacent domain runbooks, corpus coverage diagnostics and answer gap reports must not be counted" in runbook
    assert "Annual Leave / Leave Management corpus coverage diagnostic classifies" in runbook
    assert "No Annual Leave / Leave Management-specific answer gap report service or script exists" in runbook
    assert "app/services/annual_leave_corpus_coverage_service.py" in runbook
    assert "scripts\\scan_annual_leave_corpus_coverage.py" in runbook
    assert "app/services/annual_leave_answer_gap_report_service.py" in runbook
    assert "scripts/build_annual_leave_answer_gap_report.py" in runbook
    assert "scan_leave_accrual_processing_corpus_coverage.py" in runbook
    assert "scan_leave_source_model_corpus_coverage.py" in runbook
    assert "scan_leave_requests_workflow_corpus_coverage.py" in runbook
    assert "scan_public_holidays_corpus_coverage.py" in runbook
    assert "Do not use adjacent leave-domain answer gap reports as substitutes" in runbook
    assert "Minerva explains Annual Leave but does not calculate leave" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "no live LLM" in runbook
    assert "no corpus mutation" in runbook
    assert "no database schema change" in runbook
    assert "no endpoint or UI changes" in runbook
    assert "no workforce-platform changes" in runbook
    assert "Do not weaken benchmark expectations" in runbook
    assert "do not create an Annual Leave baseline pack" in runbook


def test_finalisation_readiness_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/FINALISATION_READINESS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.finalisation_readiness.json" in runbook
    assert "scan_finalisation_readiness_corpus_coverage.py" in runbook
    assert "build_finalisation_readiness_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Minerva does not determine readiness" in runbook
    assert "blockers, warnings and green readiness" in runbook
    assert "current-effective payroll output" in runbook
    assert "Amber warnings must not be silent or ignored" in runbook
    assert "payment execution readiness is different from gross-to-net readiness" in runbook
    assert "finalised outcome truth" in runbook
    assert "warning acknowledgement and audit evidence" in runbook


def test_leave_source_model_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/LEAVE_SOURCE_MODEL_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.leave_source_model.json" in runbook
    assert "scan_leave_source_model_corpus_coverage.py" in runbook
    assert "build_leave_source_model_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "LeaveTypeRule alone is final applicability truth" in runbook
    assert "applicability versus rule content" in runbook
    assert "no entitlement versus missing leave output" in runbook
    assert "contact versus appointment scope" in runbook
    assert "source dimensions and precedence" in runbook
    assert "Minerva does not calculate leave applicability" in runbook


def test_oncosts_employer_liabilities_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/ONCOSTS_EMPLOYER_LIABILITIES_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.oncosts_employer_liabilities.json" in runbook
    assert "scan_oncosts_employer_liabilities_corpus_coverage.py" in runbook
    assert "build_oncosts_employer_liabilities_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Employer liability is not worker pay" in runbook
    assert "Minerva does not calculate on-costs" in runbook
    assert "RateSource and date-effective rates" in runbook
    assert "governed basis membership" in runbook
    assert "state/worksite/runtime location resolution" in runbook
    assert "account-wide fallback demo behavior" in runbook
    assert "not proof that demo account-wide fallback is production truth" in runbook
    assert "super, payroll tax and WorkCover / WIC" in runbook


def test_award_build_evidence_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/AWARD_BUILD_EVIDENCE_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.award_build_evidence.json" in runbook
    assert "scan_award_build_evidence_corpus_coverage.py" in runbook
    assert "build_award_build_evidence_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Award Build / Award Evidence is not runtime payroll calculation" in runbook
    assert "Minerva does not interpret awards at runtime" in runbook
    assert "award documents and pay guides as source evidence" in runbook
    assert "RateType and AwardRateType" in runbook
    assert "RateSource and date-effective rate evidence" in runbook
    assert "DecisionEvidenceIndex" in runbook
    assert "RateSourceEvidenceIndex" in runbook
    assert "NEEDS_CONFIGURATION" in runbook
    assert "Durable AwardEvidenceSet" in runbook


def test_imports_actuals_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/IMPORTS_ACTUALS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.imports_actuals.json" in runbook
    assert "scan_imports_actuals_corpus_coverage.py" in runbook
    assert "build_imports_actuals_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Imported actuals are external outcome truth" in runbook
    assert "imported timesheets" in runbook
    assert "source truth" in runbook
    assert "source-system mapping" in runbook
    assert "pay code / RateType mapping" in runbook
    assert "position/classification mapping" in runbook
    assert "ObjectTime/source truth" in runbook
    assert "evidence provenance and audit" in runbook
    assert "Comparison / Remediation keeps ownership" in runbook


def test_objecttime_source_truth_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/OBJECTTIME_SOURCE_TRUTH_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.objecttime_source_truth.json" in runbook
    assert "scan_objecttime_source_truth_corpus_coverage.py" in runbook
    assert "build_objecttime_source_truth_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "ObjectTime is source evidence, not payroll calculation truth" in runbook
    assert "PayRun inclusion" in runbook
    assert "source truth" in runbook
    assert "SourceTruth versus WorkedHours" in runbook
    assert "raw span hours are not user-facing worked hours" in runbook
    assert "current-effective payroll output" in runbook
    assert "Worker Story" in runbook
    assert "Payroll Bases" in runbook
    assert "Leave Accrual" in runbook
    assert "corrections, dirty contacts and reprocessing" in runbook
    assert "evidence provenance and audit" in runbook


def test_contacts_employee_appointments_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/CONTACTS_EMPLOYEE_APPOINTMENTS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.contacts_employee_appointments.json" in runbook
    assert "scan_contacts_employee_appointments_corpus_coverage.py" in runbook
    assert "build_contacts_employee_appointments_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "Contact versus EmployeeAppointment" in runbook
    assert "PayRun admission" in runbook
    assert "ObjectTime / Source Truth" in runbook
    assert "AwardPositionClass" in runbook
    assert "WorksitePosition" in runbook
    assert "worksite/state/runtime location" in runbook
    assert "leave source/accrual" in runbook
    assert "Worker Story" in runbook
    assert "Contact history" in runbook
    assert "dirty contact and reprocessing" in runbook
    assert "classification lenses rather than duplicate full appointments" in runbook


def test_process_period_payrun_lifecycle_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PROCESS_PERIOD_PAYRUN_LIFECYCLE_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.process_period_payrun_lifecycle.json" in runbook
    assert "scan_process_period_payrun_lifecycle_corpus_coverage.py" in runbook
    assert "build_process_period_payrun_lifecycle_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "ProcessPeriod" in runbook
    assert "ProcessPeriodGroup" in runbook
    assert "open, not-open and closed lifecycle" in runbook
    assert "closed dominates open" in runbook
    assert "close rolls forward" in runbook
    assert "PaymentDate" in runbook
    assert "RunType" in runbook
    assert "RunPurpose" in runbook
    assert "regular, supplementary and retro PayRuns" in runbook
    assert "PayRunContact" in runbook
    assert "admission is not processing" in runbook
    assert "current-effective output" in runbook
    assert "Finalisation Readiness" in runbook
    assert "Payment Execution" in runbook
    assert "Worker Story" in runbook
    assert "Admin Queue" in runbook
    assert "Movement Review" in runbook


def test_costing_gl_consequence_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/COSTING_GL_CONSEQUENCE_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.costing_gl_consequence.json" in runbook
    assert "scan_costing_gl_consequence_corpus_coverage.py" in runbook
    assert "build_costing_gl_consequence_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "downstream financial consequence evidence" in runbook
    assert "finalised payroll outcome truth" in runbook
    assert "Payment Execution / Remittance" in runbook
    assert "employer liabilities / on-costs" in runbook
    assert "obligation write-off" in runbook or "obligation writeoff" in runbook
    assert "remediation variance" in runbook
    assert "leave valuation" in runbook
    assert "negative net pay" in runbook
    assert "deferred/final costing slice" in runbook


def test_worker_attention_issue_resolution_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/WORKER_ATTENTION_ISSUE_RESOLUTION_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.worker_attention_issue_resolution.json" in runbook
    assert "scan_worker_attention_issue_resolution_corpus_coverage.py" in runbook
    assert "build_worker_attention_issue_resolution_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "Worker Attention" in runbook
    assert "WorkerIssue" in runbook or "worker issue" in runbook
    assert "deterministic fix link" in runbook
    assert "dirty contact" in runbook or "PayRunContact dirty" in runbook
    assert "payment allocation" in runbook
    assert "negative net pay" in runbook
    assert "Worker Story" in runbook
    assert "PayRun Admin Queue" in runbook
    assert "Contacts / Employee Appointments" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook or "no Code Evidence Index answer integration" in runbook
    assert "Minerva does not resolve, clear, reprocess, calculate, approve, suppress, finalise or mutate payroll truth" in runbook


def test_gross_to_net_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/GROSS_TO_NET_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.gross_to_net.json" in runbook
    assert "scan_gross_to_net_corpus_coverage.py" in runbook
    assert "build_gross_to_net_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "Gross-to-Net" in runbook
    assert "gross earnings" in runbook
    assert "net pay" in runbook
    assert "taxable basis" in runbook
    assert "PAYG" in runbook or "withholding" in runbook
    assert "deductions" in runbook
    assert "obligations" in runbook
    assert "negative net pay" in runbook
    assert "payment allocation" in runbook or "payment execution" in runbook
    assert "current-effective payroll output" in runbook
    assert "Worker Story" in runbook
    assert "Tax / PAYG" in runbook
    assert "Deductions / Obligations" in runbook
    assert "Payment Execution / Remittance" in runbook
    assert "Payroll Bases & Totals" in runbook
    assert "Minerva does not calculate, withhold, apply deductions, approve, resolve, generate payment files, finalise or mutate payroll truth" in runbook


def test_rate_source_rate_story_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/RATE_SOURCE_RATE_STORY_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.rate_source_rate_story.json" in runbook
    assert "scan_rate_source_rate_story_corpus_coverage.py" in runbook
    assert "build_rate_source_rate_story_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "RateSource" in runbook
    assert "Rate Story" in runbook
    assert "RateSourceEvidenceIndex" in runbook
    assert "selected rate" in runbook or "rate selection" in runbook
    assert "rate amount evidence" in runbook
    assert "date-effective rates" in runbook
    assert "award/account/class scope" in runbook
    assert "pay guide evidence" in runbook
    assert "Decision Story" in runbook
    assert "Worker Story" in runbook
    assert "Gross-to-Net" in runbook
    assert "Award Build / Award Evidence" in runbook
    assert "Payroll Bases & Totals" in runbook
    assert "Minerva does not select rates, calculate pay, interpret awards at runtime, change RateSource records, validate payroll correctness or mutate payroll truth" in runbook


def test_decision_story_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/DECISION_STORY_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.decision_story.json" in runbook
    assert "scan_decision_story_corpus_coverage.py" in runbook
    assert "build_decision_story_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "Decision Story" in runbook
    assert "DecisionEvidenceIndex" in runbook
    assert "treatment or entitlement selection" in runbook
    assert "why a payroll line exists" in runbook
    assert "allowance" in runbook
    assert "penalty" in runbook
    assert "overtime" in runbook
    assert "shift" in runbook
    assert "break" in runbook
    assert "public holiday" in runbook
    assert "Rate Story" in runbook
    assert "Worker Story" in runbook
    assert "Gross-to-Net" in runbook
    assert "Award Build / Award Evidence" in runbook
    assert "Payroll Bases & Totals" in runbook
    assert "Minerva does not select treatments, decide entitlements, interpret awards at runtime, calculate payroll, change decision evidence, validate payroll correctness or mutate payroll truth" in runbook


def test_payroll_output_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PAYROLL_OUTPUT_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.payroll_output.json" in runbook
    assert "scan_payroll_output_corpus_coverage.py" in runbook
    assert "build_payroll_output_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "Payroll Output" in runbook
    assert "PayRun Output" in runbook
    assert "Process Period Output" in runbook
    assert "Run Output" in runbook
    assert "current-effective payroll output" in runbook
    assert "payroll lines" in runbook or "output lines" in runbook
    assert "Worker Story" in runbook
    assert "Gross-to-Net" in runbook
    assert "Decision Story" in runbook
    assert "RateSource" in runbook or "Rate Story" in runbook
    assert "Payroll Bases & Totals" in runbook
    assert "Finalisation Readiness" in runbook
    assert "Payment Execution / Remittance" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook or "no Code Evidence Index answer integration" in runbook
    assert "Minerva does not calculate payroll output, change output lines, finalise PayRuns, approve output, select treatments, select rates, generate payment files or mutate payroll truth" in runbook


def test_contact_payroll_history_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/CONTACT_PAYROLL_HISTORY_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    assert "samples\\eval\\rich_answer_benchmark.contact_payroll_history.json" in runbook
    assert "scan_contact_payroll_history_corpus_coverage.py" in runbook
    assert "build_contact_payroll_history_answer_gap_report.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "Contact Payroll History" in runbook
    assert "contact/worker-level payroll history" in runbook
    assert "PayRun participation" in runbook
    assert "current and historical payroll output" in runbook
    assert "Gross-to-Net" in runbook
    assert "deductions and obligations" in runbook
    assert "tax/payment readiness" in runbook
    assert "leave/accrual evidence" in runbook
    assert "Worker Story" in runbook
    assert "Retro / Replay" in runbook
    assert "correction context" in runbook
    assert "Movement Review" in runbook
    assert "PayRun Admin Queue" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook or "no Code Evidence Index answer integration" in runbook
    assert "Minerva does not calculate payroll history, change historical records, correct payroll outcomes, perform retro/replay, approve payroll changes, finalise PayRuns or mutate payroll truth" in runbook


def test_leave_requests_workflow_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/LEAVE_REQUESTS_WORKFLOW_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/LEAVE_REQUESTS_WORKFLOW_EVALUATION_RUNBOOK.md" in readme
    assert ".\\.venv\\Scripts\\python.exe -m pytest --basetemp .\\.pytest_tmp" in runbook
    assert "samples\\eval\\rich_answer_benchmark.leave_requests_workflow.json" in runbook
    assert "scan_leave_requests_workflow_corpus_coverage.py" in runbook
    assert "build_leave_requests_workflow_answer_gap_report.py" in runbook
    assert "tests\\test_domain_retrieval_plans.py" in runbook
    assert "tests\\test_rich_answer_contract.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "not proof of runtime operational truth" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "request_lifecycle_and_status_transitions" in runbook
    assert "preview_overlap_and_shortfall_handling" in runbook
    assert "taken_leave_valuation_and_hard_fail" in runbook
    assert "leaveledger_posting_and_balance_effects" in runbook
    assert "leave_source_and_applicability_relationship" in runbook
    assert "worker_story_payrun_and_finalisation_relationship" in runbook
    assert "idempotency_reopen_and_approval_governance" in runbook
    assert "minerva_boundaries_and_non_mutation_guardrails" in runbook
    assert "Leave Requests / Leave Workflow" in runbook
    assert "creating, submitting, reviewing, approving, rejecting, reopening, valuing, posting and explaining leave requests" in runbook
    assert "Minerva explains Leave Requests / Leave Workflow" in runbook
    assert "Minerva does not approve leave" in runbook
    assert "Minerva does not calculate leave" in runbook
    assert "Minerva does not post LeaveLedger rows" in runbook
    assert "Minerva does not change leave balances" in runbook
    assert "Minerva does not reopen leave requests" in runbook
    assert "Minerva does not resolve shortfalls" in runbook
    assert "Minerva does not finalise PayRuns" in runbook
    assert "Minerva does not approve leave, calculate leave, post LeaveLedger rows, change leave balances, reopen leave requests, resolve shortfalls, finalise PayRuns or mutate operational leave/payroll truth" in runbook
    assert "Diagnostics do not approve, post, reopen, resolve or finalise anything" in runbook
    assert "Do not use operational JSON or Code Evidence as a shortcut" in runbook


def test_public_holidays_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PUBLIC_HOLIDAYS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/PUBLIC_HOLIDAYS_EVALUATION_RUNBOOK.md" in readme
    assert ".\\.venv\\Scripts\\python.exe -m pytest --basetemp .\\.pytest_tmp" in runbook
    assert "samples\\eval\\rich_answer_benchmark.public_holidays.json" in runbook
    assert "scan_public_holidays_corpus_coverage.py" in runbook
    assert "build_public_holidays_answer_gap_report.py" in runbook
    assert "tests\\test_domain_retrieval_plans.py" in runbook
    assert "tests\\test_rich_answer_contract.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "not proof of runtime operational truth" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "public_holiday_source_and_calendar" in runbook
    assert "worksite_state_and_applicability_context" in runbook
    assert "payroll_treatment_and_decision_story" in runbook
    assert "leave_interaction_and_deducts_on_public_holiday" in runbook
    assert "worker_story_admin_queue_and_finalisation" in runbook
    assert "minerva_boundaries_and_non_mutation_guardrails" in runbook
    assert "Public Holidays is the Minerva product-domain explaining governed public holiday source/calendar evidence" in runbook
    assert "PublicHolidayGroup context" in runbook
    assert "worksite/state applicability" in runbook
    assert "Worker Story evidence" in runbook
    assert "Admin Queue / Worker Attention" in runbook
    assert "Finalisation Readiness" in runbook
    assert "Minerva explains Public Holiday handling" in runbook
    assert "Minerva does not calculate public holiday entitlements" in runbook
    assert "Minerva does not decide payroll treatment" in runbook
    assert "Minerva does not post payroll output" in runbook
    assert "Minerva does not approve leave" in runbook
    assert "Minerva does not calculate leave" in runbook
    assert "Minerva does not post LeaveLedger rows" in runbook
    assert "Minerva does not change leave balances" in runbook
    assert "Minerva does not change PublicHolidayGroup configuration" in runbook
    assert "Minerva does not mutate Worksite, EmployeeAppointment, PayRun, LeaveRequest or payroll truth" in runbook
    assert "Minerva does not determine finalisation readiness" in runbook
    assert "Minerva does not finalise PayRuns" in runbook
    assert "diagnostics do not mutate corpus" in runbook
    assert "diagnostics do not call a live LLM" in runbook
    assert "diagnostics do not ingest operational JSON" in runbook
    assert "diagnostics do not connect Code Evidence to answer generation" in runbook
    assert "diagnostics do not prove runtime operational truth" in runbook
    assert "diagnostics do not calculate public holiday entitlements" in runbook
    assert "diagnostics do not decide payroll treatment" in runbook
    assert "diagnostics do not approve or calculate leave" in runbook
    assert "diagnostics do not post LeaveLedger rows" in runbook
    assert "diagnostics do not mutate Worksite/PublicHolidayGroup/EmployeeAppointment/PayRun/LeaveRequest truth" in runbook
    assert "diagnostics do not determine or finalise readiness" in runbook
    assert "When To Improve What" in runbook
    assert "Improve retrieval terms when formal evidence exists but diagnostic coverage is `WEAK`" in runbook
    assert "Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete" in runbook
    assert "Add formal source evidence later when the group is genuinely `MISSING`" in runbook
    assert "Keep existing behavior where coverage and answer quality are acceptable" in runbook
    assert "Do not use operational JSON or Code Evidence as a shortcut" in runbook


def test_rosters_patterns_scheduling_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/ROSTERS_PATTERNS_SCHEDULING_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/ROSTERS_PATTERNS_SCHEDULING_EVALUATION_RUNBOOK.md" in readme
    assert ".\\.venv\\Scripts\\python.exe -m pytest --basetemp .\\.pytest_tmp" in runbook
    assert "samples\\eval\\rich_answer_benchmark.rosters_patterns_scheduling.json" in runbook
    assert "scan_rosters_patterns_scheduling_corpus_coverage.py" in runbook
    assert "build_rosters_patterns_scheduling_answer_gap_report.py" in runbook
    assert "tests\\test_domain_retrieval_plans.py" in runbook
    assert "tests\\test_rich_answer_contract.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "not proof of runtime operational truth" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "roster_pattern_source_and_configuration" in runbook
    assert "appointment_worksite_and_applicability_context" in runbook
    assert "ordinary_hours_leave_basis_and_public_holiday_context" in runbook
    assert "payroll_interpretation_and_worker_story_relationship" in runbook
    assert "admin_queue_finalisation_and_readiness_relationship" in runbook
    assert "minerva_boundaries_and_non_mutation_guardrails" in runbook
    assert "Rosters / Patterns / Scheduling is the Minerva product-domain explaining governed roster, pattern and schedule evidence" in runbook
    assert "expected work context" in runbook
    assert "Pattern / PatternDay / EmployeeAppointmentPattern configuration" in runbook
    assert "appointment/worksite applicability" in runbook
    assert "ordinary-hours and leave-basis context" in runbook
    assert "ObjectTime/source-truth boundaries" in runbook
    assert "Worker Story and payroll evidence relationships" in runbook
    assert "Admin Queue / Worker Attention / Finalisation Readiness" in runbook
    assert "Minerva explains Rosters / Patterns / Scheduling" in runbook
    assert "Minerva does not create rosters" in runbook
    assert "Minerva does not change worker schedules" in runbook
    assert "Minerva does not mutate Pattern, PatternDay or EmployeeAppointmentPattern truth" in runbook
    assert "Minerva does not mutate ObjectTime" in runbook
    assert "Minerva does not calculate payroll" in runbook
    assert "Minerva does not decide entitlements" in runbook
    assert "Minerva does not calculate leave" in runbook
    assert "Minerva does not approve leave" in runbook
    assert "Minerva does not determine finalisation readiness" in runbook
    assert "Minerva does not finalise PayRuns" in runbook
    assert "Minerva does not mutate operational workforce/payroll/leave truth" in runbook
    assert "diagnostics do not mutate corpus" in runbook
    assert "diagnostics do not call a live LLM" in runbook
    assert "diagnostics do not ingest operational JSON" in runbook
    assert "diagnostics do not connect Code Evidence to answer generation" in runbook
    assert "diagnostics do not prove runtime operational truth" in runbook
    assert "diagnostics do not create rosters" in runbook
    assert "diagnostics do not change worker schedules" in runbook
    assert "diagnostics do not mutate Pattern, PatternDay or EmployeeAppointmentPattern truth" in runbook
    assert "diagnostics do not mutate ObjectTime" in runbook
    assert "diagnostics do not calculate payroll" in runbook
    assert "diagnostics do not decide entitlements" in runbook
    assert "diagnostics do not calculate or approve leave" in runbook
    assert "diagnostics do not determine or finalise readiness" in runbook
    assert "diagnostics do not mutate operational workforce/payroll/leave truth" in runbook
    assert "When To Improve What" in runbook
    assert "Improve retrieval terms when formal evidence exists but diagnostic coverage is `WEAK`" in runbook
    assert "Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete" in runbook
    assert "Add formal source evidence later when the group is genuinely `MISSING`" in runbook
    assert "Keep existing behavior where coverage and answer quality are acceptable" in runbook
    assert "Do not use operational JSON or Code Evidence as a shortcut" in runbook


def test_award_positions_classifications_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/AWARD_POSITIONS_CLASSIFICATIONS_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/AWARD_POSITIONS_CLASSIFICATIONS_EVALUATION_RUNBOOK.md" in readme
    assert ".\\.venv\\Scripts\\python.exe -m pytest --basetemp .\\.pytest_tmp" in runbook
    assert "samples\\eval\\rich_answer_benchmark.award_positions_classifications.json" in runbook
    assert "scan_award_positions_classifications_corpus_coverage.py" in runbook
    assert "build_award_positions_classifications_answer_gap_report.py" in runbook
    assert "tests\\test_award_positions_classifications_corpus_coverage.py" in runbook
    assert "tests\\test_award_positions_classifications_answer_gap_report.py" in runbook
    assert "tests\\test_domain_retrieval_plans.py" in runbook
    assert "tests\\test_rich_answer_contract.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "not proof of runtime operational truth" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "award_position_classification_source_and_build" in runbook
    assert "appointment_position_and_worksite_assignment" in runbook
    assert "payroll_interpretation_rate_and_decision_story" in runbook
    assert "comparison_remediation_and_classification_lenses" in runbook
    assert "worker_story_admin_queue_and_readiness_relationship" in runbook
    assert "minerva_boundaries_and_non_mutation_guardrails" in runbook
    assert "Award Positions / Classifications is the Minerva product-domain explaining governed award position/classification evidence" in runbook
    assert "AwardPosition and AwardPositionClass source/build evidence" in runbook
    assert "EmployeeAppointment / WorksitePosition / Position assignment context" in runbook
    assert "classification relationship to RateSource, Rate Story, Decision Story and Payroll Output" in runbook
    assert "comparison/remediation classification lenses" in runbook
    assert "Worker Story / Admin Queue / Worker Attention / Finalisation Readiness" in runbook
    assert "Minerva explains Award Positions / Classifications" in runbook
    assert "Minerva does not classify workers" in runbook
    assert "Minerva does not change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records" in runbook
    assert "Minerva does not select award classes at runtime" in runbook
    assert "Minerva does not interpret awards at runtime" in runbook
    assert "Minerva does not calculate payroll" in runbook
    assert "Minerva does not decide entitlements" in runbook
    assert "Minerva does not mutate payroll output" in runbook
    assert "Minerva does not determine finalisation readiness" in runbook
    assert "Minerva does not finalise PayRuns" in runbook
    assert "Minerva does not mutate operational workforce/payroll/award truth" in runbook
    assert "diagnostics do not mutate corpus" in runbook
    assert "diagnostics do not call a live LLM" in runbook
    assert "diagnostics do not ingest operational JSON" in runbook
    assert "diagnostics do not connect Code Evidence to answer generation" in runbook
    assert "diagnostics do not prove runtime operational truth" in runbook
    assert "diagnostics do not classify workers" in runbook
    assert "diagnostics do not change EmployeeAppointment, WorksitePosition, Position or AwardPositionClass records" in runbook
    assert "diagnostics do not select award classes at runtime" in runbook
    assert "diagnostics do not interpret awards at runtime" in runbook
    assert "diagnostics do not calculate payroll" in runbook
    assert "diagnostics do not decide entitlements" in runbook
    assert "diagnostics do not mutate payroll output" in runbook
    assert "diagnostics do not determine or finalise readiness" in runbook
    assert "diagnostics do not mutate operational workforce/payroll/award truth" in runbook
    assert "When To Improve What" in runbook
    assert "Improve retrieval terms when formal evidence exists but diagnostic coverage is `WEAK`" in runbook
    assert "Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete" in runbook
    assert "Add formal source evidence later when the group is genuinely `MISSING`" in runbook
    assert "Keep existing behavior where coverage and answer quality are acceptable" in runbook
    assert "Do not use operational JSON or Code Evidence as a shortcut" in runbook


def test_payroll_tax_workcover_wic_liability_detail_evaluation_runbook_exists_and_lists_required_guidance():
    runbook_path = Path("docs/PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_EVALUATION_RUNBOOK.md")

    assert runbook_path.exists()

    runbook = runbook_path.read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/PAYROLL_TAX_WORKCOVER_WIC_LIABILITY_DETAIL_EVALUATION_RUNBOOK.md" in readme
    assert ".\\.venv\\Scripts\\python.exe -m pytest --basetemp .\\.pytest_tmp" in runbook
    assert "samples\\eval\\rich_answer_benchmark.payroll_tax_workcover_wic_liability_detail.json" in runbook
    assert "scan_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py" in runbook
    assert "build_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py" in runbook
    assert "tests\\test_payroll_tax_workcover_wic_liability_detail_corpus_coverage.py" in runbook
    assert "tests\\test_payroll_tax_workcover_wic_liability_detail_answer_gap_report.py" in runbook
    assert "tests\\test_domain_retrieval_plans.py" in runbook
    assert "tests\\test_rich_answer_contract.py" in runbook
    assert "diagnostic-only" in runbook
    assert "no corpus mutation" in runbook
    assert "no live LLM" in runbook
    assert "no database schema change" in runbook
    assert "no operational JSON ingestion" in runbook
    assert "no Code Evidence answer integration" in runbook
    assert "no Code Evidence Index answer integration" in runbook
    assert "not proof of runtime operational truth" in runbook
    assert "STRONG" in runbook
    assert "WEAK" in runbook
    assert "MISSING" in runbook
    assert "GOOD" in runbook
    assert "NEEDS_REFINEMENT" in runbook
    assert "INSUFFICIENT_CORPUS" in runbook
    assert "KEEP" in runbook
    assert "IMPROVE_RETRIEVAL_TERMS" in runbook
    assert "IMPROVE_SYNTHESIS" in runbook
    assert "ADD_FORMAL_SOURCE_EVIDENCE_LATER" in runbook
    assert "liability_scope_and_employer_side_boundary" in runbook
    assert "jurisdiction_worksite_and_state_context" in runbook
    assert "governed_basis_membership_and_payroll_bases" in runbook
    assert "rates_sources_and_liability_evidence" in runbook
    assert "worker_story_output_and_finalisation_relationship" in runbook
    assert "minerva_boundaries_and_non_mutation_guardrails" in runbook
    assert "Payroll Tax / WorkCover / WIC Liability Detail is the Minerva product-domain explaining employer-side statutory/liability evidence" in runbook
    assert "jurisdiction/worksite/state context" in runbook
    assert "governed payroll basis membership" in runbook
    assert "liability rate/source evidence" in runbook
    assert "relationship to Payroll Bases, Payroll Output, Worker Story, Gross-to-Net boundaries and Finalisation Readiness" in runbook
    assert "Minerva explains Payroll Tax / WorkCover / WIC liability evidence" in runbook
    assert "Minerva does not calculate payroll tax" in runbook
    assert "Minerva does not calculate WorkCover or WIC liability" in runbook
    assert "Minerva does not lodge or remit statutory returns" in runbook
    assert "Minerva does not decide statutory liability" in runbook
    assert "Minerva does not change employer-liability configuration" in runbook
    assert "Minerva does not change Worksite / State / jurisdiction truth" in runbook
    assert "Minerva does not calculate payroll" in runbook
    assert "Minerva does not mutate payroll output" in runbook
    assert "Minerva does not determine finalisation readiness" in runbook
    assert "Minerva does not finalise PayRuns" in runbook
    assert "Minerva does not mutate operational workforce/payroll/liability truth" in runbook
    assert "diagnostics do not mutate corpus" in runbook
    assert "diagnostics do not call a live LLM" in runbook
    assert "diagnostics do not ingest operational JSON" in runbook
    assert "diagnostics do not connect Code Evidence to answer generation" in runbook
    assert "diagnostics do not prove runtime operational truth" in runbook
    assert "diagnostics do not calculate payroll tax" in runbook
    assert "diagnostics do not calculate WorkCover or WIC liability" in runbook
    assert "diagnostics do not lodge or remit statutory returns" in runbook
    assert "diagnostics do not decide statutory liability" in runbook
    assert "diagnostics do not change employer-liability configuration" in runbook
    assert "diagnostics do not change Worksite / State / jurisdiction truth" in runbook
    assert "diagnostics do not calculate payroll" in runbook
    assert "diagnostics do not mutate payroll output" in runbook
    assert "diagnostics do not determine or finalise readiness" in runbook
    assert "diagnostics do not mutate operational workforce/payroll/liability truth" in runbook
    assert "When To Improve What" in runbook
    assert "Improve retrieval terms when formal evidence exists but diagnostic coverage is `WEAK`" in runbook
    assert "Improve synthesis when coverage is `STRONG` but benchmark or human review shows the answer is incomplete" in runbook
    assert "Add formal source evidence later when the group is genuinely `MISSING`" in runbook
    assert "Keep existing behavior where coverage and answer quality are acceptable" in runbook
    assert "Do not use operational JSON or Code Evidence as a shortcut" in runbook
