import json

import pytest

from app.services.golden_question_service import GoldenQuestionError, run_golden_questions
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
