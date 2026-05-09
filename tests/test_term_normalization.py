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


def test_project_term_normalization_matches_deducts_on_public_holiday_variants():
    assert contains_normalized_term("deductsonpublicholiday is configured", "DeductsOnPublicHoliday")
    assert contains_normalized_term("deducts on public holiday is configured", "DeductsOnPublicHoliday")
    assert contains_normalized_term("DeductsOnPublicHoliday is configured", "deducts on public holiday")


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
