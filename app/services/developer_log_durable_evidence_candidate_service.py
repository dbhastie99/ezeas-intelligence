import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


DEVELOPER_LOG_CANDIDATE_READY = "DEVELOPER_LOG_CANDIDATE_READY"
NEEDS_SOURCE_REFERENCE = "NEEDS_SOURCE_REFERENCE"
NEEDS_SOURCE_STATUS = "NEEDS_SOURCE_STATUS"
NEEDS_REQUIRED_SECTIONS = "NEEDS_REQUIRED_SECTIONS"
NEEDS_SENSITIVE_DATA_REVIEW = "NEEDS_SENSITIVE_DATA_REVIEW"
BLOCKED_PROHIBITED_CLAIMS = "BLOCKED_PROHIBITED_CLAIMS"
UNKNOWN_REQUIRES_REVIEW = "UNKNOWN_REQUIRES_REVIEW"

CANDIDATE_TYPE = "DEVELOPER_LOG"
EVIDENCE_CATEGORY = "DEVELOPER_LOG_DURABLE_EVIDENCE_CANDIDATE"

REQUIRED_DEVELOPER_LOG_SECTIONS = (
    "Purpose of This Log for Minerva",
    "Objectives",
    "Work Completed",
    "Issues Encountered",
    "Current Status",
    "Work Log",
    "Important Decisions Captured",
    "Still to Do / Do Not Lose",
    "User Guide / Rationale & Operating Model",
)

PROHIBITED_CLAIM_KEYS = (
    "corpus_mutation_performed",
    "db_write_performed",
    "code_evidence_ingestion_performed",
    "live_retrieval_performed",
    "live_llm_performed",
    "final_answer_generation_performed",
    "chat_exposure_authorised",
    "runtime_authorised",
    "deployment_authorised",
    "production_authorised",
    "runtime_readiness_claim_permitted",
    "deployment_readiness_claim_permitted",
    "production_readiness_claim_permitted",
)

PROHIBITED_CLAIM_TERMS = (
    "production ready",
    "deployment ready",
    "runtime ready",
    "live chat enabled",
    "db write performed",
    "database write performed",
    "live corpus mutation performed",
    "code evidence ingestion performed",
    "live llm performed",
    "final answer generation performed",
)

REQUIRED_CAVEATS = (
    "Developer Log evidence is a controlled durable candidate only.",
    "Source status must remain explicit and must not imply runtime, deployment, or production readiness.",
    "No live corpus mutation, DB write, Code Evidence ingestion, live retrieval, live LLM, final answer generation, or chat exposure is authorised.",
)


