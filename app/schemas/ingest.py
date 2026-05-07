from pydantic import BaseModel


class FolderIngestRequest(BaseModel):
    folder_path: str
    source_type: str = "OTHER"
    capability_status: str | None = None
    tenant_id: str | None = None


class FileIngestResponse(BaseModel):
    document_id: str
    duplicate: bool
    chunk_count: int
    source_type: str
    file_sha256: str


class FolderIngestResponse(BaseModel):
    ingested: int
    duplicates: int
    skipped: int
    errors: list[str]
