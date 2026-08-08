from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LeaveAskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_key: str = Field(min_length=1)
    semantic_version: str = Field(min_length=1)
    message: str = Field(min_length=1, max_length=2000)


class LeavePolicyContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    context_ref: str = Field(min_length=1)
    source_policy_ref: str = Field(min_length=1)
    source_policy_version: str = Field(min_length=1)
    runtime_support_declared_flag: Literal[0]


class LeaveProposalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pack_key: str = Field(min_length=1)
    semantic_version: str = Field(min_length=1)
    context: LeavePolicyContext
    requested_change: str = Field(min_length=1, max_length=1000)
    fact_ids: list[str] = Field(min_length=1, max_length=10)
    answer_plan: LeaveAnswerPlan | None = None


class PackIdentityResponse(BaseModel):
    pack_key: str
    semantic_version: str
    status: str
    manifest_fingerprint: str


class PackCitationResponse(BaseModel):
    fact_id: str
    source_id: str
    publisher: str
    source_title: str
    url: str
    locator: str


AnswerMode = Literal[
    "GENERAL_FRAMEWORK",
    "ENTITLEMENT_OVERVIEW",
    "CONTINUITY_AND_ABSENCE",
    "TERMINATION_AND_PRO_RATA",
    "TAKING_OR_PAYMENT_BOUNDARY",
    "APPLICABILITY_OR_PORTABLE_SCHEME_BOUNDARY",
    "OUT_OF_EVIDENCE",
    "REFUSED_QLEAVE_OPERATION",
    "REFUSED_UNSAFE_REQUEST",
]


class LeaveAnswerPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    answer_mode: AnswerMode
    outcome: str
    pack_key: str
    semantic_version: str
    manifest_fingerprint: str
    selected_fact_ids: list[str]
    citations: list[PackCitationResponse]
    direct_answer: str
    relevance: str
    material_facts: list[str]
    capability_boundary: str
    safe_next_step: str
    reason: str | None = None


class LeaveAskResponse(BaseModel):
    request_identity: str
    audit_identity: str
    audit_id: str | None
    outcome: str
    pack: PackIdentityResponse
    answer: str
    fact_ids: list[str]
    source_ids: list[str]
    citations: list[PackCitationResponse]
    scope_limitations: list[str]
    answer_plan: LeaveAnswerPlan


class ProposalAssertionResponse(BaseModel):
    no_write: Literal[True]
    no_approval: Literal[True]
    no_publication: Literal[True]
    non_persisted: Literal[True]


class LeaveProposalResponse(BaseModel):
    request_identity: str
    proposal_identity: str
    audit_identity: str
    outcome: Literal["DRAFT_NON_PERSISTED"]
    pack: PackIdentityResponse
    target_policy_ref: str
    source_policy_version: str
    requested_change: str
    proposed_successor_policy_intent: str
    assumptions: list[str]
    impacts: list[str]
    required_review: list[str]
    validation_steps: list[str]
    fact_ids: list[str]
    citations: list[PackCitationResponse]
    assertions: ProposalAssertionResponse
    answer_plan: LeaveAnswerPlan | None = None
