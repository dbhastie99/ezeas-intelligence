import json

import pytest

from app.services.golden_question_service import GoldenQuestionError, load_golden_manifest, run_golden_questions
from app.services.ingestion_service import ingest_file_bytes


def _ingest(db_session, file_name, text, source_type="PLATFORM_DOCTRINE", capability_status="DOCTRINE", title=None):
    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name=file_name,
        source_type=source_type,
        capability_status=capability_status,
        title=title,
    )
    assert duplicate is False
    return document


def _manifest(tmp_path, questions):
    path = tmp_path / "golden.json"
    path.write_text(
        json.dumps(
            {
                "name": "Test golden questions",
                "description": "Fixture manifest",
                "questions": questions,
            }
        ),
        encoding="utf-8",
    )
    return path


def test_golden_question_passes_when_source_type_and_phrases_match(db_session, tmp_path):
    _ingest(
        db_session,
        "boundary.txt",
        "LLM Boundary\nMinerva must not calculate payroll and is not payroll calculation truth.",
        source_type="PLATFORM_DOCTRINE",
        title="Platform Doctrine - LLM Boundary",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "boundary",
                "question": "What is Minerva not allowed to do?",
                "expected_source_types": ["PLATFORM_DOCTRINE"],
                "preferred_top_source_type": "PLATFORM_DOCTRINE",
                "expected_phrases_any": ["must not calculate"],
                "expected_answer_phrases_any": ["not allowed to calculate payroll"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["passed"] == 1
    assert result["results"][0]["checks"]["expected_source_type_present"] is True


def test_golden_question_fails_when_preferred_top_source_type_is_wrong(db_session, tmp_path):
    _ingest(
        db_session,
        "developer-direct.txt",
        "Developer Log has direct orchard evidence for this fixture.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Direct Orchard",
    )
    _ingest(
        db_session,
        "platform-weak.txt",
        "Platform Doctrine has unrelated general context.",
        source_type="PLATFORM_DOCTRINE",
        title="Platform Weak",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "preferred-wrong",
                "question": "What has direct orchard evidence?",
                "expected_source_types": ["DEVELOPER_LOG", "PLATFORM_DOCTRINE"],
                "preferred_top_source_type": "PLATFORM_DOCTRINE",
                "expected_phrases_any": ["direct orchard evidence"],
                "expected_answer_phrases_any": ["Minerva is advisory"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    item = result["results"][0]
    assert item["checks"]["preferred_top_source_type"] is False
    assert "Preferred top source type" in item["failure_reasons"][0]


def test_golden_question_passes_when_top_source_type_is_in_preferred_top_source_types_developer_log(db_session, tmp_path):
    _ingest(
        db_session,
        "chat-history-developer.txt",
        "Raw chat history is supporting material with abandoned ideas, corrections and superseded thinking. "
        "It must not override formal doctrine.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - Chat History Authority",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "developer-top-ok",
                "question": "What is the difference between Platform Doctrine and chat history?",
                "expected_source_types": ["DEVELOPER_LOG"],
                "preferred_top_source_types": ["PLATFORM_DOCTRINE", "HARDENING_LOG", "DEVELOPER_LOG"],
                "required_top_source_phrases_any": ["raw chat history", "supporting material", "must not override"],
                "expected_answer_phrases_any": ["chat history"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["results"][0]["top_sources"][0]["source_type"] == "DEVELOPER_LOG"
    assert result["results"][0]["checks"]["preferred_top_source_type"] is True


def test_golden_question_passes_when_top_source_type_is_in_preferred_top_source_types_hardening_log(db_session, tmp_path):
    _ingest(
        db_session,
        "chat-history-hardening.txt",
        "Raw chat history is supporting material. Platform Doctrine, Hardening Logs and Developer Logs outrank raw chat history.",
        source_type="HARDENING_LOG",
        capability_status="OUTSTANDING_HARDENING",
        title="Hardening Log - Chat History Authority",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "hardening-top-ok",
                "question": "Can chat history override doctrine?",
                "expected_source_types": ["HARDENING_LOG"],
                "preferred_top_source_types": ["PLATFORM_DOCTRINE", "HARDENING_LOG", "DEVELOPER_LOG"],
                "required_top_source_phrases_any": ["raw chat history", "supporting material"],
                "expected_answer_phrases_any": ["must not override"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["results"][0]["top_sources"][0]["source_type"] == "HARDENING_LOG"
    assert result["results"][0]["checks"]["preferred_top_source_type"] is True


def test_golden_question_fails_when_top_source_type_not_in_preferred_top_source_types(db_session, tmp_path):
    _ingest(
        db_session,
        "chat-history-other.txt",
        "Raw chat history is supporting material and must not override formal doctrine.",
        source_type="OTHER",
        capability_status="UNKNOWN",
        title="Other Chat History Authority",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "top-not-allowed",
                "question": "Can chat history override doctrine?",
                "expected_source_types": ["OTHER"],
                "preferred_top_source_types": ["PLATFORM_DOCTRINE", "HARDENING_LOG", "DEVELOPER_LOG"],
                "required_top_source_phrases_any": ["raw chat history", "supporting material"],
                "expected_answer_phrases_any": ["must not override"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["top_sources"][0]["source_type"] == "OTHER"
    assert result["results"][0]["checks"]["preferred_top_source_type"] is False


def test_golden_question_backward_compatibility_with_singular_preferred_top_source_type(db_session, tmp_path):
    _ingest(
        db_session,
        "boundary-singular.txt",
        "LLM Boundary\nMinerva must not calculate payroll and is not payroll calculation truth.",
        source_type="PLATFORM_DOCTRINE",
        title="Platform Doctrine - LLM Boundary",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "singular-preferred",
                "question": "What is Minerva not allowed to do?",
                "expected_source_types": ["PLATFORM_DOCTRINE"],
                "preferred_top_source_type": "PLATFORM_DOCTRINE",
                "expected_phrases_any": ["must not calculate"],
                "expected_answer_phrases_any": ["not allowed to calculate payroll"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["results"][0]["checks"]["preferred_top_source_type"] is True


def test_golden_question_fails_when_answer_phrase_is_missing(db_session, tmp_path):
    _ingest(
        db_session,
        "database.txt",
        "Separate Intelligence Store Doctrine\nMinerva uses ezeas-intelligence-db as a separate database.",
        source_type="PLATFORM_DOCTRINE",
        title="Platform Doctrine - Separate Intelligence Store Doctrine",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "missing-answer",
                "question": "Why does Minerva use a separate database?",
                "expected_source_types": ["PLATFORM_DOCTRINE"],
                "expected_phrases_any": ["separate database"],
                "expected_answer_phrases_any": ["this phrase is intentionally absent"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["expected_answer_phrase_any"] is False


def test_golden_question_fails_when_expected_answer_phrases_all_is_missing(db_session, tmp_path):
    _ingest(
        db_session,
        "source-authority.txt",
        "Source Authority Doctrine\nPlatform Doctrine, Hardening Logs and Developer Logs outrank raw chat history.",
        source_type="PLATFORM_DOCTRINE",
        title="Platform Doctrine - Source Authority Doctrine",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "missing-all",
                "question": "Why does source authority matter?",
                "expected_source_types": ["PLATFORM_DOCTRINE"],
                "expected_phrases_any": ["source authority doctrine"],
                "expected_answer_phrases_all": ["Platform Doctrine", "phrase intentionally absent"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["expected_answer_phrases_all"] is False


def test_golden_question_fails_when_forbidden_answer_phrase_appears(db_session, tmp_path):
    _ingest(
        db_session,
        "boundary.txt",
        "LLM Boundary\nMinerva must not calculate payroll and must not finalise PayRuns.",
        source_type="PLATFORM_DOCTRINE",
        title="Platform Doctrine - LLM Boundary",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "forbidden",
                "question": "What is Minerva not allowed to do?",
                "expected_source_types": ["PLATFORM_DOCTRINE"],
                "expected_phrases_any": ["must not calculate"],
                "forbidden_answer_phrases_any": ["not allowed to calculate payroll"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["forbidden_answer_phrases_any"] is False


def test_golden_required_top_source_phrase_any_is_enforced(db_session, tmp_path):
    _ingest(
        db_session,
        "developer-direct.txt",
        "Developer Log: RBAC-Before-LLM Hardening. User permissions must be enforced before evidence reaches the LLM.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - RBAC-Before-LLM Hardening",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "top-source-phrase",
                "question": "What does RBAC-before-LLM mean?",
                "expected_source_types": ["DEVELOPER_LOG"],
                "expected_phrases_any": ["rbac-before-llm hardening"],
                "required_top_source_phrases_any": ["rbac-before-llm hardening"],
                "expected_answer_phrases_any": ["permissions must be checked before evidence"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert result["results"][0]["checks"]["required_top_source_phrase_any"] is True


def test_golden_source_phrase_can_be_satisfied_by_matched_phrases(db_session, tmp_path):
    _ingest(
        db_session,
        "rbac.txt",
        "RBAC-Before-LLM Doctrine\nUser permissions must be enforced before evidence reaches the LLM.",
        source_type="HARDENING_LOG",
        capability_status="OUTSTANDING_HARDENING",
        title="Hardening Doctrine - RBAC-Before-LLM Doctrine",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "rbac",
                "question": "What does RBAC-before-LLM mean?",
                "expected_source_types": ["HARDENING_LOG"],
                "expected_phrases_any": ["rbac-before-llm doctrine"],
                "expected_answer_phrases_any": ["permissions must be checked before evidence"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    assert "rbac-before-llm doctrine" in result["results"][0]["top_sources"][0]["matched_phrases"]


def test_golden_manifest_missing_or_malformed_fails_cleanly(db_session, tmp_path):
    missing_path = tmp_path / "missing.json"
    malformed_path = tmp_path / "malformed.json"
    malformed_path.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(GoldenQuestionError, match="not found"):
        run_golden_questions(db_session, missing_path)

    with pytest.raises(GoldenQuestionError, match="not valid JSON"):
        run_golden_questions(db_session, malformed_path)


def test_annual_leave_golden_manifest_loads_and_validates():
    manifest = load_golden_manifest("samples/eval/golden_questions.annual_leave.json")

    assert manifest["name"] == "Annual Leave and Leave Management golden questions"
    assert len(manifest["questions"]) >= 8
    assert {question["id"] for question in manifest["questions"]} >= {
        "annual-leave-managed",
        "annual-leave-accrual",
        "annual-leave-taken",
        "annual-leave-public-holidays",
        "annual-leave-valuation",
        "annual-leave-worker-story",
        "leave-rule-ui",
        "annual-leave-outstanding",
    }


def test_golden_question_runs_leave_style_terms_against_fixture_document(db_session, tmp_path):
    _ingest(
        db_session,
        "annual-leave-managed.txt",
        "Annual Leave Management Developer Log\n"
        "Annual Leave is managed through LeaveType and LeaveTypeRule rule resolution. "
        "The LeaveLedger records accrual and TAKEN rows in PayRun processing. "
        "Worker Story evidence shows valuation and story output for leave outcomes.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - Annual Leave Management",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "annual-leave-fixture",
                "question": "How is Annual Leave managed in the system?",
                "expected_source_types": ["DEVELOPER_LOG"],
                "expected_source_terms_all": ["LeaveType", "LeaveTypeRule", "LeaveLedger", "accrual", "TAKEN"],
                "expected_answer_terms_all": ["LeaveType", "LeaveLedger", "accrual", "TAKEN", "PayRun"],
                "expected_answer_terms_any": ["Worker Story", "evidence", "valuation"],
                "forbidden_answer_phrases_any": ["Source 1:"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is True
    checks = result["results"][0]["checks"]
    assert checks["expected_source_terms_all"] is True
    assert checks["expected_answer_terms_all"] is True
    assert checks["expected_answer_terms_any"] is True


def test_golden_question_fails_when_expected_answer_terms_all_is_missing(db_session, tmp_path):
    _ingest(
        db_session,
        "annual-leave-accrual.txt",
        "Annual Leave accrual uses interpreter truth and posts LeaveLedger accrual minutes.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - Annual Leave Accrual",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "missing-answer-term",
                "question": "How is Annual Leave accrual calculated?",
                "expected_source_types": ["DEVELOPER_LOG"],
                "expected_answer_terms_all": ["interpreter truth", "LeaveLedger", "missing term"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["expected_answer_terms_all"] is False


def test_golden_question_fails_when_expected_source_terms_all_is_missing(db_session, tmp_path):
    _ingest(
        db_session,
        "annual-leave-public-holiday.txt",
        "Annual Leave public holiday handling uses DeductsOnPublicHoliday and a resolver.",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log - Annual Leave Public Holiday",
    )
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "id": "missing-source-term",
                "question": "How are public holidays handled for Annual Leave?",
                "expected_source_types": ["DEVELOPER_LOG"],
                "expected_source_terms_all": ["public holiday", "DeductsOnPublicHoliday", "missing source term"],
            }
        ],
    )

    result = run_golden_questions(db_session, manifest_path)

    assert result["all_passed"] is False
    assert result["results"][0]["checks"]["expected_source_terms_all"] is False
