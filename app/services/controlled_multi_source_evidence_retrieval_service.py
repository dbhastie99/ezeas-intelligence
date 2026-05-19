import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from app.services.controlled_durable_evidence_retrieval_harness_service import (
    BOUNDARY_FLAGS,
)
from app.services.controlled_evidence_intake_dry_run_service import (
    build_controlled_evidence_intake_dry_run,
)
from app.services.evidence_source_status_boundary_service import (
    build_evidence_source_status_boundary,
)


RETRIEVAL_MODE = "DETERMINISTIC_MULTI_SOURCE_KEYWORD_METADATA_FIXTURE_RETRIEVAL_V0_1"
EVIDENCE_UNIVERSE = "CONTROLLED_MULTI_SOURCE_LOCAL_FIXTURES_V0_1"

PLATFORM_DOCTRINE = "PLATFORM_DOCTRINE"
HARDENING_LOG = "HARDENING_LOG"
DEVELOPER_LOG = "DEVELOPER_LOG"
THREAD_CONTINUANCE_PROMPT = "THREAD_CONTINUANCE_PROMPT"

EVIDENCE_TYPES_SEARCHED = (
    PLATFORM_DOCTRINE,
    HARDENING_LOG,
    DEVELOPER_LOG,
)
EVIDENCE_TYPES_OUT_OF_SCOPE = (
    THREAD_CONTINUANCE_PROMPT,
    "CODE_EVIDENCE",
    "LIVE_DB",
    "LIVE_CORPUS",
    "ANALYTICS_READINESS_SUMMARY",
    "GENERAL_HISTORICAL_NOTE",
)

AUTHORITY_ORDER = {
    PLATFORM_DOCTRINE: 1,
    HARDENING_LOG: 2,
    DEVELOPER_LOG: 3,
    THREAD_CONTINUANCE_PROMPT: 4,
    "GENERAL_HISTORICAL_NOTE": 5,
}
AUTHORITY_LEVELS = {
    PLATFORM_DOCTRINE: "AUTHORITY_1_PLATFORM_DOCTRINE",
    HARDENING_LOG: "AUTHORITY_2_HARDENING_LOG",
    DEVELOPER_LOG: "AUTHORITY_3_DEVELOPER_LOG",
    THREAD_CONTINUANCE_PROMPT: "AUTHORITY_4_THREAD_CONTINUANCE_PROMPT",
    "GENERAL_HISTORICAL_NOTE": "AUTHORITY_5_GENERAL_HISTORICAL_NOTE",
}

AUTHORITY_POLICY_APPLIED = (
    "CONTROLLED_SOURCE_AUTHORITY_POLICY_V0_1: ranking combines deterministic "
    "query-term matches, simple query intent, source authority, source/status "
    "boundaries, and answer-use safety. Source authority is not treated as the "
    "same thing as query relevance."
)
NEXT_SAFE_STEP = (
    "Review the structured retrieval envelope; a later controlled-answer "
    "preparation slice may consume it, but this service must not generate a "
    "final answer or expose chat."
)
UNSUPPORTED_EVIDENCE_TYPE_NOTE = (
    "The requested source type is outside this controlled multi-source fixture "
    "universe. No evidence is fabricated; onboard that evidence type in a later "
    "controlled fixture slice before retrieval."
)

FIXTURE_DIR = (
    Path(__file__).resolve().parents[2]
    / "tests"
    / "fixtures"
    / "controlled_evidence_intake"
)
DEFAULT_FIXTURE_PATHS = (
    FIXTURE_DIR / "platform_doctrine_evidence.json",
    FIXTURE_DIR / "hardening_log_evidence.json",
    FIXTURE_DIR / "developer_log_evidence.json",
)

STOP_TERMS = {
    "a",
    "about",
    "after",
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
    "on",
    "say",
    "says",
    "the",
    "to",
    "what",
    "whether",
}

TERM_ALIASES = {
    "called": "call",
    "calls": "call",
    "completed": "complete",
    "generated": "generation",
    "paths": "path",
    "prohibited": "prohibit",
    "prohibits": "prohibit",
    "remaining": "remain",
    "remains": "remain",
    "sources": "source",
}

