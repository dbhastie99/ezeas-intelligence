from dataclasses import asdict, dataclass
from typing import Any, Iterable


EVIDENCE_TYPES = (
    "FINAL_INDEX",
    "FINAL_STATUS",
    "RESUME_MAP",
    "NO_ACTION_ATTESTATION",
    "CLOSEOUT",
    "DECISION_GATE",
    "DESIGN_PACK",
    "IMPLEMENTATION_CANDIDATE",
    "MIDSTREAM_PLANNING_NOTE",
    "HISTORICAL_CONTEXT",
    "UNKNOWN",
)

EVIDENCE_PREFERENCE_RANK = {
    "FINAL_INDEX": 0,
    "FINAL_STATUS": 1,
    "RESUME_MAP": 2,
    "NO_ACTION_ATTESTATION": 3,
    "CLOSEOUT": 4,
    "DECISION_GATE": 5,
    "DESIGN_PACK": 6,
    "IMPLEMENTATION_CANDIDATE": 7,
    "MIDSTREAM_PLANNING_NOTE": 8,
    "HISTORICAL_CONTEXT": 9,
    "UNKNOWN": 10,
}

FINAL_CURRENT_EVIDENCE_TYPES = {
    "FINAL_INDEX",
    "FINAL_STATUS",
    "RESUME_MAP",
    "NO_ACTION_ATTESTATION",
    "CLOSEOUT",
}

NON_OVERRIDE_EVIDENCE_TYPES = {
    "IMPLEMENTATION_CANDIDATE",
    "DESIGN_PACK",
    "MIDSTREAM_PLANNING_NOTE",
    "HISTORICAL_CONTEXT",
    "UNKNOWN",
}

EVIDENCE_TYPE_KEYWORDS = (
    ("NO_ACTION_ATTESTATION", ("no-action attestation", "no action attestation")),
    ("FINAL_INDEX", ("final index",)),
    ("FINAL_STATUS", ("final status",)),
    ("RESUME_MAP", ("resume map", "resume-map")),
    ("CLOSEOUT", ("closeout", "closed at controlled-readiness")),
    ("DECISION_GATE", ("decision gate", "go/no-go", "go no-go")),
    ("DESIGN_PACK", ("design pack", "design-pack")),
    ("IMPLEMENTATION_CANDIDATE", ("implementation candidate", "candidate implementation")),
    ("MIDSTREAM_PLANNING_NOTE", ("midstream planning", "planning note")),
    ("HISTORICAL_CONTEXT", ("historical context", "historical-only context")),
)

STATUS_TERM_PATTERNS = (
    ("CONTROLLED_READINESS", ("controlled-readiness", "controlled readiness")),
    ("PRODUCTION_READINESS", ("production readiness", "production-ready")),
    ("DEPLOYMENT_READINESS", ("deployment readiness", "deployment-ready")),
    ("RUNTIME_READINESS", ("runtime readiness", "runtime-ready")),
    ("EXPOSURE_DEFERRED", ("exposure deferred", "exposure-deferred")),
    ("NO_INTERNAL_CHAT_EXPOSURE", ("no internal chat exposure", "internal exposure deferred")),
    ("NO_PRODUCTION_CHAT_EXPOSURE", ("no production", "no public", "no tenant", "no customer")),
    ("NOT_IMPLEMENTED", ("not implemented", "no-action", "no action")),
    ("NOT_EXPOSED", ("not exposed", "no exposure", "exposure not enabled")),
    ("NOT_DEPLOYED", ("not deployed", "no deployment", "deployment deferred")),
    ("RUNTIME_DEFERRED", ("runtime deferred", "runtime-creation-deferred", "runtime creation deferred")),
    ("DB_VALIDATION_DEFERRED", ("db-validation-deferred", "db validation deferred")),
    ("FINAL_ANSWER_GENERATION", ("final answer generation", "natural-language answer generation")),
)

BASE_PROHIBITED_OVERSTATEMENTS = (
    "CONTROLLED_READINESS_IS_NOT_PRODUCTION_READINESS",
    "CONTROLLED_READINESS_IS_NOT_DEPLOYMENT_READINESS",
    "CONTROLLED_READINESS_IS_NOT_RUNTIME_READINESS",
    "FINAL_NATURAL_LANGUAGE_ANSWER_GENERATION_NOT_ENABLED",
)

BASE_REQUIRED_CAVEATS = (
    "Controlled-readiness is evidence/status guard readiness only.",
    "This guard does not authorise runtime, deployment, production, exposure, or final natural-language answer generation.",
)


@dataclass(frozen=True)
class ControlledReadinessEvidenceRecord:
    evidence_type: str = "UNKNOWN"
    title: str = ""
    content: str = ""


