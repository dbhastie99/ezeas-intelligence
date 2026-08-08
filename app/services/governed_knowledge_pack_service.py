"""Governed, versioned knowledge-pack proof for Minerva's Queensland LSL slice.

The pack is a checked-in reviewed publication boundary.  This module deliberately
does not retrieve URLs, use an LLM, calculate an entitlement, or connect to an
operational system.  Its database bridge delegates source ingestion and keyword
retrieval to the repository's existing services and is intended for the ephemeral
test adapter in this slice.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeDocument
from app.schemas.common import SourceReference
from app.schemas.minerva_leave import (
    LeaveAnswerPlan,
    LeaveAskResponse,
    PackCitationResponse,
    PackIdentityResponse,
)
from app.services.audit_service import write_ai_interaction_audit
from app.services.ingestion_service import ingest_file_bytes
from app.services.knowledge_retrieval_service import RetrievalResult, retrieve_relevant_chunks
from app.services.minerva_qld_lsl_answer_planner import (
    MODE_FACT_IDS,
    build_answer_plan,
    classify_question,
    render_answer,
)


PACK_KEY = "queensland-general-lsl-v1"
SEMANTIC_VERSION = "1.0.0"
PUBLISHED = "PUBLISHED"
PACK_ROOT = Path(__file__).resolve().parents[2] / "docs" / "knowledge" / "packs" / PACK_KEY
DEFAULT_MANIFEST_PATH = PACK_ROOT / "manifest.json"
PROMPT_POLICY = "MINERVA_GOVERNED_PACK_READ_ONLY"

QLEAVE_OPERATION_TERMS = (
    "qleave",
    "portable scheme",
    "portable schemes",
    "reimbursement",
    "registration",
    "register",
    "levy",
    "return",
    "claim",
    "claims",
    "operational procedure",
    "operational process",
)
PROMPT_INJECTION_TERMS = (
    "ignore previous",
    "ignore the instructions",
    "system prompt",
    "prompt injection",
    "reveal your instructions",
)
STOPWORDS = {"the", "and", "for", "with", "this", "that", "does", "what", "how", "are", "its"}


class PackValidationError(ValueError):
    pass


class PackNotIngestedError(ValueError):
    pass


class UnsupportedPackRequest(ValueError):
    pass


class ProposalRequestError(ValueError):
    pass


@dataclass(frozen=True)
class PackIngestionResult:
    pack_key: str
    semantic_version: str
    manifest_fingerprint: str
    ingestion_identity: str
    source_document_ids: dict[str, str]
    ingested_count: int
    duplicate_count: int


@dataclass(frozen=True)
class LoadedPack:
    data: dict[str, Any]
    root: Path
    manifest_path: Path

    @property
    def pack_key(self) -> str:
        return self.data["pack_key"]

    @property
    def semantic_version(self) -> str:
        return self.data["semantic_version"]

    @property
    def manifest_fingerprint(self) -> str:
        return self.data["manifest"]["content_fingerprint"]

    def identity_response(self) -> PackIdentityResponse:
        return PackIdentityResponse(
            pack_key=self.pack_key,
            semantic_version=self.semantic_version,
            status=self.data["status"],
            manifest_fingerprint=self.manifest_fingerprint,
        )


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _fingerprint_material(data: dict[str, Any]) -> dict[str, Any]:
    material = json.loads(json.dumps(data))
    manifest = material.get("manifest")
    if isinstance(manifest, dict):
        for field in ("content_fingerprint", "ingestion_identity", "audit_identity"):
            manifest.pop(field, None)
    return material


def manifest_fingerprint(data: dict[str, Any]) -> str:
    return _sha256(_canonical_json(_fingerprint_material(data)))


def _identity(prefix: str, *parts: str) -> str:
    digest = _sha256("|".join(parts).encode("utf-8"))
    return f"{prefix}_{digest[:32]}"


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PackValidationError(f"{label} must be a non-empty string.")
    return value


def _require_date(value: Any, label: str, allow_none: bool = False) -> None:
    if value is None and allow_none:
        return
    text = _require_string(value, label)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise PackValidationError(f"{label} must be an ISO date.")


def _require_url(value: Any, label: str) -> str:
    url = _require_string(value, label)
    if not url.startswith("https://") or not ("legislation.qld.gov.au" in url or "business.qld.gov.au" in url):
        raise PackValidationError(f"{label} must be an authoritative Queensland Government HTTPS URL.")
    return url


def _source_content_bytes(path: Path) -> bytes:
    """Hash and ingest the committed LF content consistently on Windows checkouts."""

    return path.read_bytes().replace(b"\r\n", b"\n")


def validate_pack(data: dict[str, Any], root: Path) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise PackValidationError("Pack manifest root must be an object.")
    if data.get("status") != PUBLISHED:
        raise PackValidationError("Only a PUBLISHED pack can be retrieved.")
    pack_key = _require_string(data.get("pack_key"), "pack_key")
    version = _require_string(data.get("semantic_version"), "semantic_version")
    if data.get("successor_pack_ref") is not None:
        raise PackValidationError("The published pack must not have a successor reference.")
    _require_string(data.get("title"), "title")
    if data.get("jurisdiction") != "Queensland" or data.get("domain") != "Leave":
        raise PackValidationError("Pack jurisdiction/domain must be Queensland/Leave.")
    for field in ("audience_purpose", "advisory_notice", "scope_statement", "excluded_scope"):
        _require_string(data.get(field), field)
    if "advisory information only; not legal advice" not in data["advisory_notice"].lower():
        raise PackValidationError("The pack must state that it is advisory information only and not legal advice.")
    excluded = data["excluded_scope"].lower()
    for term in ("qleave", "registration", "levy", "reimbursement", "operational"):
        if term not in excluded:
            raise PackValidationError("The QLeave operational boundary is incomplete.")
    publication_timestamp = _require_string(data.get("publication_timestamp"), "publication_timestamp")
    if "t" not in publication_timestamp.lower() or "+" not in publication_timestamp:
        raise PackValidationError("publication_timestamp must include a timezone.")
    sources = data.get("sources")
    facts = data.get("facts")
    if not isinstance(sources, list) or not sources:
        raise PackValidationError("Pack must contain reviewed sources.")
    if not isinstance(facts, list) or not facts:
        raise PackValidationError("Pack must contain governed facts.")

    source_ids: set[str] = set()
    source_fingerprints: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise PackValidationError("Each source must be an object.")
        source_id = _require_string(source.get("source_id"), "source_id")
        if source_id in source_ids:
            raise PackValidationError(f"Duplicate source identity: {source_id}.")
        source_ids.add(source_id)
        _require_string(source.get("publisher"), f"{source_id}.publisher")
        _require_url(source.get("url"), f"{source_id}.url")
        _require_string(source.get("title"), f"{source_id}.title")
        _require_date(source.get("retrieval_date"), f"{source_id}.retrieval_date")
        _require_date(source.get("review_date"), f"{source_id}.review_date")
        _require_date(source.get("effective_date"), f"{source_id}.effective_date", allow_none=True)
        _require_string(source.get("source_version"), f"{source_id}.source_version")
        _require_string(source.get("citation_locator"), f"{source_id}.citation_locator")
        content_path = _require_string(source.get("content_path"), f"{source_id}.content_path")
        resolved = (root / content_path).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError as exc:
            raise PackValidationError(f"{source_id}.content_path escapes the pack directory.") from exc
        if not resolved.is_file():
            raise PackValidationError(f"Missing reviewed source content: {content_path}.")
        fingerprint = _require_string(source.get("content_fingerprint"), f"{source_id}.content_fingerprint")
        actual = _sha256(_source_content_bytes(resolved))
        if actual != fingerprint:
            raise PackValidationError(f"Source content fingerprint mismatch: {source_id}.")
        if fingerprint in source_fingerprints:
            raise PackValidationError(f"Duplicate source content fingerprint: {source_id}.")
        source_fingerprints.add(fingerprint)

    fact_ids: set[str] = set()
    for fact in facts:
        if not isinstance(fact, dict):
            raise PackValidationError("Each fact must be an object.")
        fact_id = _require_string(fact.get("fact_id"), "fact_id")
        if fact_id in fact_ids:
            raise PackValidationError(f"Duplicate fact identity: {fact_id}.")
        fact_ids.add(fact_id)
        for field in ("claim", "plain_language_explanation", "scope", "limits_exclusions", "review_status"):
            _require_string(fact.get(field), f"{fact_id}.{field}")
        if fact["review_status"] != "REVIEWED":
            raise PackValidationError(f"Fact is not reviewed: {fact_id}.")
        effective_period = fact.get("effective_period")
        if not isinstance(effective_period, dict):
            raise PackValidationError(f"{fact_id}.effective_period must be an object.")
        _require_date(effective_period.get("from"), f"{fact_id}.effective_period.from")
        _require_date(effective_period.get("to"), f"{fact_id}.effective_period.to", allow_none=True)
        refs = fact.get("source_refs")
        if not isinstance(refs, list) or not refs or any(ref not in source_ids for ref in refs):
            raise PackValidationError(f"Fact must have valid source citations: {fact_id}.")

    manifest = data.get("manifest")
    if not isinstance(manifest, dict):
        raise PackValidationError("Pack manifest metadata is required.")
    expected = _require_string(manifest.get("content_fingerprint"), "manifest.content_fingerprint")
    actual_manifest = manifest_fingerprint(data)
    if expected != actual_manifest:
        raise PackValidationError("Pack manifest fingerprint mismatch.")
    expected_ingestion = _identity("ing", pack_key, version, expected)
    expected_audit = _identity("aud", pack_key, version, expected)
    if manifest.get("ingestion_identity") != expected_ingestion or manifest.get("audit_identity") != expected_audit:
        raise PackValidationError("Pack ingestion/audit identity mismatch.")
    return data


def load_pack(manifest_path: Path = DEFAULT_MANIFEST_PATH) -> LoadedPack:
    resolved = Path(manifest_path).resolve()
    if not resolved.is_file():
        raise PackValidationError(f"Pack manifest not found: {resolved}")
    try:
        data = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PackValidationError(f"Pack manifest is not valid JSON: {exc}") from exc
    validate_pack(data, resolved.parent)
    return LoadedPack(data=data, root=resolved.parent, manifest_path=resolved)


def require_requested_pack(pack: LoadedPack, pack_key: str, semantic_version: str) -> None:
    if pack_key != pack.pack_key or semantic_version != pack.semantic_version:
        raise UnsupportedPackRequest("The requested pack key/version is not the explicitly published pack.")


def ingest_pack(db: Session, manifest_path: Path = DEFAULT_MANIFEST_PATH) -> PackIngestionResult:
    pack = load_pack(manifest_path)
    source_document_ids: dict[str, str] = {}
    ingested_count = duplicate_count = 0
    for source in pack.data["sources"]:
        source_path = pack.root / source["content_path"]
        document, duplicate = ingest_file_bytes(
            db=db,
            content=_source_content_bytes(source_path),
            original_file_name=source_path.name,
            source_type="OTHER",
            capability_status="DOCTRINE",
            title=source["title"],
        )
        source_document_ids[source["source_id"]] = document.KnowledgeDocumentId
        if duplicate:
            duplicate_count += 1
        else:
            ingested_count += 1
    return PackIngestionResult(
        pack_key=pack.pack_key,
        semantic_version=pack.semantic_version,
        manifest_fingerprint=pack.manifest_fingerprint,
        ingestion_identity=pack.data["manifest"]["ingestion_identity"],
        source_document_ids=source_document_ids,
        ingested_count=ingested_count,
        duplicate_count=duplicate_count,
    )


def _source_document_ids(db: Session, pack: LoadedPack) -> dict[str, str]:
    fingerprints = [source["content_fingerprint"] for source in pack.data["sources"]]
    documents = db.scalars(select(KnowledgeDocument).where(KnowledgeDocument.FileSha256.in_(fingerprints))).all()
    by_fingerprint = {document.FileSha256: document.KnowledgeDocumentId for document in documents}
    missing = [source["source_id"] for source in pack.data["sources"] if source["content_fingerprint"] not in by_fingerprint]
    if missing:
        raise PackNotIngestedError("The explicitly requested published pack has not been ingested: " + ", ".join(missing))
    return {source["source_id"]: by_fingerprint[source["content_fingerprint"]] for source in pack.data["sources"]}


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) >= 3 and token not in STOPWORDS}


def _is_prompt_injection(text: str) -> bool:
    normalized = " ".join(text.lower().split())
    return any(term in normalized for term in PROMPT_INJECTION_TERMS)


def _is_qleave_operation(text: str) -> bool:
    normalized = " ".join(text.lower().split())
    return any(term in normalized for term in QLEAVE_OPERATION_TERMS)


def _facts_for_results(
    pack: LoadedPack,
    results: list[RetrievalResult],
    query: str,
    source_documents: dict[str, str],
) -> list[dict[str, Any]]:
    retrieved_document_ids = {result.document_id for result in results}
    source_ids = {source_id for source_id, document_id in source_documents.items() if document_id in retrieved_document_ids}
    query_tokens = _tokens(query)
    scored: list[tuple[int, str, dict[str, Any]]] = []
    for fact in pack.data["facts"]:
        if not set(fact["source_refs"]) & source_ids:
            continue
        material = " ".join(
            [fact["claim"], fact["plain_language_explanation"], fact["scope"], fact["limits_exclusions"]]
        )
        score = len(query_tokens & _tokens(material))
        if score:
            scored.append((score, fact["fact_id"], fact))
    return [fact for _, _, fact in sorted(scored, key=lambda item: (-item[0], item[1]))]


def _citation(pack: LoadedPack, fact: dict[str, Any], source: dict[str, Any]) -> PackCitationResponse:
    return PackCitationResponse(
        fact_id=fact["fact_id"],
        source_id=source["source_id"],
        publisher=source["publisher"],
        source_title=source["title"],
        url=source["url"],
        locator=source["citation_locator"],
    )


def _source_references(results: list[RetrievalResult]) -> list[SourceReference]:
    return [
        SourceReference(
            document_id=result.document_id,
            chunk_id=result.chunk_id,
            title=result.title,
            original_file_name=result.original_file_name,
            source_type=result.source_type,
            source_authority=result.source_authority,
            chunk_index=result.chunk_index,
            score=round(result.score, 3),
            matched_tokens=result.matched_tokens,
            snippet=result.snippet,
            detected_intent=result.detected_intent,
            matched_phrases=result.matched_phrases,
            match_reason=result.match_reason,
            domain_plan_id=result.domain_plan_id,
            evidence_group_id=result.evidence_group_id,
            evidence_group_label=result.evidence_group_label,
        )
        for result in results
    ]


def _minimum_audit_payload(
    *,
    request_identity: str,
    audit_identity: str,
    plan: LeaveAnswerPlan,
) -> str:
    return json.dumps(
        {
            "audit_identity": audit_identity,
            "request_identity": request_identity,
            "pack_key": plan.pack_key,
            "semantic_version": plan.semantic_version,
            "manifest_fingerprint": plan.manifest_fingerprint,
            "answer_mode": plan.answer_mode,
            "outcome": plan.outcome,
            "selected_fact_ids": plan.selected_fact_ids,
            "citation_ids": sorted({f"{item.fact_id}:{item.source_id}" for item in plan.citations}),
        },
        sort_keys=True,
    )


def _persist_minimum_audit(
    *,
    db: Session,
    request_identity: str,
    audit_identity: str,
    plan: LeaveAnswerPlan,
    pack_key: str,
    semantic_version: str,
) -> str:
    """Persist one redacted audit outcome; persistence errors deliberately propagate."""

    audit = write_ai_interaction_audit(
        db=db,
        user_question=f"MINERVA_QG_LSL_REQUEST:{request_identity}",
        response_text=_minimum_audit_payload(
            request_identity=request_identity,
            audit_identity=audit_identity,
            plan=plan,
        ),
        source_references=[],
        model_name="DETERMINISTIC_GOVERNED_PACK",
        prompt_policy=f"{PROMPT_POLICY}:{pack_key}:{semantic_version}",
    )
    db.commit()
    return audit.AIInteractionAuditId


def _ask_published_pack_legacy(
    db: Session,
    question: str,
    pack_key: str,
    semantic_version: str,
    *,
    persist_audit: bool = False,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> LeaveAskResponse:
    if not question.strip() or len(question) > 2000:
        raise UnsupportedPackRequest("Question must be non-empty and within the governed length limit.")
    if _is_prompt_injection(question):
        raise UnsupportedPackRequest("Prompt-injected requests are not supported by the governed pack assistant.")
    pack = load_pack(manifest_path)
    require_requested_pack(pack, pack_key, semantic_version)
    request_identity = _identity("req", pack_key, semantic_version, question.strip())
    scope_limitations = [
        pack.data["scope_statement"],
        pack.data["excluded_scope"],
        pack.data["advisory_notice"],
        "This pack is not a service-history calculator, entitlement engine, payroll valuation engine, or QLeave operational implementation.",
    ]
    if _is_qleave_operation(question):
        answer = (
            "I can’t answer that QLeave operational question from this pack. "
            "queensland-general-lsl-v1 covers Queensland General Long Service Leave only; "
            "QLeave portable-scheme registration, levies, returns, claims, reimbursements, payments, "
            "and operational procedures are explicitly excluded."
        )
        audit_identity = _identity("aud", request_identity, "REFUSED_QLEAVE")
        audit_id = None
        if persist_audit:
            audit = write_ai_interaction_audit(
                db=db,
                user_question=question,
                response_text=answer,
                source_references=[],
                model_name="DETERMINISTIC_GOVERNED_PACK",
                prompt_policy=f"{PROMPT_POLICY}:{pack_key}:{semantic_version}",
            )
            db.commit()
            audit_id = audit.AIInteractionAuditId
        return LeaveAskResponse(
            request_identity=request_identity,
            audit_identity=audit_identity,
            audit_id=audit_id,
            outcome="REFUSED_OUT_OF_SCOPE",
            pack=pack.identity_response(),
            answer=answer,
            fact_ids=[],
            source_ids=[],
            citations=[],
            scope_limitations=scope_limitations,
        )

    source_documents = _source_document_ids(db, pack)
    results = retrieve_relevant_chunks(
        db=db,
        query=question,
        top_k=8,
        include_samples=False,
        document_ids=list(source_documents.values()),
    )
    facts = _facts_for_results(pack, results, question, source_documents)
    if not facts:
        raise UnsupportedPackRequest("The published pack has no retrieved fact that supports this request.")
    source_by_id = {source["source_id"]: source for source in pack.data["sources"]}
    fact_ids = [fact["fact_id"] for fact in facts]
    source_ids = sorted({source_id for fact in facts for source_id in fact["source_refs"]})
    citations = [_citation(pack, fact, source_by_id[source_id]) for fact in facts for source_id in fact["source_refs"]]
    deduped_citations = list({(item.fact_id, item.source_id): item for item in citations}.values())
    answer_lines = ["This is advisory information from the explicitly requested Queensland General LSL pack:"]
    for fact in facts:
        answer_lines.append(f"- {fact['plain_language_explanation']}")
    answer_lines.append("It does not decide an individual case or calculate a live entitlement; obtain specialist advice where the cited material does not determine the answer.")
    answer = "\n".join(answer_lines)
    audit_identity = _identity("aud", request_identity, *fact_ids, *sorted(source_ids))
    audit_id = None
    if persist_audit:
        audit = write_ai_interaction_audit(
            db=db,
            user_question=question,
            response_text=answer + "\nCitations: " + ", ".join(item.url for item in deduped_citations),
            source_references=_source_references(results),
            model_name="DETERMINISTIC_GOVERNED_PACK",
            prompt_policy=f"{PROMPT_POLICY}:{pack_key}:{semantic_version}",
        )
        db.commit()
        audit_id = audit.AIInteractionAuditId
    return LeaveAskResponse(
        request_identity=request_identity,
        audit_identity=audit_identity,
        audit_id=audit_id,
        outcome="ANSWERED_FROM_PUBLISHED_PACK",
        pack=pack.identity_response(),
        answer=answer,
        fact_ids=fact_ids,
        source_ids=source_ids,
        citations=deduped_citations,
        scope_limitations=scope_limitations,
    )


def ask_published_pack(
    db: Session,
    question: str,
    pack_key: str,
    semantic_version: str,
    *,
    persist_audit: bool = False,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
) -> LeaveAskResponse:
    """Answer from one explicitly requested published pack and a typed plan."""

    if not question.strip() or len(question) > 2000:
        raise UnsupportedPackRequest("Question must be non-empty and within the governed length limit.")
    answer_mode = classify_question(question)
    if answer_mode == "REFUSED_UNSAFE_REQUEST" and not persist_audit:
        raise UnsupportedPackRequest("Prompt-injected requests are not supported by the governed pack assistant.")

    pack = load_pack(manifest_path)
    require_requested_pack(pack, pack_key, semantic_version)
    request_identity = _identity("req", pack_key, semantic_version, question.strip())
    scope_limitations = [
        pack.data["scope_statement"],
        pack.data["excluded_scope"],
        pack.data["advisory_notice"],
        "This pack is not a service-history calculator, entitlement engine, payroll valuation engine, or QLeave operational implementation.",
    ]


    if answer_mode in {"REFUSED_QLEAVE_OPERATION", "REFUSED_UNSAFE_REQUEST", "OUT_OF_EVIDENCE"}:
        plan = build_answer_plan(
            mode=answer_mode,
            selected_facts=[],
            citations=[],
            pack_key=pack.pack_key,
            semantic_version=pack.semantic_version,
            manifest_fingerprint=pack.manifest_fingerprint,
        )
        answer = render_answer(plan)
        audit_suffix = {
            "REFUSED_QLEAVE_OPERATION": "REFUSED_QLEAVE",
            "REFUSED_UNSAFE_REQUEST": "REFUSED_UNSAFE",
            "OUT_OF_EVIDENCE": "OUT_OF_EVIDENCE",
        }[answer_mode]
        audit_identity = _identity("aud", request_identity, audit_suffix)
        audit_id = (
            _persist_minimum_audit(
                db=db,
                request_identity=request_identity,
                audit_identity=audit_identity,
                plan=plan,
                pack_key=pack_key,
                semantic_version=semantic_version,
            )
            if persist_audit
            else None
        )
        return LeaveAskResponse(
            request_identity=request_identity,
            audit_identity=audit_identity,
            audit_id=audit_id,
            outcome=plan.outcome,
            pack=pack.identity_response(),
            answer=answer,
            fact_ids=[],
            source_ids=[],
            citations=[],
            scope_limitations=scope_limitations,
            answer_plan=plan,
        )

    source_documents = _source_document_ids(db, pack)
    results = retrieve_relevant_chunks(
        db=db,
        query=question,
        top_k=8,
        include_samples=False,
        document_ids=list(source_documents.values()),
    )
    facts_by_id = {fact["fact_id"]: fact for fact in pack.data["facts"]}
    selected_fact_ids = MODE_FACT_IDS[answer_mode]
    selected_facts = [facts_by_id[fact_id] for fact_id in selected_fact_ids]
    source_by_id = {source["source_id"]: source for source in pack.data["sources"]}
    source_ids = sorted({source_id for fact in selected_facts for source_id in fact["source_refs"]})
    citations = [
        _citation(pack, fact, source_by_id[source_id])
        for fact in selected_facts
        for source_id in fact["source_refs"]
    ]
    deduped_citations = list({(item.fact_id, item.source_id): item for item in citations}.values())
    plan = build_answer_plan(
        mode=answer_mode,
        selected_facts=selected_facts,
        citations=deduped_citations,
        pack_key=pack.pack_key,
        semantic_version=pack.semantic_version,
        manifest_fingerprint=pack.manifest_fingerprint,
    )
    answer = render_answer(plan)
    fact_ids = list(selected_fact_ids)
    audit_identity = _identity("aud", request_identity, *fact_ids, *sorted(source_ids))
    audit_id = None
    if persist_audit:
        audit_id = _persist_minimum_audit(
            db=db,
            request_identity=request_identity,
            audit_identity=audit_identity,
            plan=plan,
            pack_key=pack_key,
            semantic_version=semantic_version,
        )
    return LeaveAskResponse(
        request_identity=request_identity,
        audit_identity=audit_identity,
        audit_id=audit_id,
        outcome=plan.outcome,
        pack=pack.identity_response(),
        answer=answer,
        fact_ids=fact_ids,
        source_ids=source_ids,
        citations=deduped_citations,
        scope_limitations=scope_limitations,
        answer_plan=plan,
    )
