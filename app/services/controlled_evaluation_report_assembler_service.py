from dataclasses import asdict, dataclass
from typing import Any

from app.services.evaluation_output_publication_gate_service import (
    evaluate_evaluation_output_publication_gate,
)


REPORT_TYPES = (
    "CONTROLLED_EVALUATION_REPORT",
    "DEVELOPER_HANDOFF",
    "PROGRESS_SUMMARY",
    "NEXT_SLICE_RECOMMENDATION",
    "UNKNOWN_REQUIRES_REVIEW",
)

BASE_REQUIRED_CAVEATS = (
    "Minerva remains controlled-readiness only.",
    "This report assembler does not authorise runtime, deployment, production, exposure, DB access, corpus mutation, Code Evidence ingestion, live LLM use, or final natural-language answer generation.",
)

SECTION_KEYS = (
    "report_scope",
    "current_status",
    "evidence_inputs",
    "preferred_current_state_evidence",
    "controlled_readiness_summary",
    "publication_decision",
    "required_caveats",
    "preserved_boundaries",
    "blocked_or_deferred_capabilities",
    "no_action_attestation",
    "risks_and_unknowns",
    "recommended_next_slice",
    "developer_handoff",
    "safe_for_controlled_evaluation_report",
    "safe_for_final_answer_generation",
    "explanation",
)

REPORT_TYPE_PATTERNS = (
    (
        "DEVELOPER_HANDOFF",
        ("developer handoff", "handoff note", "handoff notes"),
    ),
    (
        "PROGRESS_SUMMARY",
        ("progress summary", "progress-summary", "status summary", "slice summary"),
    ),
    (
        "NEXT_SLICE_RECOMMENDATION",
        ("next-slice recommendation", "next slice recommendation", "recommended next slice"),
    ),
    (
        "CONTROLLED_EVALUATION_REPORT",
        ("controlled evaluation report", "evaluation report", "controlled-readiness report"),
    ),
)

BOUNDARY_TO_CAPABILITY = {
    "CONTROLLED_READINESS_ONLY": "production/deployment/runtime readiness remains unauthorised",
    "PRODUCTION_DEFERRED": "production readiness deferred",
    "DEPLOYMENT_DEFERRED": "deployment readiness deferred",
    "RUNTIME_DEFERRED": "runtime enablement deferred",
    "CHAT_EXPOSURE_DEFERRED": "chat exposure deferred",
    "ENDPOINT_EXPOSURE_DEFERRED": "endpoint exposure deferred",
    "FINAL_ANSWER_GENERATION_DEFERRED": "final natural-language answer generation deferred",
    "LIVE_LLM_DEFERRED": "live LLM use deferred",
    "DB_ACCESS_DEFERRED": "DB access deferred",
    "DB_VALIDATION_DEFERRED": "DB validation deferred",
    "CORPUS_MUTATION_DEFERRED": "corpus mutation deferred",
    "CODE_EVIDENCE_INGESTION_DEFERRED": "Code Evidence ingestion deferred",
    "WORKFORCE_RUNTIME_INTEGRATION_DEFERRED": "workforce-platform runtime integration deferred",
    "ANALYTICS_RUNTIME_INTEGRATION_DEFERRED": "ezeas-analytics runtime integration deferred",
}

BLOCKED_CLAIM_TO_CAPABILITY = {
    "PRODUCTION_READINESS_CLAIM": "production readiness claim blocked",
    "DEPLOYMENT_READINESS_CLAIM": "deployment readiness claim blocked",
    "RUNTIME_READINESS_CLAIM": "runtime readiness claim blocked",
    "CHAT_EXPOSURE_CLAIM": "chat exposure claim blocked",
    "ENDPOINT_EXPOSURE_CLAIM": "endpoint exposure claim blocked",
    "FINAL_ANSWER_GENERATION_CLAIM": "final answer generation claim blocked",
    "LIVE_LLM_CLAIM": "live LLM claim blocked",
    "DB_ACCESS_CLAIM": "DB access claim blocked",
    "DB_VALIDATION_CLAIM": "DB validation claim blocked",
    "CORPUS_MUTATION_CLAIM": "corpus mutation claim blocked",
    "CODE_EVIDENCE_INGESTION_CLAIM": "Code Evidence ingestion claim blocked",
    "WORKFORCE_RUNTIME_INTEGRATION_CLAIM": "workforce-platform runtime integration claim blocked",
    "ANALYTICS_RUNTIME_INTEGRATION_CLAIM": "ezeas-analytics runtime integration claim blocked",
}


