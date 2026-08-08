"""Draft-only hand-off for a later separately authorised Leave integration."""

from __future__ import annotations

from pathlib import Path

from app.schemas.minerva_leave import LeavePolicyContext, LeaveProposalResponse, ProposalAssertionResponse
from app.services.governed_knowledge_pack_service import (
    DEFAULT_MANIFEST_PATH,
    ProposalRequestError,
    _identity,
    load_pack,
    require_requested_pack,
)


INJECTION_TERMS = ("ignore previous", "system prompt", "prompt injection", "json patch", '"op":')


def _validate_synthetic_context(context: LeavePolicyContext) -> None:
    if not context.context_ref.startswith("synthetic:"):
        raise ProposalRequestError("Proposal context must be explicitly synthetic.")
    if not context.source_policy_ref.startswith("synthetic:"):
        raise ProposalRequestError("Proposal source policy must be explicitly synthetic.")
    if not context.source_policy_version.strip():
        raise ProposalRequestError("Proposal source policy version is required.")
    if context.runtime_support_declared_flag != 0:
        raise ProposalRequestError("The proof context must preserve supplied RuntimeSupportDeclaredFlag = 0.")


def _contains_injection(text: str) -> bool:
    normalized = " ".join(text.lower().split())
    return any(term in normalized for term in INJECTION_TERMS if isinstance(term, str))


def build_draft_leave_proposal(
    *,
    context: LeavePolicyContext,
    requested_change: str,
    fact_ids: list[str],
    pack_key: str,
    semantic_version: str,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> LeaveProposalResponse:
    if _contains_injection(requested_change) or not requested_change.strip():
        raise ProposalRequestError("Malformed or prompt-injected proposal request.")
    if len(set(fact_ids)) != len(fact_ids) or not fact_ids:
        raise ProposalRequestError("Proposal requires one or more distinct cited fact identities.")
    _validate_synthetic_context(context)
    pack = load_pack(manifest_path)
    require_requested_pack(pack, pack_key, semantic_version)
    facts_by_id = {fact["fact_id"]: fact for fact in pack.data["facts"]}
    if any(fact_id not in facts_by_id for fact_id in fact_ids):
        raise ProposalRequestError("Every proposal fact identity must belong to the explicitly requested pack/version.")
    if "qleave" not in requested_change.lower() and "portable" not in requested_change.lower():
        raise ProposalRequestError("This proof proposal must explicitly address the external portable-scheme/QLeave boundary.")
    source_by_id = {source["source_id"]: source for source in pack.data["sources"]}
    citations = []
    for fact_id in fact_ids:
        fact = facts_by_id[fact_id]
        for source_id in fact["source_refs"]:
            source = source_by_id[source_id]
            citations.append(
                {
                    "fact_id": fact_id,
                    "source_id": source_id,
                    "publisher": source["publisher"],
                    "source_title": source["title"],
                    "url": source["url"],
                    "locator": source["citation_locator"],
                }
            )
    unique_citations = list({(item["fact_id"], item["source_id"]): item for item in citations}.values())
    request_identity = _identity(
        "req",
        pack_key,
        semantic_version,
        context.context_ref,
        context.source_policy_ref,
        context.source_policy_version,
        requested_change.strip(),
        *fact_ids,
    )
    proposal_identity = _identity("prop", request_identity)
    audit_identity = _identity("aud", proposal_identity, pack.data["manifest"]["content_fingerprint"])
    return LeaveProposalResponse(
        request_identity=request_identity,
        proposal_identity=proposal_identity,
        audit_identity=audit_identity,
        outcome="DRAFT_NON_PERSISTED",
        pack=pack.identity_response(),
        target_policy_ref=context.source_policy_ref,
        source_policy_version=context.source_policy_version,
        requested_change=requested_change.strip(),
        proposed_successor_policy_intent=(
            "In a separately reviewed successor policy, make the external portable-scheme/QLeave boundary explicit "
            "in user-facing explanatory material while preserving supplied RuntimeSupportDeclaredFlag = 0."
        ),
        assumptions=[
            "The supplied context is synthetic and is not a live Workforce Platform policy record.",
            "RuntimeSupportDeclaredFlag = 0 is a supplied context fact only; this repository does not assert that field exists.",
            "The successor policy would remain subject to the existing approval and publishing path outside this slice.",
        ],
        impacts=[
            "Users would see that QLeave portable-scheme operations are outside this Queensland General LSL pack.",
            "No entitlement, service history, payroll, leave request, or policy value is calculated or changed.",
        ],
        required_review=[
            "Qualified employment-law review of scope, wording, and any applicable instrument interactions.",
            "Separate Workforce Platform contract review for authenticated, tenant-filtered read-only context.",
            "Product and approval-owner review before any successor policy is considered.",
        ],
        validation_steps=[
            "Verify citations still resolve to the reviewed Queensland Government sources.",
            "Verify the target policy/version identity and supplied RuntimeSupportDeclaredFlag = 0.",
            "Verify a later integration performs no write before explicit approval and publication.",
        ],
        fact_ids=fact_ids,
        citations=unique_citations,
        assertions=ProposalAssertionResponse(
            no_write=True,
            no_approval=True,
            no_publication=True,
            non_persisted=True,
        ),
    )
