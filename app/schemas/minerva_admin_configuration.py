from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TypedEvidenceValue(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    value_type: str
    value: str | int | float | bool | None
    unit: str | None = None


class ConfigurationEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    configuration_id: str
    label: str
    value: TypedEvidenceValue
    applicability: str
    source_reference: str
    rationale_reference: str
    configuration_origin: Literal["SUPPLIED_CONFIGURATION", "TENANT_CONFIGURATION", "KNOWLEDGE_PACK_FACT"]
    locked: bool
    selectable: bool
    derived: bool
    minimum_or_better: bool
    unresolved: bool
    unsupported: bool
    readiness: Literal["Configured", "Needs review", "inactive", "HOLD"]


class ReadinessEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    overall: Literal["Configured", "Needs review", "inactive", "HOLD"]
    classifications: tuple[Literal["Configured", "Needs review", "inactive", "HOLD"], ...]
    runtime_support_declared_flag: Literal[0]
    findings: tuple[str, ...]
    blockers: tuple[str, ...]


class LeavePolicyConfigurationEvidencePacket(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_name: Literal["LeavePolicyConfigurationEvidencePacket"]
    schema_version: Literal["1.0.0"]
    packet_id: str
    generated_at: str
    packet_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    producer_identity: str
    producer_version: str
    producer_repository: str
    producer_ref: str
    producer_sha: str = Field(pattern=r"^[0-9a-f]{40}$")
    authenticated_context_ref: str
    tenant_reference: str
    selected_policy_id: str
    selected_policy_version_id: str
    policy_family: str
    jurisdiction: str
    selection_status: Literal["EXPLICITLY_SELECTED"]
    ownership_status: Literal["SUPPLIED", "TENANT_OWNED"]
    predecessor_identity: str
    successor_identity: str | None
    immutable_version_lineage: tuple[str, ...]
    effective_from: str
    effective_to: str | None
    lifecycle_state: str
    supplied_policy_source_identity: str
    knowledge_pack_key: str
    knowledge_pack_version: str
    knowledge_pack_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    configuration_evidence: tuple[ConfigurationEvidence, ...]
    readiness: ReadinessEvidence
    boundary_evidence: tuple[str, ...]
    proposed_change_context: tuple[str, ...]

    def __hash__(self) -> int:
        return hash(self.packet_fingerprint)


class AdminConfigurationAskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet: LeavePolicyConfigurationEvidencePacket
    message: str = Field(min_length=1, max_length=2000)


class AdminConfigurationAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_identity: str
    audit_identity: str
    audit_id: str | None
    outcome: Literal["ANSWERED", "REFUSED", "OUT_OF_EVIDENCE"]
    intent: str
    packet_id: str
    packet_fingerprint: str
    answer: str
    what_matters: tuple[str, ...]
    capability_boundary: str
    sources: tuple[str, ...]
    evidence_classifications: tuple[str, ...]


class AdminConfigurationProposalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    packet: LeavePolicyConfigurationEvidencePacket
    requested_change: str = Field(min_length=1, max_length=1000)


class AdminConfigurationProposalPreview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_identity: str
    audit_identity: str
    audit_id: str | None
    outcome: Literal["PREVIEW_ONLY", "REFUSED"]
    target_policy_id: str
    target_policy_version_id: str
    affected_configuration_ids: tuple[str, ...]
    successor_version_required: bool
    minimum_or_better_risk: str
    evidence_gaps: tuple[str, ...]
    preview: str
    no_mutation: Literal[True]
    no_save: Literal[True]
    no_approval: Literal[True]
    no_publication: Literal[True]
