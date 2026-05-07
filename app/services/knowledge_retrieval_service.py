import re
from dataclasses import dataclass, field

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import normalize_source_type
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument

GENERIC_QUERY_TERMS = {
    "not",
    "allowed",
    "mean",
    "means",
    "does",
    "what",
    "why",
    "how",
    "can",
    "cannot",
    "must",
}
STOPWORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "what",
    "why",
    "how",
    "does",
    "do",
    "to",
    "of",
    "and",
    "or",
    "in",
    "on",
    "for",
    "with",
    "this",
    "that",
    "it",
} | GENERIC_QUERY_TERMS
IMPORTANT_ACRONYMS = {"llm", "rbac", "json", "sql"}
HIGH_SIGNAL_TERMS = {"minerva", "rbac", "llm", "json", "sql", "database", "advisory", "payroll"}
SOURCE_TYPE_QUERY_BOOSTS = {
    "PLATFORM_DOCTRINE": {"minerva", "allowed", "advisory", "payroll", "truth", "boundary", "doctrine"},
    "HARDENING_LOG": {"hardening", "rbac", "before", "security", "tenant", "audit"},
    "DEVELOPER_LOG": {"developer", "history", "implemented", "context", "decision"},
    "REQUIREMENTS": {"requirement", "requirements", "planning", "roadmap", "future"},
    "CHAT_HISTORY": {"thread", "chat", "discussion", "context"},
}
CAPABILITY_STATUS_BOOSTS = {
    "DOCTRINE": 2.5,
    "IMPLEMENTED": 2.0,
    "PHASE_ONE": 1.5,
    "OUTSTANDING_HARDENING": 1.0,
    "FUTURE_ROADMAP": 0.75,
    "DESIGN_DISCUSSION": 0.5,
}


@dataclass(frozen=True)
class QueryIntentDefinition:
    name: str
    trigger_terms: tuple[str, ...]
    trigger_phrases: tuple[str, ...]
    evidence_phrases: tuple[str, ...]
    preferred_source_types: tuple[str, ...]


