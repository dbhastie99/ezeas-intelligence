from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ingest import FileIngestResponse, FolderIngestRequest, FolderIngestResponse
from app.services.document_extraction_service import UnsupportedDocumentTypeError
from app.services.ingestion_service import IngestionError, ingest_file_bytes, ingest_folder

router = APIRouter()


@router.post("/file", response_model=FileIngestResponse)
async def ingest_file(
    file: UploadFile = File(...),
    source_type: str = Form("OTHER"),
    capability_status: str | None = Form(None),
    tenant_id: str | None = Form(None),
    title: str | None = Form(None),
    db: Session = Depends(get_db),
) -> FileIngestResponse:
    content = await file.read()
    try:
        document, duplicate = ingest_file_bytes(
            db=db,
            content=content,
            original_file_name=file.filename or "uploaded-file",
            source_type=source_type,
            capability_status=capability_status,
            tenant_id=tenant_id,
            title=title,
        )
    except UnsupportedDocumentTypeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IngestionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FileIngestResponse(
        document_id=document.KnowledgeDocumentId,
        duplicate=duplicate,
        chunk_count=document.ChunkCount,
        source_type=document.SourceType,
        file_sha256=document.FileSha256,
    )


@router.post("/folder", response_model=FolderIngestResponse)
def ingest_folder_endpoint(request: FolderIngestRequest, db: Session = Depends(get_db)) -> FolderIngestResponse:
    try:
        result = ingest_folder(
            db=db,
            folder_path=request.folder_path,
            source_type=request.source_type,
            capability_status=request.capability_status,
            tenant_id=request.tenant_id,
        )
    except IngestionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FolderIngestResponse(**result)
