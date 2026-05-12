from app.services.domain_retrieval_plan_service import ANNUAL_LEAVE_MANAGEMENT_PLAN
from app.services.evidence_group_synthesis_service import synthesize_evidence_group
from app.schemas.common import SourceReference
from app.services.golden_question_service import _evaluate_question, run_golden_questions
from app.services.ingestion_service import ingest_file_bytes
from app.services.knowledge_retrieval_service import RetrievalResult
from app.utils.term_normalization import contains_normalized_term


def _group(group_id: str):
    return next(group for group in ANNUAL_LEAVE_MANAGEMENT_PLAN.evidence_groups if group.group_id == group_id)


def _result(text: str, group_id: str) -> RetrievalResult:
    group = _group(group_id)
    return RetrievalResult(
        chunk_id=f"chunk-{group_id}",
        document_id=f"document-{group_id}",
        chunk_index=0,
        chunk_text=text,
        title="Developer Log - Annual Leave",
        original_file_name=f"{group_id}.txt",
        source_type="DEVELOPER_LOG",
        source_authority=80,
        score=50.0,
        matched_tokens=[],
        snippet=text,
        match_ratio=1.0,
        domain_plan_id=ANNUAL_LEAVE_MANAGEMENT_PLAN.plan_id,
        evidence_group_id=group.group_id,
        evidence_group_label=group.label,
    )


def _ingest(db_session, text: str, title: str):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name=f"{title.lower().replace(' ', '-')}.txt",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    return document


def test_project_term_normalization_matches_leaveledger_variants():
    assert contains_normalized_term("leaveledger movement exists", "LeaveLedger")
    assert contains_normalized_term("leave ledger movement exists", "LeaveLedger")
    assert contains_normalized_term("LeaveLedger movement exists", "leave ledger")


def test_project_term_normalization_matches_leavetyperule_variants():
    assert contains_normalized_term("leavetyperule configuration exists", "LeaveTypeRule")
    assert contains_normalized_term("leave type rule configuration exists", "LeaveTypeRule")
    assert contains_normalized_term("LeaveTypeRule configuration exists", "leave type rule")


def test_project_term_normalization_matches_finalisation_readiness_variants():
    assert contains_normalized_term("Finalization Readiness is checked", "Finalisation Readiness")
    assert contains_normalized_term("finalisation is gated", "finalization")
    assert contains_normalized_term("finalized outcome is durable", "finalised outcome")
    assert contains_normalized_term("finalized totals exist", "finalised totals")
    assert contains_normalized_term("warning acknowledgment is required", "warning acknowledgement")
    assert contains_normalized_term("blockers stop finalisation", "blockers")
    assert contains_normalized_term("warnings need review", "warnings")
    assert contains_normalized_term("WorkerAttention is surfaced", "Worker Attention")
    assert contains_normalized_term("Admin Queue has actions", "Admin Queue")
    assert contains_normalized_term("PayrollBasesReadiness is checked", "Payroll Bases readiness")
    assert contains_normalized_term("leave readiness is checked", "leave readiness")
    assert contains_normalized_term("paymentreadiness is checked", "payment readiness")
    assert contains_normalized_term("current effective payroll output exists", "current-effective payroll output")


def test_project_term_normalization_matches_oncosts_employer_liabilities_variants():
    assert contains_normalized_term("Oncosts are employer-side evidence", "On-costs")
    assert contains_normalized_term("on costs are employer-side evidence", "On-costs")
    assert contains_normalized_term("Employer Liability evidence exists", "Employer Liabilities")
    assert contains_normalized_term("superannuation on cost applies", "superannuation on-cost")
    assert contains_normalized_term("SUPER_ONCOST is configured", "SUPER_ONCOST")
    assert contains_normalized_term("PAYROLLTAX_ONCOST is configured", "PAYROLLTAX_ONCOST")
    assert contains_normalized_term("WORKCOVER_ONCOST is configured", "WORKCOVER_ONCOST")
    assert contains_normalized_term("Work Cover is jurisdictional", "WorkCover")
    assert contains_normalized_term("WIC is jurisdictional", "WIC")
    assert contains_normalized_term("Rate Source is date effective", "RateSource")
    assert contains_normalized_term("date effective rates exist", "date-effective rates")
    assert contains_normalized_term("state scoped rate source exists", "state-scoped RateSource")
    assert contains_normalized_term("runtimelocation is resolved", "runtime location")
    assert contains_normalized_term("account wide fallback exists", "account-wide fallback")
    assert contains_normalized_term("Award Rate Type setting exists", "AwardRateType")
    assert contains_normalized_term("Rate Type default exists", "RateType")
    assert contains_normalized_term("governedbasismembership matters", "governed basis membership")


