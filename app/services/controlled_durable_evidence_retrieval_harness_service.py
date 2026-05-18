import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from app.services.controlled_evidence_intake_dry_run_service import (
    build_controlled_evidence_intake_dry_run,
)
from app.services.evidence_source_status_boundary_service import (
    build_evidence_source_status_boundary,
)


RETRIEVAL_MODE = "DETERMINISTIC_KEYWORD_METADATA_FIXTURE_RETRIEVAL_V0_1"
FIXTURE_UNIVERSE = "CONTROLLED_DURABLE_DEVELOPER_LOG_FIXTURES_V0_1"
DEVELOPER_LOG = "DEVELOPER_LOG"
EVIDENCE_TYPES_IN_SCOPE = (DEVELOPER_LOG,)
EVIDENCE_TYPES_OUT_OF_SCOPE = (
    "HARDENING_LOG",
    "PLATFORM_DOCTRINE",
    "THREAD_CONTINUANCE_PROMPT",
    "CODE_EVIDENCE",
    "LIVE_CORPUS",
)
UNSUPPORTED_EVIDENCE_TYPE_NOTE = (
    "This v0.1 harness searches only existing controlled durable Developer Log "
    "fixtures. Hardening Log and Platform Doctrine evidence onboarding is a "
    "future slice and no result is invented."
)
NEXT_SAFE_STEP = (
    "Review the retrieval envelope and decide a later controlled-answer "
    "preparation slice; do not generate a final answer from this harness."
)

BOUNDARY_FLAGS = {
    "LiveLLMCalled": False,
    "FinalAnswerGenerated": False,
    "ChatExposureEnabled": False,
    "DatabaseReadPerformed": False,
    "DatabaseWritePerformed": False,
    "LiveCorpusMutationPerformed": False,
    "CodeEvidenceIngestionPerformed": False,
    "RetrievalBackendChanged": False,
    "RuntimeIntegrationPerformed": False,
    "ProductionReadinessClaimed": False,
}

STOP_TERMS = {
    "a",
    "an",
    "and",
    "are",
    "does",
    "did",
    "for",
    "from",
    "is",
    "it",
    "of",
    "says",
    "the",
    "to",
    "what",
    "whether",
}

TERM_ALIASES = {
    "called": "call",
    "calls": "call",
    "generated": "generation",
    "prohibited": "prohibit",
    "prohibits": "prohibit",
    "remaining": "remain",
    "remains": "remain",
}

DEFAULT_FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "tests"
    / "fixtures"
    / "controlled_evidence_intake"
    / "developer_log_evidence.json"
)