@dataclass(frozen=True)
class ControlledEvaluationReportAssemblerResult:
    report_title: str
    report_type: str
    safe_for_controlled_evaluation_report: bool
    safe_for_developer_handoff: bool
    safe_for_progress_summary: bool
    safe_for_final_answer_generation: bool
    publication_decision: str
    sections: dict[str, Any]
    required_caveats: tuple[str, ...]
    missing_caveats: tuple[str, ...]
    preserved_boundaries: tuple[str, ...]
    violated_boundaries: tuple[str, ...]
    blocked_or_deferred_capabilities: tuple[str, ...]
    no_action_attestation: Any
    recommended_next_slice: Any
    risks_and_unknowns: Any
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def assemble_controlled_evaluation_report(metadata: Any) -> dict[str, Any]:
    normalized = _normalize_metadata(metadata)
    report_type = _report_type(normalized)
    report_title = _report_title(normalized, report_type)
    candidate = _publication_candidate(normalized, report_type)
    gate = evaluate_evaluation_output_publication_gate(candidate)

    if gate["publication_decision"] in (
        "NEEDS_CAVEAT_BEFORE_PUBLICATION",
        "UNKNOWN_REQUIRES_HUMAN_REVIEW",
    ):
        report_type = "UNKNOWN_REQUIRES_REVIEW"

    safe_for_controlled_evaluation_report = (
        gate["safe_for_controlled_evaluation_report"]
        and report_type in ("CONTROLLED_EVALUATION_REPORT", "NEXT_SLICE_RECOMMENDATION")
    )
    safe_for_developer_handoff = (
        gate["safe_for_developer_handoff"] and report_type == "DEVELOPER_HANDOFF"
    )
    safe_for_progress_summary = (
        gate["safe_for_progress_summary"] and report_type == "PROGRESS_SUMMARY"
    )

    required_caveats = _dedupe(
        BASE_REQUIRED_CAVEATS + tuple(gate.get("required_caveats", ()))
    )
    preserved_boundaries = tuple(gate.get("preserved_boundaries", ()))
    blocked_or_deferred = _blocked_or_deferred_capabilities(
        preserved_boundaries,
        tuple(gate.get("block_reasons", ())),
        normalized.get("blocked_or_deferred_capabilities"),
    )

    sections = _sections(
        normalized=normalized,
        gate=gate,
        required_caveats=required_caveats,
        preserved_boundaries=preserved_boundaries,
        blocked_or_deferred=blocked_or_deferred,
        safe_for_controlled_evaluation_report=safe_for_controlled_evaluation_report,
    )

    return ControlledEvaluationReportAssemblerResult(
        report_title=report_title,
        report_type=report_type,
        safe_for_controlled_evaluation_report=safe_for_controlled_evaluation_report,
        safe_for_developer_handoff=safe_for_developer_handoff,
        safe_for_progress_summary=safe_for_progress_summary,
        safe_for_final_answer_generation=False,
        publication_decision=gate["publication_decision"],
        sections=sections,
        required_caveats=required_caveats,
        missing_caveats=tuple(gate.get("missing_caveats", ())),
        preserved_boundaries=preserved_boundaries,
        violated_boundaries=tuple(gate.get("violated_boundaries", ())),
        blocked_or_deferred_capabilities=blocked_or_deferred,
        no_action_attestation=normalized.get("no_action_attestation", ""),
        recommended_next_slice=normalized.get("recommended_next_slice", ""),
        risks_and_unknowns=normalized.get("risks_and_unknowns", ()),
        explanation=_explanation(gate, report_type),
    ).to_dict()


def assemble_minerva_controlled_evaluation_report(metadata: Any) -> dict[str, Any]:
    return assemble_controlled_evaluation_report(metadata)


def _normalize_metadata(metadata: Any) -> dict[str, Any]:
    if metadata is None:
        return {}
    if isinstance(metadata, dict):
        return dict(metadata)
    return {"content": metadata}


def _publication_candidate(metadata: dict[str, Any], report_type: str) -> dict[str, Any]:
    candidate = dict(metadata)
    candidate["publication_target"] = _publication_target(report_type)
    return candidate


def _publication_target(report_type: str) -> str:
    if report_type == "DEVELOPER_HANDOFF":
        return "developer handoff"
    if report_type == "PROGRESS_SUMMARY":
        return "progress summary"
    return "controlled evaluation report"


def _report_type(metadata: dict[str, Any]) -> str:
    supplied = str(
        metadata.get("report_type")
        or metadata.get("publication_target")
        or metadata.get("target")
        or metadata.get("artifact_type")
        or metadata.get("artefact_type")
        or ""
    )
    normalized_supplied = supplied.strip().upper().replace("-", "_").replace(" ", "_")
    if normalized_supplied in REPORT_TYPES:
        return normalized_supplied

    text = _normalize_text(_metadata_text(metadata))
    for report_type, patterns in REPORT_TYPE_PATTERNS:
        if _contains_any(text, patterns):
            return report_type
    return "CONTROLLED_EVALUATION_REPORT" if text.strip() else "UNKNOWN_REQUIRES_REVIEW"


def _report_title(metadata: dict[str, Any], report_type: str) -> str:
    supplied_title = str(metadata.get("report_title") or metadata.get("title") or "").strip()
    if supplied_title:
        return supplied_title
    return report_type.replace("_", " ").title()


def _sections(
    normalized: dict[str, Any],
    gate: dict[str, Any],
    required_caveats: tuple[str, ...],
    preserved_boundaries: tuple[str, ...],
    blocked_or_deferred: tuple[str, ...],
    safe_for_controlled_evaluation_report: bool,
) -> dict[str, Any]:
    sections = {
        "report_scope": normalized.get("report_scope", ""),
        "current_status": normalized.get("current_status", ""),
        "evidence_inputs": normalized.get("evidence_inputs", ()),
        "preferred_current_state_evidence": normalized.get(
            "preferred_current_state_evidence", ""
        ),
        "controlled_readiness_summary": normalized.get(
            "controlled_readiness_summary", ""
        ),
        "publication_decision": gate["publication_decision"],
        "required_caveats": required_caveats,
        "preserved_boundaries": preserved_boundaries,
        "blocked_or_deferred_capabilities": blocked_or_deferred,
        "no_action_attestation": normalized.get("no_action_attestation", ""),
        "risks_and_unknowns": normalized.get("risks_and_unknowns", ()),
        "recommended_next_slice": normalized.get("recommended_next_slice", ""),
        "developer_handoff": normalized.get("developer_handoff", ""),
        "safe_for_controlled_evaluation_report": safe_for_controlled_evaluation_report,
        "safe_for_final_answer_generation": False,
        "explanation": gate["explanation"],
    }
    return {key: sections[key] for key in SECTION_KEYS}


def _blocked_or_deferred_capabilities(
    preserved_boundaries: tuple[str, ...],
    block_reasons: tuple[str, ...],
    supplied: Any,
) -> tuple[str, ...]:
    capabilities: list[str] = []
    capabilities.extend(_as_tuple(supplied))
    capabilities.extend(
        BOUNDARY_TO_CAPABILITY[boundary]
        for boundary in preserved_boundaries
        if boundary in BOUNDARY_TO_CAPABILITY
    )
    capabilities.extend(
        BLOCKED_CLAIM_TO_CAPABILITY[reason]
        for reason in block_reasons
        if reason in BLOCKED_CLAIM_TO_CAPABILITY
    )
    return _dedupe(tuple(str(capability) for capability in capabilities if capability))


def _metadata_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(f"{key}: {_metadata_text(item)}" for key, item in value.items())
    if isinstance(value, (list, tuple, set)):
        return "\n".join(_metadata_text(item) for item in value)
    return str(value)


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().replace("_", " ").split())


def _contains_any(normalized_text: str, patterns: tuple[str, ...]) -> bool:
    return any(pattern in normalized_text for pattern in patterns)


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


def _dedupe(values: tuple[Any, ...]) -> tuple[Any, ...]:
    return tuple(dict.fromkeys(values))


def _explanation(gate: dict[str, Any], report_type: str) -> str:
    if report_type == "UNKNOWN_REQUIRES_REVIEW":
        return (
            "Controlled report assembly requires review because required caveats are "
            "missing or the publication target/status is ambiguous."
        )
    return (
        gate["explanation"]
        + " The assembler returned structured internal report metadata only and never "
        "marks output safe for final answer generation."
    )