def test_project_term_normalization_matches_payroll_tax_workcover_wic_liability_detail_variants():
    assert contains_normalized_term("Payroll Tax is state scoped", "PayrollTax")
    assert contains_normalized_term("payrolltax is state scoped", "PayrollTax")
    assert contains_normalized_term("Work Cover is jurisdictional", "WorkCover")
    assert contains_normalized_term("Workers Insurance applies", "WIC")
    assert contains_normalized_term("Workers Compensation evidence applies", "WIC")
    assert contains_normalized_term("Employer Liability evidence is separate", "EmployerLiability")
    assert contains_normalized_term("Worksite State context exists", "WorksiteState")
    assert contains_normalized_term("Worksite.StateId context exists", "WorksiteState")
    assert contains_normalized_term("liabilitywages are basis evidence", "liability wages")
    assert contains_normalized_term("taxablewages are basis evidence", "taxable wages")


def test_project_term_normalization_matches_award_build_evidence_variants():
    assert contains_normalized_term("AwardBuild creates configuration", "Award Build")
    assert contains_normalized_term("award evidence is traceable", "Award Evidence")
    assert contains_normalized_term("Award Evidence Set persists sources", "AwardEvidenceSet")
    assert contains_normalized_term("durable award evidence set remains hardening", "Durable AwardEvidenceSet")
    assert contains_normalized_term("Decision Evidence Index exists", "DecisionEvidenceIndex")
    assert contains_normalized_term("Rate Source Evidence Index exists", "RateSourceEvidenceIndex")
    assert contains_normalized_term("Rate Source stores dates", "RateSource")
    assert contains_normalized_term("Rate Type is conceptual", "RateType")
    assert contains_normalized_term("Award Rate Type is scoped", "AwardRateType")
    assert contains_normalized_term("payguideevidence includes cells", "pay guide evidence")
    assert contains_normalized_term("needs configuration is a status", "NEEDS_CONFIGURATION")


def test_project_term_normalization_matches_imports_actuals_variants():
    assert contains_normalized_term("Imports and Actuals are governed", "Imports / Actuals")
    assert contains_normalized_term("imports actuals are governed", "Imports and Actuals")
    assert contains_normalized_term("importedactuals are external", "imported actuals")
    assert contains_normalized_term("payroll actuals are imported", "payroll actuals")
    assert contains_normalized_term("actualslane is separate", "actuals lane")
    assert contains_normalized_term("imported timesheets are mapped", "imported timesheets")
    assert contains_normalized_term("source system mapping exists", "source-system mapping")
    assert contains_normalized_term("paycodemapping exists", "pay code mapping")
    assert contains_normalized_term("Rate Type Mapping exists", "RateType mapping")
    assert contains_normalized_term("Imported Position Classification Map exists", "ImportedPositionClassificationMap")
    assert contains_normalized_term("Object Time Source Truth is preserved", "ObjectTime source truth")
    assert contains_normalized_term("sourcerow is preserved", "source row")
    assert contains_normalized_term("importprovenance is preserved", "import provenance")
    assert contains_normalized_term("import run is audited", "import run")
    assert contains_normalized_term("unmappedactuals need review", "unmapped actuals")


def test_project_term_normalization_matches_objecttime_source_truth_variants():
    assert contains_normalized_term("ObjectTime Source Truth matters", "ObjectTime / Source Truth")
    assert contains_normalized_term("Object Time exists", "ObjectTime")
    assert contains_normalized_term("sourcetruth explains inclusion", "Source Truth")
    assert contains_normalized_term("Source Truth explains inclusion", "SourceTruth")
    assert contains_normalized_term("sourcerow is preserved", "source row")
    assert contains_normalized_term("rawspanhours are not payable", "raw span hours")
    assert contains_normalized_term("span hours are raw", "span hours")
    assert contains_normalized_term("workedhours are interpreted", "worked hours")
    assert contains_normalized_term("Pay Run Inclusion is explained", "PayRun inclusion")
    assert contains_normalized_term("current effective output is connected", "current-effective output")
    assert contains_normalized_term("dirtycontact needs review", "dirty contact")
    assert contains_normalized_term("reprocessing is required", "reprocessing")
    assert contains_normalized_term("correctionaudit is preserved", "correction audit")


def test_project_term_normalization_matches_contacts_employee_appointments_variants():
    assert contains_normalized_term("Contacts and Employee Appointments are governed", "Contacts / Employee Appointments")
    assert contains_normalized_term("Contact identity exists", "Contact")
    assert contains_normalized_term("Employee Appointment carries assignment context", "EmployeeAppointment")
    assert contains_normalized_term("EmployeeAppointment carries assignment context", "Employee Appointment")
    assert contains_normalized_term("contacthistory is surfaced", "Contact history")
    assert contains_normalized_term("Pay Run Admission depends on appointment context", "PayRun admission")
    assert contains_normalized_term("Worksite Position is configured", "WorksitePosition")
    assert contains_normalized_term("Award Position Class is configured", "AwardPositionClass")
    assert contains_normalized_term("classificationlens evidence exists", "classification lens")
    assert contains_normalized_term("workerreadiness is contact-level", "worker readiness")
    assert contains_normalized_term("Worker Attention is surfaced", "worker attention")


def test_project_term_normalization_matches_process_period_payrun_lifecycle_variants():
    assert contains_normalized_term(
        "Process Periods and PayRun Lifecycle are governed",
        "Process Periods / PayRun Lifecycle",
    )
    assert contains_normalized_term("Process Period is open", "ProcessPeriod")
    assert contains_normalized_term("ProcessPeriod is open", "Process Period")
    assert contains_normalized_term("Process Period Group defines calendar policy", "ProcessPeriodGroup")
    assert contains_normalized_term("ProcessPeriodGroup defines payment policy", "Process Period Group")
    assert contains_normalized_term("Pay Run Lifecycle is governed", "PayRun lifecycle")
    assert contains_normalized_term("Pay Run Contact tracks worker participation", "PayRunContact")
    assert contains_normalized_term("Run Type is separate", "RunType")
    assert contains_normalized_term("Run Purpose is separate", "RunPurpose")
    assert contains_normalized_term("regular pay run is distinct", "regular PayRun")
    assert contains_normalized_term("supplementary pay run is distinct", "supplementary PayRun")
    assert contains_normalized_term("retro pay run is distinct", "retro PayRun")
    assert contains_normalized_term("Payment Date is governed", "PaymentDate")
    assert contains_normalized_term("paymentdate is governed", "payment date")
    assert contains_normalized_term("close rolls forward", "close rolls forward")
    assert contains_normalized_term("current effective output is guarded", "current-effective output")
    assert contains_normalized_term("Period Close is downstream", "period close")


def test_project_term_normalization_matches_costing_gl_consequence_variants():
    assert contains_normalized_term("Costing and GL Consequence Evidence is downstream", "Costing / GL Consequence")
    assert contains_normalized_term("Costing GL Consequence Evidence is downstream", "Costing / GL Consequence Evidence")
    assert contains_normalized_term("costing evidence exists", "Costing")
    assert contains_normalized_term("GL Consequence is tracked", "GL consequence")
    assert contains_normalized_term("GL consequences are tracked", "GL consequences")
    assert contains_normalized_term("financialconsequence is tracked", "financial consequence")
    assert contains_normalized_term("financial consequences are tracked", "financial consequences")
    assert contains_normalized_term("obligation writeoff needs treatment", "obligation write-off")
    assert contains_normalized_term("provisionreduction needs audit", "provision reduction")
    assert contains_normalized_term("out of pay record exists", "out-of-pay")
    assert contains_normalized_term("remediationvariance needs downstream treatment", "remediation variance")
    assert contains_normalized_term("variance line is typed", "variance line")
    assert contains_normalized_term("leave valuation can flow", "leave valuation")
    assert contains_normalized_term("Employer Liabilities are downstream", "employer liabilities")
    assert contains_normalized_term("on costs are downstream", "on-costs")
    assert contains_normalized_term("finalised payroll outcome exists", "finalised payroll outcome")
    assert contains_normalized_term("payment execution is downstream", "payment execution")


def test_project_term_normalization_matches_worker_attention_issue_resolution_variants():
    assert contains_normalized_term("WorkerAttention issue evidence", "Worker Attention")
    assert contains_normalized_term("Worker Attention Centre", "Worker Attention Centre")
    assert contains_normalized_term("WorkerIssue severity", "Worker issue")
    assert contains_normalized_term("deterministic fix links", "deterministic fix link")
    assert contains_normalized_term("PayRunContact dirty", "PayRunContact dirty")


def test_project_term_normalization_matches_gross_to_net_variants():
    assert contains_normalized_term("Gross to Net explains outcomes", "Gross-to-Net")
    assert contains_normalized_term("GrossToNet explains outcomes", "Gross to Net")
    assert contains_normalized_term("gross earnings are captured", "gross earnings")
    assert contains_normalized_term("grosspay is captured", "gross pay")
    assert contains_normalized_term("netpay is ready", "net pay")
    assert contains_normalized_term("tax withholding is explained", "tax withholding")
    assert contains_normalized_term("withholding is explained", "withholding")


