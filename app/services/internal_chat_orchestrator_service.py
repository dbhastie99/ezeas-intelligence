from dataclasses import asdict, dataclass, field
from enum import StrEnum
import re
from typing import Any

from app.services.code_evidence_answer_policy_service import (
    CodeEvidenceDisclosureMode,
    CodeEvidenceRole,
)
from app.services.code_evidence_answer_support_service import (
    CodeEvidenceAnswerSupportPacket,
    CodeEvidenceAnswerSupportService,
    CodeEvidenceSupportStatus,
)


class InternalChatRole(StrEnum):
    DEVELOPER = "DEVELOPER"
    PAYROLL_ADMINISTRATOR = "PAYROLL_ADMINISTRATOR"
    PAYROLL_MANAGER = "PAYROLL_MANAGER"
    PAYROLL_USER = "PAYROLL_USER"
    CUSTOMER_ADMINISTRATOR = "CUSTOMER_ADMINISTRATOR"
    WORKER = "WORKER"
    ANALYTICS_USER = "ANALYTICS_USER"


class InternalChatSourceScope(StrEnum):
    PLATFORM_KNOWLEDGE = "PLATFORM_KNOWLEDGE"
    IMPLEMENTATION_STATE = "IMPLEMENTATION_STATE"
    CODE_EVIDENCE = "CODE_EVIDENCE"
    TEST_EVIDENCE = "TEST_EVIDENCE"
    PROMPT_ARTEFACTS = "PROMPT_ARTEFACTS"
    EVALUATION_BASELINES = "EVALUATION_BASELINES"
    RUNTIME_OBJECT_EVIDENCE = "RUNTIME_OBJECT_EVIDENCE"
    ANALYTICS_EVIDENCE = "ANALYTICS_EVIDENCE"


class InternalChatStatus(StrEnum):
    READY_FOR_ANSWER_SUPPORT = "READY_FOR_ANSWER_SUPPORT"
    ANSWER_SUPPORT_BUILT = "ANSWER_SUPPORT_BUILT"
    ANSWER_NOT_PERMITTED = "ANSWER_NOT_PERMITTED"
    ROLE_RESTRICTED = "ROLE_RESTRICTED"
    NEEDS_MORE_EVIDENCE = "NEEDS_MORE_EVIDENCE"
    PROHIBITED_CLAIM_BLOCKED = "PROHIBITED_CLAIM_BLOCKED"
    LIVE_LLM_DISABLED = "LIVE_LLM_DISABLED"
    FINAL_ANSWER_GENERATION_DISABLED = "FINAL_ANSWER_GENERATION_DISABLED"
    UNSUPPORTED_SCOPE = "UNSUPPORTED_SCOPE"


NO_ACTION_ATTESTATION = {
    "LiveLlmCalled": False,
    "DatabaseAccessed": False,
    "ExternalRepoMutated": False,
    "PayrollCalculationPerformed": False,
    "WriteActionPerformed": False,
    "RuntimeObjectEvidenceFetched": False,
    "FinalAnswerGenerationPerformed": False,
    "UiExposed": False,
    "ChatPersistencePerformed": False,
}

NO_ACTION_ATTESTATION_TEXT = (
    "No live LLM called; no DB accessed; no external repo mutated; no payroll "
    "calculation performed; no write action performed; no runtime object evidence "
    "fetched; no final answer generation performed; no UI exposed; no chat "
    "persistence performed."
)

SUPPORTED_METADATA_SCOPES = {
    InternalChatSourceScope.PLATFORM_KNOWLEDGE,
    InternalChatSourceScope.IMPLEMENTATION_STATE,
    InternalChatSourceScope.CODE_EVIDENCE,
    InternalChatSourceScope.TEST_EVIDENCE,
    InternalChatSourceScope.PROMPT_ARTEFACTS,
    InternalChatSourceScope.EVALUATION_BASELINES,
}

ACTION_TERMS = {
    "approve",
    "authorise",
    "authorize",
    "change",
    "create",
    "delete",
    "edit",
    "finalise",
    "finalize",
    "mark",
    "mutate",
    "pay",
    "process",
    "rerun",
    "save",
    "submit",
    "update",
    "write",
}
CALCULATION_TERMS = {
    "calculate",
    "calculated",
    "calculation",
    "compute",
    "computed",
    "overtime",
    "pay",
    "payslip",
    "rate",
    "total",
}
RAW_CODE_TERMS = {"raw code", "source code", "show me the code", "see the code", "code behind"}
RUNTIME_SCOPE_TERMS = {"tenant", "customer", "enabled", "live", "production", "runtime", "available"}


