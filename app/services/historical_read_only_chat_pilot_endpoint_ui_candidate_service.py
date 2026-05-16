from dataclasses import asdict, dataclass
from typing import Any

from app.services.historical_read_only_chat_pilot_orchestrator_candidate_service import (
    evaluate_historical_read_only_chat_pilot_orchestrator_candidate,
)


GUARDRAILS = (
    "internal-only candidate service",
    "metadata/envelope-only request",
    "calls existing in-memory orchestrator candidate only",
    "no global route registration",
    "no UI creation",
    "no production chat exposure",
    "no public or tenant/customer access",
    "no live LLM call",
    "no final natural-language answer generation",
    "no live retrieval backend",
    "no vector or corpus search",
    "no corpus mutation",
    "no database read or write",
)

NON_GOALS = (
    "production chat exposure",
    "public endpoint",
    "tenant/customer endpoint",
    "source content ingestion",
    "operational corpus mutation",
    "Code Evidence ingestion",
    "schema migration",
    "workforce-platform change",
    "award-configurator-v1 change",
    "ezeas-analytics change",
    "current-truth promotion",
    "runtime answer-use activation",
    "runtime retrieval activation",
)


@dataclass(frozen=True)
class HistoricalReadOnlyChatPilotEndpointUiCandidateResponse:
    MinimalEndpointUiCandidateImplemented: bool
    EndpointCreatedThisSlice: bool
    RouteRegisteredGlobally: bool
    UICreatedThisSlice: bool
    ChatExposedThisSlice: bool
    LiveLLMCalled: bool
    FinalAnswerGenerated: bool
    LiveRetrievalPerformed: bool
    CorpusMutationPerformed: bool
    DatabaseReadPerformed: bool
    DatabaseWritePerformed: bool
    RequestId: str | None
    OperatorContext: str | None
    OrchestratorResponse: dict[str, Any]
    PilotResponseStatus: str
    PilotResponseMode: str
    RefusalRequired: bool
    RefusalReason: str | None
    CitationReady: bool
    CaveatRequired: bool
    RuntimeBoundaryAsserted: bool
    Guardrails: tuple[str, ...]
    NonGoals: tuple[str, ...]
    Explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_historical_read_only_chat_pilot_endpoint_ui_candidate(
    request: dict[str, Any] | object,
) -> dict[str, Any]:
    supplied_metadata = _as_dict(request)
    orchestrator_response = evaluate_historical_read_only_chat_pilot_orchestrator_candidate(
        supplied_metadata
    )

    return HistoricalReadOnlyChatPilotEndpointUiCandidateResponse(
        MinimalEndpointUiCandidateImplemented=True,
        EndpointCreatedThisSlice=False,
        RouteRegisteredGlobally=False,
        UICreatedThisSlice=False,
        ChatExposedThisSlice=False,
        LiveLLMCalled=False,
        FinalAnswerGenerated=False,
        LiveRetrievalPerformed=False,
        CorpusMutationPerformed=False,
        DatabaseReadPerformed=False,
        DatabaseWritePerformed=False,
        RequestId=_optional_string(supplied_metadata.get("RequestId")),
        OperatorContext=_optional_string(supplied_metadata.get("OperatorContext")),
        OrchestratorResponse=orchestrator_response,
        PilotResponseStatus=str(orchestrator_response.get("PilotResponseStatus", "")),
        PilotResponseMode=str(orchestrator_response.get("PilotResponseMode", "")),
        RefusalRequired=bool(orchestrator_response.get("RefusalRequired", False)),
        RefusalReason=_optional_string(orchestrator_response.get("RefusalReason")),
        CitationReady=bool(orchestrator_response.get("CitationReady", False)),
        CaveatRequired=bool(orchestrator_response.get("CaveatRequired", False)),
        RuntimeBoundaryAsserted=True,
        Guardrails=GUARDRAILS,
        NonGoals=NON_GOALS,
        Explanation=(
            "The minimal endpoint/UI candidate service consumed supplied metadata, "
            "called the existing in-memory orchestrator candidate, and returned a "
            "status envelope only. No route was globally registered, no UI was "
            "created, no production chat was exposed, and no live retrieval, LLM, "
            "final answer generation, database access, or corpus mutation occurred."
        ),
    ).to_dict()


def _as_dict(request: dict[str, Any] | object) -> dict[str, Any]:
    if isinstance(request, dict):
        return dict(request)
    return {
        field_name: getattr(request, field_name)
        for field_name in dir(request)
        if not field_name.startswith("_") and not callable(getattr(request, field_name))
    }


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)