def test_project_term_normalization_matches_rate_source_rate_story_variants():
    assert contains_normalized_term("Rate Source Rate Story explains selected rates", "RateSource / Rate Story")
    assert contains_normalized_term("RateStory explains rate evidence", "Rate Story")
    assert contains_normalized_term("Rate Source Evidence Index exists", "RateSourceEvidenceIndex")
    assert contains_normalized_term("payguiderateevidence exists", "pay guide rate evidence")
    assert contains_normalized_term("rateamount is explained", "rate amount")
    assert contains_normalized_term("selectedrate is explained", "selected rate")
    assert contains_normalized_term("date effective rate applies", "date-effective rate")
    assert contains_normalized_term("awardrate applies", "award rate")
    assert contains_normalized_term("account rate applies", "account rate")
    assert contains_normalized_term("classrate applies", "class rate")


def test_project_term_normalization_matches_decision_story_variants():
    assert contains_normalized_term("DecisionStory explains decisions", "Decision Story")
    assert contains_normalized_term("Decision Evidence Index exists", "DecisionEvidenceIndex")
    assert contains_normalized_term("treatmentselection explains the line", "treatment selection")
    assert contains_normalized_term("entitlementdecision is explained", "entitlement decision")
    assert contains_normalized_term("payrolldecision is explained", "payroll decision")
    assert contains_normalized_term("why a line exists", "why the line exists")
    assert contains_normalized_term("whyatreatmentwasselected is recorded", "why a treatment was selected")
    assert contains_normalized_term("allowancedecision is recorded", "allowance decision")
    assert contains_normalized_term("penalty decision is recorded", "penalty decision")
    assert contains_normalized_term("overtimedecision is recorded", "overtime decision")
    assert contains_normalized_term("shiftdecision is recorded", "shift decision")
    assert contains_normalized_term("publicholidaydecision is recorded", "public holiday decision")
    assert contains_normalized_term("breaktreatment is recorded", "break treatment")
    assert contains_normalized_term("missedbreak is recorded", "missed break")
    assert contains_normalized_term("minimumengagement is recorded", "minimum engagement")


def test_project_term_normalization_matches_payroll_output_variants():
    assert contains_normalized_term("Payroll Output explains calculated results", "Payroll Output")
    assert contains_normalized_term("PayRunOutput exists", "PayRun Output")
    assert contains_normalized_term("Process Period Output is a lens", "Process Period Output")
    assert contains_normalized_term("RunOutput is a lens", "Run Output")
    assert contains_normalized_term("current effective payroll output is current truth", "current-effective payroll output")
    assert contains_normalized_term("calculatedpayrolloutput is evidence", "calculated payroll output")
    assert contains_normalized_term("payrollline is explained", "payroll line")
    assert contains_normalized_term("output line is explained", "output line")
    assert contains_normalized_term("workeroutput is explained", "worker output")
    assert contains_normalized_term("PayRun totals are captured", "PayRun totals")
    assert contains_normalized_term("payrollresult is captured", "payroll result")
    assert contains_normalized_term("finalized outcome truth is captured", "finalised outcome truth")
    assert contains_normalized_term("CalcInterpreterRun exists", "CalcInterpreterRun")
    assert contains_normalized_term("CalcInterpreterLine exists", "CalcInterpreterLine")


def test_project_term_normalization_matches_contact_payroll_history_variants():
    assert contains_normalized_term("ContactPayrollHistory explains history", "Contact Payroll History")
    assert contains_normalized_term("payrollhistory is visible", "Payroll history")
    assert contains_normalized_term("worker payroll history is visible", "worker payroll history")
    assert contains_normalized_term("contact level payroll history is visible", "contact-level payroll history")
    assert contains_normalized_term("historicalpayrolloutput is visible", "historical payroll output")
    assert contains_normalized_term("PayRun participation is visible", "PayRun participation")
    assert contains_normalized_term("workerhistory is visible", "worker history")
    assert contains_normalized_term("payroll outcome history is visible", "payroll outcome history")
    assert contains_normalized_term("contactdeductions are visible", "contact deductions")
    assert contains_normalized_term("contact obligations are visible", "contact obligations")
    assert contains_normalized_term("contacttax is visible", "contact tax")
    assert contains_normalized_term("contact payment is visible", "contact payment")
    assert contains_normalized_term("leavehistory is visible", "leave history")
    assert contains_normalized_term("accrual history is visible", "accrual history")
    assert contains_normalized_term("retrohistory is visible", "retro history")
    assert contains_normalized_term("correction history is visible", "correction history")


def test_project_term_normalization_matches_leave_accrual_processing_variants():
    assert contains_normalized_term("Leave Accrual evidence exists", "Leave Accrual")
    assert contains_normalized_term("LeaveProcessing is queued", "Leave Processing")
    assert contains_normalized_term("leave source model remains hardening", "Leave Source Model")
    assert contains_normalized_term("leavevaluationbasis is mandatory", "leave valuation basis")
    assert contains_normalized_term("accrualbasis is PER_HOUR", "accrual basis")
    assert contains_normalized_term("accrualability is award rate type first", "accrualability")
    assert contains_normalized_term("Calc Interpreter Line exists", "CalcInterpreterLine")
    assert contains_normalized_term("current effective payroll output exists", "current-effective payroll output")
    assert contains_normalized_term("Leave Process Run exists", "LeaveProcessRun")
    assert contains_normalized_term("takenleave needs valuation", "TAKEN leave")
    assert contains_normalized_term("per hour accrual exists", "PER_HOUR")


def test_project_term_normalization_matches_leave_requests_workflow_variants():
    assert contains_normalized_term("LeaveRequest is visible", "LeaveRequest")
    assert contains_normalized_term("Leave Requests are visible", "Leave Requests")
    assert contains_normalized_term("leaveworkflow is visible", "leave workflow")
    assert contains_normalized_term("leave submission is visible", "leave submission")
    assert contains_normalized_term("submitleave is visible", "submit leave")
    assert contains_normalized_term("approve leave is visible", "approve leave")
    assert contains_normalized_term("rejectleave is visible", "reject leave")
    assert contains_normalized_term("reopen leave is visible", "reopen leave")
    assert contains_normalized_term("leavestatus is visible", "leave status")
    assert contains_normalized_term("IdempotencyKey is visible", "IdempotencyKey")
    assert contains_normalized_term("leaveoverlap is visible", "leave overlap")
    assert contains_normalized_term("shortfall substitution is visible", "shortfall substitution")
    assert contains_normalized_term("takenleave needs valuation", "TAKEN leave")
    assert contains_normalized_term("leavevaluation is visible", "leave valuation")
    assert contains_normalized_term("LeaveLedger exists", "LeaveLedger")
    assert contains_normalized_term("leaveposting is visible", "leave posting")
    assert contains_normalized_term("leave request payment exists", "leave request payment")
    assert contains_normalized_term("leave balance is visible", "leave balance")
    assert contains_normalized_term("leaverequestpreview is visible", "leave request preview")


def test_project_term_normalization_matches_leave_source_model_variants():
    assert contains_normalized_term("LeaveSourceModel remains planned", "Leave Source Model")
    assert contains_normalized_term("leave source truth determines applicability", "leave source truth")
    assert contains_normalized_term("leaveapplicability is governed", "leave applicability")
    assert contains_normalized_term("Leave Type Rule is policy content", "LeaveTypeRule")
    assert contains_normalized_term("leavereadiness is checked", "leave readiness")
    assert contains_normalized_term("missingleaveoutput is investigated", "missing leave output")
    assert contains_normalized_term("contactscope must be clear", "Contact scope")
    assert contains_normalized_term("Employee Appointment Scope must be clear", "EmployeeAppointment scope")
    assert contains_normalized_term("appointment aware leave is needed", "appointment-aware leave")
    assert contains_normalized_term("finalapplicabilitytruth is separate", "final applicability truth")


def test_project_term_normalization_matches_deducts_on_public_holiday_variants():
    assert contains_normalized_term("PublicHoliday is configured", "Public Holiday")
    assert contains_normalized_term("Public Holiday Group is selected", "PublicHolidayGroup")
    assert contains_normalized_term("public holidays are governed", "Public Holidays")
    assert contains_normalized_term("observedday is configured", "observed day")
    assert contains_normalized_term("PH calendar evidence exists", "PH")
    assert contains_normalized_term("deductsonpublicholiday is configured", "DeductsOnPublicHoliday")
    assert contains_normalized_term("deducts on public holiday is configured", "DeductsOnPublicHoliday")
    assert contains_normalized_term("DeductsOnPublicHoliday is configured", "deducts on public holiday")


def test_project_term_normalization_matches_roster_pattern_scheduling_variants():
    assert contains_normalized_term("rosters patterns scheduling evidence exists", "Rosters / Patterns / Scheduling")
    assert contains_normalized_term("Roster evidence exists", "Rosters")
    assert contains_normalized_term("Patterns are configured", "Pattern")
    assert contains_normalized_term("Pattern Day is configured", "PatternDay")
    assert contains_normalized_term("patternday is configured", "Pattern Day")
    assert contains_normalized_term("Employee Appointment Pattern is configured", "EmployeeAppointmentPattern")
    assert contains_normalized_term("employeeappointmentpattern is configured", "Employee Appointment Pattern")
    assert contains_normalized_term("work schedule evidence exists", "Schedule")
    assert contains_normalized_term("ordinary-hours are expected", "ordinary hours")
    assert contains_normalized_term("ordinary hours are expected", "ordinary-hours")


def test_project_term_normalization_matches_award_positions_classifications_variants():
    assert contains_normalized_term("award positions classifications evidence exists", "Award Positions / Classifications")
    assert contains_normalized_term("Award Position is configured", "AwardPosition")
    assert contains_normalized_term("awardposition is configured", "Award Position")
    assert contains_normalized_term("Award Position Class is configured", "AwardPositionClass")
    assert contains_normalized_term("awardpositionclass is configured", "Award Position Class")
    assert contains_normalized_term("Position Class is configured", "PositionClass")
    assert contains_normalized_term("positionclass is configured", "Position Class")
    assert contains_normalized_term("Employee Appointment is assigned", "EmployeeAppointment")
    assert contains_normalized_term("Worksite Position is assigned", "WorksitePosition")
    assert contains_normalized_term("classification evidence exists", "class")
    assert contains_normalized_term("level evidence exists", "classification")


def test_project_term_normalization_matches_worker_story_variants():
    assert contains_normalized_term("workerstory explains evidence", "Worker Story")
    assert contains_normalized_term("Worker Story explains evidence", "WorkerStory")
    assert contains_normalized_term("source truth input exists", "SourceTruth")
    assert contains_normalized_term("Decision Evidence Index exists", "DecisionEvidenceIndex")
    assert contains_normalized_term("RateSourceEvidenceIndex exists", "Rate Source Evidence Index")
    assert contains_normalized_term("current effective payroll output exists", "current-effective")
    assert contains_normalized_term("Object Time grouping exists", "ObjectTime")
    assert contains_normalized_term("Pay Run evidence exists", "PayRun")


def test_project_term_normalization_matches_payroll_bases_variants():
    assert contains_normalized_term("Payroll Bases and Totals evidence exists", "Payroll Bases & Totals")
    assert contains_normalized_term("Payroll Bases & Totals evidence exists", "Payroll Bases and Totals")
    assert contains_normalized_term("payrollbucketresult rows exist", "Payroll Bucket Result")
    assert contains_normalized_term("Payroll Bucket Result rows exist", "PayrollBucketResult")
    assert contains_normalized_term("payrollbucketdefinition exists", "Payroll Bucket Definition")
    assert contains_normalized_term("Payroll Bucket Definition exists", "PayrollBucketDefinition")


def test_project_term_normalization_matches_payrun_admin_queue_variants():
    assert contains_normalized_term("PayRun Admin Queue shows actions", "Admin Queue")
    assert contains_normalized_term("PayRun Queue shows actions", "PayRun Admin Queue")
    assert contains_normalized_term("WorkerAttention exists", "Worker Attention")
    assert contains_normalized_term("dirtycontacts need review", "dirty contacts")
    assert contains_normalized_term("finalization readiness is checked", "finalisation readiness")
    assert contains_normalized_term("AssuranceSnapshot exists", "Assurance Snapshot")
    assert contains_normalized_term("Command Center opens review", "Command Centre")
    assert contains_normalized_term("MovementReview opens review", "Movement Review")


def test_project_term_normalization_matches_movement_review_variants():
    assert contains_normalized_term("Payroll Movement Review explains variance", "Movement Review")
    assert contains_normalized_term("review worthy movement exists", "review-worthy")
    assert contains_normalized_term("comparableperiod is available", "comparable period")
    assert contains_normalized_term("rollingaverage is shown", "rolling average")
    assert contains_normalized_term("trend only evidence exists", "trend-only")


