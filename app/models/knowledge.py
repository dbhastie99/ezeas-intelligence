from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class KnowledgeDocument(Base):
    __tablename__ = "KnowledgeDocument"
    __table_args__ = (UniqueConstraint("FileSha256", name="uq_knowledge_document_file_sha256"),)

    KnowledgeDocumentId: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    TenantId: Mapped[str | None] = mapped_column(String(100), nullable=True)
    SourceType: Mapped[str] = mapped_column(String(50), nullable=False)
    SourceAuthority: Mapped[int] = mapped_column(Integer, nullable=False)
    CapabilityStatus: Mapped[str | None] = mapped_column(String(50), nullable=True)
    OriginalFileName: Mapped[str] = mapped_column(String(255), nullable=False)
    StoredFilePath: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    FileExtension: Mapped[str] = mapped_column(String(20), nullable=False)
    FileSha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    Title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    DocumentStatus: Mapped[str] = mapped_column(String(50), nullable=False, default="ACTIVE")
    ExtractedTextLength: Mapped[int] = mapped_column(Integer, nullable=False)
    ChunkCount: Mapped[int] = mapped_column(Integer, nullable=False)
    CreatedAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    UpdatedAt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    chunks: Mapped[list["KnowledgeChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )


class KnowledgeChunk(Base):
    __tablename__ = "KnowledgeChunk"

    KnowledgeChunkId: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    KnowledgeDocumentId: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("KnowledgeDocument.KnowledgeDocumentId"),
        nullable=False,
        index=True,
    )
    ChunkIndex: Mapped[int] = mapped_column(Integer, nullable=False)
    ChunkText: Mapped[str] = mapped_column(Text, nullable=False)
    ChunkHash: Mapped[str] = mapped_column(String(64), nullable=False)
    SourcePage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    SourceSection: Mapped[str | None] = mapped_column(String(255), nullable=True)
    TokenEstimate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CreatedAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    document: Mapped[KnowledgeDocument] = relationship(back_populates="chunks")
