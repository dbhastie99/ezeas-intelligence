from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.knowledge import utc_now


class KnowledgeChatSession(Base):
    __tablename__ = "KnowledgeChatSession"

    KnowledgeChatSessionId: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    TenantId: Mapped[str | None] = mapped_column(Unicode(100), nullable=True)
    UserId: Mapped[str | None] = mapped_column(Unicode(100), nullable=True)
    Title: Mapped[str | None] = mapped_column(Unicode(255), nullable=True)
    CreatedAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    UpdatedAt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    messages: Mapped[list["KnowledgeChatMessage"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class KnowledgeChatMessage(Base):
    __tablename__ = "KnowledgeChatMessage"

    KnowledgeChatMessageId: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    KnowledgeChatSessionId: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("KnowledgeChatSession.KnowledgeChatSessionId"),
        nullable=False,
        index=True,
    )
    Role: Mapped[str] = mapped_column(Unicode(20), nullable=False)
    Content: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    CreatedAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)

    session: Mapped[KnowledgeChatSession] = relationship(back_populates="messages")