@dataclass(frozen=True)
class ControlledReadinessStatusGuardResult:
    preferred_evidence_type: str
    preferred_evidence_reason: str
    status_terms_detected: tuple[str, ...]
    prohibited_overstatements: tuple[str, ...]
    required_caveats: tuple[str, ...]
    current_state_confidence: str
    fallback_required: bool
    exposure_deferred_preserved: bool
    runtime_deferred_preserved: bool
    deployment_deferred_preserved: bool
    production_readiness_claim_permitted: bool
    final_answer_generation_claim_permitted: bool
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_controlled_readiness_status_guard(
    evidence_records: Iterable[dict[str, Any] | ControlledReadinessEvidenceRecord | object],
) -> dict[str, Any]:
    records = [_normalize_record(record) for record in evidence_records]
    if not records:
        return _result(
            preferred_evidence_type="UNKNOWN",
            preferred_evidence_reason="No evidence records were supplied.",
            status_terms_detected=(),
            prohibited_overstatements=BASE_PROHIBITED_OVERSTATEMENTS,
            required_caveats=BASE_REQUIRED_CAVEATS
            + ("Fallback required because no current-state evidence was supplied.",),
            current_state_confidence="LOW",
            fallback_required=True,
            exposure_deferred_preserved=False,
            runtime_deferred_preserved=False,
            deployment_deferred_preserved=False,
            explanation="No evidence can support a confident current-state claim.",
        )

    preferred = min(records, key=lambda record: EVIDENCE_PREFERENCE_RANK[record.evidence_type])
    preferred_type = preferred.evidence_type
    all_text = "\n".join(_record_text(record) for record in records)
    terms = _detect_status_terms(all_text)
    prohibited = _prohibited_overstatements(records, terms)
    caveats = _required_caveats(records, terms)
    fallback_required = preferred_type == "UNKNOWN" or all(
        record.evidence_type == "UNKNOWN" for record in records
    )

    return _result(
        preferred_evidence_type=preferred_type,
        preferred_evidence_reason=_preferred_reason(preferred_type),
        status_terms_detected=terms,
        prohibited_overstatements=prohibited,
        required_caveats=caveats,
        current_state_confidence=_confidence(preferred_type, fallback_required),
        fallback_required=fallback_required,
        exposure_deferred_preserved=_has_any(
            terms,
            (
                "EXPOSURE_DEFERRED",
                "NO_INTERNAL_CHAT_EXPOSURE",
                "NO_PRODUCTION_CHAT_EXPOSURE",
                "NOT_EXPOSED",
            ),
        ),
        runtime_deferred_preserved=_has_any(terms, ("RUNTIME_DEFERRED", "NOT_IMPLEMENTED")),
        deployment_deferred_preserved=_has_any(
            terms, ("NOT_DEPLOYED", "DB_VALIDATION_DEFERRED")
        ),
        explanation=_explanation(preferred_type, fallback_required),
    )


def recognize_controlled_readiness_evidence_type(
    evidence_record: dict[str, Any] | ControlledReadinessEvidenceRecord | object,
) -> str:
    return _normalize_record(evidence_record).evidence_type


def _result(
    preferred_evidence_type: str,
    preferred_evidence_reason: str,
    status_terms_detected: tuple[str, ...],
    prohibited_overstatements: tuple[str, ...],
    required_caveats: tuple[str, ...],
    current_state_confidence: str,
    fallback_required: bool,
    exposure_deferred_preserved: bool,
    runtime_deferred_preserved: bool,
    deployment_deferred_preserved: bool,
    explanation: str,
) -> dict[str, Any]:
    return ControlledReadinessStatusGuardResult(
        preferred_evidence_type=preferred_evidence_type,
        preferred_evidence_reason=preferred_evidence_reason,
        status_terms_detected=status_terms_detected,
        prohibited_overstatements=prohibited_overstatements,
        required_caveats=required_caveats,
        current_state_confidence=current_state_confidence,
        fallback_required=fallback_required,
        exposure_deferred_preserved=exposure_deferred_preserved,
        runtime_deferred_preserved=runtime_deferred_preserved,
        deployment_deferred_preserved=deployment_deferred_preserved,
        production_readiness_claim_permitted=False,
        final_answer_generation_claim_permitted=False,
        explanation=explanation,
    ).to_dict()


def _normalize_record(
    record: dict[str, Any] | ControlledReadinessEvidenceRecord | object,
) -> ControlledReadinessEvidenceRecord:
    if isinstance(record, ControlledReadinessEvidenceRecord):
        supplied_type = record.evidence_type
        title = record.title
        content = record.content
    elif isinstance(record, dict):
        supplied_type = _first_value(record, ("evidence_type", "EvidenceType", "type", "Type"))
        title = str(_first_value(record, ("title", "Title", "name", "Name")) or "")
        content = str(_first_value(record, ("content", "Content", "body", "Body", "text", "Text")) or "")
    else:
        supplied_type = _first_attr(record, ("evidence_type", "EvidenceType", "type", "Type"))
        title = str(_first_attr(record, ("title", "Title", "name", "Name")) or "")
        content = str(_first_attr(record, ("content", "Content", "body", "Body", "text", "Text")) or "")

    evidence_type = _normalize_evidence_type(supplied_type, title, content)
    return ControlledReadinessEvidenceRecord(
        evidence_type=evidence_type,
        title=title,
        content=content,
    )