def test_project_term_normalization_matches_comparison_remediation_variants():
    assert contains_normalized_term("Comparison Remediation evidence exists", "Comparison / Remediation")
    assert contains_normalized_term("Award Comparison policy exists", "Award Comparison")
    assert contains_normalized_term("PayRun Comparison Run exists", "PayRunComparisonRun")
    assert contains_normalized_term("PayRunComparisonLine exists", "PayRun Comparison Line")
    assert contains_normalized_term("PayRun Variance Line exists", "PayRunVarianceLine")
    assert contains_normalized_term("Award Comparison Policy exists", "AwardComparisonPolicy")
    assert contains_normalized_term("comparatoraward evidence exists", "comparator award")
    assert contains_normalized_term("importedactuals are separate", "imported actuals")
    assert contains_normalized_term("actualslane is separate", "actuals lane")
    assert contains_normalized_term("remediation top up exists", "remediation top-up")
    assert contains_normalized_term("Award Position Class Comparison Map exists", "AwardPositionClassComparisonMap")
    assert contains_normalized_term(
        "Employee Appointment Award Class Assignment exists",
        "EmployeeAppointmentAwardClassAssignment",
    )
    assert contains_normalized_term("Object Time Classification Resolution exists", "ObjectTimeClassificationResolution")


def test_project_term_normalization_matches_tax_payg_variants():
    assert contains_normalized_term("Tax PAYG evidence exists", "Tax / PAYG")
    assert contains_normalized_term("PAYG withholding exists", "PAYG withholding")
    assert contains_normalized_term("Tax Story explains withholding", "TaxStory")
    assert contains_normalized_term("taxablebasis is governed", "taxable basis")
    assert contains_normalized_term("taxableearnings are aligned", "taxable earnings")
    assert contains_normalized_term("worker tax declaration exists", "worker tax declaration")
    assert contains_normalized_term("withholdinginstruction exists", "withholding instruction")
    assert contains_normalized_term("Process Period Payment Date exists", "ProcessPeriod PaymentDate")
    assert contains_normalized_term("paymentdate drives tax", "payment date")
    assert contains_normalized_term("gross to net is shown", "gross-to-net")
    assert contains_normalized_term("finalized totals exist", "finalised totals")
    assert contains_normalized_term("supplementaryincrementalpayg exists", "supplementary incremental PAYG")


def test_project_term_normalization_matches_deductions_obligations_variants():
    assert contains_normalized_term("Deductions and Obligations evidence exists", "Deductions / Obligations")
    assert contains_normalized_term("Library Deduction Template exists", "LibraryDeductionTemplate")
    assert contains_normalized_term("AccountDeductionTemplate exists", "Account Deduction Template")
    assert contains_normalized_term("Contact Payroll Deduction exists", "ContactPayrollDeduction")
    assert contains_normalized_term("PayRunDeductionApplication exists", "PayRun Deduction Application")
    assert contains_normalized_term("Contact Payroll Obligation exists", "ContactPayrollObligation")
    assert contains_normalized_term("ContactPayrollObligationLedger exists", "Contact Payroll Obligation Ledger")
    assert contains_normalized_term("supplementarydeductionmemory exists", "supplementary deduction memory")
    assert contains_normalized_term("reducing balance recovery exists", "reducing-balance recovery")
    assert contains_normalized_term("carry forward is visible", "carry-forward")
    assert contains_normalized_term("negativenetpay is governed", "negative net pay")


def test_project_term_normalization_matches_retro_replay_variants():
    assert contains_normalized_term("Retro Replay evidence exists", "Retro / Replay")
    assert contains_normalized_term("retro pay run exists", "retro PayRun")
    assert contains_normalized_term("supplementarypayrun exists", "supplementary PayRun")
    assert contains_normalized_term("attributedperiod is preserved", "attributed period")
    assert contains_normalized_term("paid period is preserved", "paid period")
    assert contains_normalized_term("finalized outcome memory exists", "finalised outcome memory")
    assert contains_normalized_term("current effective truth is distinct", "current-effective truth")
    assert contains_normalized_term("dependencydetection creates candidates", "dependency detection")
    assert contains_normalized_term("bucket rebuild needs governance", "bucket rebuild")
    assert contains_normalized_term("historicalbucketevidence exists", "historical bucket evidence")
    assert contains_normalized_term("correction replay is auditable", "correction/replay")


def test_project_term_normalization_matches_payment_execution_remittance_variants():
    assert contains_normalized_term("Payment Execution and Remittance evidence exists", "Payment Execution / Remittance")
    assert contains_normalized_term("GenerateBankFile is available", "Generate Bank File")
    assert contains_normalized_term("Bank File generation is reviewed", "BankFile")
    assert contains_normalized_term("PeriodClose is blocked", "Period Close")
    assert contains_normalized_term("paymentallocation exists", "payment allocation")
    assert contains_normalized_term("paymentdestination is missing", "payment destination")
    assert contains_normalized_term("bankallocation is split", "bank allocation")
    assert contains_normalized_term("workernetpay is ready", "worker net pay")
    assert contains_normalized_term("third party remittance exists", "third-party remittance")
    assert contains_normalized_term("remittancereconciliation is needed", "remittance reconciliation")
    assert contains_normalized_term("paymentfile is generated", "payment file")
    assert contains_normalized_term("obligation write off needs coding", "obligation write-off")


