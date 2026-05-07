from pydantic import BaseModel

from app.schemas.common import SourceReference


class ChatSessionCreate(BaseModel):
    tenant_id: str | None = None
    user_id: str | None = None
    title: str | None = None


class ChatSessionResponse(BaseModel):
    session_id: str


class ChatMessageRequest(BaseModel):
    session_id: str
    message: str
    tenant_id: str | None = None
    user_id: str | None = None


class ChatMessageResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
    audit_id: str