@dataclass(frozen=True)
class InternalChatRequest:
    question_text: str
    user_role: InternalChatRole | str
    source_scopes_requested: list[InternalChatSourceScope | str] = field(default_factory=list)
    surface_context: dict[str, Any] | None = None
    domain_topic_tags: list[str] = field(default_factory=list)
    candidate_evidence_metadata: list[dict[str, Any]] = field(default_factory=list)
    claimed_answer_to_validate: str | None = None
    allow_final_answer_generation: bool = False
    allow_live_llm: bool = False

    def model_dump(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["user_role"] = _enum_value(self.user_role)
        payload["source_scopes_requested"] = [_enum_value(scope) for scope in self.source_scopes_requested]
        return payload


@dataclass(frozen=True)
class InternalChatEvidenceContext:
    candidate_evidence_metadata: list[dict[str, Any]] = field(default_factory=list)
    synthetic_runtime_metadata_supplied: bool = False
    synthetic_analytics_metadata_supplied: bool = False

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalChatResponseEnvelope:
    status: InternalChatStatus
    question: str
    role: InternalChatRole
    disclosure_mode: CodeEvidenceDisclosureMode
    source_scopes_requested: list[InternalChatSourceScope]
    source_scopes_used: list[InternalChatSourceScope]
    unsupported_scopes: list[InternalChatSourceScope]
    evidence_support_packet: CodeEvidenceAnswerSupportPacket
    evidence_summary: str
    role_safe_evidence_summary: str
    required_caveats: list[str]
    prohibited_claims: list[str]
    blocked_claims: list[str]
    answer_permitted: bool
    final_answer_generation_permitted: bool
    live_llm_used: bool
    final_answer_text: str | None
    suggested_deterministic_summary: str | None
    no_action_attestation: dict[str, bool]
    no_action_attestation_text: str
    audit_summary: dict[str, Any]
    next_step_recommendation: str

    def model_dump(self) -> dict[str, Any]:
        return {
            "Status": self.status.value,
            "Question": self.question,
            "Role": self.role.value,
            "DisclosureMode": self.disclosure_mode.value,
            "SourceScopesRequested": [scope.value for scope in self.source_scopes_requested],
            "SourceScopesUsed": [scope.value for scope in self.source_scopes_used],
            "UnsupportedScopes": [scope.value for scope in self.unsupported_scopes],
            "EvidenceSupportPacket": self.evidence_support_packet.model_dump(),
            "EvidenceSummary": self.evidence_summary,
            "RoleSafeEvidenceSummary": self.role_safe_evidence_summary,
            "RequiredCaveats": list(self.required_caveats),
            "ProhibitedClaims": list(self.prohibited_claims),
            "BlockedClaims": list(self.blocked_claims),
            "AnswerPermitted": self.answer_permitted,
            "FinalAnswerGenerationPermitted": self.final_answer_generation_permitted,
            "LiveLlmUsed": self.live_llm_used,
            "FinalAnswerText": self.final_answer_text,
            "SuggestedDeterministicSummary": self.suggested_deterministic_summary,
            "NoActionAttestation": dict(self.no_action_attestation),
            "NoActionAttestationText": self.no_action_attestation_text,
            "AuditSummary": dict(self.audit_summary),
            "NextStepRecommendation": self.next_step_recommendation,
        }


class InternalChatOrchestratorService:
    def __init__(self, answer_support_service: CodeEvidenceAnswerSupportService | None = None) -> None:
        self.answer_support_service = answer_support_service or CodeEvidenceAnswerSupportService()

    def orchestrate(
        self,
        request: InternalChatRequest | dict[str, Any],
        evidence_context: InternalChatEvidenceContext | None = None,
    ) -> InternalChatResponseEnvelope:
        normalized_request = _request_from_any(request)
        role = _normalize_internal_role(normalized_request.user_role)
        code_role = _code_evidence_role_for_chat_role(role)
        requested_scopes = _normalize_scopes(normalized_request.source_scopes_requested)
        if not requested_scopes:
            requested_scopes = _default_scopes_for_request(normalized_request)

        context = evidence_context or InternalChatEvidenceContext(
            candidate_evidence_metadata=list(normalized_request.candidate_evidence_metadata),
            synthetic_runtime_metadata_supplied=_has_supplied_scope_metadata(
                normalized_request.candidate_evidence_metadata,
                InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE,
            ),
            synthetic_analytics_metadata_supplied=_has_supplied_scope_metadata(
                normalized_request.candidate_evidence_metadata,
                InternalChatSourceScope.ANALYTICS_EVIDENCE,
            ),
        )
        evidence_metadata = list(context.candidate_evidence_metadata or normalized_request.candidate_evidence_metadata)
        metadata_scopes = _metadata_scopes(evidence_metadata)
        unsupported_scopes = _unsupported_scopes(requested_scopes, metadata_scopes, context)
        source_scopes_used = _source_scopes_used(requested_scopes, metadata_scopes, context, unsupported_scopes)

        support_packet = self.answer_support_service.build_support_packet(
            question_text=normalized_request.question_text,
            user_role=code_role,
            topic_tags=list(normalized_request.domain_topic_tags),
            candidate_evidence_items=_answer_support_metadata(evidence_metadata, requested_scopes),
            answer_claim=normalized_request.claimed_answer_to_validate,
        )

        blocked_claims = _dedupe(support_packet.blocked_claims + _chat_blocked_claims(normalized_request))
        required_caveats = _required_chat_caveats(support_packet.required_caveats, requested_scopes, unsupported_scopes)
        status = _chat_status(
            request=normalized_request,
            support_packet=support_packet,
            blocked_claims=blocked_claims,
            unsupported_scopes=unsupported_scopes,
        )
        answer_permitted = not blocked_claims and status not in {
            InternalChatStatus.ANSWER_NOT_PERMITTED,
            InternalChatStatus.PROHIBITED_CLAIM_BLOCKED,
        }

        summary = _deterministic_summary(status, support_packet, source_scopes_used, unsupported_scopes)
        return InternalChatResponseEnvelope(
            status=status,
            question=normalized_request.question_text,
            role=role,
            disclosure_mode=support_packet.disclosure_mode,
            source_scopes_requested=requested_scopes,
            source_scopes_used=source_scopes_used,
            unsupported_scopes=unsupported_scopes,
            evidence_support_packet=support_packet,
            evidence_summary=support_packet.evidence_summary,
            role_safe_evidence_summary=support_packet.role_safe_evidence_summary,
            required_caveats=required_caveats,
            prohibited_claims=support_packet.prohibited_claims,
            blocked_claims=blocked_claims,
            answer_permitted=answer_permitted,
            final_answer_generation_permitted=False,
            live_llm_used=False,
            final_answer_text=None,
            suggested_deterministic_summary=summary,
            no_action_attestation=dict(NO_ACTION_ATTESTATION),
            no_action_attestation_text=NO_ACTION_ATTESTATION_TEXT,
            audit_summary={
                "EnvelopeVersion": "MINERVA_INTERNAL_CHAT_ORCHESTRATOR_ENVELOPE_V0_1",
                "RequestedLiveLlm": normalized_request.allow_live_llm,
                "RequestedFinalAnswerGeneration": normalized_request.allow_final_answer_generation,
                "LiveLlmUsed": False,
                "FinalAnswerGenerationPerformed": False,
                "EvidenceMetadataCount": len(evidence_metadata),
                "RoleMappedForAnswerSupport": code_role.value,
            },
            next_step_recommendation=_next_step(status, unsupported_scopes),
        )


def _request_from_any(request: InternalChatRequest | dict[str, Any]) -> InternalChatRequest:
    if isinstance(request, InternalChatRequest):
        return request
    return InternalChatRequest(
        question_text=str(request.get("question_text") or request.get("Question") or ""),
        user_role=request.get("user_role") or request.get("Role") or InternalChatRole.PAYROLL_USER,
        source_scopes_requested=list(
            request.get("source_scopes_requested") or request.get("SourceScopesRequested") or []
        ),
        surface_context=request.get("surface_context") or request.get("SurfaceContext"),
        domain_topic_tags=list(request.get("domain_topic_tags") or request.get("DomainTopicTags") or []),
        candidate_evidence_metadata=list(
            request.get("candidate_evidence_metadata") or request.get("CandidateEvidenceMetadata") or []
        ),
        claimed_answer_to_validate=request.get("claimed_answer_to_validate")
        or request.get("ClaimedAnswerToValidate"),
        allow_final_answer_generation=bool(
            request.get("allow_final_answer_generation") or request.get("AllowFinalAnswerGeneration")
        ),
        allow_live_llm=bool(request.get("allow_live_llm") or request.get("AllowLiveLlm")),
    )


def _normalize_internal_role(role: InternalChatRole | str) -> InternalChatRole:
    if isinstance(role, InternalChatRole):
        return role
    try:
        return InternalChatRole(str(role).upper())
    except ValueError:
        return InternalChatRole.PAYROLL_USER


def _code_evidence_role_for_chat_role(role: InternalChatRole) -> CodeEvidenceRole:
    mapping = {
        InternalChatRole.DEVELOPER: CodeEvidenceRole.DEVELOPER,
        InternalChatRole.PAYROLL_ADMINISTRATOR: CodeEvidenceRole.PAYROLL_ADMINISTRATOR,
        InternalChatRole.PAYROLL_MANAGER: CodeEvidenceRole.PAYROLL_ADMINISTRATOR,
        InternalChatRole.PAYROLL_USER: CodeEvidenceRole.PAYROLL_USER,
        InternalChatRole.CUSTOMER_ADMINISTRATOR: CodeEvidenceRole.CUSTOMER_ADMINISTRATOR,
        InternalChatRole.WORKER: CodeEvidenceRole.WORKER,
        InternalChatRole.ANALYTICS_USER: CodeEvidenceRole.PAYROLL_USER,
    }
    return mapping[role]


def _normalize_scopes(scopes: list[InternalChatSourceScope | str]) -> list[InternalChatSourceScope]:
    normalized: list[InternalChatSourceScope] = []
    for scope in scopes:
        if isinstance(scope, InternalChatSourceScope):
            normalized_scope = scope
        else:
            try:
                normalized_scope = InternalChatSourceScope(str(scope).upper())
            except ValueError:
                continue
        if normalized_scope not in normalized:
            normalized.append(normalized_scope)
    return normalized


def _default_scopes_for_request(request: InternalChatRequest) -> list[InternalChatSourceScope]:
    scopes = [
        InternalChatSourceScope.PLATFORM_KNOWLEDGE,
        InternalChatSourceScope.IMPLEMENTATION_STATE,
    ]
    text = _normalize_text(" ".join([request.question_text, request.claimed_answer_to_validate or ""]))
    if "code" in text or request.candidate_evidence_metadata:
        scopes.extend(
            [
                InternalChatSourceScope.CODE_EVIDENCE,
                InternalChatSourceScope.TEST_EVIDENCE,
                InternalChatSourceScope.PROMPT_ARTEFACTS,
                InternalChatSourceScope.EVALUATION_BASELINES,
            ]
        )
    return scopes


def _metadata_scopes(metadata: list[dict[str, Any]]) -> set[InternalChatSourceScope]:
    scopes: set[InternalChatSourceScope] = set()
    for item in metadata:
        scope = _scope_for_metadata_item(item)
        if scope:
            scopes.add(scope)
    return scopes


def _scope_for_metadata_item(item: dict[str, Any]) -> InternalChatSourceScope | None:
    requested_scope = item.get("source_scope") or item.get("scope")
    if requested_scope:
        try:
            return InternalChatSourceScope(str(requested_scope).upper())
        except ValueError:
            pass
    category = str(item.get("evidence_category") or item.get("category") or item.get("source_type") or "").upper()
    if category in {"DOCTRINE", "KNOWLEDGE", "KNOWLEDGE_DOC", "SLICE_KNOWLEDGE_DOC"}:
        return InternalChatSourceScope.PLATFORM_KNOWLEDGE
    if "IMPLEMENTATION_STATE" in category:
        return InternalChatSourceScope.IMPLEMENTATION_STATE
    if category in {"CODE", "PYTHON_FILE", "TYPESCRIPT_FILE", "ROUTE_DEFINITION", "SERVICE_CLASS", "FUNCTION"}:
        return InternalChatSourceScope.CODE_EVIDENCE
    if category in {"TEST", "TEST_FILE", "TEST_EVIDENCE"}:
        return InternalChatSourceScope.TEST_EVIDENCE
    if category in {"PROMPT", "PROMPT_ARTEFACT", "PROMPT_ARTIFACT"}:
        return InternalChatSourceScope.PROMPT_ARTEFACTS
    if category in {"EVALUATION", "EVALUATION_DOC", "EVALUATION_BASELINE"}:
        return InternalChatSourceScope.EVALUATION_BASELINES
    if category in {"RUNTIME", "RUNTIME_OBJECT", "RUNTIME_OBJECT_EVIDENCE"}:
        return InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE
    if category in {"ANALYTICS", "ANALYTICS_EVIDENCE"}:
        return InternalChatSourceScope.ANALYTICS_EVIDENCE
    return None


def _has_supplied_scope_metadata(metadata: list[dict[str, Any]], scope: InternalChatSourceScope) -> bool:
    return any(_scope_for_metadata_item(item) == scope for item in metadata)


def _unsupported_scopes(
    requested_scopes: list[InternalChatSourceScope],
    metadata_scopes: set[InternalChatSourceScope],
    context: InternalChatEvidenceContext,
) -> list[InternalChatSourceScope]:
    unsupported: list[InternalChatSourceScope] = []
    for scope in requested_scopes:
        if scope in SUPPORTED_METADATA_SCOPES:
            continue
        if scope == InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE:
            if not context.synthetic_runtime_metadata_supplied and scope not in metadata_scopes:
                unsupported.append(scope)
        elif scope == InternalChatSourceScope.ANALYTICS_EVIDENCE:
            if not context.synthetic_analytics_metadata_supplied and scope not in metadata_scopes:
                unsupported.append(scope)
        else:
            unsupported.append(scope)
    return unsupported


def _source_scopes_used(
    requested_scopes: list[InternalChatSourceScope],
    metadata_scopes: set[InternalChatSourceScope],
    context: InternalChatEvidenceContext,
    unsupported_scopes: list[InternalChatSourceScope],
) -> list[InternalChatSourceScope]:
    used: list[InternalChatSourceScope] = []
    for scope in requested_scopes:
        if scope in unsupported_scopes:
            continue
        if scope in SUPPORTED_METADATA_SCOPES and (scope in metadata_scopes or not metadata_scopes):
            used.append(scope)
        elif scope == InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE and context.synthetic_runtime_metadata_supplied:
            used.append(scope)
        elif scope == InternalChatSourceScope.ANALYTICS_EVIDENCE and context.synthetic_analytics_metadata_supplied:
            used.append(scope)
    return used


def _answer_support_metadata(
    metadata: list[dict[str, Any]],
    requested_scopes: list[InternalChatSourceScope],
) -> list[dict[str, Any]]:
    allowed = SUPPORTED_METADATA_SCOPES & set(requested_scopes)
    return [
        item
        for item in metadata
        if (_scope_for_metadata_item(item) in allowed or _scope_for_metadata_item(item) is None)
    ]


def _chat_blocked_claims(request: InternalChatRequest) -> list[str]:
    text = _normalize_text(" ".join([request.question_text, request.claimed_answer_to_validate or ""]))
    blocked: list[str] = []
    if _contains_payroll_calculation_request(text):
        blocked.append("payroll calculation request blocked")
    if _contains_write_action_request(text):
        blocked.append("write action request blocked")
    if any(term in text for term in RAW_CODE_TERMS):
        role = _normalize_internal_role(request.user_role)
        if role in {InternalChatRole.PAYROLL_USER, InternalChatRole.CUSTOMER_ADMINISTRATOR, InternalChatRole.WORKER}:
            blocked.append("raw code disclosure request blocked")
    return blocked


def _contains_payroll_calculation_request(text: str) -> bool:
    terms = set(text.split())
    if not ({"calculate", "calculated", "calculation", "compute", "computed"} & terms):
        return False
    return bool(CALCULATION_TERMS & terms)


def _contains_write_action_request(text: str) -> bool:
    terms = set(text.split())
    if not (ACTION_TERMS & terms):
        return False
    if "please" in terms or "now" in terms or "for" in terms and "me" in terms:
        return True
    return bool({"approve", "authorise", "authorize", "delete", "edit", "finalise", "finalize", "save", "submit", "update", "write"} & terms)


def _required_chat_caveats(
    support_caveats: list[str],
    requested_scopes: list[InternalChatSourceScope],
    unsupported_scopes: list[InternalChatSourceScope],
) -> list[str]:
    caveats = list(support_caveats)
    if InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE in requested_scopes:
        caveats.append(
            "Runtime object evidence is recognised in v0.1 but is not fetched; it must be supplied as safe synthetic metadata."
        )
    if InternalChatSourceScope.ANALYTICS_EVIDENCE in requested_scopes:
        caveats.append(
            "Analytics evidence is recognised as a registered future scope and is inactive by default in v0.1 unless safe synthetic metadata is supplied."
        )
    if unsupported_scopes:
        caveats.append("Unsupported or unavailable scopes require a later runtime, analytics, or evidence-ingestion slice.")
    caveats.append("Final natural-language answer generation remains disabled for this v0.1 envelope.")
    caveats.append("Live LLM calls remain disabled for this v0.1 envelope.")
    return _dedupe(caveats)


def _chat_status(
    *,
    request: InternalChatRequest,
    support_packet: CodeEvidenceAnswerSupportPacket,
    blocked_claims: list[str],
    unsupported_scopes: list[InternalChatSourceScope],
) -> InternalChatStatus:
    if blocked_claims:
        return InternalChatStatus.PROHIBITED_CLAIM_BLOCKED
    if request.allow_live_llm:
        return InternalChatStatus.LIVE_LLM_DISABLED
    if request.allow_final_answer_generation:
        return InternalChatStatus.FINAL_ANSWER_GENERATION_DISABLED
    if support_packet.support_status == CodeEvidenceSupportStatus.PROHIBITED_CLAIM_BLOCKED:
        return InternalChatStatus.PROHIBITED_CLAIM_BLOCKED
    if support_packet.support_status == CodeEvidenceSupportStatus.ROLE_RESTRICTED:
        return InternalChatStatus.ROLE_RESTRICTED
    if support_packet.support_status == CodeEvidenceSupportStatus.NEEDS_RUNTIME_EVIDENCE:
        return InternalChatStatus.NEEDS_MORE_EVIDENCE
    if unsupported_scopes:
        if InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE in unsupported_scopes and _question_mentions_runtime(request):
            return InternalChatStatus.NEEDS_MORE_EVIDENCE
        return InternalChatStatus.UNSUPPORTED_SCOPE
    if support_packet.support_status == CodeEvidenceSupportStatus.UNSUPPORTED:
        return InternalChatStatus.NEEDS_MORE_EVIDENCE
    return InternalChatStatus.ANSWER_SUPPORT_BUILT


def _question_mentions_runtime(request: InternalChatRequest) -> bool:
    terms = set(_normalize_text(" ".join([request.question_text, request.claimed_answer_to_validate or ""])).split())
    return bool(RUNTIME_SCOPE_TERMS & terms)


def _deterministic_summary(
    status: InternalChatStatus,
    support_packet: CodeEvidenceAnswerSupportPacket,
    used_scopes: list[InternalChatSourceScope],
    unsupported_scopes: list[InternalChatSourceScope],
) -> str:
    used = ", ".join(scope.value for scope in used_scopes) or "none"
    unsupported = ", ".join(scope.value for scope in unsupported_scopes) or "none"
    return (
        f"Deterministic envelope status {status.value}; answer support "
        f"{support_packet.support_status.value}; used scopes: {used}; "
        f"unsupported scopes: {unsupported}; final answer generation disabled."
    )


def _next_step(status: InternalChatStatus, unsupported_scopes: list[InternalChatSourceScope]) -> str:
    if status == InternalChatStatus.PROHIBITED_CLAIM_BLOCKED:
        return "Do not answer the blocked claim or action request; collect permitted evidence and reformulate as a read-only question."
    if InternalChatSourceScope.RUNTIME_OBJECT_EVIDENCE in unsupported_scopes:
        return "Supply authorised runtime object evidence in a later slice before answering object, tenant, live, or production questions."
    if InternalChatSourceScope.ANALYTICS_EVIDENCE in unsupported_scopes:
        return "Keep analytics interpretation deferred until an analytics evidence intake slice supplies safe metadata."
    if status in {InternalChatStatus.LIVE_LLM_DISABLED, InternalChatStatus.FINAL_ANSWER_GENERATION_DISABLED}:
        return "Keep the response as an internal deterministic envelope; do not call a live LLM or generate final answer text."
    return "Use this envelope for internal review or a later controlled Ask Minerva answer-generation slice."


def _normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower().replace("_", " ").replace("-", " ")).strip()


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped
