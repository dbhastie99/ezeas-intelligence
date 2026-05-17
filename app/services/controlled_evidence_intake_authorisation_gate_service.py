import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE = (
    "AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE"
)
NEEDS_SOURCE_CONTEXT = "NEEDS_SOURCE_CONTEXT"
NEEDS_STATUS_BOUNDARY = "NEEDS_STATUS_BOUNDARY"
NEEDS_TRUST_REVIEW = "NEEDS_TRUST_REVIEW"
BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT = (
    "BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT"
)
BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM = (
    "BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM"
)
BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM = "BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM"
BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM = (
    "BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM"
)
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

UNKNOWN_VALUES = {"", "UNKNOWN", "UNKNOWN_REQUIRES_REVIEW", "UNTRUSTED", "REQUIRES_REVIEW"}

RUNTIME_OR_PRODUCTION_CLAIM_KEYS = (
    "runtime_claim_permitted",
    "production_claim_permitted",
    "deployment_claim_permitted",
    "runtime_authorised",
    "production_authorised",
    "deployment_authorised",
    "runtime_readiness_claim_permitted",
    "production_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
)

INGESTION_OR_CORPUS_MUTATION_CLAIM_KEYS = (
    "ingestion_authorised",
    "ingestion_authorised_now",
    "evidence_ingestion_authorised",
    "evidence_ingestion_authorised_now",
    "evidence_ingestion_performed",
    "ingestion_performed",
    "corpus_mutation_authorised",
    "corpus_mutation_authorised_now",
    "corpus_mutation_performed",
)

CODE_EVIDENCE_INGESTION_CLAIM_KEYS = (
    "code_evidence_ingestion_authorised",
    "code_evidence_ingestion_authorised_now",
    "code_evidence_ingestion_performed",
)

DB_RETRIEVAL_LLM_FINAL_ANSWER_CLAIM_KEYS = (
    "db_write_authorised",
    "db_write_authorised_now",
    "db_write_performed",
    "db_access_authorised",
    "db_read_performed",
    "live_retrieval_authorised",
    "live_retrieval_performed",
    "live_llm_authorised",
    "live_llm_performed",
    "final_answer_generation_authorised",
    "final_answer_generation_performed",
)

