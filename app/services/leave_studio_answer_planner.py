from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable

from app.schemas.leave_studio_minerva import (
    EvidenceReference,
    LeaveStudioAnswerPlan,
    LeaveStudioContextV1,
    LeaveStudioQuestionRequest,
    QuestionClassification,
    SelectedMaterialFact,
)


class LeaveStudioContractError(ValueError):
    pass


def _canonical(value: object) -> bytes:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_context_fingerprint(context: LeaveStudioContextV1) -> str:
    return _sha256(_canonical(context))


def validate_request(request: LeaveStudioQuestionRequest) -> LeaveStudioQuestionRequest:
    context = request.StudioContext
    if request.StudioContextSchemaVersion != context.SchemaVersion:
        raise LeaveStudioContractError("Studio context schema identity does not match the request envelope.")
    if request.PackageCode != context.PackageCode:
        raise LeaveStudioContractError("Package identity does not match the governed Studio context.")
    if request.LeaveTypeVersionId != context.LeaveTypeVersionId:
        raise LeaveStudioContractError("LeaveTypeVersion identity does not match the governed Studio context.")
    expected = canonical_context_fingerprint(context)
    if request.StudioContextFingerprint != expected:
        raise LeaveStudioContractError("Studio context fingerprint mismatch.")
    if not context.ConfidentialDataExcluded:
        raise LeaveStudioContractError("Confidential policy context must be excluded.")
    return request