@dataclass(frozen=True)
class ControlledDurableEvidenceRetrievalResult:
    RecordId: str
    SourceType: str
    SourceTitle: str
    SourceStatus: str
    ImplementationStatus: str
    AnswerUseStatus: str
    MatchedTerms: tuple[str, ...]
    MatchReasons: tuple[str, ...]
    Rank: int
    Score: int
    CanProve: tuple[str, ...]
    CannotProve: tuple[str, ...]
    CaveatRequired: bool
    FinalAnswerPermitted: bool
    BoundaryFlags: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ControlledDurableEvidenceRetrievalEnvelope:
    QueryText: str
    NormalizedQueryTerms: tuple[str, ...]
    RetrievalMode: str
    FixtureUniverse: str
    EvidenceTypesInScope: tuple[str, ...]
    EvidenceTypesOutOfScope: tuple[str, ...]
    ResultCount: int
    Results: tuple[dict[str, Any], ...]
    BoundaryFlags: dict[str, bool]
    NextStep: str
    Caveats: tuple[str, ...]
    UnsupportedEvidenceTypes: tuple[str, ...]
    FinalAnswerPermitted: bool
    RetrievalStoryOnly: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def retrieve_controlled_durable_evidence(
    query_text: str,
    filters: dict[str, Any] | None = None,
    fixture_payloads: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Retrieve controlled Developer Log fixture evidence without runtime action."""

    query = str(query_text or "")
    terms = _normalize_terms(query)
    filters = filters or {}
    unsupported = _unsupported_evidence_types(query, filters)

    if unsupported and not _developer_log_requested(query, filters):
        return _envelope(
            query=query,
            terms=terms,
            results=(),
            caveats=(
                UNSUPPORTED_EVIDENCE_TYPE_NOTE,
                "No controlled Developer Log fixture was requested strongly enough to search.",
            ),
            unsupported=unsupported,
        )

    fixture_records = _fixture_records(fixture_payloads)
    candidate_records = tuple(
        record
        for record in fixture_records
        if _record_evidence_type(record) == DEVELOPER_LOG
    )
    if filters.get("evidence_type") and _normalize_evidence_type(filters["evidence_type"]) != DEVELOPER_LOG:
        candidate_records = ()

    scored = tuple(
        scored_record
        for record in candidate_records
        if (scored_record := _score_record(record, terms)) is not None
    )
    ordered = sorted(
        scored,
        key=lambda item: (
            -item["score"],
            -len(item["matched_terms"]),
            item["source_type"].lower(),
            item["source_title"].lower(),
            item["record_id"].lower(),
        ),
    )
    results = tuple(_result(item, rank=index + 1) for index, item in enumerate(ordered))
    caveats = (
        "Retrieval is deterministic keyword/metadata matching over local fixtures only.",
        "Developer Log evidence is controlled planning evidence and does not prove runtime, deployment, or production truth.",
        "Final answer generation is not performed or permitted by this harness.",
    )
    if unsupported:
        caveats = (*caveats, UNSUPPORTED_EVIDENCE_TYPE_NOTE)

    return _envelope(
        query=query,
        terms=terms,
        results=results,
        caveats=caveats,
        unsupported=unsupported,
    )


def build_controlled_durable_evidence_retrieval_harness(
    query_text: str,
    filters: dict[str, Any] | None = None,
    fixture_payloads: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return retrieve_controlled_durable_evidence(query_text, filters, fixture_payloads)


def _envelope(
    *,
    query: str,
    terms: tuple[str, ...],
    results: tuple[dict[str, Any], ...],
    caveats: tuple[str, ...],
    unsupported: tuple[str, ...],
) -> dict[str, Any]:
    return ControlledDurableEvidenceRetrievalEnvelope(
        QueryText=query,
        NormalizedQueryTerms=terms,
        RetrievalMode=RETRIEVAL_MODE,
        FixtureUniverse=FIXTURE_UNIVERSE,
        EvidenceTypesInScope=EVIDENCE_TYPES_IN_SCOPE,
        EvidenceTypesOutOfScope=EVIDENCE_TYPES_OUT_OF_SCOPE,
        ResultCount=len(results),
        Results=results,
        BoundaryFlags=dict(BOUNDARY_FLAGS),
        NextStep=NEXT_SAFE_STEP,
        Caveats=caveats,
        UnsupportedEvidenceTypes=unsupported,
        FinalAnswerPermitted=False,
        RetrievalStoryOnly=True,
    ).to_dict()


def _fixture_records(fixture_payloads: Iterable[dict[str, Any]] | None) -> tuple[dict[str, Any], ...]:
    if fixture_payloads is not None:
        payloads = tuple(dict(payload) for payload in fixture_payloads)
    else:
        payloads = (json.loads(DEFAULT_FIXTURE_PATH.read_text(encoding="utf-8")),)
    return tuple(sorted(payloads, key=lambda record: str(record.get("fixture_id", ""))))


def _score_record(record: dict[str, Any], terms: tuple[str, ...]) -> dict[str, Any] | None:
    search_fields = _search_fields(record)
    searchable = " ".join(search_fields.values()).lower()
    matched_terms = tuple(term for term in terms if term in searchable)
    if not matched_terms:
        return None

    reasons = tuple(
        f"{term} matched {field_name}"
        for term in matched_terms
        for field_name, field_value in search_fields.items()
        if term in field_value.lower()
    )
    return {
        "record": record,
        "record_id": str(record.get("fixture_id") or _metadata(record).get("evidence_id") or ""),
        "source_type": _source_type(record),
        "source_title": _source_title(record),
        "source_status": _source_status(record),
        "implementation_status": _implementation_status(record),
        "answer_use_status": _answer_use_status(record),
        "matched_terms": matched_terms,
        "match_reasons": tuple(dict.fromkeys(reasons)),
        "score": _score(matched_terms, reasons),
    }


def _result(scored: dict[str, Any], rank: int) -> dict[str, Any]:
    return ControlledDurableEvidenceRetrievalResult(
        RecordId=scored["record_id"],
        SourceType=scored["source_type"],
        SourceTitle=scored["source_title"],
        SourceStatus=scored["source_status"],
        ImplementationStatus=scored["implementation_status"],
        AnswerUseStatus=scored["answer_use_status"],
        MatchedTerms=scored["matched_terms"],
        MatchReasons=scored["match_reasons"],
        Rank=rank,
        Score=scored["score"],
        CanProve=_can_prove(scored["record"]),
        CannotProve=_cannot_prove(scored["record"]),
        CaveatRequired=True,
        FinalAnswerPermitted=False,
        BoundaryFlags=dict(BOUNDARY_FLAGS),
    ).to_dict()


def _search_fields(record: dict[str, Any]) -> dict[str, str]:
    metadata = _metadata(record)
    dry_run = build_controlled_evidence_intake_dry_run(record)
    boundary = build_evidence_source_status_boundary(metadata)
    searchable = {
        "fixture_id": str(record.get("fixture_id") or ""),
        "fixture_purpose": str(record.get("fixture_purpose") or ""),
        "evidence_category": str(metadata.get("evidence_category") or ""),
        "source_type": str(metadata.get("source_type") or ""),
        "source_title": str(metadata.get("title") or ""),
        "source_status": str(dry_run.get("source_status") or metadata.get("source_status") or ""),
        "dry_run_decision": str(dry_run.get("dry_run_decision") or ""),
        "gate_decision": str(dry_run.get("gate_decision") or ""),
        "required_caveats": " ".join(str(item) for item in dry_run.get("required_caveats", ())),
        "prohibited_inferences": " ".join(
            str(item) for item in dry_run.get("prohibited_inferences", ())
        ),
        "no_action_attestation": str(dry_run.get("no_action_attestation") or ""),
        "boundary_explanation": str(boundary.get("explanation") or ""),
        "can_prove": " ".join(_can_prove(record)),
        "cannot_prove": " ".join(_cannot_prove(record)),
    }
    return searchable


def _metadata(record: dict[str, Any]) -> dict[str, Any]:
    if isinstance(record.get("input_metadata"), dict):
        return dict(record["input_metadata"])
    return dict(record)


def _record_evidence_type(record: dict[str, Any]) -> str:
    return _normalize_evidence_type(_metadata(record).get("evidence_category"))


def _source_type(record: dict[str, Any]) -> str:
    metadata = _metadata(record)
    return str(metadata.get("source_type") or metadata.get("evidence_category") or "")


def _source_title(record: dict[str, Any]) -> str:
    metadata = _metadata(record)
    return str(metadata.get("title") or metadata.get("source_label") or record.get("fixture_id") or "")


def _source_status(record: dict[str, Any]) -> str:
    dry_run = build_controlled_evidence_intake_dry_run(record)
    metadata = _metadata(record)
    return str(dry_run.get("source_status") or metadata.get("source_status") or "")


def _implementation_status(record: dict[str, Any]) -> str:
    boundary = build_evidence_source_status_boundary(_metadata(record))
    if boundary.get("implementation_claim_permitted") is True:
        return "IMPLEMENTATION_CLAIM_PERMITTED_BY_EXPLICIT_PROOF"
    return "IMPLEMENTATION_NOT_PROVEN_BY_THIS_FIXTURE"


def _answer_use_status(record: dict[str, Any]) -> str:
    metadata = _metadata(record)
    return str(
        metadata.get("answer_use_status")
        or metadata.get("AnswerUseStatus")
        or "FINAL_ANSWER_NOT_PERMITTED_RETRIEVAL_ONLY"
    )


def _can_prove(record: dict[str, Any]) -> tuple[str, ...]:
    metadata = _metadata(record)
    title = str(metadata.get("title") or "Developer Log fixture")
    return (
        f"{title} exists as a controlled local Developer Log fixture.",
        f"The source/status boundary is {_source_status(record)}.",
        "The fixture preserves no-action boundaries for controlled planning use.",
        "The retrieval harness can return matched fixture metadata and caveats.",
    )


def _cannot_prove(record: dict[str, Any]) -> tuple[str, ...]:
    return (
        "final user-facing answer correctness",
        "runtime readiness",
        "deployment readiness",
        "production readiness",
        "live LLM execution",
        "chat exposure",
        "database-backed retrieval",
        "corpus mutation or durable ingestion performed now",
        "Code Evidence ingestion",
    )


def _score(matched_terms: tuple[str, ...], reasons: tuple[str, ...]) -> int:
    return len(matched_terms) * 10 + len(tuple(dict.fromkeys(reasons)))


def _normalize_terms(query: str) -> tuple[str, ...]:
    raw_terms = re.findall(r"[a-z0-9]+", query.lower().replace("-", " "))
    terms = [
        TERM_ALIASES.get(term, term)
        for term in raw_terms
        if len(term) > 1 and term not in STOP_TERMS
    ]
    return tuple(dict.fromkeys(terms))


def _normalize_evidence_type(value: Any) -> str:
    return str(value or "").strip().upper().replace("-", "_").replace(" ", "_")


def _unsupported_evidence_types(query: str, filters: dict[str, Any]) -> tuple[str, ...]:
    terms = set(_normalize_terms(query))
    requested = set()
    filter_type = filters.get("evidence_type")
    if filter_type:
        requested.add(_normalize_evidence_type(filter_type))
    if {"hardening", "log"} <= terms or "hardening" in terms:
        requested.add("HARDENING_LOG")
    if {"platform", "doctrine"} <= terms or "doctrine" in terms:
        requested.add("PLATFORM_DOCTRINE")
    return tuple(sorted(item for item in requested if item in EVIDENCE_TYPES_OUT_OF_SCOPE))


def _developer_log_requested(query: str, filters: dict[str, Any]) -> bool:
    terms = set(_normalize_terms(query))
    filter_type = filters.get("evidence_type")
    if filter_type and _normalize_evidence_type(filter_type) == DEVELOPER_LOG:
        return True
    return "developer" in terms or "dev" in terms or "minerva" in terms
