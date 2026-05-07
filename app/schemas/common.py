from pydantic import BaseModel


class SourceReference(BaseModel):
    document_id: str
    chunk_id: str
    title: str | None = None
    original_file_name: str
    source_type: str
    source_authority: int
    chunk_index: int
