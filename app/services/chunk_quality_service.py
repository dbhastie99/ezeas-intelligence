from collections import Counter
from dataclasses import asdict, dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import normalize_source_type
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument


@dataclass(frozen=True)
class ChunkQualityReport:
    total_documents: int
    total_chunks: int
    average_chunk_length: float
    min_chunk_length: int
    max_chunk_length: int
    chunks_missing_source_section: int
    largest_documents_by_chunk_count: list[dict]
    source_types_summary: dict[str, int]
    chunks_per_document: dict[str, int]

    def model_dump(self) -> dict:
        return asdict(self)


def build_chunk_quality_report(
    db: Session,
    source_type: str | None = None,
    title_contains: str | None = None,
    largest_limit: int = 10,
) -> ChunkQualityReport:
    doc_stmt = select(KnowledgeDocument)
    chunk_stmt = select(KnowledgeChunk).options(joinedload(KnowledgeChunk.document)).join(KnowledgeDocument)
    if source_type:
        normalized_source_type = normalize_source_type(source_type)
        doc_stmt = doc_stmt.where(KnowledgeDocument.SourceType == normalized_source_type)
        chunk_stmt = chunk_stmt.where(KnowledgeDocument.SourceType == normalized_source_type)
    if title_contains:
        doc_stmt = doc_stmt.where(KnowledgeDocument.Title.contains(title_contains))
        chunk_stmt = chunk_stmt.where(KnowledgeDocument.Title.contains(title_contains))

    documents = list(db.scalars(doc_stmt).all())
    chunks = list(db.scalars(chunk_stmt).all())
    lengths = [len(chunk.ChunkText or "") for chunk in chunks]
    chunks_per_document = {document.KnowledgeDocumentId: document.ChunkCount for document in documents}
    largest_documents = sorted(
        [
            {
                "document_id": document.KnowledgeDocumentId,
                "title": document.Title,
                "source_type": document.SourceType,
                "chunk_count": document.ChunkCount,
            }
            for document in documents
        ],
        key=lambda item: item["chunk_count"],
        reverse=True,
    )[:largest_limit]

    return ChunkQualityReport(
        total_documents=len(documents),
        total_chunks=len(chunks),
        average_chunk_length=(sum(lengths) / len(lengths)) if lengths else 0.0,
        min_chunk_length=min(lengths) if lengths else 0,
        max_chunk_length=max(lengths) if lengths else 0,
        chunks_missing_source_section=sum(1 for chunk in chunks if not chunk.SourceSection),
        largest_documents_by_chunk_count=largest_documents,
        source_types_summary=dict(Counter(document.SourceType for document in documents)),
        chunks_per_document=chunks_per_document,
    )
