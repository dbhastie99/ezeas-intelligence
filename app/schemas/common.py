from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    document_id: str
    chunk_id: str
    title: str | None = None
    original_file_name: str
    source_type: str
    source_authority: int
    chunk_index: int
    score: float | None = None
    matched_tokens: list[str] = Field(default_factory=list)
    snippet: str | None = None