INTENT_TERMS = {
    PLATFORM_DOCTRINE: {
        "doctrine",
        "platform",
        "governance",
        "runtime",
        "boundary",
        "prompt",
        "knowledge",
        "slice",
        "truth",
    },
    HARDENING_LOG: {
        "hardening",
        "prohibit",
        "remain",
        "risk",
        "llm",
        "final",
        "answer",
        "chat",
        "db",
        "database",
        "corpus",
        "mutation",
        "ingestion",
        "evidence",
        "path",
    },
    DEVELOPER_LOG: {
        "developer",
        "dev",
        "durable",
        "complete",
        "completed",
        "work",
        "controlled",
        "readiness",
        "retrieval",
        "path",
    },
}

CONTROLLED_CLAIMS = {
    PLATFORM_DOCTRINE: (
        "No live Minerva runtime is authorised until explicitly approved.",
        "Source and status boundaries must be preserved in retrieval output.",
        "A prompt is not durable knowledge; slice knowledge records preserve durable context.",
        "Platform Doctrine is governance context, not execution proof.",
    ),
    HARDENING_LOG: (
        "Remaining prohibited actions include live LLM calls, final answer generation, chat exposure, DB reads or writes, live corpus mutation, and Code Evidence ingestion.",
        "Do not add live evidence paths before deterministic retrieval behaviour is proven.",
        "Hardening prohibition evidence is not implementation proof.",
    ),
    DEVELOPER_LOG: (
        "Developer Log durable evidence path completed at controlled-readiness level.",
        "Retrieval readiness and controlled answer preparation path were proven over Developer Log fixtures.",
        "Developer Log evidence does not prove runtime implementation, deployment, production readiness, live LLM use, DB access, chat exposure, or live corpus mutation.",
    ),
}

CURRENT_TRUTH_STATUS = {
    PLATFORM_DOCTRINE: "CURRENT_DOCTRINE_CONTEXT_NOT_EXECUTION_PROOF",
    HARDENING_LOG: "CURRENT_HARDENING_BOUNDARY_NOT_IMPLEMENTATION_PROOF",
    DEVELOPER_LOG: "HISTORICAL_WORK_RECORD_NOT_CURRENT_RUNTIME_TRUTH",
}

ANSWER_USE_STATUS = "FINAL_ANSWER_NOT_PERMITTED_RETRIEVAL_ONLY"


@dataclass(frozen=True)
class ControlledMultiSourceEvidenceRetrievalResult:
    RecordId: str
    EvidenceType: str
    SourceType: str
    SourceTitle: str
    SourceStatus: str
    AuthorityLevel: str
    ImplementationStatus: str
    CurrentTruthStatus: str
    AnswerUseStatus: str
    MatchedTerms: tuple[str, ...]
    MatchReasons: tuple[str, ...]
    Rank: int
    Score: int
    CanProve: tuple[str, ...]
    CannotProve: tuple[str, ...]
    RequiredCaveats: tuple[str, ...]
    CaveatRequired: bool
    FinalAnswerPermitted: bool
    BoundaryFlags: dict[str, bool]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ControlledMultiSourceEvidenceRetrievalEnvelope:
    QueryText: str
    NormalizedQueryTerms: tuple[str, ...]
    RetrievalMode: str
    EvidenceUniverse: str
    EvidenceTypesSearched: tuple[str, ...]
    EvidenceTypesOutOfScope: tuple[str, ...]
    AuthorityPolicyApplied: str
    ResultCount: int
    Results: tuple[dict[str, Any], ...]
    BoundaryFlags: dict[str, bool]
    Caveats: tuple[str, ...]
    UnsupportedEvidenceTypes: tuple[str, ...]
    NextStep: str
    FinalAnswerPermitted: bool
    RetrievalStoryOnly: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def retrieve_controlled_multi_source_evidence(
    query_text: str,
    filters: dict[str, Any] | None = None,
    fixture_payloads: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Retrieve controlled local fixture evidence across approved source types."""

    query = str(query_text or "")
    filters = filters or {}
    terms = _normalize_terms(query)
    unsupported = _unsupported_evidence_types(query, filters)
    requested_supported = _requested_supported_types(query, filters)

    if unsupported and not requested_supported:
        return _envelope(
            query=query,
            terms=terms,
            results=(),
            unsupported=unsupported,
            caveats=(
                "Retrieval is deterministic keyword/metadata matching over controlled local fixtures only.",
                UNSUPPORTED_EVIDENCE_TYPE_NOTE,
            ),
        )

    records = tuple(
        record
        for record in _fixture_records(fixture_payloads)
        if _record_evidence_type(record) in EVIDENCE_TYPES_SEARCHED
    )
    if requested_supported:
        records = tuple(
            record
            for record in records
            if _record_evidence_type(record) in requested_supported
        )

    scored = tuple(
        scored_record
        for record in records
        if (scored_record := _score_record(record, terms)) is not None
    )
    ordered = sorted(
        scored,
        key=lambda item: (
            -item["score"],
            AUTHORITY_ORDER.get(item["evidence_type"], 99),
            item["source_title"].lower(),
            item["record_id"].lower(),
        ),
    )
    results = tuple(_result(item, rank=index + 1) for index, item in enumerate(ordered))

    caveats = (
        "Retrieval is deterministic keyword/metadata matching over controlled local fixtures only.",
        "Controlled-readiness does not imply runtime, deployment, or production readiness.",
        "Developer Log evidence does not prove runtime implementation.",
        "Hardening Log evidence does not prove repair or implementation.",
        "Platform Doctrine evidence does not prove execution.",
        "Historical evidence is not current truth by default.",
        "Final answer generation is not performed or permitted by this service.",
    )
    if unsupported:
        caveats = (*caveats, UNSUPPORTED_EVIDENCE_TYPE_NOTE)

    return _envelope(
        query=query,
        terms=terms,
        results=results,
        unsupported=unsupported,
        caveats=caveats,
    )


def build_controlled_multi_source_evidence_retrieval(
    query_text: str,
    filters: dict[str, Any] | None = None,
    fixture_payloads: Iterable[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return retrieve_controlled_multi_source_evidence(query_text, filters, fixture_payloads)


def _envelope(
    *,
    query: str,
    terms: tuple[str, ...],
    results: tuple[dict[str, Any], ...],
    unsupported: tuple[str, ...],
    caveats: tuple[str, ...],
) -> dict[str, Any]:
    return ControlledMultiSourceEvidenceRetrievalEnvelope(
        QueryText=query,
        NormalizedQueryTerms=terms,
        RetrievalMode=RETRIEVAL_MODE,
        EvidenceUniverse=EVIDENCE_UNIVERSE,
        EvidenceTypesSearched=EVIDENCE_TYPES_SEARCHED,
        EvidenceTypesOutOfScope=EVIDENCE_TYPES_OUT_OF_SCOPE,
        AuthorityPolicyApplied=AUTHORITY_POLICY_APPLIED,
        ResultCount=len(results),
        Results=results,
        BoundaryFlags=dict(BOUNDARY_FLAGS),
        Caveats=caveats,
        UnsupportedEvidenceTypes=unsupported,
        NextStep=NEXT_SAFE_STEP,
        FinalAnswerPermitted=False,
        RetrievalStoryOnly=True,
    ).to_dict()


def _fixture_records(fixture_payloads: Iterable[dict[str, Any]] | None) -> tuple[dict[str, Any], ...]:
    if fixture_payloads is not None:
        records = tuple(dict(payload) for payload in fixture_payloads)
    else:
        records = tuple(
            json.loads(path.read_text(encoding="utf-8"))
            for path in DEFAULT_FIXTURE_PATHS
        )
    return tuple(sorted(records, key=lambda record: str(record.get("fixture_id", ""))))


def _score_record(record: dict[str, Any], terms: tuple[str, ...]) -> dict[str, Any] | None:
    evidence_type = _record_evidence_type(record)
    search_fields = _search_fields(record)
    searchable = " ".join(search_fields.values()).lower()
    matched_terms = tuple(term for term in terms if term in searchable)
    intent_matches = tuple(term for term in terms if term in INTENT_TERMS[evidence_type])
    if not matched_terms and not intent_matches:
        return None

    reasons = [
        f"{term} matched {field_name}"
        for term in matched_terms
        for field_name, field_value in search_fields.items()
        if term in field_value.lower()
    ]
    reasons.extend(f"{term} matched {evidence_type} query intent" for term in intent_matches)
    return {
        "record": record,
        "record_id": str(_metadata(record).get("evidence_id") or record.get("fixture_id") or ""),
        "evidence_type": evidence_type,
        "source_title": _source_title(record),
        "source_status": _source_status(record),
        "implementation_status": _implementation_status(record),
        "answer_use_status": _answer_use_status(record),
        "current_truth_status": CURRENT_TRUTH_STATUS[evidence_type],
        "matched_terms": tuple(dict.fromkeys((*matched_terms, *intent_matches))),
        "match_reasons": tuple(dict.fromkeys(reasons)),
        "score": _score(
            evidence_type=evidence_type,
            matched_terms=matched_terms,
            intent_matches=intent_matches,
            reasons=tuple(dict.fromkeys(reasons)),
        ),
    }


def _result(scored: dict[str, Any], rank: int) -> dict[str, Any]:
    evidence_type = scored["evidence_type"]
    return ControlledMultiSourceEvidenceRetrievalResult(
        RecordId=scored["record_id"],
        EvidenceType=evidence_type,
        SourceType=evidence_type,
        SourceTitle=scored["source_title"],
        SourceStatus=scored["source_status"],
        AuthorityLevel=AUTHORITY_LEVELS[evidence_type],
        ImplementationStatus=scored["implementation_status"],
        CurrentTruthStatus=scored["current_truth_status"],
        AnswerUseStatus=scored["answer_use_status"],
        MatchedTerms=scored["matched_terms"],
        MatchReasons=scored["match_reasons"],
        Rank=rank,
        Score=scored["score"],
        CanProve=_can_prove(scored["record"]),
        CannotProve=_cannot_prove(scored["record"]),
        RequiredCaveats=_required_caveats(scored["record"]),
        CaveatRequired=True,
        FinalAnswerPermitted=False,
        BoundaryFlags=dict(BOUNDARY_FLAGS),
    ).to_dict()


def _search_fields(record: dict[str, Any]) -> dict[str, str]:
    metadata = _metadata(record)
    dry_run = build_controlled_evidence_intake_dry_run(record)
    boundary = build_evidence_source_status_boundary(metadata)
    evidence_type = _record_evidence_type(record)
    return {
        "fixture_id": str(record.get("fixture_id") or ""),
        "fixture_purpose": str(record.get("fixture_purpose") or ""),
        "evidence_type": evidence_type,
        "source_title": _source_title(record),
        "source_status": str(dry_run.get("source_status") or metadata.get("source_status") or ""),
        "trust_level": str(metadata.get("trust_level") or ""),
        "required_caveats": " ".join(str(item) for item in _required_caveats(record)),
        "expected_summary_terms": " ".join(str(item) for item in record.get("expected_summary_terms", ())),
        "expected_no_action_attestation": str(record.get("expected_no_action_attestation") or ""),
        "prohibited_inferences": " ".join(
            str(item) for item in dry_run.get("prohibited_inferences", ())
        ),
        "boundary_explanation": str(boundary.get("explanation") or ""),
        "controlled_claims": " ".join(CONTROLLED_CLAIMS[evidence_type]),
        "can_prove": " ".join(_can_prove(record)),
        "cannot_prove": " ".join(_cannot_prove(record)),
    }


def _metadata(record: dict[str, Any]) -> dict[str, Any]:
    if isinstance(record.get("input_metadata"), dict):
        return dict(record["input_metadata"])
    return dict(record)


def _record_evidence_type(record: dict[str, Any]) -> str:
    metadata = _metadata(record)
    return _normalize_evidence_type(
        metadata.get("evidence_category")
        or metadata.get("category")
        or record.get("expected_evidence_category")
    )


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
        or ANSWER_USE_STATUS
    )


def _required_caveats(record: dict[str, Any]) -> tuple[str, ...]:
    evidence_type = _record_evidence_type(record)
    metadata = _metadata(record)
    dry_run = build_controlled_evidence_intake_dry_run(record)
    boundary = build_evidence_source_status_boundary(metadata)
    caveats = (
        *_as_tuple(metadata.get("required_caveats")),
        *_as_tuple(dry_run.get("required_caveats")),
        *_as_tuple(boundary.get("required_caveats")),
        _type_boundary_caveat(evidence_type),
        "Final answer generation is not permitted from retrieval output.",
    )
    return tuple(dict.fromkeys(str(caveat) for caveat in caveats if str(caveat)))


def _can_prove(record: dict[str, Any]) -> tuple[str, ...]:
    evidence_type = _record_evidence_type(record)
    return {
        PLATFORM_DOCTRINE: (
            "The controlled Platform Doctrine fixture exists in the local fixture universe.",
            "The fixture records doctrine boundaries for no live Minerva runtime unless explicitly authorised.",
            "The fixture records source/status boundary preservation and prompt-is-not-knowledge doctrine.",
        ),
        HARDENING_LOG: (
            "The controlled Hardening Log fixture exists in the local fixture universe.",
            "The fixture records prohibited live actions and remaining evidence-path hardening boundaries.",
            "The fixture records that hardening/prohibition evidence must not be treated as implementation proof.",
        ),
        DEVELOPER_LOG: (
            "The controlled Developer Log fixture exists in the local fixture universe.",
            "The fixture records Developer Log durable evidence path completion at controlled-readiness level.",
            "The fixture records controlled retrieval readiness without live LLM, DB, chat exposure, or corpus mutation.",
        ),
    }[evidence_type]


def _cannot_prove(record: dict[str, Any]) -> tuple[str, ...]:
    evidence_type = _record_evidence_type(record)
    common = (
        "final user-facing answer correctness",
        "final answer generation permission",
        "live LLM execution",
        "chat exposure",
        "database-backed retrieval or live DB state",
        "live corpus mutation",
        "Code Evidence ingestion",
        "runtime readiness",
        "deployment readiness",
        "production readiness",
        "current truth without explicit current-proof status",
    )
    specific = {
        PLATFORM_DOCTRINE: (
            "execution proof",
            "implementation completed",
        ),
        HARDENING_LOG: (
            "implementation proof",
            "repair completed",
            "fix completed",
        ),
        DEVELOPER_LOG: (
            "runtime implementation",
            "controlled-readiness as production readiness",
        ),
    }[evidence_type]
    return (*specific, *common)


def _type_boundary_caveat(evidence_type: str) -> str:
    return {
        PLATFORM_DOCTRINE: "Platform Doctrine is doctrine context, not execution proof.",
        HARDENING_LOG: "Hardening Log records prohibition or findings, not implementation proof.",
        DEVELOPER_LOG: "Developer Log records controlled work, not runtime or production truth.",
    }[evidence_type]


def _score(
    *,
    evidence_type: str,
    matched_terms: tuple[str, ...],
    intent_matches: tuple[str, ...],
    reasons: tuple[str, ...],
) -> int:
    authority_tiebreak = 6 - AUTHORITY_ORDER.get(evidence_type, 5)
    return (
        len(tuple(dict.fromkeys(matched_terms))) * 10
        + len(tuple(dict.fromkeys(intent_matches))) * 8
        + len(reasons)
        + authority_tiebreak
    )


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
    requested = _requested_types(query, filters)
    return tuple(
        sorted(item for item in requested if item in EVIDENCE_TYPES_OUT_OF_SCOPE)
    )


def _requested_supported_types(query: str, filters: dict[str, Any]) -> tuple[str, ...]:
    requested = _requested_types(query, filters)
    return tuple(
        item for item in EVIDENCE_TYPES_SEARCHED if item in requested
    )


def _requested_types(query: str, filters: dict[str, Any]) -> set[str]:
    terms = set(_normalize_terms(query))
    requested: set[str] = set()
    filter_type = filters.get("evidence_type")
    if filter_type:
        requested.add(_normalize_evidence_type(filter_type))
    if "developer" in terms or "dev" in terms:
        requested.add(DEVELOPER_LOG)
    if "hardening" in terms:
        requested.add(HARDENING_LOG)
    if "platform" in terms or "doctrine" in terms:
        requested.add(PLATFORM_DOCTRINE)
    if "thread" in terms or "continuance" in terms:
        requested.add(THREAD_CONTINUANCE_PROMPT)
    if "code" in terms:
        requested.add("CODE_EVIDENCE")
    if "db" in terms or "database" in terms:
        requested.add("LIVE_DB")
    if "corpus" in terms and "live" in terms:
        requested.add("LIVE_CORPUS")
    if "analytics" in terms:
        requested.add("ANALYTICS_READINESS_SUMMARY")
    return requested


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None or value == "":
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, set):
        return tuple(sorted(value))
    return (value,)
