from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.services.internal_chat_deterministic_answer_draft_service import (
    DeterministicAnswerDraft,
    InternalChatDeterministicAnswerDraftService,
)
from app.services.internal_chat_orchestrator_service import (
    InternalChatOrchestratorService,
    InternalChatRequest,
    InternalChatResponseEnvelope,
    InternalChatRole,
    InternalChatSourceScope,
)


class InternalChatApiStubStatus(StrEnum):
    STUB_RESPONSE_BUILT = "STUB_RESPONSE_BUILT"
    REQUEST_REJECTED = "REQUEST_REJECTED"


API_STUB_VERSION = "MINERVA_INTERNAL_CHAT_API_STUB_V0_1"

NO_ACTION_ATTESTATION = {
    "LiveLlmCalled": False,
    "DatabaseAccessed": False,
    "ExternalApiCalled": False,
    "CodeExecuted": False,
    "ExternalRepoMutated": False,
    "PayrollCalculationPerformed": False,
    "WriteActionPerformed": False,
    "RuntimeObjectEvidenceFetched": False,
    "FinalAnswerGenerated": False,
    "FinalAnswerGenerationPerformed": False,
    "ChatPersistencePerformed": False,
    "UiExposed": False,
}

NO_ACTION_ATTESTATION_TEXT = (
    "No live LLM called; no DB accessed; no external API called; no code executed; "
    "no external repo mutated; no payroll calculation performed; no write action "
    "performed; no runtime object evidence fetched; no final answer generated; no "
    "chat persistence performed; no UI exposed."
)

BOUNDARY_FLAGS = [
    "INTERNAL_STUB_ONLY",
    "NOT_CUSTOMER_FACING_CHAT",
    "LIVE_LLM_DISABLED",
    "FINAL_ANSWER_GENERATION_DISABLED",
    "DATABASE_ACCESS_DISABLED",
    "EXTERNAL_API_CALLS_DISABLED",
    "CODE_EXECUTION_DISABLED",
    "RUNTIME_OBJECT_FETCH_DISABLED",
    "WRITE_ACTIONS_DISABLED",
    "PAYROLL_CALCULATION_DISABLED",
    "CHAT_PERSISTENCE_DISABLED",
    "WORKFORCE_PLATFORM_INTEGRATION_DISABLED",
    "RAW_CODE_SNIPPETS_DISABLED",
]


@dataclass(frozen=True)
class InternalChatApiStubRequest:
    question_text: str
    user_role: InternalChatRole | str
    source_scopes_requested: list[InternalChatSourceScope | str] = field(default_factory=list)
    surface_context: dict[str, Any] | None = None
    domain_topic_tags: list[str] = field(default_factory=list)
    candidate_evidence_metadata: list[dict[str, Any]] | dict[str, Any] | None = field(default_factory=list)
    claimed_answer_to_validate: str | None = None
    allow_final_answer_generation: bool = False
    allow_live_llm: bool = False
    include_deterministic_draft: bool = True

    def model_dump(self) -> dict[str, Any]:
        return {
            "Question": self.question_text,
            "Role": _enum_value(self.user_role),
            "SourceScopes": [_enum_value(scope) for scope in self.source_scopes_requested],
            "SurfaceContext": dict(self.surface_context or {}),
            "DomainTags": list(self.domain_topic_tags),
            "CandidateEvidenceCount": len(_candidate_evidence_list(self.candidate_evidence_metadata)),
            "ClaimToValidate": self.claimed_answer_to_validate,
            "AllowFinalAnswerGeneration": self.allow_final_answer_generation,
            "AllowLiveLlm": self.allow_live_llm,
            "IncludeDeterministicDraft": self.include_deterministic_draft,
        }


@dataclass(frozen=True)
class InternalChatApiStubResponse:
    status: str
    request_echo: dict[str, Any]
    orchestrator_envelope: InternalChatResponseEnvelope
    evidence_support_packet: dict[str, Any]
    deterministic_draft: DeterministicAnswerDraft | None
    final_answer_text: None
    is_final_answer: bool
    live_llm_used: bool
    final_answer_generation_permitted: bool
    no_action_attestation: dict[str, bool]
    no_action_attestation_text: str
    required_caveats: list[str]
    blocked_claims: list[str]
    unsupported_scopes: list[str]
    disclosure_metadata: dict[str, Any]
    boundaries: list[str]
    diagnostics: dict[str, Any]
    audit_summary: dict[str, Any]

    def model_dump(self) -> dict[str, Any]:
        envelope = self.orchestrator_envelope.model_dump()
        draft = self.deterministic_draft.model_dump() if self.deterministic_draft else None
        return {
            "Status": self.status,
            "RequestEcho": dict(self.request_echo),
            "OrchestratorEnvelope": envelope,
            "EvidenceSupportPacket": dict(self.evidence_support_packet),
            "DeterministicDraft": draft,
            "FinalAnswerText": self.final_answer_text,
            "IsFinalAnswer": self.is_final_answer,
            "LiveLlmUsed": self.live_llm_used,
            "FinalAnswerGenerationPermitted": self.final_answer_generation_permitted,
            "NoActionAttestation": dict(self.no_action_attestation),
            "NoActionAttestationText": self.no_action_attestation_text,
            "RequiredCaveats": list(self.required_caveats),
            "BlockedClaims": list(self.blocked_claims),
            "UnsupportedScopes": list(self.unsupported_scopes),
            "DisclosureMetadata": dict(self.disclosure_metadata),
            "Boundaries": list(self.boundaries),
            "Diagnostics": dict(self.diagnostics),
            "AuditSummary": dict(self.audit_summary),
        }