INTENT_DEFINITIONS = {
    "MINERVA_BOUNDARY_PROHIBITION": QueryIntentDefinition(
        name="MINERVA_BOUNDARY_PROHIBITION",
        trigger_terms=("minerva", "llm", "boundary", "boundaries"),
        trigger_phrases=(
            "not allowed",
            "can minerva not",
            "minerva not do",
            "must minerva not",
            "must not",
            "llm not allowed",
            "minerva's boundaries",
            "minerva boundaries",
        ),
        evidence_phrases=(
            "llm boundary",
            "llm is not calculation truth",
            "no autonomous ai action",
            "must not calculate",
            "must not calculate payroll",
            "must not determine entitlements",
            "must not approve exceptions",
            "must not suppress warnings",
            "must not override",
            "must not mutate",
            "must not finalise",
            "minerva is advisory",
            "not payroll calculation truth",
            "deterministic platform remains source of truth",
            "payroll calculation truth",
        ),
        preferred_source_types=("PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    "SEPARATE_DATABASE": QueryIntentDefinition(
        name="SEPARATE_DATABASE",
        trigger_terms=("database", "store", "ezeas", "intelligence"),
        trigger_phrases=(
            "separate database",
            "separate intelligence store",
            "ezeas-intelligence-db",
        ),
        evidence_phrases=(
            "separate intelligence store doctrine",
            "separate database",
            "ezeas-intelligence-db",
            "operational database remains authoritative",
            "operational database remains source of payroll truth",
            "operational payroll database remains source of truth",
            "operational payroll database",
        ),
        preferred_source_types=("PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
    "RBAC_BEFORE_LLM": QueryIntentDefinition(
        name="RBAC_BEFORE_LLM",
        trigger_terms=("rbac", "llm", "permissions", "evidence"),
        trigger_phrases=(
            "rbac-before-llm",
            "rbac before llm",
            "permissions before evidence",
            "before evidence reaches the llm",
        ),
        evidence_phrases=(
            "rbac-before-llm doctrine",
            "rbac-before-llm hardening",
            "rbac before llm",
            "user permissions must be enforced before evidence reaches the llm",
            "before evidence reaches the llm",
            "the model must not receive sensitive evidence",
            "authorised to view",
            "authorized to view",
        ),
        preferred_source_types=("PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
}


@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: str
    document_id: str
    chunk_index: int
    chunk_text: str
    title: str | None
    original_file_name: str
    source_type: str
    source_authority: int
    score: float
    matched_tokens: list[str] = field(default_factory=list)
    snippet: str = ""
    match_ratio: float = 0.0
    detected_intent: str | None = None
    matched_phrases: list[str] = field(default_factory=list)
    match_reason: str | None = None


def tokenize(text: str) -> list[str]:
    seen: set[str] = set()
    tokens: list[str] = []
    for token in re.split(r"\W+", text.lower()):
        if not token or token in STOPWORDS:
            continue
        if len(token) < 3 and token not in IMPORTANT_ACRONYMS:
            continue
        if token in seen:
            continue
        seen.add(token)
        tokens.append(token)
    return tokens


def _normalized_phrase(text: str) -> str:
    return " ".join(re.split(r"\s+", text.lower())).strip()


def classify_query_intent(query: str) -> QueryIntentDefinition | None:
    normalized = _normalized_phrase(query.replace("-", " "))
    compact = _normalized_phrase(query)
    for definition in INTENT_DEFINITIONS.values():
        if any(phrase in normalized or phrase in compact for phrase in definition.trigger_phrases):
            return definition
        if definition.name == "MINERVA_BOUNDARY_PROHIBITION":
            if ("minerva" in normalized or "llm" in normalized) and (
                "boundary" in normalized
                or "boundaries" in normalized
                or "not" in normalized
                or "must not" in normalized
                or "cannot" in normalized
            ):
                return definition
        if definition.name == "SEPARATE_DATABASE":
            if ("minerva" in normalized or "intelligence" in normalized or "ezeas" in normalized) and (
                "database" in normalized or "store" in normalized
            ):
                return definition
        if definition.name == "RBAC_BEFORE_LLM":
            if "rbac" in normalized and "llm" in normalized:
                return definition
    return None


def _snippet(text: str, matched_tokens: list[str], max_length: int = 260) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_length:
        return compact

    lower = compact.lower()
    first_match = min((lower.find(token) for token in matched_tokens if lower.find(token) >= 0), default=0)
    start = max(0, first_match - 80)
    end = min(len(compact), start + max_length)
    snippet = compact[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(compact):
        snippet += "..."
    return snippet


def _validate_source_types(source_types: list[str] | None) -> list[str] | None:
    if source_types is None:
        return None
    normalized = [normalize_source_type(source_type) for source_type in source_types]
    return sorted(set(normalized))


def _source_type_boost(source_type: str, query_tokens: list[str]) -> float:
    relevant_terms = SOURCE_TYPE_QUERY_BOOSTS.get(source_type, set())
    if not relevant_terms:
        return 0.0
    return min(3.0, len(set(query_tokens) & relevant_terms) * 1.25)


def _matched_intent_phrases(text: str, title: str, intent: QueryIntentDefinition | None) -> list[str]:
    if intent is None:
        return []
    combined = _normalized_phrase(f"{title}\n{text}".replace("-", " "))
    compact_combined = _normalized_phrase(f"{title}\n{text}")
    return [
        phrase
        for phrase in intent.evidence_phrases
        if phrase in combined or phrase in compact_combined
    ]


def _intent_phrase_score(text: str, title: str, matched_phrases: list[str]) -> tuple[float, str | None]:
    if not matched_phrases:
        return 0.0, None

    normalized_text = _normalized_phrase(text.replace("-", " "))
    normalized_title = _normalized_phrase(title.replace("-", " "))
    first_lines = "\n".join(text.splitlines()[:3]).lower().replace("-", " ")
    score = 0.0
    reasons: list[str] = []

    for phrase in matched_phrases:
        phrase_score = 18.0
        if phrase in normalized_title:
            phrase_score += 14.0
            reasons.append(f"matched {phrase} in document title")
        position = normalized_text.find(phrase)
        if 0 <= position <= 300:
            phrase_score += 10.0
            reasons.append(f"matched {phrase} near chunk start")
        if phrase in first_lines:
            phrase_score += 12.0
            reasons.append(f"matched {phrase} heading")
        score += phrase_score

    return score, reasons[0] if reasons else f"matched intent phrase {matched_phrases[0]}"


def _intent_source_boost(document: KnowledgeDocument, intent: QueryIntentDefinition | None) -> float:
    if intent is None:
        return 0.0
    boost = 0.0
    if document.SourceType in intent.preferred_source_types:
        boost += 8.0
    title = (document.Title or "").lower()
    if "platform doctrine" in title or "hardening doctrine" in title:
        boost += 6.0
    return boost


def retrieve_relevant_chunks(
    db: Session,
    query: str,
    tenant_id: str | None = None,
    top_k: int = 5,
    source_types: list[str] | None = None,
) -> list[RetrievalResult]:
    keywords = tokenize(query)
    intent = classify_query_intent(query)
    if not keywords and intent is None:
        return []
    normalized_source_types = _validate_source_types(source_types)
    query_phrase = _normalized_phrase(query)
    token_phrase = " ".join(keywords)

    stmt = (
        select(KnowledgeChunk)
        .options(joinedload(KnowledgeChunk.document))
        .join(KnowledgeDocument)
        .where(KnowledgeDocument.DocumentStatus == "ACTIVE")
    )
    if tenant_id is not None:
        stmt = stmt.where(or_(KnowledgeDocument.TenantId.is_(None), KnowledgeDocument.TenantId == tenant_id))
    else:
        stmt = stmt.where(KnowledgeDocument.TenantId.is_(None))
    if normalized_source_types is not None:
        stmt = stmt.where(KnowledgeDocument.SourceType.in_(normalized_source_types))

    scored: list[RetrievalResult] = []
    for chunk in db.scalars(stmt).all():
        text_lower = chunk.ChunkText.lower()
        title_lower = (chunk.document.Title or "").lower()
        document = chunk.document
        matched_phrases = _matched_intent_phrases(chunk.ChunkText, document.Title or "", intent)
        matched_tokens = [keyword for keyword in keywords if keyword in text_lower or keyword in title_lower]
        distinct_matches = len(matched_tokens)
        if distinct_matches <= 0 and not matched_phrases:
            continue
        exact_query_match = query_phrase and query_phrase in text_lower
        token_phrase_match = len(keywords) > 1 and token_phrase in text_lower
        title_matches = [keyword for keyword in keywords if keyword in title_lower]
        match_ratio = distinct_matches / len(keywords) if keywords else 0.0

        # Avoid noisy hits where a long query only overlaps one generic term such as "minerva".
        if (
            len(keywords) > 1
            and distinct_matches == 1
            and not matched_phrases
            and not exact_query_match
            and not title_matches
            and matched_tokens[0] not in IMPORTANT_ACRONYMS
        ):
            continue
        if intent and distinct_matches <= 1 and not matched_phrases and not title_matches:
            continue

        occurrence_count = sum(min(text_lower.count(keyword), 4) for keyword in keywords)
        title_score = (len(title_matches) * 3.0) + ((len(title_matches) / len(keywords)) * 4.0 if keywords else 0.0)
        phrase_score, match_reason = _intent_phrase_score(chunk.ChunkText, document.Title or "", matched_phrases)
        generic_only_penalty = 0.0
        if intent and distinct_matches <= 1 and not matched_phrases:
            generic_only_penalty = 8.0
        score = (
            occurrence_count
            + (distinct_matches * 5.0)
            + (match_ratio * 12.0)
            + title_score
            + (22.0 if exact_query_match else 0.0)
            + (14.0 if token_phrase_match else 0.0)
            + _source_type_boost(document.SourceType, keywords)
            + CAPABILITY_STATUS_BOOSTS.get(document.CapabilityStatus or "", 0.0)
            + (document.SourceAuthority / 25.0)
            + phrase_score
            + _intent_source_boost(document, intent)
            - generic_only_penalty
        )
        scored.append(
            RetrievalResult(
                chunk_id=chunk.KnowledgeChunkId,
                document_id=document.KnowledgeDocumentId,
                chunk_index=chunk.ChunkIndex,
                chunk_text=chunk.ChunkText,
                title=document.Title,
                original_file_name=document.OriginalFileName,
                source_type=document.SourceType,
                source_authority=document.SourceAuthority,
                score=score,
                matched_tokens=matched_tokens,
                snippet=_snippet(chunk.ChunkText, matched_tokens or matched_phrases),
                match_ratio=match_ratio,
                detected_intent=intent.name if intent else None,
                matched_phrases=matched_phrases,
                match_reason=match_reason,
            )
        )
    return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]
