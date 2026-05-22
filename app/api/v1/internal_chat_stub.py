from fastapi import APIRouter, HTTPException

from app.schemas.internal_chat import InternalChatStubRequest, InternalChatStubResponse
from app.services.internal_chat_api_stub_service import InternalChatApiStubService

router = APIRouter()


@router.post("/minerva/chat/stub", response_model=InternalChatStubResponse)
def create_internal_chat_stub_response(request: InternalChatStubRequest) -> InternalChatStubResponse:
    try:
        response = InternalChatApiStubService().build_response(request.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return InternalChatStubResponse(**response.model_dump())
