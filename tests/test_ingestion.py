from io import BytesIO

from docx import Document

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.document_extraction_service import extract_text_from_docx


def test_txt_ingestion_creates_document_and_chunks(client, db_session):
    content = b"Minerva is advisory. It reads and audits knowledge evidence. " * 20

    response = client.post(
        "/api/v1/ingest/file",
        files={"file": ("doctrine.txt", content, "text/plain")},
        data={"source_type": "PLATFORM_DOCTRINE", "capability_status": "DOCTRINE"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["duplicate"] is False
    assert body["chunk_count"] > 0
    assert body["source_type"] == "PLATFORM_DOCTRINE"

    documents = db_session.query(KnowledgeDocument).all()
    chunks = db_session.query(KnowledgeChunk).all()
    assert len(documents) == 1
    assert len(chunks) == body["chunk_count"]
    assert documents[0].FileSha256 == body["file_sha256"]


def test_duplicate_ingestion_returns_duplicate_and_does_not_create_extra_chunks(client, db_session):
    content = b"Duplicate prevention by SHA256 keeps Minerva ingestion idempotent."

    first = client.post(
        "/api/v1/ingest/file",
        files={"file": ("duplicate.txt", content, "text/plain")},
        data={"source_type": "OTHER"},
    )
    second = client.post(
        "/api/v1/ingest/file",
        files={"file": ("duplicate-renamed.txt", content, "text/plain")},
        data={"source_type": "OTHER"},
    )

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["duplicate"] is True
    assert second.json()["document_id"] == first.json()["document_id"]
    assert db_session.query(KnowledgeDocument).count() == 1
    assert db_session.query(KnowledgeChunk).count() == first.json()["chunk_count"]


def test_docx_extraction_service_reads_generated_docx():
    doc = Document()
    doc.add_paragraph("Minerva extracts DOCX text.")
    doc.add_paragraph("The service remains read-only and advisory.")
    buffer = BytesIO()
    doc.save(buffer)

    text = extract_text_from_docx(buffer.getvalue())

    assert "Minerva extracts DOCX text." in text
    assert "read-only and advisory" in text


def test_json_upload_is_rejected_as_out_of_scope(client):
    response = client.post(
        "/api/v1/ingest/file",
        files={"file": ("evidence.json", b'{"payroll": true}', "application/json")},
        data={"source_type": "OTHER"},
    )

    assert response.status_code == 400
    assert "Operational JSON evidence ingestion is intentionally out of scope" in response.json()["detail"]
