from fastapi import APIRouter, HTTPException

from app.schemas.award_studio_minerva import (
    AwardStudioMinervaQuestionRequest,
    AwardStudioMinervaQuestionResponse,
)
from app.services.award_studio_answer_planner import AwardStudioContractError
from app.services.award_studio_question_service import ask_award_studio_question


router = APIRouter()


@router.post("/award-studio/questions", response_model=AwardStudioMinervaQuestionResponse)
def ask_governed_award_studio_question(
    request: AwardStudioMinervaQuestionRequest,
) -> AwardStudioMinervaQuestionResponse:
    try:
        return ask_award_studio_question(request)
    except AwardStudioContractError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
