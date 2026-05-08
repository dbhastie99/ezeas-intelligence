from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import normalize_source_type
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument


def inspect_chunks(
    db: Session,
    document_id: str | None = None,
    title_contains: str | None = None,
    source_type: str | None = None,
    start_index: int = 0,
    limit: int = 20,
) -> list[KnowledgeChunk]:
    stmt = select(KnowledgeChunk).options(joinedload(KnowledgeChunk.document)).join(KnowledgeDocument)
    if document_id:
        stmt = stmt.where(KnowledgeChunk.KnowledgeDocumentId == document_id)
    if title_contains:
        stmt = stmt.where(KnowledgeDocument.Title.contains(title_contains))
    if source_type:
        stmt = stmt.where(KnowledgeDocument.SourceType == normalize_source_type(source_type))
    stmt = stmt.where(KnowledgeChunk.ChunkIndex >= start_index)
    stmt = stmt.order_by(KnowledgeDocument.Title, KnowledgeChunk.ChunkIndex).limit(limit)
    return list(db.scalars(stmt).all())
