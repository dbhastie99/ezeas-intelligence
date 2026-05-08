import json

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.chunk_backfill_service import backfill_document_chunks, backfill_manifest
from app.services.document_admin_service import set_document_status
from app.services.document_extraction_service import extract_text
from app.services.ingestion_service import ingest_file_path


def _ingest_and_clear_sections(db_session, tmp_path, file_name: str, text: str, title: str | None = None):
    path = tmp_path / file_name
    path.write_text(text, encoding="utf-8")
    document, duplicate = ingest_file_path(
        db=db_session,
        path=path,
        source_type="DEVELOPER_LOG",
        capability_status="IMPLEMENTED",
        title=title,
    )
    assert duplicate is False
    for chunk in db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=document.KnowledgeDocumentId):
        chunk.SourceSection = None
    db_session.commit()
    return document, path


def _manifest(tmp_path, entries):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "default_source_type": "DEVELOPER_LOG",
                "default_capability_status": "IMPLEMENTED",
                "documents": entries,
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def test_backfill_replaces_chunks_and_preserves_document_id(db_session, tmp_path):
    text = "Developer Log\n" + ("Work Completed\nBackfill source sections into chunks.\n" * 30)
    document, path = _ingest_and_clear_sections(db_session, tmp_path, "developer-log.txt", text)
    original_document_id = document.KnowledgeDocumentId
    old_chunk_ids = {
        chunk.KnowledgeChunkId
        for chunk in db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=original_document_id)
    }

    result = backfill_document_chunks(db_session, original_document_id, path)

    assert result.status == "BACKFILLED"
    assert result.document_id == original_document_id
    assert result.old_missing_source_section_count == result.old_chunk_count
    assert result.new_missing_source_section_count < result.old_missing_source_section_count
    stored = db_session.get(KnowledgeDocument, original_document_id)
    assert stored.KnowledgeDocumentId == original_document_id
    assert stored.ChunkCount == result.new_chunk_count
    assert stored.ExtractedTextLength == len(extract_text(path.read_bytes(), path.name))
    assert stored.UpdatedAt is not None
    new_chunks = db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=original_document_id).all()
    assert {chunk.KnowledgeChunkId for chunk in new_chunks}.isdisjoint(old_chunk_ids)
    assert any(chunk.SourceSection == "Work Completed" for chunk in new_chunks)


def test_backfill_dry_run_does_not_modify_chunks(db_session, tmp_path):
    text = "Developer Log\nWork Completed\nDry run should not replace chunks.\n"
    document, path = _ingest_and_clear_sections(db_session, tmp_path, "dry-run.txt", text)
    old_chunks = db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=document.KnowledgeDocumentId).all()
    old_chunk_ids = [chunk.KnowledgeChunkId for chunk in old_chunks]

    result = backfill_document_chunks(db_session, document.KnowledgeDocumentId, path, dry_run=True)

    assert result.status == "DRY_RUN"
    current_chunks = db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=document.KnowledgeDocumentId).all()
    assert [chunk.KnowledgeChunkId for chunk in current_chunks] == old_chunk_ids
    assert all(chunk.SourceSection is None for chunk in current_chunks)


def test_backfill_skips_superseded_document_by_default(db_session, tmp_path):
    text = "Developer Log\nWork Completed\nSuperseded documents skip by default.\n"
    document, path = _ingest_and_clear_sections(db_session, tmp_path, "superseded.txt", text)
    set_document_status(db_session, document.KnowledgeDocumentId, "SUPERSEDED")

    result = backfill_document_chunks(db_session, document.KnowledgeDocumentId, path)

    assert result.status == "SKIPPED"
    assert "SUPERSEDED" in result.message
    chunks = db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=document.KnowledgeDocumentId).all()
    assert all(chunk.SourceSection is None for chunk in chunks)


def test_manifest_mode_resolves_paths_and_backfills_matching_document(db_session, tmp_path):
    text = "Developer Log\nCurrent State\nManifest mode should match by SHA and backfill.\n"
    document, _ = _ingest_and_clear_sections(db_session, tmp_path, "manifest-doc.txt", text, title="Manifest Doc")
    manifest_path = _manifest(
        tmp_path,
        [
            {
                "path": "manifest-doc.txt",
                "source_type": "DEVELOPER_LOG",
                "capability_status": "IMPLEMENTED",
                "title": "Manifest Doc",
            }
        ],
    )

    summary = backfill_manifest(db_session, manifest_path)

    assert summary["backfilled"] == 1
    assert summary["failed"] == 0
    assert summary["results"][0]["document_id"] == document.KnowledgeDocumentId
    chunks = db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=document.KnowledgeDocumentId).all()
    assert any(chunk.SourceSection == "Current State" for chunk in chunks)


def test_manifest_failure_rolls_back_failed_document_and_continues(db_session, tmp_path, monkeypatch):
    bad_text = "Developer Log\nWork Completed\nThis bad document should roll back.\n"
    good_text = "Developer Log\nCurrent State\nThis good document should still backfill.\n"
    bad_document, _ = _ingest_and_clear_sections(db_session, tmp_path, "bad.txt", bad_text, title="Bad Doc")
    good_document, _ = _ingest_and_clear_sections(db_session, tmp_path, "good.txt", good_text, title="Good Doc")
    manifest_path = _manifest(
        tmp_path,
        [
            {"path": "bad.txt", "source_type": "DEVELOPER_LOG", "capability_status": "IMPLEMENTED", "title": "Bad Doc"},
            {"path": "good.txt", "source_type": "DEVELOPER_LOG", "capability_status": "IMPLEMENTED", "title": "Good Doc"},
        ],
    )

    from app.services import chunk_backfill_service

    original_chunk_text = chunk_backfill_service.chunk_text

    def conditional_chunk_text(text, chunk_size, overlap):
        if "bad document" in text:
            raise RuntimeError("forced chunking failure")
        return original_chunk_text(text, chunk_size, overlap)

    monkeypatch.setattr(chunk_backfill_service, "chunk_text", conditional_chunk_text)

    summary = backfill_manifest(db_session, manifest_path)

    assert summary["backfilled"] == 1
    assert summary["failed"] == 1
    bad_chunks = db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=bad_document.KnowledgeDocumentId).all()
    good_chunks = db_session.query(KnowledgeChunk).filter_by(KnowledgeDocumentId=good_document.KnowledgeDocumentId).all()
    assert bad_chunks
    assert all(chunk.SourceSection is None for chunk in bad_chunks)
    assert any(chunk.SourceSection == "Current State" for chunk in good_chunks)