@dataclass(frozen=True)
class DeveloperLogDurableEvidenceCandidateResult:
    candidate_id: str
    candidate_type: str
    candidate_status: str
    source_reference: str
    source_status: str
    evidence_category: str
    evidence_title: str
    evidence_date: str
    repository_context: str
    phase_context: str
    required_sections_present: bool
    missing_sections: tuple[str, ...]
    sensitive_data_review_required: bool
    prohibited_claims_present: bool
    eligible_for_durable_intake: bool
    required_caveats: tuple[str, ...]
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_developer_log_durable_evidence_candidate(
    developer_log_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    return evaluate_developer_log_durable_evidence_candidate(developer_log_metadata)


def evaluate_developer_log_durable_evidence_candidate(
    developer_log_metadata: dict[str, Any] | None,
) -> dict[str, Any]:
    metadata = developer_log_metadata or {}
    source_reference = str(metadata.get("source_reference") or "")
    source_status = str(metadata.get("source_status") or "")
    evidence_title = str(metadata.get("evidence_title") or "")
    evidence_date = str(metadata.get("evidence_date") or "")
    repository_context = str(metadata.get("repository_context") or "")
    phase_context = str(metadata.get("phase_context") or "")
    present_sections = _normalised_sections(metadata)
    missing_sections = tuple(
        section
        for section in REQUIRED_DEVELOPER_LOG_SECTIONS
        if section not in present_sections
    )
    prohibited_claims_present = _prohibited_claims_present(metadata)
    status = _candidate_status(
        metadata=metadata,
        source_reference=source_reference,
        source_status=source_status,
        missing_sections=missing_sections,
        prohibited_claims_present=prohibited_claims_present,
    )
    eligible = status == DEVELOPER_LOG_CANDIDATE_READY
    material = {
        "source_reference": source_reference,
        "source_status": source_status,
        "evidence_title": evidence_title,
        "evidence_date": evidence_date,
        "repository_context": repository_context,
        "phase_context": phase_context,
        "missing_sections": missing_sections,
        "sensitive_data_review_completed": metadata.get(
            "sensitive_data_review_completed"
        ),
        "status": status,
    }

    return DeveloperLogDurableEvidenceCandidateResult(
        candidate_id=str(metadata.get("candidate_id") or _stable_id(material)),
        candidate_type=CANDIDATE_TYPE,
        candidate_status=status,
        source_reference=source_reference,
        source_status=source_status,
        evidence_category=EVIDENCE_CATEGORY,
        evidence_title=evidence_title,
        evidence_date=evidence_date,
        repository_context=repository_context,
        phase_context=phase_context,
        required_sections_present=not missing_sections,
        missing_sections=missing_sections,
        sensitive_data_review_required=metadata.get(
            "sensitive_data_review_completed"
        )
        is not True,
        prohibited_claims_present=prohibited_claims_present,
        eligible_for_durable_intake=eligible,
        required_caveats=REQUIRED_CAVEATS,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(status),
    ).to_dict()


def _normalised_sections(metadata: dict[str, Any]) -> set[str]:
    sections = metadata.get("sections_present") or metadata.get("required_sections") or ()
    return {str(section).strip() for section in sections if str(section).strip()}


def _prohibited_claims_present(metadata: dict[str, Any]) -> bool:
    if any(bool(metadata.get(key)) for key in PROHIBITED_CLAIM_KEYS):
        return True
    text = " ".join(
        str(metadata.get(key) or "")
        for key in ("evidence_title", "phase_context", "summary", "claims_text")
    ).lower()
    return any(term in text for term in PROHIBITED_CLAIM_TERMS)


def _candidate_status(
    metadata: dict[str, Any],
    source_reference: str,
    source_status: str,
    missing_sections: tuple[str, ...],
    prohibited_claims_present: bool,
) -> str:
    if prohibited_claims_present:
        return BLOCKED_PROHIBITED_CLAIMS
    if str(metadata.get("candidate_type") or CANDIDATE_TYPE) != CANDIDATE_TYPE:
        return UNKNOWN_REQUIRES_REVIEW
    if not source_reference:
        return NEEDS_SOURCE_REFERENCE
    if not source_status:
        return NEEDS_SOURCE_STATUS
    if missing_sections:
        return NEEDS_REQUIRED_SECTIONS
    if metadata.get("sensitive_data_review_completed") is not True:
        return NEEDS_SENSITIVE_DATA_REVIEW
    return DEVELOPER_LOG_CANDIDATE_READY


def _explanation(status: str) -> str:
    if status == DEVELOPER_LOG_CANDIDATE_READY:
        return (
            "Developer Log metadata is complete, sensitive-data reviewed, and "
            "eligible only for controlled local durable-intake preparation."
        )
    if status == BLOCKED_PROHIBITED_CLAIMS:
        return "Developer Log metadata contains a prohibited runtime, production, mutation, DB, retrieval, LLM, final-answer, or chat claim."
    if status == NEEDS_SOURCE_REFERENCE:
        return "Developer Log metadata must identify its source reference."
    if status == NEEDS_SOURCE_STATUS:
        return "Developer Log metadata must preserve explicit source status."
    if status == NEEDS_REQUIRED_SECTIONS:
        return "Developer Log metadata is missing one or more required sections."
    if status == NEEDS_SENSITIVE_DATA_REVIEW:
        return "Developer Log metadata requires completed sensitive-data review."
    return "Developer Log metadata is unknown or requires controlled review."


def _stable_id(material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return "developer-log-durable-evidence-candidate-" + hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()[:16]