PROHIBITED_INFERENCES = (
    "Future no-mutation intake eligibility is not current intake authorisation.",
    "Authorisation metadata is not evidence ingestion.",
    "Authorisation metadata is not corpus mutation.",
    "Authorisation metadata is not Code Evidence ingestion.",
    "Authorisation metadata is not DB, live retrieval, live LLM, or final answer generation readiness.",
    "Authorisation metadata is not runtime, deployment, or production readiness.",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeAuthorisationGateResult:
    authorisation_id: str
    candidate_id: str
    authorisation_decision: str
    eligible_for_future_no_mutation_intake: bool
    intake_authorised_now: bool
    evidence_ingestion_performed: bool
    corpus_mutation_performed: bool
    code_evidence_ingestion_performed: bool
    db_write_performed: bool
    live_retrieval_performed: bool
    live_llm_performed: bool
    final_answer_generation_performed: bool
    missing_prerequisites: tuple[str, ...]
    blocked_reasons: tuple[str, ...]
    required_caveats: tuple[str, ...]
    prohibited_inferences: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_controlled_evidence_intake_authorisation_gate(
    candidate_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    """Authorise future no-mutation intake candidacy without performing intake."""

    metadata = candidate_metadata or {}
    candidate_id = str(metadata.get("candidate_id") or metadata.get("evidence_id") or "")
    missing = _missing_prerequisites(metadata)
    blocked = _blocked_reasons(metadata)
    decision = _authorisation_decision(metadata, missing, blocked)
    eligible = decision == AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE
    caveats = _required_caveats(metadata)

    material = {
        "candidate_id": candidate_id,
        "candidate_type": metadata.get("candidate_type") or metadata.get("evidence_category") or "",
        "source_repo": metadata.get("source_repo") or "",
        "source_phase": metadata.get("source_phase") or "",
        "source_status": metadata.get("source_status") or metadata.get("status_boundary") or "",
        "trust_level": metadata.get("trust_level") or "",
        "missing": missing,
        "blocked": blocked,
        "caveats": caveats,
    }

    return ControlledEvidenceIntakeAuthorisationGateResult(
        authorisation_id=str(metadata.get("authorisation_id") or _stable_id(material)),
        candidate_id=candidate_id,
        authorisation_decision=decision,
        eligible_for_future_no_mutation_intake=eligible,
        intake_authorised_now=False,
        evidence_ingestion_performed=False,
        corpus_mutation_performed=False,
        code_evidence_ingestion_performed=False,
        db_write_performed=False,
        live_retrieval_performed=False,
        live_llm_performed=False,
        final_answer_generation_performed=False,
        missing_prerequisites=missing,
        blocked_reasons=blocked,
        required_caveats=caveats,
        prohibited_inferences=PROHIBITED_INFERENCES,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(decision),
    ).to_dict()


def build_controlled_evidence_intake_authorisation_gate(
    candidate_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return evaluate_controlled_evidence_intake_authorisation_gate(candidate_metadata)


def _missing_prerequisites(metadata: dict[str, Any]) -> tuple[str, ...]:
    missing: list[str] = []
    if _unknown(metadata.get("candidate_id") or metadata.get("evidence_id")):
        missing.append("candidate_id")
    if _unknown(metadata.get("candidate_type") or metadata.get("evidence_category")):
        missing.append("candidate_type")
    if _unknown(metadata.get("source_repo")) or _unknown(metadata.get("source_phase")):
        missing.append("source_context")
    if _unknown(metadata.get("source_status") or metadata.get("status_boundary")):
        missing.append("status_boundary")
    if _unknown(metadata.get("trust_level")):
        missing.append("trust_level")
    if not _as_tuple(metadata.get("required_caveats")):
        missing.append("required_caveats")
    return tuple(missing)


def _blocked_reasons(metadata: dict[str, Any]) -> tuple[str, ...]:
    blocked: list[str] = []
    if any(bool(metadata.get(key)) for key in RUNTIME_OR_PRODUCTION_CLAIM_KEYS):
        blocked.append("runtime_or_production_overstatement")
    if any(bool(metadata.get(key)) for key in INGESTION_OR_CORPUS_MUTATION_CLAIM_KEYS):
        blocked.append("unauthorised_ingestion_or_corpus_mutation_claim")
    if any(bool(metadata.get(key)) for key in CODE_EVIDENCE_INGESTION_CLAIM_KEYS):
        blocked.append("code_evidence_ingestion_claim")
    if any(bool(metadata.get(key)) for key in DB_RETRIEVAL_LLM_FINAL_ANSWER_CLAIM_KEYS):
        blocked.append("db_live_retrieval_llm_or_final_answer_claim")
    return tuple(blocked)


def _authorisation_decision(
    metadata: dict[str, Any],
    missing: tuple[str, ...],
    blocked: tuple[str, ...],
) -> str:
    if "runtime_or_production_overstatement" in blocked:
        return BLOCKED_RUNTIME_OR_PRODUCTION_OVERSTATEMENT
    if "unauthorised_ingestion_or_corpus_mutation_claim" in blocked:
        return BLOCKED_UNAUTHORISED_INGESTION_OR_CORPUS_MUTATION_CLAIM
    if "code_evidence_ingestion_claim" in blocked:
        return BLOCKED_CODE_EVIDENCE_INGESTION_CLAIM
    if "db_live_retrieval_llm_or_final_answer_claim" in blocked:
        return BLOCKED_DB_LIVE_RETRIEVAL_LLM_OR_FINAL_ANSWER_CLAIM
    if _unknown(metadata.get("candidate_type") or metadata.get("evidence_category")):
        return UNKNOWN_REQUIRES_REVIEW
    if "source_context" in missing:
        return NEEDS_SOURCE_CONTEXT
    if "status_boundary" in missing:
        return NEEDS_STATUS_BOUNDARY
    if "trust_level" in missing:
        return NEEDS_TRUST_REVIEW
    if missing:
        return UNKNOWN_REQUIRES_REVIEW
    return AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE


def _required_caveats(metadata: dict[str, Any]) -> tuple[str, ...]:
    return _dedupe(
        (
            *_as_tuple(metadata.get("required_caveats")),
            "Future no-mutation intake eligibility only.",
            "No evidence ingestion, corpus mutation, Code Evidence ingestion, DB write, live retrieval, live LLM, or final answer generation is authorised now.",
        )
    )


def _explanation(decision: str) -> str:
    if decision == AUTHORISED_FOR_FUTURE_NO_MUTATION_INTAKE:
        return (
            "Candidate metadata is eligible for a future no-mutation intake attempt "
            "only; intake is not authorised now and no action was performed."
        )
    if decision.startswith("BLOCKED"):
        return (
            "Candidate metadata contains a blocked claim for this local "
            "authorisation-gate slice; no action was performed."
        )
    return (
        "Candidate metadata is incomplete or unknown and requires controlled "
        "review before any future no-mutation intake attempt."
    )


def _unknown(value: Any) -> bool:
    return str(value or "").strip().upper() in UNKNOWN_VALUES


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


def _dedupe(value: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(item) for item in _as_tuple(value) if str(item)))


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "controlled-evidence-intake-authorisation-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]
