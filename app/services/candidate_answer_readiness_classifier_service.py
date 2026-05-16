from dataclasses import asdict, dataclass
from typing import Any


READINESS_CLASSIFICATIONS = (
    "SAFE_CONTROLLED_EVALUATION_ONLY",
    "NEEDS_CAVEAT",
    "BLOCKED_OVERSTATED_RUNTIME",
    "BLOCKED_OVERSTATED_DEPLOYMENT",
    "BLOCKED_OVERSTATED_PRODUCTION",
    "BLOCKED_OVERSTATED_EXPOSURE",
    "BLOCKED_FINAL_ANSWER_GENERATION_CLAIM",
    "BLOCKED_LIVE_LLM_CLAIM",
    "BLOCKED_DB_ACCESS_CLAIM",
    "BLOCKED_CORPUS_OR_CODE_EVIDENCE_CLAIM",
    "BLOCKED_CROSS_REPO_RUNTIME_CLAIM",
    "UNKNOWN_REQUIRES_REVIEW",
)

BASE_REQUIRED_CAVEATS = (
    "Minerva remains controlled-readiness only.",
    "This candidate does not authorise runtime, deployment, production, exposure, or final natural-language answer generation.",
)

CAVEAT_PATTERNS = (
    "controlled-readiness only",
    "controlled readiness only",
    "not production",
    "no production",
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

FINAL_ARTEFACT_PREFERENCE_PATTERNS = (
    "final/current artefact",
    "final/current artifact",
    "prefer final/current",
    "final status",
    "final index",
    "current artefact",
    "current artifact",
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
    (
        "DB_VALIDATION_DEFERRED",
        ("db validation pending", "db validation not performed", "db-validation-deferred"),
    ),
    ("CORPUS_MUTATION_DEFERRED", ("no corpus mutation",)),
    ("CODE_EVIDENCE_INGESTION_DEFERRED", ("no code evidence ingestion",)),
    (
        "WORKFORCE_RUNTIME_INTEGRATION_DEFERRED",
        ("no workforce-platform runtime integration",),
    ),
    (
        "ANALYTICS_RUNTIME_INTEGRATION_DEFERRED",
        ("no ezeas-analytics runtime integration", "no analytics runtime integration"),
    ),
)

BLOCKED_CLAIM_PATTERNS = (
    (
        "PRODUCTION_READINESS_CLAIM",
        "BLOCKED_OVERSTATED_PRODUCTION",
        "production",
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
        "deployment",
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
        "runtime",
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
        "BLOCKED_DB_ACCESS_CLAIM",
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
        "BLOCKED_DB_ACCESS_CLAIM",
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
class CandidateAnswerReadinessClassificationResult:
    readiness_classification: str
    safe_for_controlled_evaluation: bool
    safe_for_developer_handoff: bool
    safe_for_final_answer_generation: bool
    overstatement_detected: bool
    prohibited_claims_detected: tuple[str, ...]
    required_caveats: tuple[str, ...]
    missing_caveats: tuple[str, ...]
    preserved_boundaries: tuple[str, ...]
    violated_boundaries: tuple[str, ...]
    final_answer_generation_claim_detected: bool
    live_llm_claim_detected: bool
    chat_exposure_claim_detected: bool
    endpoint_exposure_claim_detected: bool
    db_access_claim_detected: bool
    db_validation_claim_detected: bool
    corpus_mutation_claim_detected: bool
    code_evidence_ingestion_claim_detected: bool
    workforce_runtime_integration_claim_detected: bool
    analytics_runtime_integration_claim_detected: bool
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def classify_candidate_answer_readiness(candidate: Any) -> dict[str, Any]:
    text = _candidate_text(candidate)
    normalized_text = _normalize_text(text)
    preserved_boundaries = _preserved_boundaries(normalized_text)
    prohibited_claims, violated_boundaries, classification = _blocked_claims(normalized_text)
    has_controlled_readiness = _contains_any(normalized_text, CONTROLLED_READINESS_PATTERNS)
    has_caveat = _contains_any(normalized_text, CAVEAT_PATTERNS)
    has_final_artefact_preference = _contains_any(
        normalized_text, FINAL_ARTEFACT_PREFERENCE_PATTERNS
    )
    missing_caveats = _missing_caveats(has_controlled_readiness, has_caveat)

    if prohibited_claims:
        readiness_classification = classification
    elif not text.strip():
        readiness_classification = "UNKNOWN_REQUIRES_REVIEW"
    elif not has_caveat:
        readiness_classification = "UNKNOWN_REQUIRES_REVIEW"
    elif missing_caveats:
        readiness_classification = "NEEDS_CAVEAT"
    else:
        readiness_classification = "SAFE_CONTROLLED_EVALUATION_ONLY"

    overstatement_detected = bool(prohibited_claims)
    safe_for_controlled_evaluation = (
        readiness_classification == "SAFE_CONTROLLED_EVALUATION_ONLY"
    )
    safe_for_developer_handoff = (
        safe_for_controlled_evaluation
        and has_final_artefact_preference
        and has_controlled_readiness
    )

    return CandidateAnswerReadinessClassificationResult(
        readiness_classification=readiness_classification,
        safe_for_controlled_evaluation=safe_for_controlled_evaluation,
        safe_for_developer_handoff=safe_for_developer_handoff,
        safe_for_final_answer_generation=False,
        overstatement_detected=overstatement_detected,
        prohibited_claims_detected=prohibited_claims,
        required_caveats=BASE_REQUIRED_CAVEATS,
        missing_caveats=missing_caveats,
        preserved_boundaries=preserved_boundaries,
        violated_boundaries=violated_boundaries,
        final_answer_generation_claim_detected="FINAL_ANSWER_GENERATION_CLAIM"
        in prohibited_claims,
        live_llm_claim_detected="LIVE_LLM_CLAIM" in prohibited_claims,
        chat_exposure_claim_detected="CHAT_EXPOSURE_CLAIM" in prohibited_claims,
        endpoint_exposure_claim_detected="ENDPOINT_EXPOSURE_CLAIM" in prohibited_claims,
        db_access_claim_detected="DB_ACCESS_CLAIM" in prohibited_claims,
        db_validation_claim_detected="DB_VALIDATION_CLAIM" in prohibited_claims,
        corpus_mutation_claim_detected="CORPUS_MUTATION_CLAIM" in prohibited_claims,
        code_evidence_ingestion_claim_detected="CODE_EVIDENCE_INGESTION_CLAIM"
        in prohibited_claims,
        workforce_runtime_integration_claim_detected="WORKFORCE_RUNTIME_INTEGRATION_CLAIM"
        in prohibited_claims,
        analytics_runtime_integration_claim_detected="ANALYTICS_RUNTIME_INTEGRATION_CLAIM"
        in prohibited_claims,
        explanation=_explanation(readiness_classification, prohibited_claims, missing_caveats),
    ).to_dict()


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


def _preserved_boundaries(normalized_text: str) -> tuple[str, ...]:
    boundaries = [
        boundary
        for boundary, patterns in PRESERVED_BOUNDARY_PATTERNS
        if _contains_any(normalized_text, patterns)
    ]
    return tuple(dict.fromkeys(boundaries))


def _blocked_claims(normalized_text: str) -> tuple[tuple[str, ...], tuple[str, ...], str]:
    prohibited_claims: list[str] = []
    violated_boundaries: list[str] = []
    classifications: list[str] = []
    for claim, classification, boundary, patterns in BLOCKED_CLAIM_PATTERNS:
        if _has_positive_claim(normalized_text, patterns):
            prohibited_claims.append(claim)
            violated_boundaries.append(boundary.upper())
            classifications.append(classification)

    readiness_classification = classifications[0] if classifications else ""
    return (
        tuple(dict.fromkeys(prohibited_claims)),
        tuple(dict.fromkeys(violated_boundaries)),
        readiness_classification,
    )


def _has_positive_claim(normalized_text: str, patterns: tuple[str, ...]) -> bool:
    for pattern in patterns:
        start = normalized_text.find(pattern)
        while start != -1:
            if not _is_negated(normalized_text, start, pattern):
                return True
            start = normalized_text.find(pattern, start + len(pattern))
    return False


def _is_negated(normalized_text: str, start: int, pattern: str) -> bool:
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
    readiness_classification: str,
    prohibited_claims: tuple[str, ...],
    missing_caveats: tuple[str, ...],
) -> str:
    if prohibited_claims:
        return (
            "Candidate is blocked because it contains prohibited claims: "
            + ", ".join(prohibited_claims)
            + "."
        )
    if readiness_classification == "UNKNOWN_REQUIRES_REVIEW":
        return "Candidate status is ambiguous or lacks required caveats, so review is required."
    if readiness_classification == "NEEDS_CAVEAT":
        return "Candidate needs additional controlled-readiness caveats before handoff."
    return (
        "Candidate preserves controlled-readiness boundaries and is safe only for "
        "controlled evaluation or developer handoff metadata use."
    )
