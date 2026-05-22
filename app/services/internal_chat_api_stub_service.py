from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Any

from app.services.code_evidence_answer_policy_service import CodeEvidenceDisclosureMode
from app.services.code_evidence_answer_support_service import (
    CodeEvidenceAnswerSupportPacket,
    CodeEvidenceSupportStatus,
)
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
    InternalChatStatus,
)


class InternalChatApiStubStatus(StrEnum):
    STUB_RESPONSE_BUILT = "STUB_RESPONSE_BUILT"
    REQUEST_REJECTED = "REQUEST_REJECTED"
    INVALID_FIXTURE_KEY = "INVALID_FIXTURE_KEY"


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

FIXTURE_EVIDENCE_WARNING = (
    "Fixture evidence is synthetic/internal test evidence and does not prove runtime/customer availability."
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
    fixture_key: str | None = None

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
            "FixtureKey": self.fixture_key,
        }


@dataclass(frozen=True)
class InternalChatApiStubResponse:
    status: str
    request_echo: dict[str, Any]
    orchestrator_envelope: InternalChatResponseEnvelope
    evidence_support_packet: dict[str, Any]
    deterministic_draft: DeterministicAnswerDraft | None
    final_answer_text: None
    answer_permitted: bool
    is_final_answer: bool
    live_llm_used: bool
    final_answer_generation_permitted: bool
    fixture_evidence: dict[str, Any]
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
            "AnswerPermitted": self.answer_permitted,
            "IsFinalAnswer": self.is_final_answer,
            "LiveLlmUsed": self.live_llm_used,
            "FinalAnswerGenerationPermitted": self.final_answer_generation_permitted,
            "FixtureEvidence": dict(self.fixture_evidence),
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
        fixture_resolution = _resolve_fixture(normalized_request.fixture_key)
        if fixture_resolution["Invalid"]:
            scopes = _validate_scopes(normalized_request.source_scopes_requested)
            return _invalid_fixture_key_response(
                normalized_request,
                role=role,
                scopes=scopes,
                fixture_resolution=fixture_resolution,
            )

        explicit_evidence_count = len(_candidate_evidence_list(normalized_request.candidate_evidence_metadata))
        normalized_request, fixture_metadata = _request_with_fixture_evidence(
            normalized_request,
            fixture_resolution=fixture_resolution,
            explicit_evidence_count=explicit_evidence_count,
        )
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
        request_echo = _request_echo(
            normalized_request,
            role,
            scopes,
            len(evidence_metadata),
            fixture_metadata=fixture_metadata,
        )

        return InternalChatApiStubResponse(
            status=InternalChatApiStubStatus.STUB_RESPONSE_BUILT.value,
            request_echo=request_echo,
            orchestrator_envelope=envelope,
            evidence_support_packet=support_packet,
            deterministic_draft=draft,
            final_answer_text=None,
            answer_permitted=envelope.answer_permitted,
            is_final_answer=False,
            live_llm_used=False,
            final_answer_generation_permitted=False,
            fixture_evidence=fixture_metadata,
            no_action_attestation=dict(NO_ACTION_ATTESTATION),
            no_action_attestation_text=NO_ACTION_ATTESTATION_TEXT,
            required_caveats=_dedupe(
                envelope.required_caveats
                + _fixture_required_caveats(fixture_metadata)
                + _stub_required_caveats()
            ),
            blocked_claims=list(envelope.blocked_claims),
            unsupported_scopes=[scope.value for scope in envelope.unsupported_scopes],
            disclosure_metadata=_disclosure_metadata(envelope),
            boundaries=list(BOUNDARY_FLAGS),
            diagnostics=_diagnostics(normalized_request, envelope, draft, fixture_metadata=fixture_metadata),
            audit_summary={
                **dict(envelope.audit_summary),
                "ApiStubVersion": API_STUB_VERSION,
                "InternalOnly": True,
                "RouteCustomerFacing": False,
                "CandidateEvidenceCount": len(evidence_metadata),
                "ExplicitCandidateEvidenceCount": explicit_evidence_count,
                "FixtureEvidenceUsed": fixture_metadata["FixtureEvidenceUsed"],
                "FixtureKey": fixture_metadata["FixtureKey"],
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
            fixture_key=None,
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
        fixture_key=_optional_fixture_key(request.get("fixture_key") or request.get("FixtureKey")),
    )


def _resolve_fixture(fixture_key: str | None) -> dict[str, Any]:
    if not fixture_key:
        return _no_fixture_metadata()
    from app.services.internal_chat_evidence_fixture_harness_service import (
        InternalChatEvidenceFixtureHarnessService,
    )

    harness = InternalChatEvidenceFixtureHarnessService()
    try:
        fixture = harness.get_fixture(fixture_key)
    except KeyError:
        return {
            **_no_fixture_metadata(fixture_key=fixture_key),
            "Invalid": True,
            "FixtureEvidenceStatus": InternalChatApiStubStatus.INVALID_FIXTURE_KEY.value,
            "AvailableFixtureKeys": harness.list_available_fixture_key_values(),
        }
    return {
        "Invalid": False,
        "Fixture": fixture,
        "FixtureKey": fixture.key.value,
        "FixtureEvidenceUsed": True,
        "FixtureEvidenceSynthetic": True,
        "FixtureEvidenceStatus": fixture.expected_support_status.value,
        "FixtureEvidenceWarning": FIXTURE_EVIDENCE_WARNING,
        "FixtureEvidenceNoActionAttestation": dict(fixture.no_action_attestation),
        "FixtureEvidenceNoActionAttestationText": fixture.no_action_attestation_text,
        "AvailableFixtureKeys": harness.list_available_fixture_key_values(),
    }


def _request_with_fixture_evidence(
    request: InternalChatApiStubRequest,
    *,
    fixture_resolution: dict[str, Any],
    explicit_evidence_count: int,
) -> tuple[InternalChatApiStubRequest, dict[str, Any]]:
    fixture = fixture_resolution.get("Fixture")
    if not fixture:
        return request, _no_fixture_metadata(fixture_key=request.fixture_key)

    explicit_evidence = _candidate_evidence_list(request.candidate_evidence_metadata)
    fixture_evidence = fixture.candidate_evidence()
    merged_evidence, duplicate_count = _merge_candidate_evidence(explicit_evidence, fixture_evidence)
    merged_tags = _merge_ordered(request.domain_topic_tags, fixture.domain_tags)
    merged_scopes = _merge_ordered(request.source_scopes_requested, fixture.expected_source_scopes)
    metadata = {
        "FixtureKey": fixture.key.value,
        "FixtureEvidenceUsed": True,
        "FixtureEvidenceSynthetic": True,
        "FixtureEvidenceStatus": fixture.expected_support_status.value,
        "FixtureEvidenceSources": _fixture_sources(fixture_evidence),
        "FixtureCandidateEvidenceCount": len(fixture_evidence),
        "ExplicitCandidateEvidenceCount": explicit_evidence_count,
        "MergedCandidateEvidenceCount": len(merged_evidence),
        "DuplicateCandidateEvidenceSkipped": duplicate_count,
        "FixtureDomainTags": list(fixture.domain_tags),
        "FixtureSourceScopes": [scope.value for scope in fixture.expected_source_scopes],
        "FixtureEvidenceWarning": FIXTURE_EVIDENCE_WARNING,
        "FixtureEvidenceNoActionAttestation": dict(fixture.no_action_attestation),
        "FixtureEvidenceNoActionAttestationText": fixture.no_action_attestation_text,
        "RuntimeObjectEvidenceFetched": False,
        "RuntimeObjectEvidenceSupplied": False,
        "LiveRetrievalPerformed": False,
        "ProductionAvailabilityConfirmed": False,
        "CustomerAvailabilityConfirmed": False,
        "AvailableFixtureKeys": fixture_resolution["AvailableFixtureKeys"],
    }
    return (
        replace(
            request,
            source_scopes_requested=merged_scopes,
            domain_topic_tags=merged_tags,
            candidate_evidence_metadata=merged_evidence,
            fixture_key=fixture.key.value,
        ),
        metadata,
    )


def _invalid_fixture_key_response(
    request: InternalChatApiStubRequest,
    *,
    role: InternalChatRole,
    scopes: list[InternalChatSourceScope],
    fixture_resolution: dict[str, Any],
) -> InternalChatApiStubResponse:
    fixture_metadata = dict(fixture_resolution)
    fixture_metadata.pop("Fixture", None)
    fixture_metadata["FixtureEvidenceUsed"] = False
    fixture_metadata["FixtureEvidenceSynthetic"] = True
    fixture_metadata["FixtureEvidenceWarning"] = FIXTURE_EVIDENCE_WARNING
    fixture_metadata["FixtureEvidenceSources"] = []
    fixture_metadata["FixtureEvidenceNoActionAttestation"] = dict(NO_ACTION_ATTESTATION)
    fixture_metadata["RuntimeObjectEvidenceFetched"] = False
    fixture_metadata["RuntimeObjectEvidenceSupplied"] = False
    fixture_metadata["LiveRetrievalPerformed"] = False
    support_packet = _invalid_fixture_support_packet(role)
    envelope = InternalChatResponseEnvelope(
        status=InternalChatStatus.ANSWER_NOT_PERMITTED,
        question=request.question_text,
        role=role,
        disclosure_mode=support_packet.disclosure_mode,
        source_scopes_requested=scopes,
        source_scopes_used=[],
        unsupported_scopes=[],
        evidence_support_packet=support_packet,
        evidence_summary="Invalid or unsupported fixture key; no fixture evidence was supplied.",
        role_safe_evidence_summary="Invalid or unsupported fixture key; no role-safe evidence is available.",
        required_caveats=_dedupe(
            [
                FIXTURE_EVIDENCE_WARNING,
                "Invalid fixture keys do not trigger live retrieval, runtime evidence fetch, final answer generation, or write actions.",
            ]
            + _stub_required_caveats()
        ),
        prohibited_claims=[],
        blocked_claims=[f"unsupported fixture key: {fixture_resolution['FixtureKey']}"],
        answer_permitted=False,
        final_answer_generation_permitted=False,
        live_llm_used=False,
        final_answer_text=None,
        suggested_deterministic_summary=(
            "Deterministic invalid fixture key response; answer not permitted; "
            "no live LLM, DB, runtime evidence, or write action performed."
        ),
        no_action_attestation=dict(NO_ACTION_ATTESTATION),
        no_action_attestation_text=NO_ACTION_ATTESTATION_TEXT,
        audit_summary={
            "EnvelopeVersion": "MINERVA_INTERNAL_CHAT_ORCHESTRATOR_ENVELOPE_V0_1",
            "RequestedLiveLlm": request.allow_live_llm,
            "RequestedFinalAnswerGeneration": request.allow_final_answer_generation,
            "LiveLlmUsed": False,
            "FinalAnswerGenerationPerformed": False,
            "EvidenceMetadataCount": 0,
            "InvalidFixtureKey": fixture_resolution["FixtureKey"],
        },
        next_step_recommendation="Use one of the listed internal fixture keys or omit FixtureKey.",
    )
    return InternalChatApiStubResponse(
        status=InternalChatApiStubStatus.INVALID_FIXTURE_KEY.value,
        request_echo=_request_echo(request, role, scopes, 0, fixture_metadata=fixture_metadata),
        orchestrator_envelope=envelope,
        evidence_support_packet=support_packet.model_dump(),
        deterministic_draft=None,
        final_answer_text=None,
        answer_permitted=False,
        is_final_answer=False,
        live_llm_used=False,
        final_answer_generation_permitted=False,
        fixture_evidence=fixture_metadata,
        no_action_attestation=dict(NO_ACTION_ATTESTATION),
        no_action_attestation_text=NO_ACTION_ATTESTATION_TEXT,
        required_caveats=list(envelope.required_caveats),
        blocked_claims=list(envelope.blocked_claims),
        unsupported_scopes=[],
        disclosure_metadata=_disclosure_metadata(envelope),
        boundaries=list(BOUNDARY_FLAGS),
        diagnostics=_diagnostics(request, envelope, None, fixture_metadata=fixture_metadata),
        audit_summary={
            **dict(envelope.audit_summary),
            "ApiStubVersion": API_STUB_VERSION,
            "InternalOnly": True,
            "RouteCustomerFacing": False,
            "CandidateEvidenceCount": 0,
            "FixtureEvidenceUsed": False,
            "FixtureKey": fixture_resolution["FixtureKey"],
            "NoExternalCallsOrWritesPerformed": True,
        },
    )


def _invalid_fixture_support_packet(role: InternalChatRole) -> CodeEvidenceAnswerSupportPacket:
    return CodeEvidenceAnswerSupportPacket(
        support_status=CodeEvidenceSupportStatus.UNSUPPORTED,
        disclosure_mode=_disclosure_mode_for_role(role),
        doctrine_evidence=[],
        implementation_state_evidence=[],
        code_evidence=[],
        test_evidence=[],
        prompt_evidence=[],
        knowledge_evidence=[],
        findings=[],
        evidence_summary="No evidence supplied because the fixture key is invalid.",
        role_safe_evidence_summary="No role-safe evidence supplied because the fixture key is invalid.",
        withheld_evidence=[],
        required_caveats=[FIXTURE_EVIDENCE_WARNING],
        prohibited_claims=[],
        blocked_claims=[],
        runtime_availability_caveat_required=True,
        code_cannot_prove_runtime_caveat=FIXTURE_EVIDENCE_WARNING,
        answer_permitted=False,
        final_answer_generation_permitted=False,
        no_action_attestation=NO_ACTION_ATTESTATION_TEXT,
    )


def _disclosure_mode_for_role(role: InternalChatRole) -> CodeEvidenceDisclosureMode:
    if role == InternalChatRole.DEVELOPER:
        return CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE
    if role in {
        InternalChatRole.PAYROLL_ADMINISTRATOR,
        InternalChatRole.PAYROLL_MANAGER,
        InternalChatRole.CUSTOMER_ADMINISTRATOR,
    }:
        return CodeEvidenceDisclosureMode.IMPLEMENTATION_CONFIRMATION
    if role in {InternalChatRole.PAYROLL_USER, InternalChatRole.ANALYTICS_USER}:
        return CodeEvidenceDisclosureMode.BACKGROUND_CONFIDENCE_ONLY
    return CodeEvidenceDisclosureMode.NO_CODE_EVIDENCE


def _no_fixture_metadata(fixture_key: str | None = None) -> dict[str, Any]:
    return {
        "Invalid": False,
        "FixtureKey": fixture_key,
        "FixtureEvidenceUsed": False,
        "FixtureEvidenceSynthetic": False,
        "FixtureEvidenceStatus": "NOT_REQUESTED",
        "FixtureEvidenceSources": [],
        "FixtureEvidenceWarning": None,
        "FixtureEvidenceNoActionAttestation": dict(NO_ACTION_ATTESTATION),
        "RuntimeObjectEvidenceFetched": False,
        "RuntimeObjectEvidenceSupplied": False,
        "LiveRetrievalPerformed": False,
    }


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


def _merge_candidate_evidence(
    explicit_evidence: list[dict[str, Any]],
    fixture_evidence: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    merged = [dict(item) for item in explicit_evidence]
    seen = {_candidate_evidence_identity(item) for item in merged}
    duplicate_count = 0
    for item in fixture_evidence:
        identity = _candidate_evidence_identity(item)
        if identity in seen:
            duplicate_count += 1
            continue
        merged.append(dict(item))
        seen.add(identity)
    return merged, duplicate_count


def _candidate_evidence_identity(item: dict[str, Any]) -> tuple[str, ...]:
    stable_fields = [
        "evidence_id",
        "id",
        "title",
        "source_type",
        "evidence_category",
        "source_scope",
        "repo_name",
        "repo_family",
        "file_path",
        "symbol_name",
        "route_path",
        "test_name",
    ]
    values = tuple(str(item.get(field) or "") for field in stable_fields)
    if any(values):
        return values
    return tuple(f"{key}={item[key]}" for key in sorted(item))


def _merge_ordered(explicit_values: list[Any], fixture_values: list[Any]) -> list[Any]:
    merged: list[Any] = []
    seen: set[str] = set()
    for value in [*explicit_values, *fixture_values]:
        identity = _enum_value(value)
        if identity not in seen:
            merged.append(value)
            seen.add(identity)
    return merged


def _fixture_sources(fixture_evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for item in fixture_evidence:
        sources.append(
            {
                "SourceType": str(item.get("source_type") or ""),
                "EvidenceCategory": str(item.get("evidence_category") or ""),
                "SourceScope": str(item.get("source_scope") or ""),
                "FixtureOnly": bool(item.get("fixture_only", True)),
                "Synthetic": True,
                "RuntimeObjectEvidence": False,
            }
        )
    return sources


def _request_echo(
    request: InternalChatApiStubRequest,
    role: InternalChatRole,
    scopes: list[InternalChatSourceScope],
    evidence_count: int,
    *,
    fixture_metadata: dict[str, Any],
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
        "FixtureKey": fixture_metadata["FixtureKey"],
        "FixtureEvidenceUsed": fixture_metadata["FixtureEvidenceUsed"],
        "FixtureEvidenceSynthetic": fixture_metadata["FixtureEvidenceSynthetic"],
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
    *,
    fixture_metadata: dict[str, Any],
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
        "FixtureKey": fixture_metadata["FixtureKey"],
        "FixtureEvidenceUsed": fixture_metadata["FixtureEvidenceUsed"],
        "FixtureEvidenceSynthetic": fixture_metadata["FixtureEvidenceSynthetic"],
        "FixtureEvidenceStatus": fixture_metadata["FixtureEvidenceStatus"],
    }


def _stub_required_caveats() -> list[str]:
    return [
        "This is an internal Minerva API stub, not a production or customer chat endpoint.",
        "The stub does not call a live LLM, access a database, call external APIs, execute code, fetch runtime object evidence, persist chat, or perform write actions.",
        "Final answer generation remains disabled; deterministic draft text is non-final internal review text only.",
    ]


def _fixture_required_caveats(fixture_metadata: dict[str, Any]) -> list[str]:
    if not fixture_metadata["FixtureEvidenceUsed"]:
        return []
    return [
        FIXTURE_EVIDENCE_WARNING,
        "No live runtime object evidence was fetched; fixture evidence must not be treated as production, customer, tenant, or live object evidence.",
    ]


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _optional_fixture_key(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped
