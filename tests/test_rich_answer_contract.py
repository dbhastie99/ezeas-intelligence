import json
import sys

from app.services.answer_mode_service import AnswerMode, RichAnswerPlan, classify_answer_mode
from app.services.golden_question_service import load_golden_manifest, run_golden_questions
from app.services.ingestion_service import ingest_file_bytes
from scripts import run_golden_questions as run_golden_questions_script


def _manifest(tmp_path, questions):
    path = tmp_path / "rich.json"
    path.write_text(
        json.dumps(
            {
                "name": "Rich answer fixture",
                "description": "Fixture manifest",
                "questions": questions,
            }
        ),
        encoding="utf-8",
    )
    return path


def _ingest(db_session, text: str, title: str = "Developer Log - Annual Leave"):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name="annual-leave.txt",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    return document


def test_answer_mode_classification_examples():
    assert classify_answer_mode("What is Minerva not allowed to do?") == AnswerMode.DOCTRINE.value
    assert classify_answer_mode("How is Annual Leave managed in the system?") == AnswerMode.PRODUCT_DOMAIN.value
    assert classify_answer_mode("Estimate my leave balance") == AnswerMode.WORKER_FACING.value
    assert classify_answer_mode("Why is worker leave balance wrong?") == AnswerMode.TECHNICAL_SUPPORT.value
    assert classify_answer_mode("Which hardening item explains this?") == AnswerMode.DEVELOPER_PLATFORM.value


def test_rich_answer_plan_is_lightweight_internal_structure():
    plan = RichAnswerPlan(
        answer_mode=AnswerMode.PRODUCT_DOMAIN.value,
        direct_summary="Annual Leave is managed through formal leave services.",
        system_operation_points=["LeaveLedger records accrual and TAKEN rows."],
    )

    assert plan.model_dump()["answer_mode"] == "PRODUCT_DOMAIN"
    assert plan.model_dump()["system_operation_points"] == ["LeaveLedger records accrual and TAKEN rows."]


def test_golden_evaluator_checks_required_answer_sections(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave management uses LeaveType and LeaveTypeRule. LeaveLedger records accrual and TAKEN rows. "
        "PayRun processing includes public holiday valuation evidence and Worker Story output. "
        "The Developer Log also records outstanding hardening for valuation.",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "rich-sections",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "required_answer_sections": [
                    "Direct summary",
                    "How the system works",
                    "Current implementation status",
                    "What remains outstanding",
                ],
                "expected_answer_terms_all": ["LeaveType", "LeaveLedger", "PayRun"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["results"][0]["checks"]["answer_mode"] is True
    assert result["results"][0]["checks"]["required_answer_sections"] is True


def test_golden_evaluator_fails_when_required_answer_section_missing(db_session, tmp_path):
    _ingest(db_session, "General evidence about Annual Leave and LeaveLedger.")
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "missing-section",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "required_answer_sections": ["Direct summary", "Intentionally Missing Section"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["required_answer_sections"] is False


def test_golden_evaluator_fails_when_forbidden_answer_pattern_matches(db_session, tmp_path):
    _ingest(
        db_session,
        "Annual Leave management uses LeaveType and LeaveTypeRule. LeaveLedger records accrual and TAKEN rows. "
        "PayRun public holiday valuation evidence is shown in Worker Story.",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "forbidden-pattern",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "expected_source_types": ["DEVELOPER_LOG"],
                "forbidden_answer_patterns_any": ["Direct\\s+summary"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["forbidden_answer_patterns_any"] is False


def test_rich_answer_benchmark_manifest_loads_and_can_be_evaluated(db_session):
    manifest = load_golden_manifest("samples/eval/rich_answer_benchmark.annual_leave.json")

    assert manifest["name"] == "Annual Leave rich-answer benchmark"
    result = run_golden_questions(db_session, "samples/eval/rich_answer_benchmark.annual_leave.json")
    assert result["total"] == 1
    assert result["results"][0]["checks"]["answer_mode"] is True


def test_run_golden_questions_allow_failures_returns_zero(db_session, tmp_path, monkeypatch):
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "allowed-failure",
                "question": "How is Annual Leave managed in the system?",
                "answer_mode": "PRODUCT_DOMAIN",
                "required_answer_sections": ["Missing Section"],
            }
        ],
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["run_golden_questions.py", "--manifest", str(manifest_path), "--allow-failures"],
    )

    assert run_golden_questions_script.main() == 0
