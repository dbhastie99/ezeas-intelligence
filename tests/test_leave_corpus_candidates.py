import json

from app.services.leave_corpus_candidate_service import (
    build_leave_manifest_from_candidates,
    infer_source_type,
    scan_leave_corpus_candidates,
    score_leave_candidate_text,
)


def test_candidate_scanner_scores_annual_leave_docs_above_unrelated_docs(tmp_path):
    leave_doc = tmp_path / "developer_log_annual_leave.txt"
    leave_doc.write_text(
        "Developer Log\n"
        "Annual Leave uses LeaveType, LeaveTypeRule, LeaveLedger accrual minutes and TAKEN rows in PayRun.",
        encoding="utf-8",
    )
    unrelated_doc = tmp_path / "movement_review.txt"
    unrelated_doc.write_text("Movement review reconciles unrelated totals and dashboard filters.", encoding="utf-8")

    result = scan_leave_corpus_candidates(tmp_path)

    assert result.warnings == []
    assert result.candidates[0].path == str(leave_doc)
    assert result.candidates[0].score > result.candidates[1].score
    assert "Annual Leave" in result.candidates[0].matched_terms
    assert "LeaveLedger" in result.candidates[0].matched_terms


def test_score_detects_key_leave_terms():
    score, matched_terms = score_leave_candidate_text(
        "Annual Leave public holiday handling uses DeductsOnPublicHoliday, Worker Story, "
        "Leave and Accrual Outcome, interpreter truth and no fallback."
    )

    assert score >= 6
    assert {"Annual Leave", "public holiday", "DeductsOnPublicHoliday", "Worker Story"}.issubset(set(matched_terms))


def test_manifest_builder_includes_only_docs_above_min_score(tmp_path):
    source_dir = tmp_path / "candidates"
    source_dir.mkdir()
    included = source_dir / "leave_engine_developer_log.txt"
    included.write_text(
        "Annual Leave LeaveType LeaveTypeRule LeaveLedger accrual TAKEN PayRun Worker Story.",
        encoding="utf-8",
    )
    skipped = source_dir / "unrelated.txt"
    skipped.write_text("This document is about roster display preferences.", encoding="utf-8")
    output = tmp_path / "annual_leave_seed_manifest.generated.json"

    result = build_leave_manifest_from_candidates(source_dir, output, min_score=3)

    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert result["included_count"] == 1
    assert result["skipped_count"] == 1
    assert len(manifest["documents"]) == 1
    assert manifest["documents"][0]["path"] == "candidates/leave_engine_developer_log.txt"
    assert manifest["documents"][0]["source_type"] == "DEVELOPER_LOG"


def test_source_type_inference_from_filename():
    assert infer_source_type("leave_hardening_log.docx") == "HARDENING_LOG"
    assert infer_source_type("platform_doctrine_leave.docx") == "PLATFORM_DOCTRINE"
    assert infer_source_type("leave_doctrine_note.docx") == "OTHER"
    assert infer_source_type("annual_leave_dev_log.docx") == "DEVELOPER_LOG"
    assert infer_source_type("annual_leave_notes.docx") == "DEVELOPER_LOG"


def test_manifest_builder_infers_hardening_source_type_and_status(tmp_path):
    source_dir = tmp_path / "candidates"
    source_dir.mkdir()
    hardening = source_dir / "leave_hardening_log.txt"
    hardening.write_text(
        "Hardening Log\nAnnual Leave valuation basis ordinary rate PayRun Leave Source Model production hardening.",
        encoding="utf-8",
    )
    output = tmp_path / "manifest.json"

    build_leave_manifest_from_candidates(source_dir, output, min_score=3)

    manifest = json.loads(output.read_text(encoding="utf-8"))
    document = manifest["documents"][0]
    assert document["source_type"] == "HARDENING_LOG"
    assert document["capability_status"] == "OUTSTANDING_HARDENING"


def test_scanner_reports_warning_for_malformed_docx(tmp_path):
    bad_docx = tmp_path / "annual_leave_bad.docx"
    bad_docx.write_bytes(b"not a real docx")

    result = scan_leave_corpus_candidates(tmp_path)

    assert result.candidates == []
    assert len(result.warnings) == 1
    assert "annual_leave_bad.docx" in result.warnings[0]
