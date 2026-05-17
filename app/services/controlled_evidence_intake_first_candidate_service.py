import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_authorisation_gate_service import (
    AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE,
    UNKNOWN_REQUIRES_REVIEW,
    build_controlled_evidence_intake_authorisation_gate,
)
from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DEVELOPER_LOG = "DEVELOPER_LOG"
HARDENING_LOG = "HARDENING_LOG"
PLATFORM_DOCTRINE = "PLATFORM_DOCTRINE"
ANALYTICS_READINESS_SUMMARY = "ANALYTICS_READINESS_SUMMARY"
AWARD_RECOVERY_ANALYSIS = "AWARD_RECOVERY_ANALYSIS"
CONTROLLED_EVALUATION_SUMMARY = "CONTROLLED_EVALUATION_SUMMARY"
UNKNOWN_REQUIRES_REVIEW_TYPE = "UNKNOWN_REQUIRES_REVIEW"

FUTURE_NO_MUTATION_INTAKE_ONLY = (
    "Recommended candidate is limited to a future no-mutation intake attempt."
)

TYPE_RANKS = {
    ANALYTICS_READINESS_SUMMARY: 0,
    CONTROLLED_EVALUATION_SUMMARY: 1,
    PLATFORM_DOCTRINE: 2,
    HARDENING_LOG: 3,
    DEVELOPER_LOG: 4,
    AWARD_RECOVERY_ANALYSIS: 5,
}

REJECTED_DECISIONS = {
    UNKNOWN_REQUIRES_REVIEW,
    "NEEDS_SOURCE_CONTEXT",
    "NEEDS_STATUS_BOUNDARY",
    "NEEDS_TRUST_REVIEW",
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT",
    "BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM",
    "BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM",
    "BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM",
}


@dataclass(frozen=True)
class ControlledEvidenceIntakeFirstCandidateResult:
    selection_id: str
    recommended_candidate_id: str
    recommended_candidate_type: str
    selection_reason: str
    candidate_rankings: tuple[dict[str, Any], ...]
    rejected_candidates: tuple[dict[str, Any], ...]
    required_caveats: tuple[str, ...]
    future_no_mutation_intake_only: bool
    evidence_ingestion_authorised_now: bool
    corpus_mutation_authorised_now: bool
    code_evidence_ingestion_authorised_now: bool
    db_write_authorised_now: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def select_controlled_evidence_intake_first_candidate(
    candidate_options: list[dict[str, Any]] | tuple[dict[str, Any], ...] | None,
) -> dict[str, Any]:
    """Recommend the safest first future no-mutation intake candidate."""

    options = tuple(candidate_options or ())
    evaluated = tuple(_evaluate_candidate(candidate) for candidate in options)
    accepted = tuple(item for item in evaluated if item["accepted"])
    rejected = tuple(_rejected_candidate(item) for item in evaluated if not item["accepted"])
    rankings = tuple(_ranking(item, index) for index, item in enumerate(_ranked(accepted), start=1))
    recommended = rankings[0] if rankings else None
    recommended_id = str(recommended["candidate_id"]) if recommended else ""
    recommended_type = str(recommended["candidate_type"]) if recommended else UNKNOWN_REQUIRES_REVIEW_TYPE
    caveats = _required_caveats(recommended, rejected)

    material = {
        "recommended_candidate_id": recommended_id,
        "recommended_candidate_type": recommended_type,
        "candidate_rankings": rankings,
        "rejected_candidates": rejected,
        "required_caveats": caveats,
    }

    return ControlledEvidenceIntakeFirstCandidateResult(
        selection_id=_selection_id(material),
        recommended_candidate_id=recommended_id,
        recommended_candidate_type=recommended_type,
        selection_reason=_selection_reason(recommended),
        candidate_rankings=rankings,
        rejected_candidates=rejected,
        required_caveats=caveats,
        future_no_mutation_intake_only=True,
        evidence_ingestion_authorised_now=False,
        corpus_mutation_authorised_now=False,
        code_evidence_ingestion_authorised_now=False,
        db_write_authorised_now=False,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(recommended),
    ).to_dict()