def test_golden_source_terms_all_passes_for_normalized_variants(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave leavetype rule setup posts leaveledger minutes.",
        "Developer Log - Normalized Source Terms",
    )
    manifest = tmp_path / "source_terms.json"
    manifest.write_text(
        """
        {
          "name": "Source terms",
          "questions": [
            {
              "id": "source-terms",
              "question": "How is Annual Leave managed in the system?",
              "expected_source_types": ["DEVELOPER_LOG"],
              "expected_source_terms_all": ["LeaveTypeRule", "LeaveLedger"]
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    result = run_golden_questions(db_session, manifest)

    assert result["all_passed"] is True
    assert result["results"][0]["checks"]["expected_source_terms_all"] is True


def test_golden_answer_terms_all_passes_for_normalized_variants(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave accrual posts leaveledger minutes through Pay Run context.",
        "Developer Log - Normalized Answer Terms",
    )
    manifest = tmp_path / "answer_terms.json"
    manifest.write_text(
        """
        {
          "name": "Answer terms",
          "questions": [
            {
              "id": "answer-terms",
              "question": "How is Annual Leave managed in the system?",
              "answer_mode": "PRODUCT_DOMAIN",
              "expected_source_types": ["DEVELOPER_LOG"],
              "expected_answer_terms_all": ["LeaveLedger", "PayRun"]
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    result = run_golden_questions(db_session, manifest)

    assert result["all_passed"] is True
    assert result["results"][0]["checks"]["expected_answer_terms_all"] is True


def test_evidence_group_synthesis_detects_normalized_project_terms():
    summary = synthesize_evidence_group(
        _group("taken"),
        [
            _result(
                "Annual Leave TAKEN posts leave ledger minutes. Public holiday handling uses deducts on public holiday.",
                "taken",
            )
        ],
    )

    assert summary.is_weak is False
    assert "LeaveLedger" in summary.detected_terms
    assert "DeductsOnPublicHoliday" in summary.detected_terms
    assert "public holiday deduction controlled by DeductsOnPublicHoliday" in summary.sentence


def test_golden_source_terms_all_passes_when_terms_appear_only_in_matched_tokens():
    source = SourceReference(
        document_id="doc-1",
        chunk_id="chunk-1",
        original_file_name="annual-leave.txt",
        source_type="DEVELOPER_LOG",
        source_authority=80,
        chunk_index=0,
        matched_tokens=["annual", "leave", "leaveledger"],
    )

    result = _evaluate_question(
        {
            "id": "matched-token-source-terms",
            "question": "How is Annual Leave managed in the system?",
            "expected_source_terms_all": ["Annual Leave", "LeaveLedger"],
        },
        answer="No answer terms needed for this check.",
        sources=[source],
    )

    assert result["passed"] is True
    assert result["checks"]["expected_source_terms_all"] is True


def test_golden_source_terms_all_fails_when_terms_are_absent_from_all_source_metadata():
    source = SourceReference(
        document_id="doc-1",
        chunk_id="chunk-1",
        original_file_name="annual-leave.txt",
        source_type="DEVELOPER_LOG",
        source_authority=80,
        chunk_index=0,
        snippet="Annual Leave evidence is partial.",
        matched_tokens=["annual", "leave"],
        title="Developer Log - Partial Leave Evidence",
    )

    result = _evaluate_question(
        {
            "id": "missing-source-token-terms",
            "question": "How is Annual Leave managed in the system?",
            "expected_source_terms_all": ["Annual Leave", "LeaveLedger"],
        },
        answer="No answer terms needed for this check.",
        sources=[source],
    )

    assert result["passed"] is False
    assert result["checks"]["expected_source_terms_all"] is False


def test_golden_required_top_source_phrase_can_use_matched_tokens_for_project_terms():
    source = SourceReference(
        document_id="doc-1",
        chunk_id="chunk-1",
        original_file_name="annual-leave.txt",
        source_type="DEVELOPER_LOG",
        source_authority=80,
        chunk_index=0,
        matched_tokens=["leaveledger"],
        evidence_group_label="Accrual basis and ledger posting",
    )

    result = _evaluate_question(
        {
            "id": "top-source-token-phrase",
            "question": "How is Annual Leave managed in the system?",
            "required_top_source_phrases_any": ["LeaveLedger"],
        },
        answer="No answer terms needed for this check.",
        sources=[source],
    )

    assert result["passed"] is True
    assert result["checks"]["required_top_source_phrase_any"] is True