class InternalChatApiStubService:
    def __init__(
        self,
        orchestrator_service: InternalChatOrchestratorService | None = None,
        deterministic_draft_service: InternalChatDeterministicAnswerDraftService | None = None,
    ) -> None:
        self.orchestrator_service = orchestrator_service or InternalChatOrchestratorService()
        self.deterministic_draft_service = (
            deterministic_draft_service or InternalChatDeterministicAnswerDraftService()
        )

    def build_response(
        self,
        request: InternalChatApiStubRequest | InternalChatRequest | dict[str, Any],
    ) -> InternalChatApiStubResponse:
        normalized_request = _api_request_from_any(request)
        role = _validate_role(normalized_request.user_role)
        scopes = _validate_scopes(normalized_request.source_scopes_requested)
        evidence_metadata = _candidate_evidence_list(normalized_request.candidate_evidence_metadata)

        orchestrator_request = InternalChatRequest(
            question_text=normalized_request.question_text,
            user_role=role,
            source_scopes_requested=scopes,
            surface_context=normalized_request.surface_context,
            domain_topic_tags=list(normalized_request.domain_topic_tags),
            candidate_evidence_metadata=evidence_metadata,
            claimed_answer_to_validate=normalized_request.claimed_answer_to_validate,
            allow_final_answer_generation=normalized_request.allow_final_answer_generation,
            allow_live_llm=normalized_request.allow_live_llm,
        )
        envelope = self.orchestrator_service.orchestrate(orchestrator_request)
        draft = (
            self.deterministic_draft_service.build_draft(envelope)
            if normalized_request.include_deterministic_draft
            else None
        )
        envelope_dump = envelope.model_dump()
        support_packet = envelope_dump["EvidenceSupportPacket"]
        request_echo = _request_echo(normalized_request, role, scopes, len(evidence_metadata))

        return InternalChatApiStubResponse(
            status=InternalChatApiStubStatus.STUB_RESPONSE_BUILT.value,
            request_echo=request_echo,
            orchestrator_envelope=envelope,
            evidence_support_packet=support_packet,
            deterministic_draft=draft,
            final_answer_text=None,
            is_final_answer=False,
            live_llm_used=False,
            final_answer_generation_permitted=False,
            no_action_attestation=dict(NO_ACTION_ATTESTATION),
            no_action_attestation_text=NO_ACTION_ATTESTATION_TEXT,
            required_caveats=_dedupe(envelope.required_caveats + _stub_required_caveats()),
            blocked_claims=list(envelope.blocked_claims),
            unsupported_scopes=[scope.value for scope in envelope.unsupported_scopes],
            disclosure_metadata=_disclosure_metadata(envelope),
            boundaries=list(BOUNDARY_FLAGS),
            diagnostics=_diagnostics(normalized_request, envelope, draft),
            audit_summary={
                **dict(envelope.audit_summary),
                "ApiStubVersion": API_STUB_VERSION,
                "InternalOnly": True,
                "RouteCustomerFacing": False,
                "CandidateEvidenceCount": len(evidence_metadata),
                "NoExternalCallsOrWritesPerformed": True,
            },
        )


def _api_request_from_any(
    request: InternalChatApiStubRequest | InternalChatRequest | dict[str, Any],
) -> InternalChatApiStubRequest:
    if isinstance(request, InternalChatApiStubRequest):
        return request
    if isinstance(request, InternalChatRequest):
        return InternalChatApiStubRequest(
            question_text=request.question_text,
            user_role=request.user_role,
            source_scopes_requested=list(request.source_scopes_requested),
            surface_context=request.surface_context,
            domain_topic_tags=list(request.domain_topic_tags),
            candidate_evidence_metadata=list(request.candidate_evidence_metadata),
            claimed_answer_to_validate=request.claimed_answer_to_validate,
            allow_final_answer_generation=request.allow_final_answer_generation,
            allow_live_llm=request.allow_live_llm,
            include_deterministic_draft=True,
        )
    return InternalChatApiStubRequest(
        question_text=str(request.get("question_text") or request.get("Question") or ""),
        user_role=request.get("user_role") or request.get("Role") or "",
        source_scopes_requested=list(
            request.get("source_scopes_requested")
            or request.get("SourceScopes")
            or request.get("SourceScopesRequested")
            or []
        ),
        surface_context=request.get("surface_context") or request.get("SurfaceContext"),
        domain_topic_tags=list(
            request.get("domain_topic_tags")
            or request.get("DomainTags")
            or request.get("DomainTopicTags")
            or []
        ),
        candidate_evidence_metadata=(
            request.get("candidate_evidence_metadata")
            or request.get("CandidateEvidence")
            or request.get("CandidateEvidenceMetadata")
            or []
        ),
        claimed_answer_to_validate=(
            request.get("claimed_answer_to_validate")
            or request.get("ClaimToValidate")
            or request.get("ClaimedAnswerToValidate")
        ),
        allow_final_answer_generation=bool(
            request.get("allow_final_answer_generation") or request.get("AllowFinalAnswerGeneration")
        ),
        allow_live_llm=bool(request.get("allow_live_llm") or request.get("AllowLiveLlm")),
        include_deterministic_draft=bool(
            request.get("include_deterministic_draft", request.get("IncludeDeterministicDraft", True))
        ),
    )


def _validate_role(role: InternalChatRole | str) -> InternalChatRole:
    if isinstance(role, InternalChatRole):
        return role
    try:
        return InternalChatRole(str(role).upper())
    except ValueError:
        raise ValueError(f"Unsupported internal chat role: {role!r}") from None


def _validate_scopes(scopes: list[InternalChatSourceScope | str]) -> list[InternalChatSourceScope]:
    normalized: list[InternalChatSourceScope] = []
    for scope in scopes:
        if isinstance(scope, InternalChatSourceScope):
            normalized_scope = scope
        else:
            try:
                normalized_scope = InternalChatSourceScope(str(scope).upper())
            except ValueError:
                raise ValueError(f"Unsupported internal chat source scope: {scope!r}") from None
        if normalized_scope not in normalized:
            normalized.append(normalized_scope)
    return normalized


def _candidate_evidence_list(value: list[dict[str, Any]] | dict[str, Any] | None) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, dict):
        return [dict(value)]
    return [dict(item) for item in value]


def _request_echo(
    request: InternalChatApiStubRequest,
    role: InternalChatRole,
    scopes: list[InternalChatSourceScope],
    evidence_count: int,
) -> dict[str, Any]:
    return {
        "Question": request.question_text,
        "Role": role.value,
        "SourceScopes": [scope.value for scope in scopes],
        "DomainTags": list(request.domain_topic_tags),
        "SurfaceContextKeys": sorted((request.surface_context or {}).keys()),
        "CandidateEvidenceCount": evidence_count,
        "ClaimToValidateSupplied": request.claimed_answer_to_validate is not None,
        "AllowFinalAnswerGenerationRequested": request.allow_final_answer_generation,
        "AllowLiveLlmRequested": request.allow_live_llm,
        "IncludeDeterministicDraft": request.include_deterministic_draft,
    }


def _disclosure_metadata(envelope: InternalChatResponseEnvelope) -> dict[str, Any]:
    return {
        "Role": envelope.role.value,
        "DisclosureMode": envelope.disclosure_mode.value,
        "RoleSafeEvidenceSummary": envelope.role_safe_evidence_summary,
        "RawCodeSnippetsIncluded": False,
        "CodeEvidenceMayProveRuntimeAvailability": False,
        "CustomerAvailabilityConfirmed": False,
        "ProductionAvailabilityConfirmed": False,
        "RuntimeObjectEvidenceFetched": False,
        "FinalUserFacingAnswerGenerated": False,
    }


def _diagnostics(
    request: InternalChatApiStubRequest,
    envelope: InternalChatResponseEnvelope,
    draft: DeterministicAnswerDraft | None,
) -> dict[str, Any]:
    return {
        "ApiStubVersion": API_STUB_VERSION,
        "OrchestratorEnvelopeVersion": envelope.audit_summary.get("EnvelopeVersion"),
        "RequestedLiveLlm": request.allow_live_llm,
        "RequestedFinalAnswerGeneration": request.allow_final_answer_generation,
        "IncludeDeterministicDraft": request.include_deterministic_draft,
        "DeterministicDraftIncluded": draft is not None,
        "OrchestratorStatus": envelope.status.value,
        "EvidenceSupportStatus": envelope.evidence_support_packet.support_status.value,
        "DraftStatus": draft.draft_status.value if draft else None,
        "LiveLlmUsed": False,
        "FinalAnswerGenerationPerformed": False,
        "DatabaseAccessed": False,
        "ExternalApiCalled": False,
        "RuntimeObjectEvidenceFetched": False,
        "WriteActionPerformed": False,
    }


def _stub_required_caveats() -> list[str]:
    return [
        "This is an internal Minerva API stub, not a production or customer chat endpoint.",
        "The stub does not call a live LLM, access a database, call external APIs, execute code, fetch runtime object evidence, persist chat, or perform write actions.",
        "Final answer generation remains disabled; deterministic draft text is non-final internal review text only.",
    ]


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped
