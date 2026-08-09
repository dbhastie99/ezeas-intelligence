"""Offline, deterministic Minerva administrator configuration evidence surface."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.schemas.minerva_admin_configuration import (
    AdminConfigurationAnswer,
    AdminConfigurationProposalPreview,
    ConfigurationEvidence,
    LeavePolicyConfigurationEvidencePacket,
)
from app.services.audit_service import write_ai_interaction_audit


PACKET_SCHEMA_NAME = "LeavePolicyConfigurationEvidencePacket"
PACKET_SCHEMA_VERSION = "1.0.0"
PACK_KEY = "queensland-general-lsl-v1"
PACK_VERSION = "1.0.0"
PACK_FINGERPRINT = "44497fb50e607581d68cccddc86db4fd396e8b4b3a9b268afdab1d5f48da1447"
SOURCE_REPOSITORY = "dbhastie99/workforce-platform"
SOURCE_REF = "refs/heads/leave/qld-lsl-foundation2-20260806"
SOURCE_SHA = "1d912eff59109f74af20367285fb698ed7915f96"
EVIDENCE_LABELS = (
    "Knowledge-pack fact",
    "Supplied configuration",
    "Tenant configuration",
    "Derived result",
    "Missing evidence",
    "Unsupported runtime capability",
)


class AdminConfigurationEvidenceError(ValueError):
    pass


@dataclass(frozen=True)
class _Draft:
    intent: str
    outcome: str
    direct: str
    matters: tuple[str, ...]
    boundary: str
    sources: tuple[str, ...]
    classifications: tuple[str, ...]


def _normalise(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def _canonical(packet: LeavePolicyConfigurationEvidencePacket, include_fingerprint: bool = True) -> str:
    data = packet.model_dump(mode="json")
    if not include_fingerprint:
        data.pop("packet_fingerprint", None)
    return json.dumps(data, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _identity(prefix: str, *parts: str) -> str:
    payload = "|".join(parts).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(payload).hexdigest()[:24]}"


def validate_packet(packet: LeavePolicyConfigurationEvidencePacket) -> LeavePolicyConfigurationEvidencePacket:
    if packet.schema_name != PACKET_SCHEMA_NAME or packet.schema_version != PACKET_SCHEMA_VERSION:
        raise AdminConfigurationEvidenceError("Unsupported evidence packet schema.")
    if not packet.authenticated_context_ref or not packet.tenant_reference:
        raise AdminConfigurationEvidenceError("Authenticated context and tenant scope are required.")
    if packet.selection_status != "EXPLICITLY_SELECTED":
        raise AdminConfigurationEvidenceError("Policy version must be explicitly selected.")
    if not packet.selected_policy_id or not packet.selected_policy_version_id:
        raise AdminConfigurationEvidenceError("Policy and policy-version identity are required.")
    expected_lineage = (
        packet.predecessor_identity,
        f"{packet.selected_policy_id}:{packet.selected_policy_version_id}",
    )
    if packet.immutable_version_lineage != expected_lineage:
        raise AdminConfigurationEvidenceError("Policy/version lineage is inconsistent.")
    if packet.producer_repository != SOURCE_REPOSITORY or packet.producer_ref != SOURCE_REF or packet.producer_sha != SOURCE_SHA:
        raise AdminConfigurationEvidenceError("Evidence producer provenance is not authorised.")
    if packet.knowledge_pack_key != PACK_KEY or packet.knowledge_pack_version != PACK_VERSION:
        raise AdminConfigurationEvidenceError("Packet conflicts with the published knowledge pack identity.")
    if packet.knowledge_pack_fingerprint != PACK_FINGERPRINT:
        raise AdminConfigurationEvidenceError("Packet conflicts with the published knowledge pack fingerprint.")
    if packet.readiness.runtime_support_declared_flag != 0:
        raise AdminConfigurationEvidenceError("RuntimeSupportDeclaredFlag must remain 0.")
    ids = tuple(item.configuration_id for item in packet.configuration_evidence)
    if ids != tuple(sorted(ids)) or len(ids) != len(set(ids)):
        raise AdminConfigurationEvidenceError("Configuration evidence ordering or identity is invalid.")
    required_ids = {
        "entitlement.general_entitlement_quantity",
        "entitlement.general_service_threshold",
        "qleave.operations",
        "runtime.calculation_support",
        "service.continuity.casual_break_threshold",
        "service.history.packet",
        "source.precedence.alternate_instrument",
    }
    if set(ids) != required_ids:
        raise AdminConfigurationEvidenceError("Required configured value evidence is missing or unexpected.")
    if packet.ownership_status == "SUPPLIED" and any(
        item.configuration_origin != "SUPPLIED_CONFIGURATION" for item in packet.configuration_evidence
    ):
        raise AdminConfigurationEvidenceError("Supplied and tenant configuration are conflated.")
    if any(not item.source_reference or not item.rationale_reference for item in packet.configuration_evidence):
        raise AdminConfigurationEvidenceError("Configuration evidence provenance is incomplete.")
    if "QLEAVE_OPERATIONS_ON_HOLD" not in packet.readiness.blockers:
        raise AdminConfigurationEvidenceError("QLeave HOLD boundary is required.")
    expected = hashlib.sha256(_canonical(packet, include_fingerprint=False).encode("utf-8")).hexdigest()
    if packet.packet_fingerprint != expected:
        raise AdminConfigurationEvidenceError("Evidence packet fingerprint mismatch.")
    return packet


def classify_admin_question(question: str) -> str:
    text = _normalise(question)
    if not text:
        return "OUT_OF_EVIDENCE"
    if any(term in text for term in ("save", "approve", "approval", "publish", "apply", "create a successor", "persist")):
        return "REFUSED_MUTATION_REQUEST"
    if any(term in text for term in ("calculate", "entitlement determination", "determine entitlement", "process leave", "payroll")):
        return "REFUSED_RUNTIME_REQUEST"
    if "qleave" in text and any(term in text for term in ("eligible", "eligibility", "register", "levy", "claim", "reimbursement", "how do i")):
        return "REFUSED_QLEAVE_OPERATION"
    if any(term in text for term in ("invent", "make up", "guess", "fill in the missing", "assume the missing")):
        return "REFUSED_INVENTION_REQUEST"
    if any(term in text for term in ("which policy", "which version", "selected", "policy identity")):
        return "CONFIGURATION_IDENTITY"
    if any(term in text for term in ("what would changing", "affect", "successor version", "weaken", "statutory minimum")):
        return "PROPOSED_CHANGE_IMPACT"
    if any(term in text for term in ("supplied", "successor", "organisation", "organization", "tenant-owned", "tenant owned")):
        return "OWNERSHIP_LINEAGE"
    if any(term in text for term in ("which service", "entitlement settings", "configured settings", "rule values", "configured value")):
        return "CONFIGURED_RULE_VALUES"
    if "why" in text and any(term in text for term in ("ten year", "10 years", "setting", "configured")):
        return "RATIONALE"
    if any(term in text for term in ("legal source", "source supports", "support that setting", "source reference")):
        return "SOURCE"
    if any(term in text for term in ("can an administrator change", "can i change", "changeable", "selectable", "locked")):
        return "CHANGEABILITY"
    if any(term in text for term in ("readiness", "needs review", "inactive", "on hold", "hold conditions", "blockers")):
        return "READINESS"
    if any(term in text for term in ("runtime", "enabled", "enabled", "processing")):
        return "RUNTIME_SUPPORT"
    if any(term in text for term in ("differ", "predecessor", "lineage", "version history")):
        return "VERSION_LINEAGE"
    if any(term in text for term in ("missing evidence", "evidence gap", "what is missing", "evidence is missing")):
        return "MISSING_EVIDENCE"
    if "qleave" in text and any(term in text for term in ("operational", "operations", "on hold")):
        return "QLEAVE_BOUNDARY"
    return "OUT_OF_EVIDENCE"


def _find(packet: LeavePolicyConfigurationEvidencePacket, configuration_id: str) -> ConfigurationEvidence:
    for item in packet.configuration_evidence:
        if item.configuration_id == configuration_id:
            return item
    raise AdminConfigurationEvidenceError(f"Required configuration evidence is missing: {configuration_id}.")


def _source_text(item: ConfigurationEvidence) -> str:
    return f"[Supplied configuration] {item.configuration_id}: {item.source_reference}"


def _draft(packet: LeavePolicyConfigurationEvidencePacket, intent: str) -> _Draft:
    threshold = _find(packet, "entitlement.general_service_threshold")
    quantity = _find(packet, "entitlement.general_entitlement_quantity")
    continuity = _find(packet, "service.continuity.casual_break_threshold")
    service_history = _find(packet, "service.history.packet")
    precedence = _find(packet, "source.precedence.alternate_instrument")
    runtime = _find(packet, "runtime.calculation_support")
    qleave = _find(packet, "qleave.operations")
    pack_source = f"[Knowledge-pack fact] {packet.knowledge_pack_key}@{packet.knowledge_pack_version}, fingerprint {packet.knowledge_pack_fingerprint}"
    common_boundary = "Minerva is read-only administrator evidence only; it does not access a live Workforce Platform client or database."
    if intent == "CONFIGURATION_IDENTITY":
        return _Draft(intent, "ANSWERED", f"[Supplied configuration] The explicitly selected policy is {packet.selected_policy_id}; the selected version is {packet.selected_policy_version_id}.", (f"[Supplied configuration] Selection status is {packet.selection_status} for tenant scope {packet.tenant_reference}.",), common_boundary, (pack_source, f"[Supplied configuration] Producer {packet.supplied_policy_source_identity}"), ("Supplied configuration", "Knowledge-pack fact"))
    if intent == "OWNERSHIP_LINEAGE":
        return _Draft(intent, "ANSWERED", f"[Supplied configuration] This is supplied configuration ({packet.ownership_status}), not a tenant-owned successor. The selected version follows predecessor {packet.predecessor_identity}; no tenant successor is selected.", ("[Tenant configuration] No tenant-owned successor identity is present in this packet.", f"[Supplied configuration] Lifecycle is {packet.lifecycle_state}, effective from {packet.effective_from}.") , common_boundary, (f"[Supplied configuration] {packet.supplied_policy_source_identity}",), ("Supplied configuration", "Tenant configuration"))
    if intent == "CONFIGURED_RULE_VALUES":
        return _Draft(intent, "ANSWERED", "[Supplied configuration] The packet contains three configured rule values: 10 years for the general service threshold, 8.6667 weeks for the general entitlement quantity, and 3 calendar months for the casual continuity break threshold.", (f"[Supplied configuration] {threshold.label} = {threshold.value.value} {threshold.value.unit}.", f"[Supplied configuration] {quantity.label} = {quantity.value.value} {quantity.value.unit}.", f"[Supplied configuration] {continuity.label} = {continuity.value.value} {continuity.value.unit}.", "[Knowledge-pack fact] The published pack is explanatory evidence and must not be treated as the configured value."), common_boundary, (pack_source, _source_text(threshold), _source_text(quantity), _source_text(continuity)), ("Supplied configuration", "Knowledge-pack fact"))
    if intent == "RATIONALE":
        return _Draft(intent, "ANSWERED", "[Supplied configuration] The ten-year setting was configured as the supplied Queensland General LSL threshold for the stated non-seasonal employee scope. It is locked and marked minimum-or-better, so it is not an organisation-invented entitlement value.", (f"[Supplied configuration] Rationale reference: {threshold.rationale_reference}.", "[Derived result] A proposed reduction would be a statutory-minimum risk and cannot be applied by this slice."), common_boundary, (_source_text(threshold), _source_text(quantity), pack_source), ("Supplied configuration", "Derived result", "Knowledge-pack fact"))
    if intent == "SOURCE":
        return _Draft(intent, "ANSWERED", "[Supplied configuration] The ten-year setting is supported by the controlled Queensland source reference attached to the configuration evidence; the related quantity is supported by the controlled Business Queensland entitlement reference.", (f"[Supplied configuration] Threshold source: {threshold.source_reference}.", f"[Supplied configuration] Quantity source: {quantity.source_reference}.", "[Knowledge-pack fact] The published pack retains source locators but does not replace the packet's configuration provenance."), common_boundary, (_source_text(threshold), _source_text(quantity), pack_source), ("Supplied configuration", "Knowledge-pack fact"))
    if intent == "CHANGEABILITY":
        return _Draft(intent, "ANSWERED", "[Supplied configuration] The supplied rule settings are locked and not selectable in this read-only context. An administrator can preview implications, but cannot change, save, approve or publish them here.", ("[Supplied configuration] The packet exposes `locked` and `selectable` flags per setting.", "[Tenant configuration] No tenant-owned selectable override is present.", "[Unsupported runtime capability] This context has no mutation path."), common_boundary, (pack_source, _source_text(threshold), _source_text(continuity)), ("Supplied configuration", "Tenant configuration", "Unsupported runtime capability"))
    if intent == "READINESS":
        return _Draft(intent, "ANSWERED", f"[Supplied configuration] Overall readiness is {packet.readiness.overall}. The packet explicitly represents Configured, Needs review, inactive and HOLD classifications.", tuple(f"[Supplied configuration] {finding}" for finding in packet.readiness.findings) + tuple(f"[Missing evidence] Blocker: {blocker}" for blocker in packet.readiness.blockers), common_boundary, (pack_source,), ("Supplied configuration", "Missing evidence"))
    if intent == "RUNTIME_SUPPORT":
        return _Draft(intent, "ANSWERED", f"[Unsupported runtime capability] Calculation and runtime processing are {runtime.value.value}; RuntimeSupportDeclaredFlag remains {packet.readiness.runtime_support_declared_flag}.", ("[Unsupported runtime capability] This packet is evidence for administrator inspection, not a runtime activation claim.",), "Minerva must not calculate entitlements, reconstruct service, value leave, call payroll or activate runtime support.", (pack_source, _source_text(runtime)), ("Unsupported runtime capability", "Knowledge-pack fact"))
    if intent == "VERSION_LINEAGE":
        return _Draft(intent, "ANSWERED", f"[Supplied configuration] The selected version {packet.selected_policy_version_id} succeeds {packet.predecessor_identity}; the immutable lineage is {', '.join(packet.immutable_version_lineage)}.", (f"[Supplied configuration] Effective from {packet.effective_from}; lifecycle {packet.lifecycle_state}.", "[Derived result] The v4 successor carries the calendar-month continuity repair while preserving the configured HOLD boundaries."), common_boundary, (f"[Supplied configuration] {packet.supplied_policy_source_identity}", pack_source), ("Supplied configuration", "Derived result", "Knowledge-pack fact"))
    if intent == "PROPOSED_CHANGE_IMPACT":
        return _Draft(intent, "ANSWERED", "[Derived result] A change preview would affect the identified configuration identity, require a successor version, and be checked against minimum-or-better protection. No mutation is performed.", ("[Derived result] A lower statutory threshold or quantity would weaken a statutory minimum and must fail closed.", "[Missing evidence] Alternate-instrument, service-history and QLeave operational evidence remain gaps.", "[Unsupported runtime capability] The preview cannot calculate entitlement or payment impact."), common_boundary, (pack_source, _source_text(threshold), _source_text(quantity), _source_text(continuity)), ("Derived result", "Missing evidence", "Unsupported runtime capability"))
    if intent == "MISSING_EVIDENCE":
        return _Draft(intent, "ANSWERED", "[Missing evidence] The packet does not contain a worker service-history packet, alternate-instrument content, or QLeave operational evidence. Those gaps are explicit; Minerva will not infer their values.", (f"[Missing evidence] {service_history.configuration_id} is {service_history.value.value} and marked {service_history.readiness}.", f"[Missing evidence] {precedence.configuration_id} is marked {precedence.readiness}.", "[Missing evidence] QLeave operations are an explicit HOLD boundary."), common_boundary, (pack_source, _source_text(service_history), _source_text(precedence), _source_text(qleave)), ("Missing evidence", "Knowledge-pack fact"))
    if intent == "QLEAVE_BOUNDARY":
        return _Draft(intent, "ANSWERED", "[Supplied configuration] QLeave is not operational in this slice: its operations status is ON_HOLD and it remains a separate package from Queensland General LSL.", ("[Unsupported runtime capability] QLeave eligibility and operations are not implemented.", "[Missing evidence] No QLeave operational configuration is supplied."), "Minerva can state the boundary only; it cannot determine QLeave eligibility, registration, levy, returns, claims, reimbursement or payment operations.", (pack_source, _source_text(qleave)), ("Supplied configuration", "Missing evidence", "Unsupported runtime capability"))
    if intent == "REFUSED_MUTATION_REQUEST":
        return _Draft(intent, "REFUSED", "[Unsupported runtime capability] I cannot save, approve, publish, apply or create a successor from a change preview.", ("[Derived result] A non-persisted impact preview is the only proposal result allowed here.",), common_boundary, (pack_source,), ("Unsupported runtime capability", "Derived result"))
    if intent == "REFUSED_QLEAVE_OPERATION":
        return _Draft(intent, "REFUSED", "[Unsupported runtime capability] I cannot provide QLeave eligibility or operational instructions from this Queensland General LSL context.", ("[Missing evidence] QLeave eligibility and operations remain ON_HOLD and outside this package.",), "QLeave remains a separate package; no QLeave operation is invoked.", (pack_source,), ("Unsupported runtime capability", "Missing evidence"))
    if intent == "REFUSED_INVENTION_REQUEST":
        return _Draft(intent, "REFUSED", "[Missing evidence] I cannot invent or fill a missing configured value. The packet must contain an explicit typed value and provenance.", ("[Missing evidence] Missing configuration evidence remains unresolved and fails closed.",), common_boundary, (pack_source,), ("Missing evidence", "Unsupported runtime capability"))
    if intent == "REFUSED_RUNTIME_REQUEST":
        return _Draft(intent, "REFUSED", "[Unsupported runtime capability] I cannot calculate an entitlement, determine a worker result, reconstruct service, value leave, or process payroll/leave.", ("[Knowledge-pack fact] The published pack is advisory evidence only.",), "Worker-facing entitlement and calculation capabilities are a later role-based phase.", (pack_source,), ("Unsupported runtime capability", "Knowledge-pack fact"))
    return _Draft("OUT_OF_EVIDENCE", "OUT_OF_EVIDENCE", "[Missing evidence] I cannot answer that administrator question from this controlled configuration packet.", ("[Missing evidence] No supported administrator intent was selected, so Minerva will not guess or use unrelated pack facts.",), common_boundary, (pack_source,), ("Missing evidence", "Unsupported runtime capability"))


def _render(draft: _Draft) -> str:
    lines = ["Answer", draft.direct, "", "What matters"]
    lines.extend(f"- {item}" for item in draft.matters)
    lines.extend(["", "Capability boundary", draft.boundary, "", "Sources"])
    lines.extend(f"- {item}" for item in draft.sources)
    return "\n".join(lines)


def _audit(db: Session, request_identity: str, audit_identity: str, packet: LeavePolicyConfigurationEvidencePacket, draft: _Draft) -> str:
    redacted = json.dumps(
        {
            "audit_identity": audit_identity,
            "request_identity": request_identity,
            "packet_id": packet.packet_id,
            "packet_fingerprint": packet.packet_fingerprint,
            "intent": draft.intent,
            "outcome": draft.outcome,
            "evidence_classifications": sorted(set(draft.classifications)),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    record = write_ai_interaction_audit(
        db=db,
        user_question=f"MINERVA_ADMIN_CONFIGURATION_REQUEST:{request_identity}",
        response_text=redacted,
        source_references=[],
        model_name="DETERMINISTIC_ADMIN_CONFIGURATION_PACKET",
        prompt_policy=f"MINERVA_ADMIN_CONFIGURATION_READ_ONLY:{packet.knowledge_pack_key}:{packet.knowledge_pack_version}",
    )
    db.commit()
    return record.AIInteractionAuditId


def ask_admin_configuration(
    *,
    packet: LeavePolicyConfigurationEvidencePacket,
    question: str,
    db: Session | None = None,
    persist_audit: bool = False,
) -> AdminConfigurationAnswer:
    packet = validate_packet(packet)
    if not question.strip() or len(question) > 2000:
        raise AdminConfigurationEvidenceError("Administrator question must be non-empty and within the governed length limit.")
    request_identity = _identity("req", packet.packet_id, packet.packet_fingerprint, question.strip())
    draft = _draft(packet, classify_admin_question(question))
    audit_identity = _identity("aud", request_identity, packet.packet_fingerprint, draft.intent, draft.outcome)
    audit_id = _audit(db, request_identity, audit_identity, packet, draft) if persist_audit and db is not None else None
    return AdminConfigurationAnswer(
        request_identity=request_identity,
        audit_identity=audit_identity,
        audit_id=audit_id,
        outcome=draft.outcome,
        intent=draft.intent,
        packet_id=packet.packet_id,
        packet_fingerprint=packet.packet_fingerprint,
        answer=_render(draft),
        what_matters=draft.matters,
        capability_boundary=draft.boundary,
        sources=draft.sources,
        evidence_classifications=draft.classifications,
    )


def preview_admin_configuration_change(
    *,
    packet: LeavePolicyConfigurationEvidencePacket,
    requested_change: str,
    db: Session | None = None,
    persist_audit: bool = False,
) -> AdminConfigurationProposalPreview:
    packet = validate_packet(packet)
    if not requested_change.strip() or len(requested_change) > 1000:
        raise AdminConfigurationEvidenceError("Proposed change must be non-empty and within the governed length limit.")
    request_identity = _identity("req", packet.packet_id, packet.packet_fingerprint, requested_change.strip())
    if classify_admin_question(requested_change) == "REFUSED_MUTATION_REQUEST":
        audit_identity = _identity("aud", request_identity, packet.packet_fingerprint, "REFUSED_MUTATION_REQUEST")
        draft = _draft(packet, "REFUSED_MUTATION_REQUEST")
        audit_id = _audit(db, request_identity, audit_identity, packet, draft) if persist_audit and db is not None else None
        return AdminConfigurationProposalPreview(
            request_identity=request_identity, audit_identity=audit_identity, audit_id=audit_id, outcome="REFUSED",
            target_policy_id=packet.selected_policy_id, target_policy_version_id=packet.selected_policy_version_id,
            affected_configuration_ids=(), successor_version_required=False,
            minimum_or_better_risk="REFUSED_MUTATION_REQUEST", evidence_gaps=(), preview=_render(draft),
            no_mutation=True, no_save=True, no_approval=True, no_publication=True,
        )
    text = _normalise(requested_change)
    affected = []
    if any(term in text for term in ("ten year", "10 years", "threshold", "entitlement")):
        affected.extend(("entitlement.general_service_threshold", "entitlement.general_entitlement_quantity"))
    if any(term in text for term in ("three month", "3 months", "calendar month", "continuity", "casual")):
        affected.append("service.continuity.casual_break_threshold")
    if not affected:
        affected = [item.configuration_id for item in packet.configuration_evidence if item.configuration_id.startswith(("entitlement.", "service.continuity."))]
    affected = list(dict.fromkeys(affected))
    minimum_risk = "HIGH — proposed reduction or weakening would breach minimum-or-better review" if any(term in text for term in ("lower", "reduce", "weaken", "less", "below")) else "REVIEW_REQUIRED — minimum-or-better impact cannot be cleared by Minerva"
    gaps = ("service-history", "alternate-instrument", "external-QLeave-operations")
    audit_identity = _identity("aud", request_identity, packet.packet_fingerprint, "PREVIEW_ONLY")
    audit_draft = _Draft("PROPOSED_CHANGE_IMPACT", "ANSWERED", "", (), "", (), ("Derived result",))
    audit_id = _audit(db, request_identity, audit_identity, packet, audit_draft) if persist_audit and db is not None else None
    return AdminConfigurationProposalPreview(
        request_identity=request_identity, audit_identity=audit_identity, audit_id=audit_id, outcome="PREVIEW_ONLY",
        target_policy_id=packet.selected_policy_id, target_policy_version_id=packet.selected_policy_version_id,
        affected_configuration_ids=tuple(affected), successor_version_required=True,
        minimum_or_better_risk=minimum_risk, evidence_gaps=gaps,
        preview=(f"Preview only: a proposed change would affect {', '.join(affected)} in {packet.selected_policy_version_id}; "
                 "a successor version would be required. No draft is created, and no approval, publication, calculation or runtime action occurs."),
        no_mutation=True, no_save=True, no_approval=True, no_publication=True,
    )
