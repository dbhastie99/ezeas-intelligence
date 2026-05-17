import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any


CONTROLLED_READINESS_EVIDENCE = "CONTROLLED_READINESS_EVIDENCE"
PLANNING_EVIDENCE = "PLANNING_EVIDENCE"
ANALYSIS_EVIDENCE = "ANALYSIS_EVIDENCE"
IMPLEMENTATION_CANDIDATE_EVIDENCE = "IMPLEMENTATION_CANDIDATE_EVIDENCE"
RUNTIME_EVIDENCE = "RUNTIME_EVIDENCE"
DEPLOYMENT_EVIDENCE = "DEPLOYMENT_EVIDENCE"
PRODUCTION_EVIDENCE = "PRODUCTION_EVIDENCE"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

KNOWN_SOURCE_STATUSES = (
    CONTROLLED_READINESS_EVIDENCE,
    PLANNING_EVIDENCE,
    ANALYSIS_EVIDENCE,
    IMPLEMENTATION_CANDIDATE_EVIDENCE,
    RUNTIME_EVIDENCE,
    DEPLOYMENT_EVIDENCE,
    PRODUCTION_EVIDENCE,
)

STATUS_PATTERNS = (
    (CONTROLLED_READINESS_EVIDENCE, ("controlled-readiness", "controlled readiness")),
    (PLANNING_EVIDENCE, ("planning", "plan")),
    (ANALYSIS_EVIDENCE, ("analysis", "finding", "assessment")),
    (IMPLEMENTATION_CANDIDATE_EVIDENCE, ("implementation candidate", "candidate implementation")),
    (RUNTIME_EVIDENCE, ("runtime evidence", "runtime proof")),
    (DEPLOYMENT_EVIDENCE, ("deployment evidence", "deployment proof")),
    (PRODUCTION_EVIDENCE, ("production evidence", "production proof")),
)

CAVEATS_BY_STATUS = {
    CONTROLLED_READINESS_EVIDENCE: (
        "Controlled-readiness evidence does not imply runtime enablement.",
    ),
    PLANNING_EVIDENCE: (
        "Planning evidence does not imply implementation.",
    ),
    ANALYSIS_EVIDENCE: (
        "Analysis evidence does not imply repair, remediation, or fix completion.",
    ),
    IMPLEMENTATION_CANDIDATE_EVIDENCE: (
        "Implementation candidate evidence does not imply deployed or runtime-enabled behaviour.",
    ),
    RUNTIME_EVIDENCE: (
        "Runtime evidence requires explicit proof before any runtime claim is permitted.",
    ),
    DEPLOYMENT_EVIDENCE: (
        "Deployment evidence requires explicit proof before any deployment claim is permitted.",
    ),
    PRODUCTION_EVIDENCE: (
        "Production evidence requires explicit proof before any production claim is permitted.",
    ),
    UNKNOWN_REQUIRES_REVIEW: (
        "Unknown evidence requires status boundary review before planning use.",
    ),
}

PROHIBITED_INFERENCES_BY_STATUS = {
    CONTROLLED_READINESS_EVIDENCE: (
        "runtime readiness",
        "deployment readiness",
        "production readiness",
    ),
    PLANNING_EVIDENCE: (
        "implementation completed",
        "runtime readiness",
        "production readiness",
    ),
    ANALYSIS_EVIDENCE: (
        "repair completed",
        "fix completed",
        "deployment readiness",
        "production readiness",
    ),
    IMPLEMENTATION_CANDIDATE_EVIDENCE: (
        "deployed",
        "runtime enabled",
        "production readiness",
    ),
    RUNTIME_EVIDENCE: (
        "runtime claim without explicit proof",
        "deployment readiness",
        "production readiness",
    ),
    DEPLOYMENT_EVIDENCE: (
        "deployment claim without explicit proof",
        "production readiness",
    ),
    PRODUCTION_EVIDENCE: (
        "production claim without explicit proof",
    ),
    UNKNOWN_REQUIRES_REVIEW: (
        "implementation truth",
        "runtime readiness",
        "deployment readiness",
        "production readiness",
    ),
}


@dataclass(frozen=True)
class EvidenceSourceStatusBoundaryResult:
    boundary_id: str
    source_status: str
    evidence_exists: bool
    implementation_claim_permitted: bool
    runtime_claim_permitted: bool
    deployment_claim_permitted: bool
    production_claim_permitted: bool
    required_caveats: tuple[str, ...]
    prohibited_inferences: tuple[str, ...]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_evidence_source_status_boundary(metadata: dict[str, Any] | None) -> dict[str, Any]:
    """Preserve evidence-status boundaries without making runtime truth claims."""

    evidence_metadata = metadata or {}
    source_status = _source_status(evidence_metadata)
    explicit_proof = bool(
        evidence_metadata.get("explicit_proof")
        or evidence_metadata.get("runtime_proof")
        or evidence_metadata.get("deployment_proof")
        or evidence_metadata.get("production_proof")
    )
    implementation_permitted = source_status in {
        IMPLEMENTATION_CANDIDATE_EVIDENCE,
        RUNTIME_EVIDENCE,
        DEPLOYMENT_EVIDENCE,
        PRODUCTION_EVIDENCE,
    } and explicit_proof
    runtime_permitted = source_status == RUNTIME_EVIDENCE and explicit_proof
    deployment_permitted = source_status == DEPLOYMENT_EVIDENCE and explicit_proof
    production_permitted = source_status == PRODUCTION_EVIDENCE and explicit_proof

    material = {
        "source_status": source_status,
        "explicit_proof": explicit_proof,
        "source": evidence_metadata.get("source") or evidence_metadata.get("path") or "",
    }

    return EvidenceSourceStatusBoundaryResult(
        boundary_id=str(evidence_metadata.get("boundary_id") or _stable_id(material)),
        source_status=source_status,
        evidence_exists=source_status != UNKNOWN_REQUIRES_REVIEW,
        implementation_claim_permitted=implementation_permitted,
        runtime_claim_permitted=runtime_permitted,
        deployment_claim_permitted=deployment_permitted,
        production_claim_permitted=production_permitted,
        required_caveats=CAVEATS_BY_STATUS[source_status],
        prohibited_inferences=PROHIBITED_INFERENCES_BY_STATUS[source_status],
        explanation=_explanation(source_status, explicit_proof),
    ).to_dict()


def build_evidence_source_status_boundary(metadata: dict[str, Any] | None) -> dict[str, Any]:
    return evaluate_evidence_source_status_boundary(metadata)


def _source_status(metadata: dict[str, Any]) -> str:
    explicit = str(
        metadata.get("source_status")
        or metadata.get("status_boundary")
        or metadata.get("evidence_status")
        or ""
    ).upper()
    if explicit in KNOWN_SOURCE_STATUSES:
        return explicit

    haystack = " ".join(
        str(metadata.get(key, ""))
        for key in ("source_status", "status_boundary", "evidence_status", "title", "description")
    ).lower()
    for source_status, patterns in STATUS_PATTERNS:
        if any(pattern in haystack for pattern in patterns):
            return source_status
    return UNKNOWN_REQUIRES_REVIEW


def _explanation(source_status: str, explicit_proof: bool) -> str:
    if source_status == UNKNOWN_REQUIRES_REVIEW:
        return "Unknown evidence requires review before implementation, runtime, deployment, or production inferences."
    if source_status in {RUNTIME_EVIDENCE, DEPLOYMENT_EVIDENCE, PRODUCTION_EVIDENCE} and not explicit_proof:
        return f"{source_status} was identified, but explicit proof is required before claims are permitted."
    return f"{source_status} boundary evaluated deterministically with no unauthorised inference."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, default=str).encode("utf-8")
    return "source-status-boundary-" + hashlib.sha256(encoded).hexdigest()[:16]