def build_controlled_evidence_intake_first_candidate(
    candidate_options: list[dict[str, Any]] | tuple[dict[str, Any], ...] | None,
) -> dict[str, Any]:
    return select_controlled_evidence_intake_first_candidate(candidate_options)


def _evaluate_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    gate = build_controlled_evidence_intake_authorisation_gate(candidate)
    candidate_type = _candidate_type(candidate)
    accepted = (
        gate["authorisation_decision"] == AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE
        and candidate_type in TYPE_RANKS
    )
    return {
        "candidate": dict(candidate),
        "candidate_id": str(candidate.get("candidate_id") or candidate.get("evidence_id") or ""),
        "candidate_type": candidate_type,
        "authorisation_decision": gate["authorisation_decision"],
        "blocked_reasons": tuple(gate["blocked_reasons"]),
        "required_caveats": tuple(gate["required_caveats"]),
        "accepted": accepted,
        "rank_score": TYPE_RANKS.get(candidate_type, 99),
        "trust_score": _trust_score(candidate.get("trust_level")),
    }


def _ranked(evaluated: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    return tuple(
        sorted(
            evaluated,
            key=lambda item: (
                item["rank_score"],
                item["trust_score"],
                item["candidate_id"],
            ),
        )
    )


def _ranking(item: dict[str, Any], rank: int) -> dict[str, Any]:
    return {
        "rank": rank,
        "candidate_id": item["candidate_id"],
        "candidate_type": item["candidate_type"],
        "authorisation_decision": item["authorisation_decision"],
        "selection_basis": "complete_controlled_metadata",
    }


def _rejected_candidate(item: dict[str, Any]) -> dict[str, Any]:
    reason = item["authorisation_decision"]
    if item["candidate_type"] not in TYPE_RANKS:
        reason = UNKNOWN_REQUIRES_REVIEW_TYPE
    return {
        "candidate_id": item["candidate_id"],
        "candidate_type": item["candidate_type"],
        "rejection_reason": reason,
        "blocked_reasons": item["blocked_reasons"],
    }


def _candidate_type(candidate: dict[str, Any]) -> str:
    return str(
        candidate.get("candidate_type")
        or candidate.get("evidence_category")
        or UNKNOWN_REQUIRES_REVIEW_TYPE
    ).strip().upper()


def _trust_score(trust_level: Any) -> int:
    normalized = str(trust_level or "").strip().upper()
    if normalized in {"CONTROLLED_INTERNAL", "CONTROLLED_SUMMARY", "TRUSTED_CONTROLLED"}:
        return 0
    if normalized in {"INTERNAL", "REVIEWED"}:
        return 1
    return 9


def _required_caveats(
    recommended: dict[str, Any] | None,
    rejected: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    caveats: list[str] = [FUTURE_NO_MUTATION_INTAKE_ONLY]
    if recommended:
        caveats.extend(str(item) for item in recommended.get("required_caveats", ()))
    if rejected:
        caveats.append("Rejected or unknown candidates require controlled review.")
    caveats.append(
        "No evidence ingestion, corpus mutation, Code Evidence ingestion, or DB write is authorised now."
    )
    return tuple(dict.fromkeys(item for item in caveats if item))


def _selection_reason(recommended: dict[str, Any] | None) -> str:
    if not recommended:
        return "No candidate is eligible; unknown or blocked candidates require controlled review."
    return (
        f"{recommended['candidate_type']} has complete controlled metadata and "
        "is the safest ranked future no-mutation intake candidate."
    )


def _explanation(recommended: dict[str, Any] | None) -> str:
    if recommended:
        return (
            "Selection ranks eligible candidates for a future no-mutation intake "
            "attempt only; no ingestion, mutation, Code Evidence ingestion, or DB "
            "write is authorised now."
        )
    return (
        "No eligible first candidate was selected because all supplied candidates "
        "were unknown, incomplete, or blocked; no action was performed."
    )


def _selection_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-evidence-intake-first-candidate-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]
