import re
from dataclasses import dataclass, field

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import normalize_source_type
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument

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
}
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


def retrieve_relevant_chunks(
    db: Session,
    query: str,
    tenant_id: str | None = None,
    top_k: int = 5,
    source_types: list[str] | None = None,
) -> list[RetrievalResult]:
    keywords = tokenize(query)
    if not keywords:
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
        matched_tokens = [keyword for keyword in keywords if keyword in text_lower or keyword in title_lower]
        distinct_matches = len(matched_tokens)
        if distinct_matches <= 0:
            continue
        document = chunk.document
        exact_query_match = query_phrase and query_phrase in text_lower
        token_phrase_match = len(keywords) > 1 and token_phrase in text_lower
        title_matches = [keyword for keyword in keywords if keyword in title_lower]
        match_ratio = distinct_matches / len(keywords)

        # Avoid noisy hits where a long query only overlaps one generic term such as "minerva".
        if (
            len(keywords) > 1
            and distinct_matches == 1
            and not exact_query_match
            and not title_matches
            and matched_tokens[0] not in IMPORTANT_ACRONYMS
        ):
            continue

        occurrence_count = sum(min(text_lower.count(keyword), 4) for keyword in keywords)
        title_score = (len(title_matches) * 3.0) + ((len(title_matches) / len(keywords)) * 4.0)
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
                snippet=_snippet(chunk.ChunkText, matched_tokens),
                match_ratio=match_ratio,
            )
        )
    return sorted(scored, key=lambda result: result.score, reverse=True)[:top_k]
