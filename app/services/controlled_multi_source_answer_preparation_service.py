import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from app.services.controlled_durable_evidence_retrieval_harness_service import (
    BOUNDARY_FLAGS,
)
from app.services.controlled_multi_source_evidence_retrieval_service import (
    DEVELOPER_LOG,
    HARDENING_LOG,
    PLATFORM_DOCTRINE,
    build_controlled_multi_source_evidence_retrieval,
)


ANSWER_PREPARATION_MODE = (
    "DETERMINISTIC_MULTI_SOURCE_ANSWER_PREPARATION_V0_1"
)
ANSWER_PREPARATION_UNIVERSE = (
    "CONTROLLED_MULTI_SOURCE_RETRIEVAL_RESULTS_LOCAL_FIXTURES_V0_1"
)

GENERAL_CONTROLLED_PREPARATION = "GENERAL_CONTROLLED_PREPARATION"
STATUS_EXPLANATION = "STATUS_EXPLANATION"
DOCTRINE_EXPLANATION = "DOCTRINE_EXPLANATION"
WORK_COMPLETED_EXPLANATION = "WORK_COMPLETED_EXPLANATION"
PROHIBITION_EXPLANATION = "PROHIBITION_EXPLANATION"

PREPARED = "PREPARED"
PREPARED_WITH_CAVEATS = "PREPARED_WITH_CAVEATS"
INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
BLOCKED_PROHIBITED_CLAIM = "BLOCKED_PROHIBITED_CLAIM"
OUT_OF_SCOPE = "OUT_OF_SCOPE"

SUPPORTED = "SUPPORTED"
SUPPORTED_WITH_CAVEAT = "SUPPORTED_WITH_CAVEAT"
UNSUPPORTED = "UNSUPPORTED"
PROHIBITED = "PROHIBITED"
REQUIRES_CURRENT_RUNTIME_EVIDENCE = "REQUIRES_CURRENT_RUNTIME_EVIDENCE"
REQUIRES_CODE_EVIDENCE = "REQUIRES_CODE_EVIDENCE"
REQUIRES_DB_EVIDENCE = "REQUIRES_DB_EVIDENCE"
REQUIRES_DEPLOYMENT_EVIDENCE = "REQUIRES_DEPLOYMENT_EVIDENCE"

PLATFORM_DOCTRINE_GROUP = "PlatformDoctrineEvidence"
HARDENING_LOG_GROUP = "HardeningLogEvidence"
DEVELOPER_LOG_GROUP = "DeveloperLogEvidence"
OUT_OF_SCOPE_GROUP = "OutOfScopeEvidence"

SOURCE_GROUPS = {
    PLATFORM_DOCTRINE: PLATFORM_DOCTRINE_GROUP,
    HARDENING_LOG: HARDENING_LOG_GROUP,
    DEVELOPER_LOG: DEVELOPER_LOG_GROUP,
}

SOURCE_PERMITTED_USE = {
    PLATFORM_DOCTRINE: (
        "Can establish platform doctrine, rules, principles, and source/status "
        "boundaries. Cannot prove runtime implementation, execution, deployment, "
        "or production readiness."
    ),
    HARDENING_LOG: (
        "Can establish risks, prohibitions, deferred work, and required "
        "boundaries. Cannot prove implementation, repair completion, runtime "
        "behaviour, deployment, or production readiness."
    ),
    DEVELOPER_LOG: (
        "Can establish work completed, tests run, implementation-status records, "
        "and decisions captured at controlled-readiness level. Cannot prove "
        "current runtime state, deployment, or production readiness."
    ),
}

SOURCE_CANNOT_PROVE = {
    PLATFORM_DOCTRINE: (
        "implementation completed",
        "runtime behaviour",
        "deployment readiness",
        "production readiness",
    ),
    HARDENING_LOG: (
        "implementation completed",
        "repair completed",
        "runtime behaviour",
        "production readiness",
    ),
    DEVELOPER_LOG: (
        "current runtime truth",
        "live DB state",
        "deployment readiness",
        "production readiness",
    ),
}

NEXT_STEP = (
    "Use this preparation packet only for controlled review or a later citation/"
    "provenance slice. Final answer generation, chat exposure, live LLM calls, "
    "DB access, corpus mutation, runtime integration, and production-readiness "
    "claims remain prohibited."
)

