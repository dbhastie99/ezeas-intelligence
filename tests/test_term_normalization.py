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
