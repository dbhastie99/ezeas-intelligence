import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


DEVELOPER_LOG = "DEVELOPER_LOG"
HARDENING_LOG = "HARDENING_LOG"
PLATFORM_DOCTRINE = "PLATFORM_DOCTRINE"
THREAD_CONTINUANCE_PROMPT = "THREAD_CONTINUANCE_PROMPT"
ANALYTICS_READINESS_SUMMARY = "ANALYTICS_READINESS_SUMMARY"
AWARD_RECOVERY_ANALYSIS = "AWARD_RECOVERY_ANALYSIS"
WORKFORCE_CONTROLLED_READINESS_DOC = "WORKFORCE_CONTROLLED_READINESS_DOC"
CODE_EVIDENCE_PLANNING_OUTPUT = "CODE_EVIDENCE_PLANNING_OUTPUT"
CONTROLLED_EVALUATION_SUMMARY = "CONTROLLED_EVALUATION_SUMMARY"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

KNOWN_EVIDENCE_CATEGORIES = (
    DEVELOPER_LOG,
    HARDENING_LOG,
    PLATFORM_DOCTRINE,
    THREAD_CONTINUANCE_PROMPT,
    ANALYTICS_READINESS_SUMMARY,
    AWARD_RECOVERY_ANALYSIS,
    WORKFORCE_CONTROLLED_READINESS_DOC,
    CODE_EVIDENCE_PLANNING_OUTPUT,
    CONTROLLED_EVALUATION_SUMMARY,
)

DEFAULT_TRUST_LEVEL_BY_CATEGORY = {
    DEVELOPER_LOG: "CONTROLLED_INTERNAL",
    HARDENING_LOG: "CONTROLLED_INTERNAL",
    PLATFORM_DOCTRINE: "CONTROLLED_DOCTRINE",
    THREAD_CONTINUANCE_PROMPT: "CONTROLLED_HANDOFF",
    ANALYTICS_READINESS_SUMMARY: "CONTROLLED_ANALYSIS",
    AWARD_RECOVERY_ANALYSIS: "CONTROLLED_ANALYSIS",
    WORKFORCE_CONTROLLED_READINESS_DOC: "CONTROLLED_READINESS",
    CODE_EVIDENCE_PLANNING_OUTPUT: "CONTROLLED_PLANNING",
    CONTROLLED_EVALUATION_SUMMARY: "CONTROLLED_EVALUATION",
    UNKNOWN_REQUIRES_REVIEW: "UNKNOWN",
}

DEFAULT_CAVEATS_BY_CATEGORY = {
    DEVELOPER_LOG: (
        "Developer log evidence is planning evidence only.",
        "It does not authorise ingestion, corpus mutation, runtime, deployment, or production claims.",
    ),
    HARDENING_LOG: (
        "Hardening log evidence records controlled work or findings only.",
        "It does not prove runtime exposure, deployment, production use, or completed repair.",
    ),
    PLATFORM_DOCTRINE: (
        "Platform doctrine evidence is governance context only.",
        "It does not authorise ingestion, corpus mutation, runtime, deployment, or production claims.",
    ),
    THREAD_CONTINUANCE_PROMPT: (
        "Thread continuance prompt evidence is handoff context only.",
        "It must not be treated as ingested corpus or runtime truth.",
    ),
    ANALYTICS_READINESS_SUMMARY: (
        "Analytics readiness summary evidence is controlled-readiness context only.",
        "It does not enable analytics runtime integration.",
    ),
    AWARD_RECOVERY_ANALYSIS: (
        "Award recovery analysis evidence is analysis context only.",
        "It does not prove repair, implementation, deployment, or production state.",
    ),
    WORKFORCE_CONTROLLED_READINESS_DOC: (
        "Workforce-platform controlled-readiness evidence is readiness documentation only.",
        "It does not enable workforce-platform runtime integration.",
    ),
    CODE_EVIDENCE_PLANNING_OUTPUT: (
        "Code Evidence planning output is planning evidence only.",
        "It does not authorise Code Evidence ingestion or corpus mutation.",
    ),
    CONTROLLED_EVALUATION_SUMMARY: (
        "Controlled evaluation summary evidence is deterministic evaluation metadata only.",
        "It does not authorise final answer generation or runtime exposure.",
    ),
    UNKNOWN_REQUIRES_REVIEW: (
        "Unknown or untrusted evidence requires source, trust, and status review before planning use.",
    ),
}

CATEGORY_PATTERNS = (
    (DEVELOPER_LOG, ("developer log", "dev log", "development log")),
    (HARDENING_LOG, ("hardening log", "hardening")),
    (PLATFORM_DOCTRINE, ("platform doctrine", "doctrine")),
    (THREAD_CONTINUANCE_PROMPT, ("thread continuance", "continuance prompt", "resume prompt")),
    (ANALYTICS_READINESS_SUMMARY, ("analytics readiness", "analytics summary")),
    (AWARD_RECOVERY_ANALYSIS, ("award recovery", "recovery analysis")),
    (
        WORKFORCE_CONTROLLED_READINESS_DOC,
        ("workforce controlled-readiness", "workforce controlled readiness", "workforce-platform controlled-readiness"),
    ),
    (CODE_EVIDENCE_PLANNING_OUTPUT, ("code evidence planning", "code evidence plan")),
    (CONTROLLED_EVALUATION_SUMMARY, ("controlled evaluation summary", "evaluation summary")),
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeTaxonomyResult:
    evidence_id: str
    evidence_category: str
    source_repo: str
    source_phase: str
    evidence_status: str
    trust_level: str
    ingestion_authorised: bool
    corpus_mutation_authorised: bool
    runtime_claim_permitted: bool
    production_claim_permitted: bool
    required_caveats: tuple[str, ...]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def classify_controlled_evidence_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    """Classify evidence metadata without ingesting, mutating, or calling external systems."""

    evidence_metadata = metadata or {}
    category = _classify_category(evidence_metadata)
    source_repo = str(evidence_metadata.get("source_repo") or evidence_metadata.get("repo") or "")
    source_phase = str(evidence_metadata.get("source_phase") or evidence_metadata.get("phase") or "")
    evidence_status = str(
        evidence_metadata.get("evidence_status")
        or evidence_metadata.get("status")
        or "UNKNOWN_REQUIRES_REVIEW"
    )
    trust_level = str(
        evidence_metadata.get("trust_level")
        or DEFAULT_TRUST_LEVEL_BY_CATEGORY[category]
    )
    caveats = _as_tuple(
        evidence_metadata.get("required_caveats")
        or DEFAULT_CAVEATS_BY_CATEGORY[category]
    )

    material = {
        "category": category,
        "source_repo": source_repo,
        "source_phase": source_phase,
        "evidence_status": evidence_status,
        "trust_level": trust_level,
        "caveats": caveats,
    }

    return ControlledEvidenceIntakeTaxonomyResult(
        evidence_id=str(evidence_metadata.get("evidence_id") or _stable_id(material)),
        evidence_category=category,
        source_repo=source_repo,
        source_phase=source_phase,
        evidence_status=evidence_status,
        trust_level=trust_level,
        ingestion_authorised=False,
        corpus_mutation_authorised=False,
        runtime_claim_permitted=False,
        production_claim_permitted=False,
        required_caveats=caveats,
        explanation=_explanation(category),
    ).to_dict()


def build_controlled_evidence_intake_taxonomy(metadata: dict[str, Any] | None) -> dict[str, Any]:
    return classify_controlled_evidence_metadata(metadata)


def _classify_category(metadata: dict[str, Any]) -> str:
    explicit = str(
        metadata.get("evidence_category")
        or metadata.get("category")
        or metadata.get("source_type")
        or ""
    ).upper()
    if explicit in KNOWN_EVIDENCE_CATEGORIES:
        return explicit

    haystack = " ".join(
        str(metadata.get(key, ""))
        for key in (
            "evidence_category",
            "category",
            "source_type",
            "source_name",
            "title",
            "path",
            "description",
        )
    ).lower().replace("_", " ").replace("-", " ")
    for category, patterns in CATEGORY_PATTERNS:
        if any(pattern in haystack for pattern in patterns):
            return category
    return UNKNOWN_REQUIRES_REVIEW


def _explanation(category: str) -> str:
    if category == UNKNOWN_REQUIRES_REVIEW:
        return (
            "Evidence metadata did not match a controlled category; source, trust, "
            "and status review is required before future intake planning."
        )
    return (
        f"Evidence metadata classified as {category} for controlled planning only; "
        "ingestion, corpus mutation, runtime claims, and production claims remain unauthorised."
    )


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, default=str).encode("utf-8")
    return "evidence-taxonomy-" + hashlib.sha256(encoded).hexdigest()[:16]
