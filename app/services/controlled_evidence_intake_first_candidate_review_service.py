import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_authorisation_gate_service import (
    AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


FIRST_CANDIDATE_REVIEW_READY = "FIRST_CANDIDATE_REVIEW_READY"
FIRST_CANDIDATE_NEEDS_HUMAN_REVIEW = "FIRST_CANDIDATE_NEEDS_HUMAN_REVIEW"
FIRST_CANDIDATE_BLOCKED_MUTATION_OR_INGESTION_CLAIM = (
    "FIRST_CANDIDATE_BLOCKED_MUTATION_OR_INGESTION_CLAIM"
)
FIRST_CANDIDATE_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "FIRST_CANDIDATE_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

INGESTION_OR_MUTATION_CLAIM_KEYS = (
    "intake_authorised_now",
    "ingestion_authorised_now",
    "evidence_ingestion_authorised_now",
    "evidence_ingestion_performed",
    "corpus_mutation_authorised_now",
    "corpus_mutation_performed",
    "code_evidence_ingestion_authorised_now",
    "code_evidence_ingestion_performed",
)

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "db_write_performed",
    "db_write_authorised_now",
    "db_access_authorised",
    "db_read_performed",
    "live_retrieval_performed",
    "live_retrieval_authorised",
    "live_llm_performed",
    "live_llm_authorised",
    "final_answer_generation_performed",
    "final_answer_generation_authorised",
    "runtime_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_authorised",
    "deployment_readiness_claim_permitted",
    "production_authorised",
    "production_readiness_claim_permitted",
)

REQUIRED_CAVEATS = (
    "Candidate is eligible only for a future no-mutation intake attempt.",
    "Intake is not authorised now.",
    "No evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM, or final answer generation has been performed.",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeFirstCandidateReviewResult:
    review_id: str
    candidate_id: str
    candidate_type: str
    review_status: str
    candidate_eligible_for_future_no_mutation_intake: bool
    candidate_authorised_for_intake_now: bool
    evidence_ingestion_performed: bool
    corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    db_write_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    required_caveats: tuple[str, ...]
    review_findings: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def review_controlled_evidence_intake_first_candidate(
    first_candidate_metadata: dict[str, Any] | None,
    authorisation_gate_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Review the first candidate decision without authorising intake."""

    selection = first_candidate_metadata or {}
    authorisation = authorisation_gate_metadata or {}
    candidate_id = str(selection.get("recommended_candidate_id") or "")
    candidate_type = str(selection.get("recommended_candidate_type") or "")
    blocked = _blocked_reasons(selection, authorisation)
    findings = _review_findings(selection, authorisation)
    status = _review_status(selection, authorisation, blocked, findings)
    ready = status == FIRST_CANDIDATE_REVIEW_READY
    material = {
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "status": status,
        "findings": findings,
        "blocked": blocked,
    }

    return ControlledEvidenceIntakeFirstCandidateReviewResult(
        review_id=_stable_id(material),
        candidate_id=candidate_id,
        candidate_type=candidate_type,
        review_status=status,
        candidate_eligible_for_future_no_mutation_intake=ready,
        candidate_authorised_for_intake_now=False,
        evidence_ingestion_performed=False,
        corpus_mutation_performed=False,
        code_evidence_ingestion_performed=False,
        db_write_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        required_caveats=_required_caveats(selection, authorisation),
        review_findings=findings,
        blocked_reasons=blocked,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def build_controlled_evidence_intake_first_candidate_review(
    first_candidate_metadata: dict[str, Any] | None,
    authorisation_gate_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return review_controlled_evidence_intake_first_candidate(
        first_candidate_metadata,
        authorisation_gate_metadata,
    )


def _blocked_reasons(
    selection: dict[str, Any],
    authorisation: dict[str, Any],
) -> tuple[str, ...]:
    blocked: list[str] = []
    if _has_claim(selection, INGESTION_OR_MUTATION_CLAIM_KEYS) or _has_claim(
        authorisation, INGESTION_OR_MUTATION_CLAIM_KEYS
    ):
        blocked.append("mutation_or_ingestion_claim")
    if _has_claim(selection, RUNTIME_OR_PRODUCTION_CLAIM_KEYS) or _has_claim(
        authorisation, RUNTIME_OR_PRODUCTION_CLAIM_KEYS
    ):
        blocked.append("runtime_or_production_overstatement")
    return tuple(blocked)


def _review_findings(
    selection: dict[str, Any],
    authorisation: dict[str, Any],
) -> tuple[str, ...]:
    findings: list[str] = []
    candidate_id = str(selection.get("recommended_candidate_id") or "")
    candidate_type = str(selection.get("recommended_candidate_type") or "")
    authorisation_candidate_id = str(authorisation.get("candidate_id") or "")
    if not candidate_id or not candidate_type:
        findings.append("missing_candidate_metadata")
    if not authorisation_candidate_id:
        findings.append("missing_authorisation_metadata")
    if candidate_id and authorisation_candidate_id and candidate_id != authorisation_candidate_id:
        findings.append("selection_authorisation_candidate_mismatch")
    if (
        authorisation.get("authorisation_decision")
        and authorisation.get("authorisation_decision")
        != AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE
    ):
        findings.append("authorisation_not_future_no_mutation_eligible")
    if selection.get("future_no_mutation_intake_only") is not True:
        findings.append("future_no_mutation_boundary_missing")
    if authorisation.get("eligible_for_future_no_mutation_intake") is not True:
        findings.append("authorisation_future_eligibility_missing")
    if not findings:
        findings.append("first_candidate_selection_matches_authorisation_gate")
    return tuple(findings)


def _review_status(
    selection: dict[str, Any],
    authorisation: dict[str, Any],
    blocked: tuple[str, ...],
    findings: tuple[str, ...],
) -> str:
    if "mutation_or_ingestion_claim" in blocked:
        return FIRST_CANDIDATE_BLOCKED_MUTATION_OR_INGESTION_CLAIM
    if "runtime_or_production_overstatement" in blocked:
        return FIRST_CANDIDATE_BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if not selection and not authorisation:
        return UNKNOWN_REQUIRES_REVIEW
    if findings != ("first_candidate_selection_matches_authorisation_gate",):
        return FIRST_CANDIDATE_NEEDS_HUMAN_REVIEW
    return FIRST_CANDIDATE_REVIEW_READY


def _required_caveats(
    selection: dict[str, Any],
    authorisation: dict[str, Any],
) -> tuple[str, ...]:
    caveats = [
        *[str(item) for item in _as_tuple(selection.get("required_caveats"))],
        *[str(item) for item in _as_tuple(authorisation.get("required_caveats"))],
        *REQUIRED_CAVEATS,
    ]
    return tuple(dict.fromkeys(item for item in caveats if item))


def _explanation(status: str) -> str:
    if status == FIRST_CANDIDATE_REVIEW_READY:
        return (
            "The selected first candidate matches the authorisation gate and is "
            "ready only for a future no-mutation intake decision; no intake or "
            "mutation was authorised or performed."
        )
    if status.startswith("FIRST_CANDIDATE_BLOCKED"):
        return (
            "The review found a blocked ingestion, mutation, runtime, or "
            "production claim; no action was performed."
        )
    return (
        "The selected first candidate or authorisation metadata is missing, "
        "unknown, or mismatched and requires human review."
    )


def _has_claim(metadata: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return any(bool(metadata.get(key)) for key in keys)


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(sorted(value))
    return (value,)


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-evidence-intake-first-candidate-review-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]
