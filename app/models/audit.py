from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.knowledge import utc_now


class AIInteractionAudit(Base):
    __tablename__ = "AIInteractionAudit"

    AIInteractionAuditId: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    TenantId: Mapped[str | None] = mapped_column(Unicode(100), nullable=True)
    UserId: Mapped[str | None] = mapped_column(Unicode(100), nullable=True)
    KnowledgeChatSessionId: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("KnowledgeChatSession.KnowledgeChatSessionId"),
        nullable=True,
        index=True,
    )
    UserQuestion: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    RetrievedChunkIdsJson: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    RetrievedDocumentIdsJson: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    SourceReferencesJson: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    ModelName: Mapped[str] = mapped_column(Unicode(100), nullable=False, default="STUB_LLM")
    PromptPolicy: Mapped[str] = mapped_column(Unicode(100), nullable=False, default="MINERVA_V0_GROUNDED_READ_ONLY")
    ResponseText: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    CreatedAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
