from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from app.schemas.award_studio_minerva import (
    AuthorityClassification,
    AwardCompletenessEntry,
    AwardEvidenceReference,
    AwardHold,
    AwardSemanticNode,
    AwardSemanticRelationship,
    AwardStudioMinervaAnswerPlan,
    AwardStudioMinervaQuestionRequest,
    AwardVersionExplainableContextV1,
    QuestionClassification,
)


class AwardStudioContractError(ValueError):
    pass


_AUTHORITY_PRIORITY: dict[str, int] = {
    "EXPLICIT_STRUCTURED": 0,
    "DETERMINISTICALLY_DERIVABLE": 1,
    "NOT_CONFIGURED": 2,
    "MISSING": 3,
    "HELD": 4,
    "CONFLICT": 5,
}

_CONCEPT_TERMS: dict[str, tuple[str, ...]] = {
    "EMPLOYMENT_TYPE_COMPARISON": ("employment type", "full time", "part time", "casual"),
    "CLASSIFICATION": ("classification", "position", "award position", "class"),
    "SATURDAY": ("saturday",),
    "SUNDAY": ("sunday",),
    "PUBLIC_HOLIDAY": ("public holiday", "public_holiday", "publicholiday"),
    "OVERTIME_1": ("ot1", "overtime 1", "overtime first", "first overtime"),
    "OVERTIME_2": ("ot2", "overtime 2", "overtime second", "second overtime"),
    "ALLOWANCE_REIMBURSEMENT": ("allowance", "reimbursement", "reimburse"),
    "HOLD": ("hold", "unresolved", "review required"),
}


def _canonical(value: object) -> bytes:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_projection_fingerprint(projection: AwardVersionExplainableContextV1) -> str:
    payload = projection.model_dump(mode="json")
    payload["authorityEnvelope"] = dict(payload["authorityEnvelope"])
    payload["authorityEnvelope"].pop("projectionFingerprint", None)
    return _sha256(_canonical(payload))


def validate_request(request: AwardStudioMinervaQuestionRequest) -> AwardStudioMinervaQuestionRequest:
    expected = canonical_projection_fingerprint(request.projection)
    if request.projectionFingerprint != expected:
        raise AwardStudioContractError("AwardVersion projection fingerprint mismatch.")
    return request


def _normalise(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def classify_question(question: str) -> QuestionClassification:
    text = _normalise(question)
    if any(term in text for term in ("publish", "activate", "change this", "save this", "resolve this", "approve")):
        return "UNKNOWN_OR_UNSUPPORTED"
    if any(term in text for term in ("this worker", "this employee", "how much was paid", "calculate pay", "worker got")):
        return "UNKNOWN_OR_UNSUPPORTED"
    if any(term in text for term in ("source", "evidence", "clause", "page", "proposition", "where did")):
        return "SOURCE_EVIDENCE"
    if any(term in text for term in ("overview", "what is configured", "explain this award")):
        return "OVERVIEW"
    if any(term in text for term in ("employment type", "full time", "part time", "casual", "differ between")):
        return "EMPLOYMENT_TYPE_COMPARISON"
    if any(term in text for term in ("version", "effective", "lifecycle", "predecessor", "successor", "lineage")):
        return "VERSION_LINEAGE"
    if any(term in text for term in ("damaged clothing", "personal effects", "hold", "unresolved", "review required")):
        return "HOLD"
    if "public holiday" in text:
        return "PUBLIC_HOLIDAY"
    if "saturday" in text:
        return "SATURDAY"
    if "sunday" in text:
        return "SUNDAY"
    if any(term in text for term in ("ot1", "overtime 1", "first overtime", "overtime first")):
        return "OVERTIME_1"
    if any(term in text for term in ("ot2", "overtime 2", "second overtime", "overtime second")):
        return "OVERTIME_2"
    if "allowance" in text or "reimburse" in text:
        return "ALLOWANCE_REIMBURSEMENT"
    if "classification" in text or "award position" in text or "position class" in text:
        return "CLASSIFICATION"
    return "UNKNOWN_OR_UNSUPPORTED"


def _searchable_node(node: AwardSemanticNode) -> str:
    return _normalise(
        " ".join(
            [
                node.semanticIdentity,
                node.type,
                node.code,
                node.friendlyName,
                node.purpose or "",
                json.dumps(node.values, ensure_ascii=True, sort_keys=True),
                json.dumps(node.quantities, ensure_ascii=True, sort_keys=True),
                json.dumps(node.applicability, ensure_ascii=True, sort_keys=True),
            ]
        )
    )


def _matches_terms(value: str, terms: tuple[str, ...]) -> bool:
    normalised_terms = tuple(_normalise(term) for term in terms)
    return any(term in value for term in normalised_terms)


def _select_nodes(
    projection: AwardVersionExplainableContextV1,
    classification: QuestionClassification,
    question: str,
) -> list[AwardSemanticNode]:
    if classification == "OVERVIEW":
        return projection.semanticNodes[:8]
    if classification == "SOURCE_EVIDENCE":
        evidence_node_ids = {item.semanticIdentity for item in projection.evidence if item.semanticIdentity}
        return [node for node in projection.semanticNodes if node.semanticIdentity in evidence_node_ids][:12]
    if classification == "HOLD":
        hold_node_ids = {hold.semanticIdentity for hold in projection.holds}
        return [node for node in projection.semanticNodes if node.semanticIdentity in hold_node_ids]
    if classification == "CLASSIFICATION":
        return [node for node in projection.semanticNodes if node.type == "CLASSIFICATION"][:12]
    if classification == "EMPLOYMENT_TYPE_COMPARISON":
        return [
            node for node in projection.semanticNodes
            if node.type == "EMPLOYMENT_TYPE_PROVISION"
            or bool((node.applicability or {}).get("employmentTypes"))
        ][:20]
    terms = _CONCEPT_TERMS.get(classification, ())
    if classification == "ALLOWANCE_REIMBURSEMENT":
        question_text = _normalise(question)
        mentions_allowance = "allowance" in question_text
        mentions_reimbursement = "reimburse" in question_text
        if mentions_allowance and not mentions_reimbursement:
            terms = ("allowance",)
        elif mentions_reimbursement and not mentions_allowance:
            terms = ("reimbursement", "reimburse")
    return [node for node in projection.semanticNodes if _matches_terms(_searchable_node(node), terms)][:12]


def _searchable_completeness(item: AwardCompletenessEntry) -> str:
    return _normalise(f"{item.conceptCode} {item.friendlyName} {item.explanation}")


def _select_completeness(
    projection: AwardVersionExplainableContextV1,
    classification: QuestionClassification,
) -> list[AwardCompletenessEntry]:
    if classification == "OVERVIEW":
        return projection.completeness[:8]
    terms = _CONCEPT_TERMS.get(classification, ())
    return [item for item in projection.completeness if _matches_terms(_searchable_completeness(item), terms)]


def _select_relationships(
    projection: AwardVersionExplainableContextV1,
    nodes: list[AwardSemanticNode],
) -> list[AwardSemanticRelationship]:
    node_ids = {node.semanticIdentity for node in nodes}
    return [
        edge
        for edge in projection.relationships
        if edge.sourceSemanticIdentity in node_ids
        or (edge.targetKind == "SEMANTIC_NODE" and edge.targetIdentity in node_ids)
    ][:20]


def _select_holds(
    projection: AwardVersionExplainableContextV1,
    classification: QuestionClassification,
    nodes: list[AwardSemanticNode],
) -> list[AwardHold]:
    if classification == "HOLD":
        return projection.holds
    node_ids = {node.semanticIdentity for node in nodes}
    return [hold for hold in projection.holds if hold.semanticIdentity in node_ids]


def _select_evidence(
    projection: AwardVersionExplainableContextV1,
    classification: QuestionClassification,
    nodes: list[AwardSemanticNode],
    relationships: list[AwardSemanticRelationship],
    holds: list[AwardHold],
) -> list[AwardEvidenceReference]:
    if classification == "SOURCE_EVIDENCE":
        return projection.evidence[:20]
    ids = {evidence_id for node in nodes for evidence_id in node.evidenceIds}
    ids.update(evidence_id for hold in holds for evidence_id in hold.evidenceIds)
    ids.update(edge.targetIdentity for edge in relationships if edge.targetKind == "EVIDENCE")
    return [item for item in projection.evidence if item.evidenceIdentity in ids]


def _strongest_authority(values: list[str]) -> AuthorityClassification:
    if not values:
        return "MISSING"
    return max(values, key=lambda value: _AUTHORITY_PRIORITY[value])  # type: ignore[return-value]


def _answer_classification(
    classification: QuestionClassification,
    nodes: list[AwardSemanticNode],
    evidence: list[AwardEvidenceReference],
    holds: list[AwardHold],
    completeness: list[AwardCompletenessEntry],
) -> AuthorityClassification:
    if classification in {"OVERVIEW", "VERSION_LINEAGE"}:
        return "EXPLICIT_STRUCTURED"
    if classification == "SOURCE_EVIDENCE":
        return _strongest_authority([item.authorityClassification for item in evidence])
    if holds:
        return "HELD"
    authorities = [node.authorityClassification for node in nodes]
    authorities.extend(item.authorityClassification for item in completeness)
    return _strongest_authority(authorities)


def _display_value(value: Any) -> str:
    if value is None or value == {} or value == []:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _node_summary(node: AwardSemanticNode) -> str:
    details = [
        detail
        for detail in (
            _display_value(node.values),
            _display_value(node.quantities),
            _display_value(node.applicability),
        )
        if detail
    ]
    suffix = f" — {'; '.join(details)}" if details else ""
    return f"{node.friendlyName} [{node.authorityClassification}]{suffix}"


def _completeness_answer(
    award_version_id: str,
    classification: AuthorityClassification,
    completeness: list[AwardCompletenessEntry],
) -> str:
    explanation = completeness[0].explanation if completeness else "No matching completeness authority was supplied."
    if classification == "NOT_CONFIGURED":
        return f"This selected AwardVersion ({award_version_id}) does not contain a configured rule for this concept. {explanation}"
    if classification == "CONFLICT":
        return f"This selected AwardVersion ({award_version_id}) records conflicting authority for this concept. Minerva has not reconciled it. {explanation}"
    return f"This selected AwardVersion ({award_version_id}) is missing governed authority for this concept. {explanation}"


def _direct_answer(
    request: AwardStudioMinervaQuestionRequest,
    classification: QuestionClassification,
    answer_classification: AuthorityClassification,
    nodes: list[AwardSemanticNode],
    relationships: list[AwardSemanticRelationship],
    evidence: list[AwardEvidenceReference],
    holds: list[AwardHold],
    completeness: list[AwardCompletenessEntry],
) -> str:
    authority = request.projection.authorityEnvelope
    if classification == "UNKNOWN_OR_UNSUPPORTED":
        return (
            "Minerva can explain only the supplied exact AwardVersion configuration. It cannot change or resolve the "
            "Award, calculate a worker result, or replace missing configured authority with general Award knowledge."
        )
    if classification == "VERSION_LINEAGE":
        lineage = _display_value(authority.versionLineage)
        return (
            f"This is {authority.awardCode} AwardVersion {authority.awardVersionId}, effective from "
            f"{authority.effectiveFrom}, lifecycle {authority.lifecycle}. Configured lineage: {lineage or 'none supplied'}."
        )
    if classification == "EMPLOYMENT_TYPE_COMPARISON":
        configured = [item.EmploymentTypeCode for item in request.projection.employmentTypeScope]
        if not configured:
            return _completeness_answer(authority.awardVersionId, "MISSING", completeness)
        shared = [
            node for node in request.projection.semanticNodes
            if node.type == "CLASSIFICATION"
            and set((node.applicability or {}).get("employmentTypes") or []) >= set(configured)
        ]
        scoped = [
            node for node in request.projection.semanticNodes
            if node.type == "EMPLOYMENT_TYPE_PROVISION"
            and (node.applicability or {}).get("employmentTypes")
        ]
        return (
            f"AwardVersion {authority.awardVersionId} explicitly covers {', '.join(configured)}. "
            f"It contains {len(shared)} shared configured classifications and {len(scoped)} source-backed "
            "employment-type provision nodes. The classification remains shared where its applicability lists all "
            "configured types; different treatments are selected from the structured employmentTypes applicability. "
            "This is configuration authority only, not a worker-specific payroll result."
        )
    if classification == "HOLD" and holds:
        hold = holds[0]
        semantic_difference = ""
        if hold.sourceSemantic or hold.candidateSemantic:
            semantic_difference = (
                f" Source semantic: {hold.sourceSemantic or 'not supplied'}; configured candidate semantic: "
                f"{hold.candidateSemantic or 'not supplied'}."
            )
        action = f" Required review: {hold.requiredAction}." if hold.requiredAction else ""
        return (
            f"{hold.friendlyName} remains {hold.status} in this selected AwardVersion because {hold.reason}."
            f"{semantic_difference}{action} Minerva has not resolved or reclassified it."
        )
    if classification == "SOURCE_EVIDENCE":
        if not evidence:
            return _completeness_answer(authority.awardVersionId, "MISSING", completeness)
        sources = "; ".join(
            f"{item.sourceTitle} ({item.evidenceIdentity}, SHA-256 {item.sourceSha256})"
            for item in evidence[:5]
        )
        return f"This selected AwardVersion carries governed source evidence: {sources}."
    if answer_classification == "CONFLICT" and nodes:
        labels = "; ".join(node.friendlyName for node in nodes[:5])
        return (
            f"This selected AwardVersion ({authority.awardVersionId}) records conflicting configured authority "
            f"for: {labels}. Minerva has not reconciled or replaced that conflict."
        )
    if not nodes or answer_classification in {"NOT_CONFIGURED", "MISSING"}:
        return _completeness_answer(authority.awardVersionId, answer_classification, completeness)
    labels = "; ".join(_node_summary(node) for node in nodes[:5])
    if answer_classification == "DETERMINISTICALLY_DERIVABLE":
        return (
            f"Given the configured relationships in AwardVersion {authority.awardVersionId}, this explanation is "
            f"deterministically derivable: {labels}. Relationship count used: {len(relationships)}."
        )
    return f"This configured AwardVersion contains: {labels}."


def build_answer_plan(request: AwardStudioMinervaQuestionRequest) -> AwardStudioMinervaAnswerPlan:
    request = validate_request(request)
    projection = request.projection
    classification = classify_question(request.question)
    nodes = _select_nodes(projection, classification, request.question)
    completeness = _select_completeness(projection, classification)
    relationships = _select_relationships(projection, nodes)
    holds = _select_holds(projection, classification, nodes)
    evidence = _select_evidence(projection, classification, nodes, relationships, holds)
    answer_classification = _answer_classification(classification, nodes, evidence, holds, completeness)
    direct = _direct_answer(
        request,
        classification,
        answer_classification,
        nodes,
        relationships,
        evidence,
        holds,
        completeness,
    )
    what_matters = [_node_summary(node) for node in nodes[:8]]
    what_matters.extend(
        f"{item.friendlyName} [{item.authorityClassification}]: {item.explanation}"
        for item in completeness[:4]
    )
    plan_data = {
        "questionClassification": classification,
        "answerClassification": answer_classification,
        "awardVersionId": projection.authorityEnvelope.awardVersionId,
        "directDeterministicAnswer": direct,
        "whatMatters": what_matters,
        "semanticIdentities": [node.semanticIdentity for node in nodes],
        "relationshipIdentities": [edge.relationshipIdentity for edge in relationships],
        "evidenceIdentities": [item.evidenceIdentity for item in evidence],
        "holdIdentities": [hold.holdIdentity for hold in holds],
        "completenessConceptCodes": [item.conceptCode for item in completeness],
        "boundary": (
            "This answer describes the exact selected AwardVersion configuration only. No worker facts or runtime "
            "decision evidence were supplied, and no Award, payroll, configuration, lifecycle, or hold state was changed."
        ),
        "safeNextStep": (
            "Review the unresolved item and its cited evidence in Award Studio."
            if answer_classification in {"HELD", "CONFLICT", "MISSING"}
            else "Review the cited semantic authority and source evidence in Award Studio."
        ),
    }
    return AwardStudioMinervaAnswerPlan(
        **plan_data,
        plannerFingerprint=_sha256(_canonical(plan_data)),
    )


__all__ = [
    "AwardStudioContractError",
    "build_answer_plan",
    "canonical_projection_fingerprint",
    "classify_question",
    "validate_request",
]
