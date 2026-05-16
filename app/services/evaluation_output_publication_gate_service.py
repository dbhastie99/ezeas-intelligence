from dataclasses import asdict, dataclass
from typing import Any


PUBLICATION_DECISIONS = (
    "PUBLISH_CONTROLLED_EVALUATION_REPORT",
    "PUBLISH_DEVELOPER_HANDOFF",
    "PUBLISH_PROGRESS_SUMMARY",
    "NEEDS_CAVEAT_BEFORE_PUBLICATION",
    "BLOCKED_OVERSTATED_RUNTIME",
    "BLOCKED_OVERSTATED_DEPLOYMENT",
    "BLOCKED_OVERSTATED_PRODUCTION",
    "BLOCKED_OVERSTATED_EXPOSURE",
    "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM",
    "BLOCKED_LIVE_LLM_CLAIM",
    "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM",
    "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM",
    "BLOCKED_CROSS_REPO_RUNTIME_CLAIM",
    "UNKNOWN_REQUIRES_HUMAN_REVIEW",
)

BASE_REQUIRED_CAVEATS = (
    "Minerva remains controlled-readiness only.",
    "This publication gate does not authorise runtime, deployment, production, exposure, DB access, corpus mutation, Code Evidence ingestion, live LLM use, or final natural-language answer generation.",
)

CAVEAT_PATTERNS = (
    "controlled-readiness only",
    "controlled readiness only",
    "not production",
    "no production",
    "production deferred",
    "not deployed",
    "no deployment",
    "deployment deferred",
    "runtime deferred",
    "not runtime",
    "no runtime",
    "not exposed",
    "no exposure",
    "chat exposure remains deferred",
    "no chat exposure",
    "no endpoint",
    "no api endpoint",
    "no route registration",
    "final natural-language answer generation remains deferred",
    "no final natural-language answer generation",
    "live llm use remains deferred",
    "no live llm",
    "no db access",
    "no database access",
    "db validation pending",
    "db validation not performed",
    "no corpus mutation",
    "no code evidence ingestion",
    "no workforce-platform runtime integration",
    "no ezeas-analytics runtime integration",
)

CONTROLLED_READINESS_PATTERNS = (
    "controlled-readiness only",
    "controlled readiness only",
    "controlled-readiness",
    "controlled readiness",
)

TARGET_PATTERNS = (
    (
        "developer_handoff",
        (
            "developer handoff",
            "handoff note",
            "handoff notes",
            "developer handoff note",
            "developer handoff notes",
        ),
    ),
    (
        "progress_summary",
        (
            "progress summary",
            "progress-summary",
            "status summary",
            "slice summary",
        ),
    ),
    (
        "controlled_evaluation_report",
        (
            "controlled evaluation report",
            "evaluation report",
            "controlled-readiness documentation",
            "controlled readiness documentation",
            "next-slice recommendation",
            "next slice recommendation",
        ),
    ),
)

PRESERVED_BOUNDARY_PATTERNS = (
    ("CONTROLLED_READINESS_ONLY", ("controlled-readiness only", "controlled readiness only")),
    ("PRODUCTION_DEFERRED", ("not production", "no production", "production deferred")),
    ("DEPLOYMENT_DEFERRED", ("not deployed", "no deployment", "deployment deferred")),
    ("RUNTIME_DEFERRED", ("not runtime", "no runtime", "runtime deferred")),
    ("CHAT_EXPOSURE_DEFERRED", ("no chat exposure", "chat exposure remains deferred")),
    ("ENDPOINT_EXPOSURE_DEFERRED", ("no endpoint", "no api endpoint", "no route registration")),
    (
        "FINAL_ANSWER_GENERATION_DEFERRED",
        (
            "no final natural-language answer generation",
            "final natural-language answer generation remains deferred",
            "final answer generation remains deferred",
        ),
    ),
    ("LIVE_LLM_DEFERRED", ("no live llm", "live llm use remains deferred")),
    ("DB_ACCESS_DEFERRED", ("no db access", "no database access")),
    ("DB_VALIDATION_DEFERRED", ("db validation pending", "db validation not performed")),
    ("CORPUS_MUTATION_DEFERRED", ("no corpus mutation",)),
    ("CODE_EVIDENCE_INGESTION_DEFERRED", ("no code evidence ingestion",)),
    ("WORKFORCE_RUNTIME_INTEGRATION_DEFERRED", ("no workforce-platform runtime integration",)),
    (
        "ANALYTICS_RUNTIME_INTEGRATION_DEFERRED",
        ("no ezeas-analytics runtime integration", "no analytics runtime integration"),
    ),
)

BLOCKED_CLAIM_PATTERNS = (
    (
        "PRODUCTION_READINESS_CLAIM",
        "BLOCKED_OVERSTATED_PRODUCTION",
        "PRODUCTION_READINESS",
        "production_readiness",
        (
            "production-ready",
            "production ready",
            "ready for production",
            "production readiness achieved",
            "production use enabled",
        ),
    ),
    (
        "DEPLOYMENT_READINESS_CLAIM",
        "BLOCKED_OVERSTATED_DEPLOYMENT",
        "DEPLOYMENT_READINESS",
        "deployment_readiness",
        (
            "deployed",
            "deployment complete",
            "deployment-ready",
            "deployment ready",
            "ready for deployment",
        ),
    ),
    (
        "RUNTIME_READINESS_CLAIM",
        "BLOCKED_OVERSTATED_RUNTIME",
        "RUNTIME_READINESS",
        "runtime_readiness",
        (
            "runtime-enabled",
            "runtime enabled",
            "runtime is enabled",
            "runtime ready",
            "runtime-ready",
            "live runtime active",
        ),
    ),
    (
        "CHAT_EXPOSURE_CLAIM",
        "BLOCKED_OVERSTATED_EXPOSURE",
        "CHAT_EXPOSURE",
        "chat_exposure",
        (
            "chat exposure enabled",
            "internal chat enabled",
            "public chat enabled",
            "tenant chat enabled",
            "customer chat enabled",
            "chat is exposed",
        ),
    ),
    (
        "ENDPOINT_EXPOSURE_CLAIM",
        "BLOCKED_OVERSTATED_EXPOSURE",
        "ENDPOINT_EXPOSURE",
        "endpoint_exposure",
        (
            "endpoint exposed",
            "endpoint exposure enabled",
            "api endpoint enabled",
            "route registered",
            "endpoint is live",
        ),
    ),
    (
        "FINAL_ANSWER_GENERATION_CLAIM",
        "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM",
        "FINAL_ANSWER_GENERATION",
        "final_answer_generation",
        (
            "final answer generation enabled",
            "final natural-language answer generation enabled",
            "generates final answers",
            "final user-facing answer",
        ),
    ),
    (
        "LIVE_LLM_CLAIM",
        "BLOCKED_LIVE_LLM_CLAIM",
        "LIVE_LLM",
        "live_llm",
        (
            "live llm enabled",
            "live llm use enabled",
            "calls the live llm",
            "live llm call",
            "uses live llm",
        ),
    ),
    (
        "DB_ACCESS_CLAIM",
        "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM",
        "DB_ACCESS",
        "db_access",
        (
            "db access occurred",
            "database access occurred",
            "queried the database",
            "database query completed",
            "read from the database",
            "connected to the database",
        ),
    ),
    (
        "DB_VALIDATION_CLAIM",
        "BLOCKED_DB_ACCESS_OR_VALIDATION_CLAIM",
        "DB_VALIDATION",
        "db_validation",
        (
            "db validation occurred",
            "db validation completed",
            "db validation performed",
            "validated against the database",
            "database validation completed",
        ),
    ),
    (
        "CORPUS_MUTATION_CLAIM",
        "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM",
        "CORPUS_MUTATION",
        "corpus_mutation",
        (
            "corpus mutation occurred",
            "mutated the corpus",
            "updated the corpus",
            "wrote to the corpus",
        ),
    ),
    (
        "CODE_EVIDENCE_INGESTION_CLAIM",
        "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM",
        "CODE_EVIDENCE_INGESTION",
        "code_evidence_ingestion",
        (
            "code evidence ingestion occurred",
            "ingested code evidence",
            "code evidence ingested",
        ),
    ),
    (
        "WORKFORCE_RUNTIME_INTEGRATION_CLAIM",
        "BLOCKED_CROSS_REPO_RUNTIME_CLAIM",
        "WORKFORCE_RUNTIME_INTEGRATION",
        "workforce_runtime_integration",
        (
            "workforce-platform runtime integration occurred",
            "workforce-platform runtime integration enabled",
            "integrated with workforce-platform runtime",
        ),
    ),
    (
        "ANALYTICS_RUNTIME_INTEGRATION_CLAIM",
        "BLOCKED_CROSS_REPO_RUNTIME_CLAIM",
        "ANALYTICS_RUNTIME_INTEGRATION",
        "analytics_runtime_integration",
        (
            "analytics runtime integration occurred",
            "analytics runtime integration enabled",
            "ezeas-analytics runtime integration occurred",
            "ezeas-analytics runtime integration enabled",
        ),
    ),
)

NEGATION_PATTERNS = (
    "no ",
    "not ",
    "never ",
    "without ",
    "deferred",
    "pending",
    "not performed",
    "has not occurred",
    "did not occur",
    "does not ",
    "must not ",
    "is not ",
    "remains deferred",
)


@dataclass(frozen=True)
class EvaluationOutputPublicationGateResult:
    publication_decision: str
    safe_for_controlled_evaluation_report: bool
    safe_for_developer_handoff: bool
    safe_for_progress_summary: bool
    safe_for_final_answer_generation: bool
    publication_blocked: bool
    block_reasons: tuple[str, ...]
    required_caveats: tuple[str, ...]
    missing_caveats: tuple[str, ...]
    preserved_boundaries: tuple[str, ...]
    violated_boundaries: tuple[str, ...]
    overstatement_detected: bool
    human_review_required: bool
    final_answer_generation_claim_detected: bool
    live_llm_claim_detected: bool
    chat_exposure_claim_detected: bool
    endpoint_exposure_claim_detected: bool
    runtime_readiness_claim_detected: bool
    deployment_readiness_claim_detected: bool
    production_readiness_claim_detected: bool
    db_access_claim_detected: bool
    db_validation_claim_detected: bool
    corpus_mutation_claim_detected: bool
    code_evidence_ingestion_claim_detected: bool
    workforce_runtime_integration_claim_detected: bool
    analytics_runtime_integration_claim_detected: bool
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_evaluation_output_publication_gate(candidate: Any) -> dict[str, Any]:
    text = _candidate_text(candidate)
    normalized_text = _normalize_text(text)
    target = _publication_target(candidate, normalized_text)
    preserved_boundaries = _preserved_boundaries(normalized_text)
    block_reasons, violated_boundaries, blocked_decision = _blocked_claims(normalized_text)
    has_controlled_readiness = _contains_any(normalized_text, CONTROLLED_READINESS_PATTERNS)
    has_caveat = _contains_any(normalized_text, CAVEAT_PATTERNS)
    missing_caveats = _missing_caveats(has_controlled_readiness, has_caveat)

    if block_reasons:
        publication_decision = blocked_decision
    elif not text.strip():
        publication_decision = "UNKNOWN_REQUIRES_HUMAN_REVIEW"
    elif missing_caveats:
        publication_decision = "NEEDS_CAVEAT_BEFORE_PUBLICATION"
    elif target == "developer_handoff":
        publication_decision = "PUBLISH_DEVELOPER_HANDOFF"
    elif target == "progress_summary":
        publication_decision = "PUBLISH_PROGRESS_SUMMARY"
    else:
        publication_decision = "PUBLISH_CONTROLLED_EVALUATION_REPORT"

    publication_blocked = publication_decision.startswith("BLOCKED_")
    human_review_required = publication_decision in (
        "NEEDS_CAVEAT_BEFORE_PUBLICATION",
        "UNKNOWN_REQUIRES_HUMAN_REVIEW",
    )

    return EvaluationOutputPublicationGateResult(
        publication_decision=publication_decision,
        safe_for_controlled_evaluation_report=publication_decision
        == "PUBLISH_CONTROLLED_EVALUATION_REPORT",
        safe_for_developer_handoff=publication_decision == "PUBLISH_DEVELOPER_HANDOFF",
        safe_for_progress_summary=publication_decision == "PUBLISH_PROGRESS_SUMMARY",
        safe_for_final_answer_generation=False,
        publication_blocked=publication_blocked,
        block_reasons=block_reasons,
        required_caveats=BASE_REQUIRED_CAVEATS,
        missing_caveats=missing_caveats,
        preserved_boundaries=preserved_boundaries,
        violated_boundaries=violated_boundaries,
        overstatement_detected=publication_blocked,
        human_review_required=human_review_required,
        final_answer_generation_claim_detected="FINAL_ANSWER_GENERATION_CLAIM"
        in block_reasons,
        live_llm_claim_detected="LIVE_LLM_CLAIM" in block_reasons,
        chat_exposure_claim_detected="CHAT_EXPOSURE_CLAIM" in block_reasons,
        endpoint_exposure_claim_detected="ENDPOINT_EXPOSURE_CLAIM" in block_reasons,
        runtime_readiness_claim_detected="RUNTIME_READINESS_CLAIM" in block_reasons,
        deployment_readiness_claim_detected="DEPLOYMENT_READINESS_CLAIM" in block_reasons,
        production_readiness_claim_detected="PRODUCTION_READINESS_CLAIM" in block_reasons,
        db_access_claim_detected="DB_ACCESS_CLAIM" in block_reasons,
        db_validation_claim_detected="DB_VALIDATION_CLAIM" in block_reasons,
        corpus_mutation_claim_detected="CORPUS_MUTATION_CLAIM" in block_reasons,
        code_evidence_ingestion_claim_detected="CODE_EVIDENCE_INGESTION_CLAIM"
        in block_reasons,
        workforce_runtime_integration_claim_detected="WORKFORCE_RUNTIME_INTEGRATION_CLAIM"
        in block_reasons,
        analytics_runtime_integration_claim_detected="ANALYTICS_RUNTIME_INTEGRATION_CLAIM"
        in block_reasons,
        explanation=_explanation(publication_decision, block_reasons, missing_caveats),
    ).to_dict()


def evaluate_publication_gate(candidate: Any) -> dict[str, Any]:
    return evaluate_evaluation_output_publication_gate(candidate)


def _candidate_text(candidate: Any) -> str:
    if candidate is None:
        return ""
    if isinstance(candidate, str):
        return candidate
    if isinstance(candidate, dict):
        return "\n".join(f"{key}: {_candidate_text(value)}" for key, value in candidate.items())
    if isinstance(candidate, (list, tuple, set)):
        return "\n".join(_candidate_text(value) for value in candidate)
    return str(candidate)


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().replace("_", " ").split())


def _publication_target(candidate: Any, normalized_text: str) -> str:
    explicit_target = ""
    if isinstance(candidate, dict):
        explicit_target = str(
            candidate.get("publication_target")
            or candidate.get("target")
            or candidate.get("artifact_type")
            or candidate.get("artefact_type")
            or ""
        )
    target_text = _normalize_text(explicit_target) if explicit_target else normalized_text
    for target, patterns in TARGET_PATTERNS:
        if _contains_any(target_text, patterns):
            return target
    return "controlled_evaluation_report"


def _preserved_boundaries(normalized_text: str) -> tuple[str, ...]:
    boundaries = [
        boundary
        for boundary, patterns in PRESERVED_BOUNDARY_PATTERNS
        if _contains_any(normalized_text, patterns)
    ]
    return tuple(dict.fromkeys(boundaries))


def _blocked_claims(normalized_text: str) -> tuple[tuple[str, ...], tuple[str, ...], str]:
    block_reasons: list[str] = []
    violated_boundaries: list[str] = []
    decisions: list[str] = []
    for claim, decision, boundary, _flag, patterns in BLOCKED_CLAIM_PATTERNS:
        if _has_positive_claim(normalized_text, patterns):
            block_reasons.append(claim)
            violated_boundaries.append(boundary)
            decisions.append(decision)

    publication_decision = decisions[0] if decisions else ""
    return (
        tuple(dict.fromkeys(block_reasons)),
        tuple(dict.fromkeys(violated_boundaries)),
        publication_decision,
    )


def _has_positive_claim(normalized_text: str, patterns: tuple[str, ...]) -> bool:
    for pattern in patterns:
        start = normalized_text.find(pattern)
        while start != -1:
            if not _is_negated(normalized_text, start):
                return True
            start = normalized_text.find(pattern, start + len(pattern))
    return False


def _is_negated(normalized_text: str, start: int) -> bool:
    window_start = max(0, start - 50)
    window = normalized_text[window_start:start]
    return any(negation in window for negation in NEGATION_PATTERNS)


def _missing_caveats(has_controlled_readiness: bool, has_caveat: bool) -> tuple[str, ...]:
    missing: list[str] = []
    if not has_controlled_readiness:
        missing.append("Controlled-readiness-only caveat is missing.")
    if not has_caveat:
        missing.append("No no-action/deferred-boundary caveat was detected.")
    return tuple(missing)


def _contains_any(normalized_text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in normalized_text for pattern in patterns)


def _explanation(
    publication_decision: str,
    block_reasons: tuple[str, ...],
    missing_caveats: tuple[str, ...],
) -> str:
    if block_reasons:
        return (
            "Publication is blocked because the output contains prohibited claims: "
            + ", ".join(block_reasons)
            + "."
        )
    if publication_decision == "UNKNOWN_REQUIRES_HUMAN_REVIEW":
        return "Publication target or status is unknown, so human review is required."
    if publication_decision == "NEEDS_CAVEAT_BEFORE_PUBLICATION":
        return (
            "Publication requires controlled-readiness and no-action caveats before use: "
            + ", ".join(missing_caveats)
            + "."
        )
    return (
        "Output preserves controlled-readiness boundaries and is safe only for the "
        "selected controlled internal publication artefact."
    )
