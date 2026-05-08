from datetime import date

from app.services.chunk_inspection_service import inspect_chunks
from app.services.chunk_quality_service import build_chunk_quality_report
from app.services.chunking_service import chunk_text
from app.services.document_metadata_service import extract_document_metadata
from app.services.ingestion_service import ingest_file_bytes


def test_chunking_detects_heading_like_source_sections():
    text = (
        "Developer Log - Additive Entry - 7 May 2026\n"
        "Intro text for the entry.\n"
        "Work Completed\n"
        "Implemented chunk section detection for Minerva knowledge documents.\n"
        "Current State\n"
        "The service is ready for inspection.\n"
    )

    chunks = chunk_text(text, chunk_size=90, overlap=10)

    assert chunks
    assert any(chunk.source_section == "Work Completed" for chunk in chunks)
    assert any(chunk.source_section == "Current State" for chunk in chunks)


def test_ingestion_persists_source_section_for_heading_text(db_session):
    text = (
        "Platform Doctrine\n"
        "Minerva is advisory and read-only.\n"
        "It retrieves evidence and audits answers.\n"
    )

    document, duplicate = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name="platform-doctrine.txt",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
    )

    assert duplicate is False
    chunks = inspect_chunks(db_session, document_id=document.KnowledgeDocumentId)
    assert chunks
    assert chunks[0].SourceSection == "Platform Doctrine"


def test_inspect_chunks_filters_by_title_source_and_start_index(db_session):
    text = "Developer Log\n" + ("Chunk inspection content. " * 80)
    document, _ = ingest_file_bytes(
        db=db_session,
        content=text.encode("utf-8"),
        original_file_name="developer-log.txt",
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title="Developer Log Inspection",
    )

    chunks = inspect_chunks(
        db_session,
        title_contains="Inspection",
        source_type="DEVELOPER_LOG",
        start_index=1,
        limit=2,
    )

    assert chunks
    assert all(chunk.document.KnowledgeDocumentId == document.KnowledgeDocumentId for chunk in chunks)
    assert all(chunk.ChunkIndex >= 1 for chunk in chunks)
    assert len(chunks) <= 2


def test_metadata_extraction_from_developer_log_style_text():
    text = (
        "Developer Log - Additive Entry - 7 May 2026\n"
        "Project: Ezeas Intelligence\n"
        "Phase: Slice 1.8\n"
        "Developer: Minerva Team\n"
        "Work Completed\n"
        "Added metadata extraction.\n"
    )

    metadata = extract_document_metadata(text, "developer-log.txt", source_type="DEVELOPER_LOG")

    assert metadata.inferred_title == "Developer Log - Additive Entry - 7 May 2026"
    assert metadata.detected_document_date == date(2026, 5, 7)
    assert metadata.detected_project == "Ezeas Intelligence"
    assert metadata.detected_phase == "Slice 1.8"
    assert metadata.detected_developer == "Minerva Team"
    assert metadata.source_label == "Developer Log"


def test_metadata_extraction_from_platform_doctrine_and_hardening_additive_entries():
    platform_text = "Platform Doctrine - Additive Entry - 7 May 2026\nProject: Minerva\n"
    hardening_text = "Hardening Log - Additive Entry - 7 May 2026\nPhase: Hardening\n"

    platform_metadata = extract_document_metadata(platform_text, "platform.txt", source_type="PLATFORM_DOCTRINE")
    hardening_metadata = extract_document_metadata(hardening_text, "hardening.txt", source_type="HARDENING_LOG")

    assert platform_metadata.detected_document_date == date(2026, 5, 7)
    assert platform_metadata.source_label == "Platform Doctrine"
    assert hardening_metadata.detected_document_date == date(2026, 5, 7)
    assert hardening_metadata.source_label == "Hardening Log"


def test_chunk_quality_report_from_fixture_documents(db_session):
    ingest_file_bytes(
        db=db_session,
        content=b"Platform Doctrine\nMinerva retrieves and audits knowledge.",
        original_file_name="quality-doctrine.txt",
        source_type="PLATFORM_DOCTRINE",
        capability_status="DOCTRINE",
    )
    ingest_file_bytes(
        db=db_session,
        content=b"No heading content for missing source section.",
        original_file_name="quality-other.txt",
        source_type="OTHER",
        capability_status="UNKNOWN",
    )

    report = build_chunk_quality_report(db_session)

    assert report.total_documents == 2
    assert report.total_chunks >= 2
    assert report.average_chunk_length > 0
    assert report.min_chunk_length > 0
    assert report.max_chunk_length >= report.min_chunk_length
    assert report.chunks_missing_source_section >= 1
    assert report.source_types_summary["PLATFORM_DOCTRINE"] == 1
    assert report.source_types_summary["OTHER"] == 1
    assert len(report.largest_documents_by_chunk_count) == 2
