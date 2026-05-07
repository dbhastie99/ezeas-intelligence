import re
from dataclasses import dataclass

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: str
    document_id: str
    chunk_index: int
    chunk_text: str
    title: str | None
    original_file_name: str
    source_type: str
    source_authority: int
    score: float


def tokenize(text: str) -> list[str]:
    return [token for token in re.split(r"\W+", text.lower()) if len(token) > 1]


def retrieve_relevant_chunks(
    db: Session,
    query: str,
    tenant_id: str | None = None,
    top_k: int = 5,
) -> list[RetrievalResult]:
    keywords = tokenize(query)
    if not keywords:
        return []

    stmt = (
        select(KnowledgeChunk)
        .options(joinedload(KnowledgeChunk.document))
        .join(KnowledgeDocument)
        .where(KnowledgeDocument.DocumentStatus == "ACTIVE")
    )
    if tenant_id is not None:
        stmt = stmt.where(or_(KnowledgeDocument.TenantId.is_(None), KnowledgeDocument.TenantId == tenant_id))
    else:
        stmt = stmt.where(KnowledgeDocument.TenantId.is_(None))

    scored: list[RetrievalResult] = []
    for chunk in db.scalars(stmt).all():
        text_lower = chunk.ChunkText.lower()
        overlap = sum(text_lower.count(keyword) for keyword in keywords)
        if overlap <= 0:
            continue
        document = chunk.document
        score = overlap + (document.SourceAuthority / 1000.0)
        scored.append(
            RetrievalResult(
                chunk_id=chunk.KnowledgeChunkId,
                document_id=document.KnowledgeDocumentId,
                chunk_index=chunk.ChunkIndex,
                chunk_text=chunk.ChunkText,
                title=document.Title,
                original_file_name=document.OriginalFileName,
                source_type=document.SourceType,
                source_authority=document.SourceAuthority,
                score=score,
            )
        )
    return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]
