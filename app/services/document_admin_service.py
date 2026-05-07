from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.enums import normalize_document_status, normalize_source_type
from app.models.knowledge import KnowledgeDocument


def list_documents(
    db: Session,
    source_type: str | None = None,
    status: str | None = None,
    title_contains: str | None = None,
) -> list[KnowledgeDocument]:
    stmt = select(KnowledgeDocument).order_by(KnowledgeDocument.CreatedAt.desc())
    if source_type:
        stmt = stmt.where(KnowledgeDocument.SourceType == normalize_source_type(source_type))
    if status:
        stmt = stmt.where(KnowledgeDocument.DocumentStatus == normalize_document_status(status))
    if title_contains:
        stmt = stmt.where(KnowledgeDocument.Title.contains(title_contains))
    return list(db.scalars(stmt).all())


def set_document_status(db: Session, document_id: str, status: str) -> tuple[KnowledgeDocument, str, str]:
    normalized_status = normalize_document_status(status)
    document = db.get(KnowledgeDocument, document_id)
    if document is None:
        raise ValueError(f"KnowledgeDocument not found: {document_id}")

    previous_status = document.DocumentStatus
    document.DocumentStatus = normalized_status
    document.UpdatedAt = datetime.now(UTC)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document, previous_status, normalized_status
