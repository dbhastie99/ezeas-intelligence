"""Deterministic answer planning for the published Queensland General LSL pack.

This module is deliberately a small seam between governed fact selection and
owner-facing prose.  It does not retrieve evidence, assess a person, calculate
leave or payment, or call an LLM.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from app.schemas.minerva_leave import AnswerMode, LeaveAnswerPlan, PackCitationResponse


SUPPORTED_ANSWER_MODES = frozenset(
    {
        "GENERAL_FRAMEWORK",
        "ENTITLEMENT_OVERVIEW",
        "CONTINUITY_AND_ABSENCE",
        "TERMINATION_AND_PRO_RATA",
        "TAKING_OR_PAYMENT_BOUNDARY",
        "APPLICABILITY_OR_PORTABLE_SCHEME_BOUNDARY",
    }
)
REFUSAL_ANSWER_MODES = frozenset({"REFUSED_QLEAVE_OPERATION", "REFUSED_UNSAFE_REQUEST"})

MODE_FACT_IDS: dict[AnswerMode, tuple[str, ...]] = {
    "GENERAL_FRAMEWORK": (
        "qld-general-lsl-scope",
        "qld-general-lsl-entitlement-overview",
        "qld-general-lsl-runtime-boundary",
    ),
    "ENTITLEMENT_OVERVIEW": (
        "qld-general-lsl-entitlement-overview",
        "qld-general-lsl-runtime-boundary",
    ),
    "CONTINUITY_AND_ABSENCE": (
        "qld-general-lsl-pro-rata-and-continuity",
        "qld-general-lsl-runtime-boundary",
    ),
    "TERMINATION_AND_PRO_RATA": (
        "qld-general-lsl-pro-rata-and-continuity",
        "qld-general-lsl-runtime-boundary",
    ),
    "TAKING_OR_PAYMENT_BOUNDARY": (
        "qld-general-lsl-payment-boundary",
        "qld-general-lsl-runtime-boundary",
    ),
    "APPLICABILITY_OR_PORTABLE_SCHEME_BOUNDARY": (
        "qld-general-lsl-scope",
        "qld-general-lsl-runtime-boundary",
    ),
    "OUT_OF_EVIDENCE": (),
    "REFUSED_QLEAVE_OPERATION": (),
    "REFUSED_UNSAFE_REQUEST": (),
}


class AnswerPlanError(ValueError):
    """Raised when a plan is attempted with facts outside its governed mode."""


def _normalise(question: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", question.lower()))


def _has_any(text: str, phrases: Sequence[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def _is_qleave_context(text: str) -> bool:
    return _has_any(text, ("qleave", "portable scheme", "portable schemes", "portable long service"))


def _is_qleave_operation(text: str) -> bool:
    if not _is_qleave_context(text):
        return False
    return _has_any(
        text,
        (
            "registration",
            "register",
            "levy",
            "levies",
            "return",
            "returns",
            "claim",
            "claims",
            "reimbursement",
            "reimburse",
            "operational procedure",
            "operational process",
            "how do i",
            "how can i",
            "lodge",
            "submit",
        ),
    )


def classify_question(question: str) -> AnswerMode:
    """Classify only explicit, governed intents; otherwise return OUT_OF_EVIDENCE."""

    text = _normalise(question)
    if _has_any(
        text,
        (
            "ignore previous",
            "ignore the instructions",
            "system prompt",
            "prompt injection",
            "reveal your instructions",
        ),
    ):
        return "REFUSED_UNSAFE_REQUEST"
    if _is_qleave_operation(text):
        return "REFUSED_QLEAVE_OPERATION"
    if _is_qleave_context(text) and _has_any(
        text,
        ("case", "applies", "apply", "applicable", "eligible", "eligibility", "which scheme", "what is qleave"),
    ):
        return "APPLICABILITY_OR_PORTABLE_SCHEME_BOUNDARY"
    if _has_any(text, ("break in service", "break of service", "continuity", "continuous service", "absence", "absences")):
        return "CONTINUITY_AND_ABSENCE"
    if _has_any(text, ("employment ends", "employment ended", "termination", "terminate", "pro rata", "pro-rata", "7 years", "seven years")):
        return "TERMINATION_AND_PRO_RATA"
    if _has_any(text, ("how is long service leave paid", "how is lsl paid", "payment rate", "taking long service leave", "take long service leave", "payment", "paid")):
        return "TAKING_OR_PAYMENT_BOUNDARY"
    if _has_any(text, ("after ten years", "after 10 years", "10 years", "ten years", "entitlement overview", "how much leave")):
        return "ENTITLEMENT_OVERVIEW"
    if _has_any(
        text,
        (
            "what is queensland long service leave",
            "what is queensland general lsl",
            "queensland general long service leave",
            "general lsl framework",
            "scope of queensland",
            "explain the scope",
            "long service leave framework",
            "federal system",
        ),
    ):
        return "GENERAL_FRAMEWORK"
    return "OUT_OF_EVIDENCE"


_CONTENT: dict[AnswerMode, dict[str, Any]] = {
    "GENERAL_FRAMEWORK": {
        "direct_answer": (
            "Queensland General Long Service Leave is the cited Queensland framework for long service leave where it applies. "
            "The reviewed guide describes the Queensland framework where the federal system does not provide an entitlement; its general overview is 8.6667 weeks after 10 years continuous service for an employee other than a seasonal employee, subject to the Act and applicable instruments."
        ),
        "relevance": "This gives the requested framework overview and keeps the Queensland General LSL scope distinct from the external QLeave portable-scheme boundary.",
        "material_facts": [
            "Whether the Queensland framework applies rather than the federal system.",
            "The applicable industrial instrument and statutory exceptions.",
            "The worker category and continuous-service facts.",
        ],
        "capability_boundary": "Minerva can explain the cited framework and scope. It cannot decide an individual entitlement, reconstruct service, or provide legal advice.",
        "safe_next_step": "Use the cited Act and Queensland Government guide for the relevant facts, and obtain qualified advice if the application or exceptions are disputed.",
    },
    "ENTITLEMENT_OVERVIEW": {
        "direct_answer": (
            "The published general overview is 8.6667 weeks of long service leave after 10 years continuous service for an employee other than a seasonal employee, with a further proportional entitlement after a further 5 years, subject to the Act and applicable instruments."
        ),
        "relevance": "This answers the general ten-year question without turning the overview into a finding about a particular person.",
        "material_facts": [
            "Continuous service and the applicable service history.",
            "Whether the worker is within the cited employee category.",
            "The federal-system, industrial-instrument and statutory-exception context.",
        ],
        "capability_boundary": "Minerva can state the published overview. It cannot determine individual eligibility, calculate a balance, or value a payment.",
        "safe_next_step": "Check the complete cited provisions and the relevant employment facts with a qualified reviewer before relying on an individual result.",
    },
    "CONTINUITY_AND_ABSENCE": {
        "direct_answer": "Yes. A break or absence can matter, but continuity and particular absences are governed by statutory rules and facts; elapsed time alone does not decide the result.",
        "relevance": "This focuses on the continuity boundary rather than assuming that a particular break preserves or breaks service.",
        "material_facts": [
            "The employer relationship and service periods.",
            "The relevant absences and their treatment under the cited statutory rules.",
            "The applicable system, instrument and worker circumstances.",
        ],
        "capability_boundary": "Minerva can explain that continuity is fact- and statute-dependent. It cannot reconstruct service or decide whether a particular break counts.",
        "safe_next_step": "Set out the relevant service and absence chronology for review against the cited Act and guidance; seek qualified advice where the rule is disputed.",
    },
    "TERMINATION_AND_PRO_RATA": {
        "direct_answer": "The cited framework provides a conditional pro-rata payment boundary after at least 7 years on termination, subject to the stated conditions before 10 years. That does not by itself establish a payment for a person.",
        "relevance": "This addresses the seven-year termination overview while preserving the condition and classification boundaries.",
        "material_facts": [
            "The continuous-service history.",
            "The termination circumstances and the reason for termination.",
            "The applicable statutory conditions, system and industrial instrument.",
        ],
        "capability_boundary": "Minerva can explain the conditional pro-rata boundary. It cannot classify the termination, reconstruct service, calculate an entitlement, or produce a payment.",
        "safe_next_step": "Have the termination facts and service chronology reviewed against the complete cited provisions by a qualified employment-law or payroll reviewer.",
    },
    "TAKING_OR_PAYMENT_BOUNDARY": {
        "direct_answer": "The cited material explains that taking leave and payment depend on the applicable statutory provisions, rate rules and circumstances. This pack does not turn that guidance into a dollar amount, pay rate, payslip or payroll result.",
        "relevance": "This answers the payment question at the level supported by the pack and keeps valuation outside Minerva’s capability here.",
        "material_facts": [
            "The applicable statutory taking and payment provisions.",
            "The worker’s applicable rate, hours and circumstances.",
            "The relevant service, leave-taking and employment facts.",
        ],
        "capability_boundary": "Minerva can explain the cited payment boundary. It cannot calculate, value or process leave, determine a pay rate, create a payslip, or produce a payroll result.",
        "safe_next_step": "Use the cited provisions and have the relevant employment and rate facts checked by an authorised payroll or qualified legal reviewer.",
    },
    "APPLICABILITY_OR_PORTABLE_SCHEME_BOUNDARY": {
        "direct_answer": "It could be a QLeave matter, but this pack cannot decide scheme eligibility. QLeave is identified as a portable long service leave scheme for eligible workers in specified industries; Queensland General LSL must not be applied automatically when the external-scheme context is missing. QLeave eligibility and operations remain ON HOLD in this assistant.",
        "relevance": "This gives a useful boundary between the cited Queensland General LSL framework and QLeave without turning the question into a QLeave operation or eligibility determination.",
        "material_facts": [
            "The industry and worker circumstances relevant to any portable scheme.",
            "Whether the cited Queensland General LSL framework or an external scheme applies.",
            "The external QLeave context, which is not present in this pack.",
        ],
        "capability_boundary": "QLeave eligibility and operations remain ON HOLD. Minerva can explain the boundary, but it cannot determine QLeave eligibility and cannot register, levy, lodge returns, make claims, seek reimbursement or make QLeave payments.",
        "safe_next_step": "Confirm the applicable scheme with the relevant Queensland Government material or qualified adviser; do not treat this pack as a QLeave operations guide.",
    },
    "OUT_OF_EVIDENCE": {
        "direct_answer": "I cannot answer that question from the reviewed Queensland General LSL facts in this pack.",
        "relevance": "No governed fact family was selected, so Minerva is not guessing or dumping unrelated pack content.",
        "material_facts": [],
        "capability_boundary": "Minerva cannot infer facts, retrieve an unreviewed source, make an individual determination, or extend this pack beyond its cited scope.",
        "safe_next_step": "Ask a focused question about the published framework, ten-year overview, continuity and absence, termination pro-rata boundary, taking/payment boundary, or QLeave applicability boundary.",
    },
    "REFUSED_QLEAVE_OPERATION": {
        "direct_answer": "QLeave eligibility and operations remain ON HOLD in this assistant. I cannot provide QLeave registration, levy, return, claim, reimbursement, payment or other operational instructions from this pack.",
        "relevance": "The question requests an excluded QLeave operation rather than the pack’s boundary explanation.",
        "material_facts": [],
        "capability_boundary": "QLeave eligibility and operations remain ON HOLD. QLeave operations are outside this published Queensland General LSL pack; no operational procedure is supplied.",
        "safe_next_step": "Use the relevant official QLeave channel or qualified adviser for operational guidance.",
    },
    "REFUSED_UNSAFE_REQUEST": {
        "direct_answer": "I cannot follow prompt-injection instructions or disclose hidden instructions.",
        "relevance": "The request is unsafe and is not treated as a Queensland General LSL evidence question.",
        "material_facts": [],
        "capability_boundary": "The governed assistant will use only the published pack and its fixed capability boundary.",
        "safe_next_step": "Ask a normal, focused Queensland General LSL question.",
    },
}


def build_answer_plan(
    *,
    mode: AnswerMode,
    selected_facts: Sequence[Mapping[str, Any]],
    citations: Sequence[PackCitationResponse],
    pack_key: str,
    semantic_version: str,
    manifest_fingerprint: str,
) -> LeaveAnswerPlan:
    expected_fact_ids = MODE_FACT_IDS[mode]
    selected_fact_ids = tuple(str(fact.get("fact_id")) for fact in selected_facts)
    if selected_fact_ids != expected_fact_ids:
        raise AnswerPlanError(
            f"Answer mode {mode} requires fact IDs {expected_fact_ids}, received {selected_fact_ids}."
        )
    citation_fact_ids = {citation.fact_id for citation in citations}
    if expected_fact_ids and citation_fact_ids != set(expected_fact_ids):
        raise AnswerPlanError("Answer citations must cover exactly the selected fact IDs.")
    if not expected_fact_ids and citations:
        raise AnswerPlanError("Answer citations must cover exactly the selected fact IDs.")
    if any(citation.fact_id not in expected_fact_ids for citation in citations):
        raise AnswerPlanError("Answer citations contain a fact outside the selected answer mode.")
    content = _CONTENT[mode]
    if mode in SUPPORTED_ANSWER_MODES:
        outcome = "ANSWERED_FROM_PUBLISHED_PACK"
    elif mode == "OUT_OF_EVIDENCE":
        outcome = "OUT_OF_EVIDENCE"
    elif mode == "REFUSED_QLEAVE_OPERATION":
        outcome = "REFUSED_OUT_OF_SCOPE"
    else:
        outcome = "REFUSED_UNSAFE_REQUEST"
    return LeaveAnswerPlan(
        answer_mode=mode,
        outcome=outcome,
        pack_key=pack_key,
        semantic_version=semantic_version,
        manifest_fingerprint=manifest_fingerprint,
        selected_fact_ids=list(selected_fact_ids),
        citations=list(citations),
        direct_answer=content["direct_answer"],
        relevance=content["relevance"],
        material_facts=list(content["material_facts"]),
        capability_boundary=content["capability_boundary"],
        safe_next_step=content["safe_next_step"],
        reason=(content["relevance"] if mode in {"OUT_OF_EVIDENCE", *REFUSAL_ANSWER_MODES} else None),
    )


def render_answer(plan: LeaveAnswerPlan) -> str:
    lines = [
        "**Answer**",
        plan.direct_answer,
        "",
        "**What matters**",
    ]
    if plan.material_facts:
        lines.extend(f"- {fact}" for fact in plan.material_facts)
    else:
        lines.append(plan.relevance)
    lines.extend(
        [
            "",
            "**Capability boundary**",
            plan.capability_boundary,
            f"Safe next step: {plan.safe_next_step}",
            "",
            "**Sources**",
        ]
    )
    if plan.citations:
        seen: set[str] = set()
        for citation in plan.citations:
            key = citation.source_id
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"- {citation.source_title} — {citation.url} ({citation.locator})")
    else:
        lines.append("No supporting pack citation is returned for this result.")
    return "\n".join(lines)