FINAL_ANSWER_PROHIBITION = (
    "Final answer generation remains prohibited in this slice because the packet "
    "is a deterministic preparation artefact only, lacks full citation assembly, "
    "does not perform runtime/DB/deployment checks, and does not call a live LLM."
)


@dataclass(frozen=True)
class AnswerPreparationEnvelope:
    QueryText: str
    AnswerMode: str
    PreparationMode: str
    EvidenceUniverse: str
    PreparationStatus: str
    EvidenceUsed: tuple[dict[str, Any], ...]
    EvidenceExcluded: tuple[dict[str, Any], ...]
    EvidenceBySourceType: dict[str, dict[str, Any]]
    SourceAuthoritySummary: tuple[dict[str, Any], ...]
    CurrentTruthAssessment: dict[str, Any]
    ImplementationStatusAssessment: dict[str, Any]
    RequiredCaveats: tuple[str, ...]
    ProhibitedClaims: tuple[dict[str, Any], ...]
    SupportedClaims: tuple[dict[str, Any], ...]
    UnsupportedClaims: tuple[dict[str, Any], ...]
    ClaimsRequiringAdditionalEvidence: tuple[dict[str, Any], ...]
    AnswerOutline: tuple[dict[str, Any], ...]
    CitationRequirements: tuple[dict[str, Any], ...]
    BoundaryFlags: dict[str, bool]
    FinalAnswerPermitted: bool
    FinalAnswerProhibitionReason: str
    NextStep: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_multi_source_answer_preparation(
    query_text: str,
    retrieval_envelope: dict[str, Any] | None = None,
    answer_mode: str = GENERAL_CONTROLLED_PREPARATION,
    filters: dict[str, Any] | None = None,
    fixture_payloads: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return prepare_controlled_multi_source_answer(
        query_text=query_text,
        retrieval_envelope=retrieval_envelope,
        answer_mode=answer_mode,
        filters=filters,
        fixture_payloads=fixture_payloads,
    )


def prepare_controlled_multi_source_answer(
    query_text: str,
    retrieval_envelope: dict[str, Any] | None = None,
    answer_mode: str = GENERAL_CONTROLLED_PREPARATION,
    filters: dict[str, Any] | None = None,
    fixture_payloads: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Prepare source-aware answer material without generating a final answer."""

    query = str(query_text or "")
    retrieval = retrieval_envelope or build_controlled_multi_source_evidence_retrieval(
        query,
        filters=filters,
        fixture_payloads=fixture_payloads,
    )
    results = tuple(dict(result) for result in retrieval.get("Results", ()))
    intents = _query_intents(query)
    evidence_by_source = _evidence_by_source_type(results, retrieval)
    evidence_used = _evidence_used(results, intents)
    evidence_excluded = _evidence_excluded(results, retrieval, intents)
    supported_claims = _supported_claims(results, intents)
    prohibited_claims = _prohibited_claims(results, intents)
    unsupported_claims = _unsupported_claims(retrieval, intents, prohibited_claims)
    additional_evidence = _claims_requiring_additional_evidence(
        retrieval,
        intents,
        prohibited_claims,
    )
    caveats = _required_caveats(retrieval, results)

    return AnswerPreparationEnvelope(
        QueryText=query,
        AnswerMode=_normalize_answer_mode(answer_mode, intents),
        PreparationMode=ANSWER_PREPARATION_MODE,
        EvidenceUniverse=ANSWER_PREPARATION_UNIVERSE,
        PreparationStatus=_preparation_status(
            retrieval=retrieval,
            results=results,
            prohibited_claims=prohibited_claims,
            unsupported_claims=unsupported_claims,
            additional_evidence=additional_evidence,
            caveats=caveats,
        ),
        EvidenceUsed=evidence_used,
        EvidenceExcluded=evidence_excluded,
        EvidenceBySourceType=evidence_by_source,
        SourceAuthoritySummary=_source_authority_summary(),
        CurrentTruthAssessment=_current_truth_assessment(results, additional_evidence),
        ImplementationStatusAssessment=_implementation_status_assessment(results),
        RequiredCaveats=caveats,
        ProhibitedClaims=prohibited_claims,
        SupportedClaims=supported_claims,
        UnsupportedClaims=unsupported_claims,
        ClaimsRequiringAdditionalEvidence=additional_evidence,
        AnswerOutline=_answer_outline(
            supported_claims=supported_claims,
            unsupported_claims=unsupported_claims,
            prohibited_claims=prohibited_claims,
            additional_evidence=additional_evidence,
            caveats=caveats,
        ),
        CitationRequirements=_citation_requirements(),
        BoundaryFlags=dict(BOUNDARY_FLAGS),
        FinalAnswerPermitted=False,
        FinalAnswerProhibitionReason=FINAL_ANSWER_PROHIBITION,
        NextStep=NEXT_STEP,
    ).to_dict()


def _evidence_by_source_type(
    results: tuple[dict[str, Any], ...],
    retrieval: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    grouped = {
        PLATFORM_DOCTRINE_GROUP: _empty_group(PLATFORM_DOCTRINE),
        HARDENING_LOG_GROUP: _empty_group(HARDENING_LOG),
        DEVELOPER_LOG_GROUP: _empty_group(DEVELOPER_LOG),
        OUT_OF_SCOPE_GROUP: {
            "SourceType": OUT_OF_SCOPE_GROUP,
            "PermittedAnswerUse": (
                "Out-of-scope evidence cannot support claims in this slice. "
                "Onboard controlled fixtures in a later slice before use."
            ),
            "Evidence": tuple(
                {
                    "EvidenceType": evidence_type,
                    "ExcludedBecause": "Evidence type is outside the controlled multi-source fixture universe.",
                }
                for evidence_type in retrieval.get("UnsupportedEvidenceTypes", ())
            ),
        },
    }
    for source_type in (PLATFORM_DOCTRINE, HARDENING_LOG, DEVELOPER_LOG):
        group_name = SOURCE_GROUPS[source_type]
        grouped[group_name] = {
            **grouped[group_name],
            "Evidence": tuple(
                _evidence_reference(result)
                for result in results
                if result.get("EvidenceType") == source_type
            ),
        }
    return grouped


def _empty_group(source_type: str) -> dict[str, Any]:
    return {
        "SourceType": source_type,
        "PermittedAnswerUse": SOURCE_PERMITTED_USE[source_type],
        "CannotProve": SOURCE_CANNOT_PROVE[source_type],
        "Evidence": (),
    }


def _evidence_used(
    results: tuple[dict[str, Any], ...],
    intents: set[str],
) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            **_evidence_reference(result),
            "UsedFor": _used_for(result.get("EvidenceType"), intents),
            "PermittedAnswerUse": SOURCE_PERMITTED_USE.get(
                str(result.get("EvidenceType")),
                "No permitted answer use in this slice.",
            ),
        }
        for result in results
        if _used_for(result.get("EvidenceType"), intents)
    )


def _evidence_excluded(
    results: tuple[dict[str, Any], ...],
    retrieval: dict[str, Any],
    intents: set[str],
) -> tuple[dict[str, Any], ...]:
    exclusions: list[dict[str, Any]] = []
    for evidence_type in retrieval.get("UnsupportedEvidenceTypes", ()):
        exclusions.append(
            {
                "EvidenceType": evidence_type,
                "ExcludedBecause": "Evidence type is unsupported or out of scope for this local fixture slice.",
            }
        )

    for result in results:
        source_type = str(result.get("EvidenceType") or "")
        if "implementation" in intents and source_type in {PLATFORM_DOCTRINE, HARDENING_LOG}:
            exclusions.append(
                {
                    **_evidence_reference(result),
                    "ExcludedBecause": (
                        f"{source_type} cannot be used as completed-work or "
                        "implementation proof."
                    ),
                }
            )
        if "doctrine" in intents and source_type != PLATFORM_DOCTRINE:
            exclusions.append(
                {
                    **_evidence_reference(result),
                    "ExcludedBecause": (
                        f"{source_type} is not primary Platform Doctrine evidence."
                    ),
                }
            )

    exclusions.extend(
        (
            {
                "EvidenceType": PLATFORM_DOCTRINE,
                "ExcludedBecause": "Doctrine is not implementation, runtime, deployment, or production proof.",
            },
            {
                "EvidenceType": HARDENING_LOG,
                "ExcludedBecause": "Hardening and prohibition evidence is not completed-work proof.",
            },
            {
                "EvidenceType": DEVELOPER_LOG,
                "ExcludedBecause": "Developer Log evidence is not production-deployment proof without deployment evidence.",
            },
        )
    )
    return tuple(_dedupe_dicts(exclusions))


def _supported_claims(
    results: tuple[dict[str, Any], ...],
    intents: set[str],
) -> tuple[dict[str, Any], ...]:
    claims: list[dict[str, Any]] = []
    by_type = _results_by_type(results)

    if "implementation" in intents and by_type.get(DEVELOPER_LOG):
        claims.append(
            _claim(
                text=(
                    "Minerva has controlled multi-source retrieval and a "
                    "Developer Log durable evidence path at controlled-readiness level."
                ),
                status=SUPPORTED_WITH_CAVEAT,
                claim_type="WORK_COMPLETED_OR_IMPLEMENTATION_STATUS",
                evidence=by_type[DEVELOPER_LOG],
                caveats=(
                    "Developer Log evidence does not prove runtime implementation, deployment, or production readiness.",
                ),
            )
        )

    if "doctrine" in intents and by_type.get(PLATFORM_DOCTRINE):
        claims.append(
            _claim(
                text="Minerva must preserve source/status and answer-use boundaries.",
                status=SUPPORTED_WITH_CAVEAT,
                claim_type="DOCTRINE",
                evidence=by_type[PLATFORM_DOCTRINE],
                caveats=("Platform Doctrine is governance context, not execution proof.",),
            )
        )

    if "prohibition" in intents:
        evidence = (*by_type.get(HARDENING_LOG, ()), *by_type.get(PLATFORM_DOCTRINE, ()))
        if evidence:
            claims.append(
                _claim(
                    text=(
                        "Live LLM calls, final answer generation, chat exposure, "
                        "DB access, live corpus mutation, Code Evidence ingestion, "
                        "runtime integration, and production-readiness claims remain prohibited."
                    ),
                    status=SUPPORTED_WITH_CAVEAT,
                    claim_type="PROHIBITION_OR_HARDENING_BOUNDARY",
                    evidence=evidence,
                    caveats=(
                        "Hardening and doctrine evidence establish boundaries but do not prove implementation completed.",
                    ),
                )
            )

    if not claims and results:
        claims.append(
            _claim(
                text="Retrieved controlled evidence can be reviewed with source/status boundaries preserved.",
                status=SUPPORTED_WITH_CAVEAT,
                claim_type="GENERAL_CONTROLLED_PREPARATION",
                evidence=results,
                caveats=(
                    "This is preparation only and cannot be converted into a final answer in this slice.",
                ),
            )
        )

    return tuple(claims)


def _prohibited_claims(
    results: tuple[dict[str, Any], ...],
    intents: set[str],
) -> tuple[dict[str, Any], ...]:
    if "prohibited_overclaim" not in intents:
        return ()

    by_type = _results_by_type(results)
    boundary_evidence = (
        *by_type.get(HARDENING_LOG, ()),
        *by_type.get(PLATFORM_DOCTRINE, ()),
        *by_type.get(DEVELOPER_LOG, ()),
    )
    return (
        _claim(
            text="Minerva chat is live.",
            status=PROHIBITED,
            claim_type="CHAT_EXPOSURE_OVERCLAIM",
            evidence=boundary_evidence,
            caveats=("Chat exposure is explicitly not enabled by this slice.",),
        ),
        _claim(
            text="Minerva is production-ready.",
            status=PROHIBITED,
            claim_type="PRODUCTION_READINESS_OVERCLAIM",
            evidence=boundary_evidence,
            caveats=("Production readiness requires deployment and production evidence that is absent.",),
        ),
    )


def _unsupported_claims(
    retrieval: dict[str, Any],
    intents: set[str],
    prohibited_claims: tuple[dict[str, Any], ...],
) -> tuple[dict[str, Any], ...]:
    claims: list[dict[str, Any]] = []
    if "live_db_state" in intents:
        claims.append(
            {
                "ClaimText": "Current live DB state can be answered from this preparation packet.",
                "ClaimStatus": UNSUPPORTED,
                "ClaimType": "CURRENT_LIVE_DB_STATE",
                "EvidenceReferences": (),
                "Reason": "This slice performs no DB read and has no DB evidence.",
            }
        )
    if prohibited_claims:
        claims.append(
            {
                "ClaimText": "Runtime, chat, deployment, or production readiness can be claimed now.",
                "ClaimStatus": UNSUPPORTED,
                "ClaimType": "LIVE_OR_PRODUCTION_OVERCLAIM",
                "EvidenceReferences": tuple(
                    _evidence_reference(result)
                    for result in retrieval.get("Results", ())
                ),
                "Reason": "Controlled fixture evidence cannot prove live runtime or production status.",
            }
        )
    return tuple(claims)


def _claims_requiring_additional_evidence(
    retrieval: dict[str, Any],
    intents: set[str],
    prohibited_claims: tuple[dict[str, Any], ...],
) -> tuple[dict[str, Any], ...]:
    required: list[dict[str, Any]] = []
    unsupported_types = set(retrieval.get("UnsupportedEvidenceTypes", ()))
    if "live_db_state" in intents or "LIVE_DB" in unsupported_types:
        required.append(
            {
                "ClaimText": "Current live DB state.",
                "ClaimStatus": REQUIRES_DB_EVIDENCE,
                "RequiredEvidence": "Explicit authorised DB evidence from a later slice.",
                "MissingBecause": "DatabaseReadPerformed remains false and LIVE_DB is out of scope.",
            }
        )
    if prohibited_claims:
        required.extend(
            (
                {
                    "ClaimText": "Current live runtime readiness.",
                    "ClaimStatus": REQUIRES_CURRENT_RUNTIME_EVIDENCE,
                    "RequiredEvidence": "Authorised runtime integration evidence.",
                    "MissingBecause": "RuntimeIntegrationPerformed remains false.",
                },
                {
                    "ClaimText": "Production readiness.",
                    "ClaimStatus": REQUIRES_DEPLOYMENT_EVIDENCE,
                    "RequiredEvidence": "Deployment and production-readiness evidence.",
                    "MissingBecause": "ProductionReadinessClaimed remains false and no deployment evidence exists.",
                },
            )
        )
    if "code_evidence" in intents or "CODE_EVIDENCE" in unsupported_types:
        required.append(
            {
                "ClaimText": "Code-level implementation truth.",
                "ClaimStatus": REQUIRES_CODE_EVIDENCE,
                "RequiredEvidence": "Authorised Code Evidence ingestion from a later slice.",
                "MissingBecause": "CodeEvidenceIngestionPerformed remains false.",
            }
        )
    return tuple(_dedupe_dicts(required))


def _source_authority_summary() -> tuple[dict[str, Any], ...]:
    return (
        {
            "SourceType": PLATFORM_DOCTRINE,
            "AuthorityAppliesTo": "Doctrine, rules, principles, source/status boundaries.",
            "CannotEstablish": "Implementation, runtime execution, deployment, production readiness.",
        },
        {
            "SourceType": HARDENING_LOG,
            "AuthorityAppliesTo": "Risks, prohibitions, deferred work, required boundaries.",
            "CannotEstablish": "Completed implementation, repaired runtime behaviour, deployment.",
        },
        {
            "SourceType": DEVELOPER_LOG,
            "AuthorityAppliesTo": "Work completed, tests run, implementation status, decisions captured.",
            "CannotEstablish": "Production deployment or current live runtime truth without additional evidence.",
        },
        {
            "SourceType": "THREAD_CONTINUANCE_PROMPT",
            "AuthorityAppliesTo": "Planning and continuity evidence only if onboarded later.",
            "CannotEstablish": "Completed work or runtime truth.",
        },
    )


def _current_truth_assessment(
    results: tuple[dict[str, Any], ...],
    additional_evidence: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    return {
        "HistoricalEvidenceIsCurrentTruth": False,
        "ControlledReadinessIsRuntimeReadiness": False,
        "RuntimeReadinessIsProductionReadiness": False,
        "CurrentTruthEvidencePresent": False,
        "ObservedCurrentTruthStatuses": tuple(
            dict.fromkeys(
                str(result.get("CurrentTruthStatus") or "")
                for result in results
                if result.get("CurrentTruthStatus")
            )
        ),
        "MissingEvidence": additional_evidence,
    }


def _implementation_status_assessment(
    results: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    return {
        "DoctrineProvesImplementation": False,
        "HardeningProvesCompletedRuntimeBehaviour": False,
        "DeveloperLogProvesProductionDeployment": False,
        "ObservedImplementationStatuses": tuple(
            dict.fromkeys(
                str(result.get("ImplementationStatus") or "")
                for result in results
                if result.get("ImplementationStatus")
            )
        ),
        "Assessment": (
            "Implementation/work-completed claims require Developer Log or code evidence. "
            "Runtime, DB, deployment, and production claims require additional evidence."
        ),
    }


def _answer_outline(
    supported_claims: tuple[dict[str, Any], ...],
    unsupported_claims: tuple[dict[str, Any], ...],
    prohibited_claims: tuple[dict[str, Any], ...],
    additional_evidence: tuple[dict[str, Any], ...],
    caveats: tuple[str, ...],
) -> tuple[dict[str, Any], ...]:
    return (
        {
            "Section": "What the evidence supports",
            "PreparationNotes": tuple(claim["ClaimText"] for claim in supported_claims),
        },
        {
            "Section": "What the evidence does not prove",
            "PreparationNotes": tuple(claim["ClaimText"] for claim in unsupported_claims),
        },
        {
            "Section": "Current implementation/status",
            "PreparationNotes": (
                "Report only controlled-readiness or fixture-backed implementation status.",
                "Do not claim runtime, DB, deployment, or production status.",
            ),
        },
        {
            "Section": "Required caveats",
            "PreparationNotes": caveats,
        },
        {
            "Section": "Prohibited claims",
            "PreparationNotes": tuple(claim["ClaimText"] for claim in prohibited_claims),
        },
        {
            "Section": "Next safe step",
            "PreparationNotes": (
                "Attach claim-level provenance in a later controlled citation/provenance slice.",
                *tuple(item["ClaimText"] for item in additional_evidence),
            ),
        },
    )


def _citation_requirements() -> tuple[dict[str, Any], ...]:
    return (
        {
            "ClaimType": "DOCTRINE",
            "RequiredSourceType": PLATFORM_DOCTRINE,
            "Rule": "Doctrine claims require Platform Doctrine evidence reference.",
        },
        {
            "ClaimType": "PROHIBITION_OR_HARDENING_BOUNDARY",
            "RequiredSourceType": (HARDENING_LOG, PLATFORM_DOCTRINE),
            "Rule": "Risk or prohibition claims require Hardening Log or Platform Doctrine evidence reference.",
        },
        {
            "ClaimType": "WORK_COMPLETED_OR_IMPLEMENTATION_STATUS",
            "RequiredSourceType": DEVELOPER_LOG,
            "Rule": "Implementation, tests-run, and work-completed claims require Developer Log evidence reference.",
        },
        {
            "ClaimType": "RUNTIME_DB_DEPLOYMENT_OR_PRODUCTION",
            "RequiredSourceType": ("LIVE_DB", "RUNTIME_EVIDENCE", "DEPLOYMENT_EVIDENCE"),
            "Rule": "Runtime, DB, deployment, and production claims require evidence outside this slice.",
        },
    )


def _preparation_status(
    *,
    retrieval: dict[str, Any],
    results: tuple[dict[str, Any], ...],
    prohibited_claims: tuple[dict[str, Any], ...],
    unsupported_claims: tuple[dict[str, Any], ...],
    additional_evidence: tuple[dict[str, Any], ...],
    caveats: tuple[str, ...],
) -> str:
    if prohibited_claims:
        return BLOCKED_PROHIBITED_CLAIM
    if unsupported_claims and not results:
        unsupported_types = set(retrieval.get("UnsupportedEvidenceTypes", ()))
        if unsupported_types:
            return INSUFFICIENT_EVIDENCE
        return OUT_OF_SCOPE
    if not results:
        return INSUFFICIENT_EVIDENCE
    if additional_evidence or caveats:
        return PREPARED_WITH_CAVEATS
    return PREPARED


def _required_caveats(
    retrieval: dict[str, Any],
    results: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    caveats: list[str] = [
        "This is answer preparation only, not final answer generation.",
        "Future final answers must cite/provenance each claim.",
        "Historical evidence is not current truth by default.",
        "Controlled-readiness is not runtime readiness.",
        "Runtime readiness is not production readiness.",
        "Doctrine does not prove implementation.",
        "Hardening does not prove completed runtime behaviour.",
        "Developer Log does not prove production deployment without deployment evidence.",
    ]
    caveats.extend(str(item) for item in retrieval.get("Caveats", ()) if str(item))
    for result in results:
        caveats.extend(
            str(item)
            for item in result.get("RequiredCaveats", ())
            if str(item)
        )
    return tuple(dict.fromkeys(caveats))


def _query_intents(query: str) -> set[str]:
    normalized = query.lower().replace("-", " ")
    terms = set(re.findall(r"[a-z0-9]+", normalized))
    intents: set[str] = set()

    if terms & {"doctrine", "boundary", "boundaries", "source", "status", "principle", "rules"}:
        intents.add("doctrine")
    if terms & {"developer", "durable", "complete", "completed", "work", "retrieval", "implementation"}:
        intents.add("implementation")
    if terms & {"prohibited", "prohibit", "remain", "remaining", "hardening", "risk", "llm", "chat", "corpus", "mutation"}:
        intents.add("prohibition")
    if {"db", "database"} & terms:
        intents.add("live_db_state")
    if "code" in terms:
        intents.add("code_evidence")
    if (
        ("chat" in terms and "live" in terms)
        or "production" in terms
        or "productionready" in normalized.replace(" ", "")
        or "production-ready" in query.lower()
    ) and ({"say", "claim", "state"} & terms or "ready" in terms or "live" in terms):
        intents.add("prohibited_overclaim")
    if not intents:
        intents.add("general")
    return intents


def _normalize_answer_mode(answer_mode: str, intents: set[str]) -> str:
    requested = str(answer_mode or "").strip().upper()
    valid = {
        GENERAL_CONTROLLED_PREPARATION,
        STATUS_EXPLANATION,
        DOCTRINE_EXPLANATION,
        WORK_COMPLETED_EXPLANATION,
        PROHIBITION_EXPLANATION,
    }
    if requested in valid:
        return requested
    if "doctrine" in intents:
        return DOCTRINE_EXPLANATION
    if "implementation" in intents:
        return WORK_COMPLETED_EXPLANATION
    if "prohibition" in intents or "prohibited_overclaim" in intents:
        return PROHIBITION_EXPLANATION
    return GENERAL_CONTROLLED_PREPARATION


def _used_for(source_type: Any, intents: set[str]) -> tuple[str, ...]:
    source = str(source_type or "")
    uses: list[str] = []
    if source == PLATFORM_DOCTRINE and "doctrine" in intents:
        uses.append("DOCTRINE")
    if source == HARDENING_LOG and ("prohibition" in intents or "prohibited_overclaim" in intents):
        uses.append("PROHIBITION_OR_HARDENING_BOUNDARY")
    if source == PLATFORM_DOCTRINE and ("prohibition" in intents or "prohibited_overclaim" in intents):
        uses.append("PROHIBITION_OR_PLATFORM_BOUNDARY")
    if source == DEVELOPER_LOG and "implementation" in intents:
        uses.append("WORK_COMPLETED_OR_IMPLEMENTATION_STATUS")
    if not uses and source in SOURCE_GROUPS and "general" in intents:
        uses.append("GENERAL_CONTROLLED_PREPARATION")
    return tuple(uses)


def _claim(
    *,
    text: str,
    status: str,
    claim_type: str,
    evidence: tuple[dict[str, Any], ...],
    caveats: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "ClaimText": text,
        "ClaimStatus": status,
        "ClaimType": claim_type,
        "EvidenceReferences": tuple(_evidence_reference(result) for result in evidence),
        "RequiredCaveats": caveats,
    }


def _evidence_reference(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "RecordId": str(result.get("RecordId") or ""),
        "EvidenceType": str(result.get("EvidenceType") or result.get("SourceType") or ""),
        "SourceType": str(result.get("SourceType") or result.get("EvidenceType") or ""),
        "SourceTitle": str(result.get("SourceTitle") or ""),
        "AuthorityLevel": str(result.get("AuthorityLevel") or ""),
        "SourceStatus": str(result.get("SourceStatus") or ""),
        "ImplementationStatus": str(result.get("ImplementationStatus") or ""),
        "CurrentTruthStatus": str(result.get("CurrentTruthStatus") or ""),
        "AnswerUseStatus": str(result.get("AnswerUseStatus") or ""),
    }


def _results_by_type(results: tuple[dict[str, Any], ...]) -> dict[str, tuple[dict[str, Any], ...]]:
    return {
        source_type: tuple(
            result for result in results if result.get("EvidenceType") == source_type
        )
        for source_type in (PLATFORM_DOCTRINE, HARDENING_LOG, DEVELOPER_LOG)
    }


def _dedupe_dicts(items: Iterable[dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        key = tuple(sorted((str(k), str(v)) for k, v in item.items()))
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return tuple(unique)