def _normalise(question: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", question.lower()))


def classify_question(question: str) -> QuestionClassification:
    text = _normalise(question)
    if any(term in text for term in ("publish", "change fdv", "change this", "save this", "approve", "create leave request")):
        return "UNKNOWN_OR_UNSUPPORTED"
    if any(term in text for term in ("ignore the configuration", "australian law says", "browse", "internet", "general legal advice")):
        return "UNKNOWN_OR_UNSUPPORTED"
    if "qleave" in text or "portable scheme" in text:
        return "QLEAVE_BOUNDARY"
    if any(term in text for term in ("this employee", "current worker", "apply to john", "apply to this worker", "person entitled", "employee entitled")):
        return "APPLICABILITY_SCOPE"
    if "runtime" in text or "operational yet" in text or "implemented yet" in text:
        return "RUNTIME_SUPPORT"
    if any(term in text for term in ("ready", "readiness", "on hold", "hold", "not configured yet", "unresolved", "what is missing")):
        return "READINESS"
    if "source precedence" in text or "legal source" in text or "authority" in text or "citation" in text:
        return "SOURCE_AUTHORITY"
    if "valuation" in text or "valuation method" in text or "valuation strateg" in text:
        return "LSL_VALUATION"
    if "termination" in text or "pro rata" in text:
        return "LSL_TERMINATION"
    if "vesting" in text or "vested" in text:
        return "LSL_VESTING"
    if "service history" in text or "service facts" in text or "service rules" in text or "service mean" in text:
        return "LSL_SERVICE"
    if "payroll basis" in text or "which payroll hours" in text or "hours count" in text or "basis" in text:
        return "PAYROLL_BASIS"
    if any(term in text for term in ("version", "predecessor", "successor", "lineage")):
        return "VERSION_LINEAGE"
    if "public holiday" in text:
        return "PUBLIC_HOLIDAY"
    if "forecast" in text or "future" in text:
        return "FORECAST"
    if "privacy" in text or "confidential" in text or "payslip" in text:
        return "PRIVACY"
    if "evidence" in text or "notice" in text or "proof" in text:
        return "EVIDENCE"
    if "loading" in text:
        return "LOADING"
    if any(term in text for term in ("paid", "payment", "rate strategy", "how is it paid")):
        return "PAYMENT"
    if any(term in text for term in ("employer change", "organisation change", "organization change", "choice", "selectable")):
        return "ORGANISATION_CHOICE"
    if any(term in text for term in ("take leave", "taking", "carry forward", "accumulate", "reset", "grant")):
        return "TAKING"
    if any(term in text for term in ("hourly accrual", "accrual rate", "accrue", "accrual")):
        return "ACCRUAL"
    if any(term in text for term in ("how much", "entitlement", "ten days", "four weeks")):
        return "ENTITLEMENT"
    if any(term in text for term in ("apply", "scope", "covered", "casual", "who")):
        return "APPLICABILITY_SCOPE"
    if any(term in text for term in ("overview", "explain", "what is", "how does")):
        return "OVERVIEW"
    return "UNKNOWN_OR_UNSUPPORTED"


KEYS_BY_CLASS: dict[str, tuple[str, ...]] = {
    "OVERVIEW": ("leave_type", "version", "ownership", "EntitlementPatternCode"),
    "ENTITLEMENT": ("AnnualEntitlementWeeks", "GrantQuantityDays", "EntitlementPatternCode", "CarryForwardModeCode"),
    "ACCRUAL": ("AccrualMethodCode", "accrual_rate_per_hour", "AnnualEntitlementWeeks", "GrantQuantityDays"),
    "PAYROLL_BASIS": ("payroll_basis",),
    "PUBLIC_HOLIDAY": ("PublicHolidayAccrualModeCode", "PublicHolidayTreatmentCode"),
    "FORECAST": ("ForecastFallbackModeCode",),
    "TAKING": ("ResetModeCode", "CarryForwardModeCode", "ExpiryModeCode", "CashoutTreatmentCode"),
    "EVIDENCE": ("EvidenceTypeCode", "RequirementModeCode", "TriggerCode", "NoticeDays", "StorageModeCode"),
    "PRIVACY": ("PrivacyClassCode", "privacy_", "PayslipDisplayModeCode", "OperatorDisplayModeCode"),
    "PAYMENT": ("PaymentOutcomeCode", "RateStrategyCode", "BasisPeriodCode", "FailureDispositionCode"),
    "LOADING": ("LoadingModeCode", "LoadingPercentage"),
    "ORGANISATION_CHOICE": ("resolved_setting:",),
    "APPLICABILITY_SCOPE": ("JurisdictionCode", "EligibilityModeCode", "AmbiguityDispositionCode", "ApplicabilityLayerCode"),
}


def _key_matches(key: str, wanted: Iterable[str]) -> bool:
    return any(key == item or (item.endswith(":") and key.startswith(item)) or (item.endswith("_") and item in key) for item in wanted)


def _fact_reference_id(key: str) -> str:
    return "fact-" + re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


def _material_fact(fact) -> tuple[SelectedMaterialFact, EvidenceReference]:
    reference_id = _fact_reference_id(fact.Key)
    reference = EvidenceReference(
        EvidenceReferenceId=reference_id,
        Label=fact.Label,
        Reference=fact.CanonicalSource,
        Section=fact.Domain,
    )
    material = SelectedMaterialFact(
        FactId=fact.Key,
        Label=fact.Label,
        Value=None if fact.Value is None else str(fact.Value),
        DisplayValue=fact.DisplayValue,
        AuthorityClass=fact.AuthorityClass,
        EvidenceReferenceIds=[reference_id],
    )
    return material, reference


def _section_material(
    section_name: str,
    items,
) -> tuple[list[SelectedMaterialFact], list[EvidenceReference]]:
    facts: list[SelectedMaterialFact] = []
    references: list[EvidenceReference] = []
    for item in items:
        fact_id = f"{section_name.lower()}:{item.Code}"
        reference_id = _fact_reference_id(fact_id)
        display = item.Outcome or item.Disposition or item.Label
        facts.append(
            SelectedMaterialFact(
                FactId=fact_id,
                Label=item.Label,
                Value=display,
                DisplayValue=display,
                AuthorityClass="CANONICAL_STORED_FACT",
                EvidenceReferenceIds=[reference_id],
            )
        )
        references.append(
            EvidenceReference(
                EvidenceReferenceId=reference_id,
                Label=item.Label,
                Reference=item.Authority or item.ContentHash or item.Code,
                Section=section_name,
            )
        )
    return facts, references


def _select(context: LeaveStudioContextV1, classification: QuestionClassification):
    wanted = KEYS_BY_CLASS.get(classification, KEYS_BY_CLASS["OVERVIEW"])
    facts: list[SelectedMaterialFact] = []
    references: list[EvidenceReference] = []
    def add_synthetic(fact_id: str, label: str, value: str, authority: str, section: str = "Policy/version") -> None:
        reference_id = _fact_reference_id(fact_id)
        facts.append(SelectedMaterialFact(
            FactId=fact_id,
            Label=label,
            Value=value,
            DisplayValue=value,
            AuthorityClass=authority,
            EvidenceReferenceIds=[reference_id],
        ))
        references.append(EvidenceReference(
            EvidenceReferenceId=reference_id,
            Label=label,
            Reference=context.LeaveTypeVersionId,
            Section=section,
        ))
    for fact in context.Facts:
        if _key_matches(fact.Key, wanted):
            material, reference = _material_fact(fact)
            facts.append(material)
            references.append(reference)

    if classification == "PAYROLL_BASIS":
        for basis in context.PayrollBases:
            fact_id = f"payroll_basis_version:{basis.BasisCode}"
            reference_id = _fact_reference_id(fact_id)
            facts.append(SelectedMaterialFact(
                FactId=fact_id,
                Label=basis.BusinessName,
                Value=basis.VersionLabel,
                DisplayValue=f"{basis.BusinessName} ({basis.VersionLabel})",
                AuthorityClass="CANONICAL_STORED_FACT",
                EvidenceReferenceIds=[reference_id],
            ))
            references.append(EvidenceReference(
                EvidenceReferenceId=reference_id,
                Label=f"Payroll Basis {basis.VersionLabel}",
                Reference=basis.AuthorityExplanation,
                Section="Payroll Basis",
            ))
    if classification in {"READINESS", "RUNTIME_SUPPORT", "QLEAVE_BOUNDARY"}:
        add_synthetic("configuration_readiness", "Configuration readiness", context.ConfigurationReadiness, "CANONICAL_STORED_FACT", "Readiness assessment")
        add_synthetic("runtime_support", "Runtime support", context.RuntimeSupport, "CANONICAL_STORED_FACT", "Readiness assessment")
        for finding in context.ReadinessFindings:
            add_synthetic(
                f"readiness_finding:{finding.Code}",
                f"Readiness finding {finding.Code}",
                finding.Message,
                "CANONICAL_STORED_FACT",
                "Readiness assessment",
            )
    if classification == "VERSION_LINEAGE":
        add_synthetic("version_code", "Exact policy version", context.VersionCode, "CANONICAL_STORED_FACT")
        if context.PredecessorLeaveTypeVersionId:
            add_synthetic("predecessor_version", "Predecessor version", context.PredecessorLeaveTypeVersionId, "CANONICAL_STORED_FACT")
        add_synthetic("successor_version_count", "Configured successor count", str(len(context.SuccessorLeaveTypeVersionIds)), "DETERMINISTIC_DERIVATION")
    if classification == "APPLICABILITY_SCOPE":
        add_synthetic(
            "worker_applicability_disclaimer",
            "Worker applicability disclaimer",
            context.WorkerApplicabilityStatement,
            "DETERMINISTIC_DERIVATION",
            "Applicability",
        )
    if classification == "SOURCE_AUTHORITY":
        for index, source in enumerate(context.SourceEvidence, start=1):
            reference_id = f"source-evidence-{index}"
            facts.append(SelectedMaterialFact(
                FactId=reference_id,
                Label=source.SourceTitle,
                Value=source.Citation,
                DisplayValue=f"{source.SourceTitle}: {source.Citation}",
                AuthorityClass="CANONICAL_STORED_FACT",
                EvidenceReferenceIds=[reference_id],
            ))
            references.append(EvidenceReference(
                EvidenceReferenceId=reference_id,
                Label=source.SourceTitle,
                Reference=source.Citation,
                Section="Source evidence",
            ))
    section_map = {
        "SOURCE_AUTHORITY": ("Source precedence", context.SourcePrecedence),
        "LSL_SERVICE": ("Required facts", context.RequiredFacts),
        "LSL_VESTING": ("Service history", context.ServiceHistory),
        "LSL_TERMINATION": ("Case-level holds", context.CaseLevelHolds),
        "LSL_VALUATION": ("Valuation strategies", context.ValuationStrategies),
    }
    if classification in section_map:
        name, items = section_map[classification]
        extra_facts, extra_refs = _section_material(name, items)
        facts.extend(extra_facts)
        references.extend(extra_refs)
    if classification == "QLEAVE_BOUNDARY" and context.PortableSchemeBoundary:
        facts.append(SelectedMaterialFact(
            FactId="portable_scheme_boundary",
            Label="Portable scheme boundary",
            Value=context.PortableSchemeBoundary,
            DisplayValue=context.PortableSchemeBoundary,
            AuthorityClass="DETERMINISTIC_DERIVATION",
            EvidenceReferenceIds=["policy-version"],
        ))
        add_synthetic(
            "qleave_operational_administration",
            "QLeave operational administration",
            "Not established by this configuration context",
            "MISSING_OR_UNRESOLVED_FACT",
            "Portable scheme boundary",
        )
    if not facts:
        for fact in context.Facts[:4]:
            material, reference = _material_fact(fact)
            facts.append(material)
            references.append(reference)
    policy_reference = EvidenceReference(
        EvidenceReferenceId="policy-version",
        Label=f"{context.LeaveTypeName} — {context.VersionCode}",
        Reference=context.LeaveTypeVersionId,
        Section="Policy/version",
    )
    dedup = {reference.EvidenceReferenceId: reference for reference in [policy_reference, *references]}
    return facts, list(dedup.values())


def _by_id(facts: list[SelectedMaterialFact], fact_id: str) -> SelectedMaterialFact | None:
    return next((fact for fact in facts if fact.FactId == fact_id), None)


def _configured_text(facts: list[SelectedMaterialFact]) -> str:
    known = [f"{fact.Label}: {fact.DisplayValue}" for fact in facts if fact.AuthorityClass != "MISSING_OR_UNRESOLVED_FACT"]
    return "; ".join(known[:5])


def _direct_answer(
    question: str,
    classification: QuestionClassification,
    context: LeaveStudioContextV1,
    facts: list[SelectedMaterialFact],
) -> str:
    text = _normalise(question)
    if classification == "UNKNOWN_OR_UNSUPPORTED":
        if any(term in text for term in ("publish", "change", "save", "approve")):
            return "Ask Minerva is read-only and made no change. Use the separate Change with Minerva experience for a governed change preview; publication is not authorised here."
        return "This Ask Minerva mode explains only the governed configuration supplied by Leave Policy Studio. It does not replace missing configuration with general web or legal research."
    if classification == "APPLICABILITY_SCOPE" and any(term in text for term in ("john", "employee", "worker", "person entitled")):
        return f"The configured policy scope can be explained, but this context cannot determine whether a particular worker is covered. {context.WorkerApplicabilityStatement}"
    if classification == "READINESS":
        return f"Configuration readiness is {context.ConfigurationReadiness}. Runtime support is separately recorded as {context.RuntimeSupport}. These are different states, so configuration readiness alone is not a runtime calculation claim."
    if classification == "RUNTIME_SUPPORT":
        return f"The exact policy version reports: {context.RuntimeSupport}. Ask Minerva can explain its configuration but cannot activate, calculate, publish, or post it."
    if classification == "PAYROLL_BASIS":
        if not context.PayrollBases:
            return "No Payroll Basis is bound to this exact policy version. Minerva has not borrowed a v1 basis, predecessor basis, or basis from another version."
        return f"This exact version is bound to {', '.join(basis.VersionLabel for basis in context.PayrollBases)}. The basis identifies configured qualifying inputs; it is not proof of worker-specific inclusion or runtime calculation."
    if classification == "ACCRUAL":
        rate = _by_id(facts, "accrual_rate_per_hour")
        if rate and rate.AuthorityClass == "MISSING_OR_UNRESOLVED_FACT":
            return "No governed hourly accrual rate is configured. The entitlement may be expressed in days, but the supplied context contains no day-to-hours conversion, so Minerva will not invent a days/260, 7.6-hour, or 8-hour assumption."
        if rate:
            return f"The configured/derived accrual rate per qualifying hour is {rate.DisplayValue}. Its authority is {rate.AuthorityClass}; qualifying hours are defined separately by the exact bound Payroll Basis."
    if classification == "ENTITLEMENT":
        weeks = _by_id(facts, "AnnualEntitlementWeeks")
        days = _by_id(facts, "GrantQuantityDays")
        quantity = weeks or days
        if quantity and quantity.AuthorityClass != "MISSING_OR_UNRESOLVED_FACT":
            return f"{context.LeaveTypeName} is configured with {quantity.DisplayValue} for {quantity.Label.lower()} on exact version {context.VersionCode}."
    if classification == "PUBLIC_HOLIDAY" and "accru" in text:
        accrual_fact = _by_id(facts, "PublicHolidayAccrualModeCode")
        if accrual_fact and accrual_fact.AuthorityClass == "MISSING_OR_UNRESOLVED_FACT":
            return "The public-holiday accrual treatment is not configured in this exact version. A separate payment treatment may be present, but Minerva will not use it as an accrual default."
    if classification in ("PUBLIC_HOLIDAY", "FORECAST") and all(
        fact.AuthorityClass == "MISSING_OR_UNRESOLVED_FACT" for fact in facts
    ):
        label = "public-holiday treatment" if classification == "PUBLIC_HOLIDAY" else "forecast fallback"
        return f"The {label} is not configured in this exact version. Minerva will not substitute a generic default."
    if classification == "QLEAVE_BOUNDARY":
        boundary = context.PortableSchemeBoundary or "No portable-scheme boundary is supplied for this version."
        return f"{boundary} Operational QLeave administration is not established by this configuration-only context."
    if classification.startswith("LSL_"):
        known = _configured_text(facts)
        return f"The exact LSL version supplies governed {classification.lower().replace('_', ' ')} context. {known or 'No supporting item is configured.'} Service-history explanation is not a worker entitlement calculation."
    configured = _configured_text(facts)
    return f"For {context.LeaveTypeName} version {context.VersionCode}, the governed configuration says: {configured or 'the requested value is not configured.'}"


def build_answer_plan(request: LeaveStudioQuestionRequest) -> LeaveStudioAnswerPlan:
    request = validate_request(request)
    context = request.StudioContext
    classification = classify_question(request.Question)
    selected, references = _select(context, classification)
    missing = [
        f"{fact.Label}: {fact.DisplayValue}"
        for fact in context.Facts
        if fact.AuthorityClass == "MISSING_OR_UNRESOLVED_FACT"
    ]
    missing.extend(f"Readiness finding {finding.Code}: {finding.Message}" for finding in context.ReadinessFindings)
    missing = list(dict.fromkeys(missing))
    if classification == "APPLICABILITY_SCOPE":
        boundary = "This answer describes configured scope only; worker-specific applicability and entitlement require governed worker context that was not supplied."
    elif classification.startswith("LSL_"):
        boundary = "Minerva can explain configured LSL service/source rules but cannot replay service history or decide an individual worker's entitlement."
    elif classification == "QLEAVE_BOUNDARY":
        boundary = "Minerva can explain the external portable-scheme boundary but cannot provide QLeave registration, levy, return, claim, reimbursement, or operational administration instructions."
    else:
        boundary = "Minerva is explaining the configured policy shown in Studio. No worker calculation, configuration change, publication, payroll, or ledger action is performed."
    safe_next = (
        "Review the missing or held facts in Leave Policy Studio."
        if missing or context.ConfigurationReadiness.upper() == "HOLD"
        else "Review the cited policy/version and configuration sections in Leave Policy Studio."
    )
    direct = _direct_answer(request.Question, classification, context, selected)
    what_matters = [
        f"{fact.Label}: {fact.DisplayValue} ({fact.AuthorityClass})"
        for fact in selected[:8]
    ]
    plan_data = {
        "QuestionClassification": classification,
        "LeaveTypeVersionId": context.LeaveTypeVersionId,
        "DirectDeterministicAnswer": direct,
        "WhatMatters": what_matters,
        "SelectedMaterialFacts": [fact.model_dump(mode="json") for fact in selected],
        "FactIds": [fact.FactId for fact in selected],
        "FactAuthorityClasses": [fact.AuthorityClass for fact in selected],
        "MissingOrUnresolvedFacts": missing,
        "ReadinessState": context.ConfigurationReadiness,
        "RuntimeSupportState": context.RuntimeSupport,
        "Boundary": boundary,
        "SafeNextStep": safe_next,
        "EvidenceReferences": [reference.model_dump(mode="json") for reference in references],
        "RendererEligible": classification != "UNKNOWN_OR_UNSUPPORTED",
    }
    fingerprint = _sha256(_canonical(plan_data))
    return LeaveStudioAnswerPlan(**plan_data, PlannerFingerprint=fingerprint)