def _normalize_evidence_type(value: Any, title: str, content: str) -> str:
    supplied = str(value or "").strip().upper().replace("-", "_").replace(" ", "_")
    if supplied in EVIDENCE_TYPES:
        return supplied

    text = f"{title}\n{content}".lower()
    for evidence_type, keywords in EVIDENCE_TYPE_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            return evidence_type
    return "UNKNOWN"


def _detect_status_terms(text: str) -> tuple[str, ...]:
    lower_text = text.lower()
    detected = [
        term
        for term, patterns in STATUS_TERM_PATTERNS
        if any(pattern in lower_text for pattern in patterns)
    ]
    return tuple(dict.fromkeys(detected))


def _prohibited_overstatements(
    records: list[ControlledReadinessEvidenceRecord], terms: tuple[str, ...]
) -> tuple[str, ...]:
    prohibited = list(BASE_PROHIBITED_OVERSTATEMENTS)
    if "CONTROLLED_READINESS" in terms:
        prohibited.extend(
            (
                "DO_NOT_CONVERT_CONTROLLED_READINESS_TO_PRODUCTION_READINESS",
                "DO_NOT_CONVERT_CONTROLLED_READINESS_TO_DEPLOYMENT_READINESS",
                "DO_NOT_CONVERT_CONTROLLED_READINESS_TO_RUNTIME_READINESS",
            )
        )
    if any(record.evidence_type == "IMPLEMENTATION_CANDIDATE" for record in records):
        prohibited.extend(
            (
                "IMPLEMENTATION_CANDIDATE_IS_NOT_EXPOSURE_APPROVAL",
                "IMPLEMENTATION_CANDIDATE_IS_NOT_DEPLOYMENT_APPROVAL",
                "IMPLEMENTATION_CANDIDATE_IS_NOT_RUNTIME_APPROVAL",
                "IMPLEMENTATION_CANDIDATE_IS_NOT_PRODUCTION_APPROVAL",
            )
        )
    if _has_any(terms, ("PRODUCTION_READINESS", "DEPLOYMENT_READINESS", "RUNTIME_READINESS")):
        prohibited.append("READINESS_OVERSTATEMENT_REQUIRES_SUPPRESSION_OR_CAVEAT")
    return tuple(dict.fromkeys(prohibited))


def _required_caveats(
    records: list[ControlledReadinessEvidenceRecord], terms: tuple[str, ...]
) -> tuple[str, ...]:
    caveats = list(BASE_REQUIRED_CAVEATS)
    evidence_types = {record.evidence_type for record in records}
    if "UNKNOWN" in evidence_types:
        caveats.append("Unknown evidence type requires fallback/caveat before a current-state claim.")
    if evidence_types & NON_OVERRIDE_EVIDENCE_TYPES:
        caveats.append("Older planning, design, historical, unknown, or implementation-candidate evidence cannot override final/current artefacts.")
    if "EXPOSURE_DEFERRED" in terms or "NOT_EXPOSED" in terms:
        caveats.append("Exposure-deferred and not-exposed boundaries must be preserved.")
    if "RUNTIME_DEFERRED" in terms or "NOT_IMPLEMENTED" in terms:
        caveats.append("Runtime-deferred, runtime-creation-deferred, and not-implemented boundaries must be preserved.")
    if "NOT_DEPLOYED" in terms or "DB_VALIDATION_DEFERRED" in terms:
        caveats.append("Deployment-deferred and DB-validation-deferred boundaries must be preserved.")
    return tuple(dict.fromkeys(caveats))


def _preferred_reason(evidence_type: str) -> str:
    if evidence_type in FINAL_CURRENT_EVIDENCE_TYPES:
        return f"{evidence_type} is treated as final/current closeout evidence for stream status."
    if evidence_type == "UNKNOWN":
        return "UNKNOWN evidence cannot support a confident current-state claim."
    return f"{evidence_type} is recognised but remains below final/current closeout evidence."


def _confidence(evidence_type: str, fallback_required: bool) -> str:
    if fallback_required:
        return "LOW"
    if evidence_type in FINAL_CURRENT_EVIDENCE_TYPES:
        return "HIGH"
    return "MEDIUM_WITH_CAVEAT"


def _explanation(evidence_type: str, fallback_required: bool) -> str:
    if fallback_required:
        return "The guard requires fallback/caveat behaviour because the preferred evidence is unknown or missing."
    return (
        f"The guard selected {evidence_type} by deterministic preference order and "
        "preserved controlled-readiness, exposure, runtime, deployment, production, "
        "and final-answer-generation boundaries."
    )


def _record_text(record: ControlledReadinessEvidenceRecord) -> str:
    return f"{record.evidence_type}\n{record.title}\n{record.content}"


def _has_any(values: tuple[str, ...], expected_values: tuple[str, ...]) -> bool:
    return any(value in values for value in expected_values)


def _first_value(record: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in record:
            return record[key]
    return None


def _first_attr(record: object, keys: tuple[str, ...]) -> Any:
    for key in keys:
        if hasattr(record, key):
            return getattr(record, key)
    return None
