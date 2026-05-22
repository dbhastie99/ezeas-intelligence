from dataclasses import asdict, dataclass, field
from enum import StrEnum
import re
from typing import Any

from app.services.code_evidence_answer_policy_service import (
    CodeEvidenceAnswerPolicy,
    CodeEvidenceAnswerPolicyService,
    CodeEvidenceDisclosureMode,
    CodeEvidenceRole,
)
from app.services.code_evidence_inventory_service import (
    CodeEvidenceInventory,
    CodeEvidenceItem,
    CodeEvidenceItemType,
)


class CodeEvidenceSupportStatus(StrEnum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    NEEDS_IMPLEMENTATION_STATE_REVIEW = "NEEDS_IMPLEMENTATION_STATE_REVIEW"
    NEEDS_RUNTIME_EVIDENCE = "NEEDS_RUNTIME_EVIDENCE"
    ROLE_RESTRICTED = "ROLE_RESTRICTED"
    PROHIBITED_CLAIM_BLOCKED = "PROHIBITED_CLAIM_BLOCKED"


class CodeEvidenceSupportCategory(StrEnum):
    DOCTRINE = "DOCTRINE"
    IMPLEMENTATION_STATE = "IMPLEMENTATION_STATE"
    CODE = "CODE"
    TEST = "TEST"
    PROMPT = "PROMPT"
    KNOWLEDGE = "KNOWLEDGE"
    EVALUATION = "EVALUATION"


NO_ACTION_ATTESTATION = (
    "No code executed; no DB accessed; no external repo mutated; no live LLM called; "
    "no final user-facing answer generated; no payroll calculation performed; no UI, "
    "runtime integration, migration, or production/customer enablement occurred."
)

CODE_CANNOT_PROVE_RUNTIME_CAVEAT = (
    "Code evidence can support implementation confidence, but code evidence alone "
    "cannot prove production availability, customer availability, runtime enablement, "
    "deployed schema state, permissions, live object state, payroll result correctness, "
    "payment, or finalisation."
)

PROHIBITED_CLAIM_PATTERNS = {
    "code proves production readiness": re.compile(r"\bcode(?:\s+evidence)?\s+proves?\s+production\s+readiness\b"),
    "code proves production availability": re.compile(r"\bcode(?:\s+evidence)?\s+proves?\s+production\s+availability\b"),
    "code proves customer availability": re.compile(r"\bcode(?:\s+evidence)?\s+proves?\s+customer\s+availability\b"),
    "code proves migration applied": re.compile(r"\bcode(?:\s+evidence)?\s+proves?\s+.*\bmigration\s+(?:has\s+)?(?:been\s+)?applied\b"),
    "code proves runtime object state": re.compile(r"\bcode(?:\s+evidence)?\s+proves?\s+.*\bruntime\s+object\s+state\b"),
    "code proves payroll result correctness": re.compile(r"\bcode(?:\s+evidence)?\s+proves?\s+.*\bpayroll\s+(?:result\s+)?correctness\b"),
    "code proves finalisation or payment occurred": re.compile(
        r"\bcode(?:\s+evidence)?\s+proves?\s+.*\b(finalisation|finalization|payment)\s+occurred\b"
    ),
    "minerva calculated payroll": re.compile(r"\bminerva\s+calculated\s+payroll\b"),
    "minerva authorised payroll": re.compile(r"\bminerva\s+authori[sz]ed\s+payroll\b"),
    "tests passing means production enabled": re.compile(
        r"\btests?\s+passing\s+means\s+.*\bproduction\s+(?:is\s+)?enabled\b"
    ),
    "route file means route is deployed": re.compile(r"\broute\s+file\s+means\s+.*\broute\s+is\s+deployed\b"),
}

RUNTIME_AVAILABILITY_TERMS = {
    "available",
    "availability",
    "customer",
    "tenant",
    "live",
    "production",
    "runtime",
    "deployed",
    "enabled",
    "enablement",
}

STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "are",
    "can",
    "does",
    "for",
    "from",
    "has",
    "have",
    "how",
    "implemented",
    "into",
    "is",
    "its",
    "now",
    "should",
    "that",
    "the",
    "this",
    "what",
    "when",
    "where",
    "which",
    "with",
    "you",
}


@dataclass(frozen=True)
class CodeEvidenceQuestionContext:
    question_text: str
    user_role: CodeEvidenceRole | str
    domain_key: str | None = None
    topic_tags: list[str] = field(default_factory=list)
    query_intent: str | None = None
    expected_doctrine_terms: list[str] = field(default_factory=list)
    implementation_state_terms: list[str] = field(default_factory=list)
    answer_claim: str | None = None

    def model_dump(self) -> dict:
        payload = asdict(self)
        payload["user_role"] = (
            self.user_role.value if isinstance(self.user_role, CodeEvidenceRole) else str(self.user_role)
        )
        return payload


@dataclass(frozen=True)
class CodeEvidenceSupportSource:
    source_type: str
    evidence_category: CodeEvidenceSupportCategory | str
    title: str
    repo_name: str | None = None
    repo_family: str | None = None
    file_path: str | None = None
    symbol_name: str | None = None
    route_path: str | None = None
    test_name: str | None = None
    evidence_tags: list[str] = field(default_factory=list)
    summary: str | None = None
    matched_terms: list[str] = field(default_factory=list)

    def model_dump(self) -> dict:
        payload = asdict(self)
        payload["evidence_category"] = (
            self.evidence_category.value
            if isinstance(self.evidence_category, CodeEvidenceSupportCategory)
            else str(self.evidence_category)
        )
        return payload


@dataclass(frozen=True)
class CodeEvidenceSupportFinding:
    evidence_category: CodeEvidenceSupportCategory
    source_count: int
    matched_terms: list[str] = field(default_factory=list)
    finding_summary: str = ""

    def model_dump(self) -> dict:
        payload = asdict(self)
        payload["evidence_category"] = self.evidence_category.value
        return payload


@dataclass(frozen=True)
class CodeEvidenceAnswerSupportPacket:
    support_status: CodeEvidenceSupportStatus
    disclosure_mode: CodeEvidenceDisclosureMode
    doctrine_evidence: list[CodeEvidenceSupportSource]
    implementation_state_evidence: list[CodeEvidenceSupportSource]
    code_evidence: list[CodeEvidenceSupportSource]
    test_evidence: list[CodeEvidenceSupportSource]
    prompt_evidence: list[CodeEvidenceSupportSource]
    knowledge_evidence: list[CodeEvidenceSupportSource]
    findings: list[CodeEvidenceSupportFinding]
    evidence_summary: str
    role_safe_evidence_summary: str
    withheld_evidence: list[str]
    required_caveats: list[str]
    prohibited_claims: list[str]
    blocked_claims: list[str]
    runtime_availability_caveat_required: bool
    code_cannot_prove_runtime_caveat: str
    answer_permitted: bool
    final_answer_generation_permitted: bool
    no_action_attestation: str

    def model_dump(self) -> dict:
        return {
            "support_status": self.support_status.value,
            "disclosure_mode": self.disclosure_mode.value,
            "doctrine_evidence": [source.model_dump() for source in self.doctrine_evidence],
            "implementation_state_evidence": [
                source.model_dump() for source in self.implementation_state_evidence
            ],
            "code_evidence": [source.model_dump() for source in self.code_evidence],
            "test_evidence": [source.model_dump() for source in self.test_evidence],
            "prompt_evidence": [source.model_dump() for source in self.prompt_evidence],
            "knowledge_evidence": [source.model_dump() for source in self.knowledge_evidence],
            "findings": [finding.model_dump() for finding in self.findings],
            "evidence_summary": self.evidence_summary,
            "role_safe_evidence_summary": self.role_safe_evidence_summary,
            "withheld_evidence": list(self.withheld_evidence),
            "required_caveats": list(self.required_caveats),
            "prohibited_claims": list(self.prohibited_claims),
            "blocked_claims": list(self.blocked_claims),
            "runtime_availability_caveat_required": self.runtime_availability_caveat_required,
            "code_cannot_prove_runtime_caveat": self.code_cannot_prove_runtime_caveat,
            "answer_permitted": self.answer_permitted,
            "final_answer_generation_permitted": self.final_answer_generation_permitted,
            "no_action_attestation": self.no_action_attestation,
        }


class CodeEvidenceAnswerSupportService:
    def __init__(self, policy_service: CodeEvidenceAnswerPolicyService | None = None) -> None:
        self.policy_service = policy_service or CodeEvidenceAnswerPolicyService()

    def build_support_packet(
        self,
        question_text: str | None = None,
        *,
        query_intent: str | None = None,
        domain_key: str | None = None,
        topic_tags: list[str] | None = None,
        user_role: CodeEvidenceRole | str,
        expected_doctrine_terms: list[str] | None = None,
        implementation_state_terms: list[str] | None = None,
        code_evidence_inventory: CodeEvidenceInventory | list[CodeEvidenceItem] | None = None,
        candidate_evidence_items: list[CodeEvidenceSupportSource | CodeEvidenceItem | dict[str, Any]] | None = None,
        answer_claim: str | None = None,
    ) -> CodeEvidenceAnswerSupportPacket:
        context = CodeEvidenceQuestionContext(
            question_text=question_text or query_intent or "",
            user_role=user_role,
            domain_key=domain_key,
            topic_tags=list(topic_tags or []),
            query_intent=query_intent,
            expected_doctrine_terms=list(expected_doctrine_terms or []),
            implementation_state_terms=list(implementation_state_terms or []),
            answer_claim=answer_claim,
        )
        policy = self.policy_service.policy_for_role(user_role)
        terms = _query_terms(context)
        raw_sources = _matching_sources(
            _sources_from_inventory(code_evidence_inventory) + _sources_from_candidates(candidate_evidence_items),
            terms,
        )

        categorized = _categorize_sources(raw_sources)
        blocked_claims = _blocked_claims(context)
        runtime_claim = _contains_runtime_availability_claim(context)
        has_runtime_evidence = any(_category(source) == "RUNTIME" for source in raw_sources)
        status = _support_status(policy, categorized, blocked_claims, runtime_claim, has_runtime_evidence)

        visible_sources, withheld_evidence = _role_filter_sources(categorized, policy)
        findings = _findings(categorized)
        evidence_summary = _evidence_summary(visible_sources, policy, technical=True)
        role_safe_summary = _evidence_summary(visible_sources, policy, technical=False)
        required_caveats = _required_caveats(policy, status, runtime_claim, categorized)

        return CodeEvidenceAnswerSupportPacket(
            support_status=status,
            disclosure_mode=policy.disclosure_mode,
            doctrine_evidence=visible_sources[CodeEvidenceSupportCategory.DOCTRINE],
            implementation_state_evidence=visible_sources[CodeEvidenceSupportCategory.IMPLEMENTATION_STATE],
            code_evidence=visible_sources[CodeEvidenceSupportCategory.CODE],
            test_evidence=visible_sources[CodeEvidenceSupportCategory.TEST],
            prompt_evidence=visible_sources[CodeEvidenceSupportCategory.PROMPT],
            knowledge_evidence=visible_sources[CodeEvidenceSupportCategory.KNOWLEDGE],
            findings=findings,
            evidence_summary=evidence_summary,
            role_safe_evidence_summary=role_safe_summary,
            withheld_evidence=withheld_evidence,
            required_caveats=required_caveats,
            prohibited_claims=_all_prohibited_claims(self.policy_service),
            blocked_claims=blocked_claims,
            runtime_availability_caveat_required=_has_code_or_test_evidence(categorized) or runtime_claim,
            code_cannot_prove_runtime_caveat=CODE_CANNOT_PROVE_RUNTIME_CAVEAT,
            answer_permitted=status != CodeEvidenceSupportStatus.PROHIBITED_CLAIM_BLOCKED,
            final_answer_generation_permitted=False,
            no_action_attestation=NO_ACTION_ATTESTATION,
        )


def _sources_from_inventory(
    inventory: CodeEvidenceInventory | list[CodeEvidenceItem] | None,
) -> list[CodeEvidenceSupportSource]:
    if inventory is None:
        return []
    items = inventory.items if isinstance(inventory, CodeEvidenceInventory) else inventory
    return [_source_from_inventory_item(item) for item in items]


def _sources_from_candidates(
    candidates: list[CodeEvidenceSupportSource | CodeEvidenceItem | dict[str, Any]] | None,
) -> list[CodeEvidenceSupportSource]:
    sources: list[CodeEvidenceSupportSource] = []
    for candidate in candidates or []:
        if isinstance(candidate, CodeEvidenceSupportSource):
            sources.append(candidate)
        elif isinstance(candidate, CodeEvidenceItem):
            sources.append(_source_from_inventory_item(candidate))
        else:
            sources.append(_source_from_dict(candidate))
    return sources


def _source_from_inventory_item(item: CodeEvidenceItem) -> CodeEvidenceSupportSource:
    category = _category_for_inventory_item(item)
    title = item.symbol_name or item.test_name or item.route_path or item.file_path
    return CodeEvidenceSupportSource(
        source_type=item.item_type.value,
        evidence_category=category,
        title=title,
        repo_name=item.repo_name,
        repo_family=item.repo_family,
        file_path=item.file_path,
        symbol_name=item.symbol_name,
        route_path=item.route_path,
        test_name=item.test_name,
        evidence_tags=list(item.evidence_tags),
    )


def _source_from_dict(payload: dict[str, Any]) -> CodeEvidenceSupportSource:
    category = payload.get("evidence_category") or payload.get("category") or payload.get("source_category")
    source_type = str(payload.get("source_type") or category or "UNKNOWN")
    return CodeEvidenceSupportSource(
        source_type=source_type,
        evidence_category=_normalize_category(str(category or source_type)),
        title=str(payload.get("title") or payload.get("name") or payload.get("file_path") or source_type),
        repo_name=_optional_str(payload.get("repo_name")),
        repo_family=_optional_str(payload.get("repo_family")),
        file_path=_optional_str(payload.get("file_path")),
        symbol_name=_optional_str(payload.get("symbol_name")),
        route_path=_optional_str(payload.get("route_path")),
        test_name=_optional_str(payload.get("test_name")),
        evidence_tags=[str(tag) for tag in payload.get("evidence_tags", payload.get("tags", []))],
        summary=_optional_str(payload.get("summary")),
    )


def _category_for_inventory_item(item: CodeEvidenceItem) -> CodeEvidenceSupportCategory:
    lower_path = item.file_path.lower()
    if "implementation_state" in lower_path or "implementation-state" in lower_path:
        return CodeEvidenceSupportCategory.IMPLEMENTATION_STATE
    if item.item_type == CodeEvidenceItemType.TEST_FILE:
        return CodeEvidenceSupportCategory.TEST
    if item.item_type == CodeEvidenceItemType.PROMPT_ARTEFACT:
        return CodeEvidenceSupportCategory.PROMPT
    if item.item_type in {CodeEvidenceItemType.KNOWLEDGE_DOC, CodeEvidenceItemType.SLICE_KNOWLEDGE_DOC}:
        return CodeEvidenceSupportCategory.KNOWLEDGE
    if item.item_type == CodeEvidenceItemType.EVALUATION_DOC:
        return CodeEvidenceSupportCategory.EVALUATION
    return CodeEvidenceSupportCategory.CODE


def _normalize_category(value: str) -> CodeEvidenceSupportCategory:
    normalized = value.upper().replace("-", "_").replace(" ", "_")
    aliases = {
        "DOCTRINE_EVIDENCE": CodeEvidenceSupportCategory.DOCTRINE,
        "KNOWLEDGE_DOC": CodeEvidenceSupportCategory.KNOWLEDGE,
        "SLICE_KNOWLEDGE_DOC": CodeEvidenceSupportCategory.KNOWLEDGE,
        "IMPLEMENTATION_STATE_DOC": CodeEvidenceSupportCategory.IMPLEMENTATION_STATE,
        "IMPLEMENTATION_STATE_EVIDENCE": CodeEvidenceSupportCategory.IMPLEMENTATION_STATE,
        "TEST_FILE": CodeEvidenceSupportCategory.TEST,
        "TEST_EVIDENCE": CodeEvidenceSupportCategory.TEST,
        "PYTHON_FILE": CodeEvidenceSupportCategory.CODE,
        "TYPESCRIPT_FILE": CodeEvidenceSupportCategory.CODE,
        "ROUTE_DEFINITION": CodeEvidenceSupportCategory.CODE,
        "SERVICE_CLASS": CodeEvidenceSupportCategory.CODE,
        "FUNCTION": CodeEvidenceSupportCategory.CODE,
        "SCHEMA_CLASS": CodeEvidenceSupportCategory.CODE,
        "PROMPT_ARTEFACT": CodeEvidenceSupportCategory.PROMPT,
        "PROMPT_ARTIFACT": CodeEvidenceSupportCategory.PROMPT,
        "EVALUATION_DOC": CodeEvidenceSupportCategory.EVALUATION,
    }
    if normalized in aliases:
        return aliases[normalized]
    try:
        return CodeEvidenceSupportCategory(normalized)
    except ValueError:
        return CodeEvidenceSupportCategory.CODE


def _query_terms(context: CodeEvidenceQuestionContext) -> list[str]:
    terms: list[str] = []
    terms.extend(context.topic_tags)
    terms.extend(context.expected_doctrine_terms)
    terms.extend(context.implementation_state_terms)
    for value in [context.domain_key, context.query_intent, context.question_text, context.answer_claim]:
        terms.extend(_tokens(value or ""))
    unique_terms: list[str] = []
    for term in terms:
        normalized = _normalize_text(term)
        if normalized and normalized not in unique_terms:
            unique_terms.append(normalized)
    return unique_terms


def _tokens(text: str) -> list[str]:
    normalized = _normalize_text(text)
    return [
        token
        for token in re.findall(r"[a-z0-9]+", normalized)
        if len(token) > 2 and token not in STOPWORDS
    ]


def _matching_sources(sources: list[CodeEvidenceSupportSource], terms: list[str]) -> list[CodeEvidenceSupportSource]:
    if not terms:
        return sources
    matched_sources: list[CodeEvidenceSupportSource] = []
    for source in sources:
        haystack = _source_haystack(source)
        matched_terms = [term for term in terms if term in haystack]
        if matched_terms:
            matched_sources.append(
                CodeEvidenceSupportSource(
                    **{**source.model_dump(), "matched_terms": matched_terms}
                )
            )
    return matched_sources


def _source_haystack(source: CodeEvidenceSupportSource) -> str:
    return _normalize_text(
        " ".join(
            value
            for value in [
                source.source_type,
                str(source.evidence_category),
                source.title,
                source.repo_name,
                source.repo_family,
                source.file_path,
                source.symbol_name,
                source.route_path,
                source.test_name,
                " ".join(source.evidence_tags),
                source.summary,
            ]
            if value
        )
    )


def _categorize_sources(
    sources: list[CodeEvidenceSupportSource],
) -> dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]]:
    categorized = {category: [] for category in CodeEvidenceSupportCategory}
    for source in sources:
        category = _normalize_category(str(source.evidence_category))
        if category == CodeEvidenceSupportCategory.EVALUATION:
            categorized[CodeEvidenceSupportCategory.KNOWLEDGE].append(source)
        else:
            categorized[category].append(source)
    return categorized


def _blocked_claims(context: CodeEvidenceQuestionContext) -> list[str]:
    text = _normalize_text(" ".join(value for value in [context.question_text, context.answer_claim] if value))
    return [label for label, pattern in PROHIBITED_CLAIM_PATTERNS.items() if pattern.search(text)]


def _contains_runtime_availability_claim(context: CodeEvidenceQuestionContext) -> bool:
    text = set(_tokens(" ".join(value for value in [context.question_text, context.answer_claim] if value)))
    return bool(text & RUNTIME_AVAILABILITY_TERMS)


def _support_status(
    policy: CodeEvidenceAnswerPolicy,
    categorized: dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]],
    blocked_claims: list[str],
    runtime_claim: bool,
    has_runtime_evidence: bool,
) -> CodeEvidenceSupportStatus:
    if blocked_claims:
        return CodeEvidenceSupportStatus.PROHIBITED_CLAIM_BLOCKED
    if runtime_claim and _has_code_or_test_evidence(categorized) and not has_runtime_evidence:
        return CodeEvidenceSupportStatus.NEEDS_RUNTIME_EVIDENCE
    if not policy.may_use_code_evidence and _has_code_or_test_evidence(categorized):
        return CodeEvidenceSupportStatus.ROLE_RESTRICTED

    has_implementation_state = bool(categorized[CodeEvidenceSupportCategory.IMPLEMENTATION_STATE])
    has_code = bool(categorized[CodeEvidenceSupportCategory.CODE])
    has_test = bool(categorized[CodeEvidenceSupportCategory.TEST])
    has_doctrine_or_knowledge = bool(
        categorized[CodeEvidenceSupportCategory.DOCTRINE]
        or categorized[CodeEvidenceSupportCategory.KNOWLEDGE]
        or categorized[CodeEvidenceSupportCategory.PROMPT]
    )

    if has_implementation_state and has_code and has_test:
        return CodeEvidenceSupportStatus.SUPPORTED
    if has_code and not has_implementation_state:
        return CodeEvidenceSupportStatus.NEEDS_IMPLEMENTATION_STATE_REVIEW
    if has_doctrine_or_knowledge or has_test or has_implementation_state:
        return CodeEvidenceSupportStatus.PARTIALLY_SUPPORTED
    return CodeEvidenceSupportStatus.UNSUPPORTED


def _role_filter_sources(
    categorized: dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]],
    policy: CodeEvidenceAnswerPolicy,
) -> tuple[dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]], list[str]]:
    visible = {category: [] for category in CodeEvidenceSupportCategory}
    withheld: list[str] = []
    for category, sources in categorized.items():
        if category == CodeEvidenceSupportCategory.EVALUATION:
            continue
        for source in sources:
            allowed, reason = _source_allowed_for_role(category, policy)
            if allowed:
                visible[category].append(_sanitize_source(source, policy, category))
            else:
                withheld.append(reason)
    return visible, sorted(set(withheld))


def _source_allowed_for_role(
    category: CodeEvidenceSupportCategory,
    policy: CodeEvidenceAnswerPolicy,
) -> tuple[bool, str]:
    if category in {CodeEvidenceSupportCategory.CODE, CodeEvidenceSupportCategory.TEST, CodeEvidenceSupportCategory.PROMPT}:
        if not policy.may_use_code_evidence:
            return False, "code/test/prompt evidence withheld because the role uses NO_CODE_EVIDENCE"
    return True, ""


def _sanitize_source(
    source: CodeEvidenceSupportSource,
    policy: CodeEvidenceAnswerPolicy,
    category: CodeEvidenceSupportCategory,
) -> CodeEvidenceSupportSource:
    repo_name = source.repo_name if policy.can_show_repo_names else None
    file_path = source.file_path if policy.can_show_file_paths else None
    symbol_name = source.symbol_name if policy.can_show_symbol_names else None
    route_path = source.route_path if policy.can_show_route_paths else None
    test_name = source.test_name if policy.can_show_test_names else None
    title = _visible_title(source, policy, category)
    return CodeEvidenceSupportSource(
        source_type=source.source_type,
        evidence_category=category,
        title=title,
        repo_name=repo_name,
        repo_family=source.repo_family if policy.can_show_repo_names else None,
        file_path=file_path,
        symbol_name=symbol_name,
        route_path=route_path,
        test_name=test_name,
        evidence_tags=list(source.evidence_tags),
        summary=_visible_summary(source, policy, category),
        matched_terms=list(source.matched_terms),
    )


def _visible_title(
    source: CodeEvidenceSupportSource,
    policy: CodeEvidenceAnswerPolicy,
    category: CodeEvidenceSupportCategory,
) -> str:
    if policy.disclosure_mode == CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE:
        return source.title
    if category == CodeEvidenceSupportCategory.TEST and policy.can_show_test_names:
        return source.test_name or source.title
    if category == CodeEvidenceSupportCategory.CODE and policy.can_show_file_paths:
        return source.file_path or "implementation evidence"
    if category == CodeEvidenceSupportCategory.IMPLEMENTATION_STATE and policy.can_show_file_paths:
        return source.file_path or source.title
    if category in {CodeEvidenceSupportCategory.DOCTRINE, CodeEvidenceSupportCategory.KNOWLEDGE}:
        return source.title if not policy.background_confidence_only else "approved knowledge evidence"
    return f"{category.value.lower()} evidence"


def _visible_summary(
    source: CodeEvidenceSupportSource,
    policy: CodeEvidenceAnswerPolicy,
    category: CodeEvidenceSupportCategory,
) -> str | None:
    if policy.disclosure_mode == CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE:
        return source.summary
    if category in {CodeEvidenceSupportCategory.CODE, CodeEvidenceSupportCategory.TEST, CodeEvidenceSupportCategory.PROMPT}:
        if policy.background_confidence_only:
            return "Evidence may affect confidence only and is not exposed to this role."
        if policy.customer_safe:
            return "Customer-safe implementation confirmation only; internal identifiers are withheld."
        return "Implementation evidence is available without raw code snippets."
    return source.summary


def _findings(
    categorized: dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]],
) -> list[CodeEvidenceSupportFinding]:
    findings: list[CodeEvidenceSupportFinding] = []
    for category in [
        CodeEvidenceSupportCategory.DOCTRINE,
        CodeEvidenceSupportCategory.IMPLEMENTATION_STATE,
        CodeEvidenceSupportCategory.CODE,
        CodeEvidenceSupportCategory.TEST,
        CodeEvidenceSupportCategory.PROMPT,
        CodeEvidenceSupportCategory.KNOWLEDGE,
    ]:
        sources = categorized[category]
        matched_terms = sorted({term for source in sources for term in source.matched_terms})
        summary = f"{len(sources)} {category.value.lower().replace('_', ' ')} source(s) matched."
        findings.append(
            CodeEvidenceSupportFinding(
                evidence_category=category,
                source_count=len(sources),
                matched_terms=matched_terms,
                finding_summary=summary,
            )
        )
    return findings


def _evidence_summary(
    visible_sources: dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]],
    policy: CodeEvidenceAnswerPolicy,
    *,
    technical: bool,
) -> str:
    counts = {
        category.value.lower(): len(visible_sources[category])
        for category in [
            CodeEvidenceSupportCategory.DOCTRINE,
            CodeEvidenceSupportCategory.IMPLEMENTATION_STATE,
            CodeEvidenceSupportCategory.CODE,
            CodeEvidenceSupportCategory.TEST,
            CodeEvidenceSupportCategory.PROMPT,
            CodeEvidenceSupportCategory.KNOWLEDGE,
        ]
    }
    count_summary = ", ".join(f"{key}={value}" for key, value in counts.items())
    if not technical:
        if policy.disclosure_mode == CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE:
            return f"Technical evidence summary: {count_summary}."
        if policy.disclosure_mode == CodeEvidenceDisclosureMode.BACKGROUND_CONFIDENCE_ONLY:
            return "Operational confidence summary: code and test evidence may inform confidence but internal identifiers are withheld."
        if policy.disclosure_mode == CodeEvidenceDisclosureMode.NO_CODE_EVIDENCE:
            return "Role-safe summary: code evidence is not available for this role."
        if policy.customer_safe:
            return "Customer-safe implementation summary: implementation support may be described without internal code paths."
        return "Implementation confirmation summary: evidence may be translated without raw code snippets."
    details = _technical_source_labels(visible_sources, policy)
    if details:
        return f"Matched evidence counts: {count_summary}. Visible references: {', '.join(details)}."
    return f"Matched evidence counts: {count_summary}. No role-visible technical references."


def _technical_source_labels(
    visible_sources: dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]],
    policy: CodeEvidenceAnswerPolicy,
) -> list[str]:
    labels: list[str] = []
    for sources in visible_sources.values():
        for source in sources:
            parts = [
                value
                for value in [
                    source.repo_name,
                    source.file_path,
                    source.symbol_name,
                    source.route_path,
                    source.test_name,
                ]
                if value
            ]
            if parts:
                labels.append("::".join(parts))
            elif policy.disclosure_mode == CodeEvidenceDisclosureMode.TECHNICAL_DISCLOSURE:
                labels.append(source.title)
    return labels[:12]


def _required_caveats(
    policy: CodeEvidenceAnswerPolicy,
    status: CodeEvidenceSupportStatus,
    runtime_claim: bool,
    categorized: dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]],
) -> list[str]:
    caveats = list(policy.caveats)
    if CODE_CANNOT_PROVE_RUNTIME_CAVEAT not in caveats:
        caveats.insert(0, CODE_CANNOT_PROVE_RUNTIME_CAVEAT)
    if status == CodeEvidenceSupportStatus.NEEDS_IMPLEMENTATION_STATE_REVIEW:
        caveats.append("Implementation-state documentation is missing or did not match; review is required before claiming a landed feature.")
    if runtime_claim or status == CodeEvidenceSupportStatus.NEEDS_RUNTIME_EVIDENCE:
        caveats.append("Runtime, production, tenant, or customer availability requires separate runtime evidence.")
    if categorized[CodeEvidenceSupportCategory.TEST]:
        caveats.append("Test evidence is behavioural test-level evidence; it does not prove production deployment.")
    return _dedupe(caveats)


def _all_prohibited_claims(policy_service: CodeEvidenceAnswerPolicyService) -> list[str]:
    return _dedupe(policy_service.prohibited_claims() + list(PROHIBITED_CLAIM_PATTERNS))


def _has_code_or_test_evidence(
    categorized: dict[CodeEvidenceSupportCategory, list[CodeEvidenceSupportSource]],
) -> bool:
    return bool(
        categorized[CodeEvidenceSupportCategory.CODE]
        or categorized[CodeEvidenceSupportCategory.TEST]
        or categorized[CodeEvidenceSupportCategory.PROMPT]
    )


def _category(source: CodeEvidenceSupportSource) -> str:
    return str(source.evidence_category).upper()


def _normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower().replace("_", " ").replace("-", " ")).strip()


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped
