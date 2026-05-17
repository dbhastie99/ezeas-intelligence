import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DURABLE_EVIDENCE_INTAKE_DESIGN_READY = "DURABLE_EVIDENCE_INTAKE_DESIGN_READY"
NEEDS_STORAGE_BOUNDARY = "NEEDS_STORAGE_BOUNDARY"
NEEDS_MUTATION_BOUNDARY = "NEEDS_MUTATION_BOUNDARY"
NEEDS_REVIEW_BOUNDARY = "NEEDS_REVIEW_BOUNDARY"
NEEDS_ROLLBACK_POLICY = "NEEDS_ROLLBACK_POLICY"
BLOCKED_DURABLE_INGESTION_CLAIM = "BLOCKED_DURABLE_INGESTION_CLAIM"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

REQUIRED_DESIGN_COMPONENTS = (
    "storage_boundary_model",
    "mutation_boundary_model",
    "review_boundary_model",
    "rollback_or_removal_policy",
)

REQUIRED_CAVEATS = (
    "Durable intake design exists as deterministic design metadata only.",
    "Durable evidence intake is not authorised yet.",
    "Corpus mutation, DB writes, and Code Evidence ingestion are not authorised yet.",
    "Future durable intake requires explicit authorisation, evidence envelope, source-status boundary, no-overstatement checks, audit metadata, rollback/removal policy, and reviewer confirmation.",
)

DURABLE_INGESTION_CLAIM_KEYS = (
    "durable_intake_authorised_now",
    "durable_ingestion_authorised",
    "durable_evidence_ingestion_authorised",
    "durable_intake_performed",
    "durable_ingestion_performed",
    "ready_for_durable_ingestion",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "db_access_authorised",
    "db_access_performed",
    "db_read_authorised",
    "db_read_performed",
    "db_write_authorised_now",
    "db_write_authorised",
    "db_write_performed",
    "live_retrieval_authorised",
    "live_retrieval_performed",
    "live_llm_authorised",
    "live_llm_performed",
    "final_answer_generation_authorised",
    "final_answer_generation_performed",
    "chat_exposure_authorised",
    "endpoint_exposure_authorised",
    "route_registration_authorised",
    "runtime_integration_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "production_readiness_claim_permitted",
)

MUTATION_CLAIM_KEYS = (
    "corpus_mutation_authorised_now",
    "corpus_mutation_authorised",
    "corpus_mutation_performed",
    "code_evidence_ingestion_authorised_now",
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_performed",
)


@dataclass(frozen=True)
class ControlledDurableEvidenceIntakeDesignResult:
    design_id: str
    design_status: str
    durable_intake_design_ready: bool
    durable_intake_authorised_now: bool
    corpus_mutation_authorised_now: bool
    db_write_authorised_now: bool
    code_evidence_ingestion_authorised_now: bool
    required_design_components: tuple[str, ...]
    missing_design_components: tuple[str, ...]
    storage_boundary_model: str
    mutation_boundary_model: str
    review_boundary_model: str
    rollback_or_removal_policy_required: bool
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_durable_evidence_intake_design(
    design_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return deterministic future durable-intake design metadata only."""

    metadata = design_metadata or {}
    missing = _missing_design_components(metadata)
    status = _design_status(metadata, missing)
    ready = status == DURABLE_EVIDENCE_INTAKE_DESIGN_READY
    material = {
        "status": status,
        "missing": missing,
        "storage_boundary_model": _field_text(metadata, "storage_boundary_model"),
        "mutation_boundary_model": _field_text(metadata, "mutation_boundary_model"),
        "review_boundary_model": _field_text(metadata, "review_boundary_model"),
    }

    return ControlledDurableEvidenceIntakeDesignResult(
        design_id=_stable_id(material),
        design_status=status,
        durable_intake_design_ready=ready,
        durable_intake_authorised_now=False,
        corpus_mutation_authorised_now=False,
        db_write_authorised_now=False,
        code_evidence_ingestion_authorised_now=False,
        required_design_components=REQUIRED_DESIGN_COMPONENTS,
        missing_design_components=missing,
        storage_boundary_model=_field_text(metadata, "storage_boundary_model"),
        mutation_boundary_model=_field_text(metadata, "mutation_boundary_model"),
        review_boundary_model=_field_text(metadata, "review_boundary_model"),
        rollback_or_removal_policy_required=True,
        required_caveats=REQUIRED_CAVEATS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _design_status(metadata: dict[str, Any], missing: tuple[str, ...]) -> str:
    if _has_claim(metadata, DURABLE_INGESTION_CLAIM_KEYS) or _status_claims_ingestion(metadata):
        return BLOCKED_DURABLE_INGESTION_CLAIM
    if _has_claim(metadata, MUTATION_CLAIM_KEYS):
        return BLOCKED_DURABLE_INGESTION_CLAIM
    if _has_claim(metadata, RUNTIME_OR_PRODUCTION_CLAIM_KEYS) or _status_claims_runtime(metadata):
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not metadata:
        return UNKNOWN_REQUIRES_REVIEW
    if "storage_boundary_model" in missing:
        return NEEDS_STORAGE_BOUNDARY
    if "mutation_boundary_model" in missing:
        return NEEDS_MUTATION_BOUNDARY
    if "review_boundary_model" in missing:
        return NEEDS_REVIEW_BOUNDARY
    if "rollback_or_removal_policy" in missing:
        return NEEDS_ROLLBACK_POLICY
    return DURABLE_EVIDENCE_INTAKE_DESIGN_READY


def _missing_design_components(metadata: dict[str, Any]) -> tuple[str, ...]:
    missing = [
        key
        for key in REQUIRED_DESIGN_COMPONENTS
        if not _component_present(metadata, key)
    ]
    return tuple(missing)


def _component_present(metadata: dict[str, Any], key: str) -> bool:
    if key == "rollback_or_removal_policy":
        return bool(
            metadata.get("rollback_or_removal_policy")
            or metadata.get("rollback_or_removal_policy_required") is True
            or metadata.get("rollback_policy_required") is True
        )
    return bool(metadata.get(key))


def _has_claim(metadata: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return any(bool(metadata.get(key)) for key in keys)


def _status_claims_ingestion(metadata: dict[str, Any]) -> bool:
    status = _status_text(metadata)
    return "DURABLE_INGESTION" in status or "DURABLE_INTAKE_AUTHORISED" in status


def _status_claims_runtime(metadata: dict[str, Any]) -> bool:
    status = _status_text(metadata)
    return "RUNTIME_OR_PRODUCTION" in status or "PRODUCTION_READY" in status


def _status_text(metadata: dict[str, Any]) -> str:
    return " ".join(
        str(metadata.get(key) or "")
        for key in ("design_status", "phase_status", "claim_status")
    )


def _field_text(metadata: dict[str, Any], key: str) -> str:
    return str(metadata.get(key) or "")


def _explanation(status: str) -> str:
    if status == DURABLE_EVIDENCE_INTAKE_DESIGN_READY:
        return (
            "The durable intake design metadata is complete for review. It "
            "authorises no durable ingestion, corpus mutation, DB write, or "
            "Code Evidence ingestion."
        )
    if status == BLOCKED_DURABLE_INGESTION_CLAIM:
        return (
            "The design metadata includes an unauthorised durable ingestion, "
            "corpus mutation, or Code Evidence ingestion claim."
        )
    if status == BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT:
        return (
            "The design metadata includes DB, live retrieval, live LLM, route, "
            "runtime, deployment, or production overstatement."
        )
    return "The durable intake design metadata is missing, incomplete, or requires review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-durable-evidence-intake-design-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]
