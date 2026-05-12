from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.services.domain_retrieval_plan_service import AWARD_POSITIONS_CLASSIFICATIONS_PLAN, EvidenceGroup
from app.services.knowledge_retrieval_service import RetrievalResult, retrieve_relevant_chunks


AWARD_POSITIONS_CLASSIFICATIONS_DIAGNOSTIC_GROUPS: tuple[EvidenceGroup, ...] = (
    *AWARD_POSITIONS_CLASSIFICATIONS_PLAN.evidence_groups,
    EvidenceGroup(
        group_id="minerva_boundaries_and_non_mutation_guardrails",
        label="Award Positions / Classifications Minerva boundaries and non-mutation guardrails",
        query_terms=(
            "Minerva does not classify workers",
            "change EmployeeAppointment WorksitePosition Position AwardPositionClass records",
            "select award classes at runtime",
            "interpret awards at runtime",
            "calculate payroll",
            "decide entitlements",
            "mutate payroll output",
            "determine finalisation readiness",
            "finalise PayRuns",
            "mutate operational workforce payroll award truth",
        ),
        required_terms_any=(
            "Minerva does not classify workers",
            "change EmployeeAppointment",
            "select award classes at runtime",
            "interpret awards at runtime",
            "calculate payroll",
            "decide entitlements",
            "mutate operational workforce",
        ),
        preferred_source_types=("DEVELOPER_LOG", "PLATFORM_DOCTRINE", "HARDENING_LOG"),
    ),
)


@dataclass(frozen=True)
class AwardPositionsClassificationsGroupCoverage:
    group_key: str
    group_label: str
    search_terms_used: list[str]
    matched_chunk_count: int
    matched_document_count: int
    matched_sources: list[dict]
    representative_matched_terms: list[str]
    coverage_status: str
    diagnostic_notes: list[str]

    def to_dict(self) -> dict:
        return {
            "group_key": self.group_key,
            "group_label": self.group_label,
            "search_terms_used": self.search_terms_used,
            "matched_chunk_count": self.matched_chunk_count,
            "matched_document_count": self.matched_document_count,
            "matched_sources": self.matched_sources,
            "representative_matched_terms": self.representative_matched_terms,
            "coverage_status": self.coverage_status,
            "diagnostic_notes": self.diagnostic_notes,
        }


@dataclass(frozen=True)
class AwardPositionsClassificationsCoverageReport:
    plan_id: str
    domain: str
    generated_at_utc: str
    total_evidence_groups: int
    coverage_counts: dict[str, int]
    corpus_document_count: int
    corpus_chunk_count: int
    groups: list[AwardPositionsClassificationsGroupCoverage]
    mutation_performed: bool = False
    live_llm_call_performed: bool = False
    operational_json_ingestion_performed: bool = False

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id,
            "domain": self.domain,
            "generated_at_utc": self.generated_at_utc,
            "total_evidence_groups": self.total_evidence_groups,
            "coverage_counts": self.coverage_counts,
            "corpus_document_count": self.corpus_document_count,
            "corpus_chunk_count": self.corpus_chunk_count,
            "mutation_performed": self.mutation_performed,
            "live_llm_call_performed": self.live_llm_call_performed,
            "operational_json_ingestion_performed": self.operational_json_ingestion_performed,
            "groups": [group.to_dict() for group in self.groups],
        }


def _term_in_text(term: str, text: str) -> bool:
    return term.lower() in text.lower()


def _matched_terms(group: EvidenceGroup, results: list[RetrievalResult]) -> list[str]:
    terms = list(dict.fromkeys([*group.query_terms, *group.required_terms_any]))
    matched: list[str] = []
    for term in terms:
        if any(_term_in_text(term, f"{result.title or ''}\n{result.chunk_text}") for result in results):
            matched.append(term)
    return matched


def _matched_sources(results: list[RetrievalResult]) -> list[dict]:
    sources: dict[str, dict] = {}
    for result in results:
        key = result.document_id
        if key not in sources:
            sources[key] = {
                "title": result.title,
                "source_type": result.source_type,
                "original_file_name": result.original_file_name,
                "matched_chunk_count": 0,
            }
        sources[key]["matched_chunk_count"] += 1
    return sorted(
        sources.values(),
        key=lambda item: (str(item["title"] or "").lower(), str(item["source_type"]).lower()),
    )


def _coverage_status(matched_chunk_count: int, matched_document_count: int, matched_term_count: int) -> str:
    if matched_chunk_count == 0 or matched_term_count == 0:
        return "MISSING"
    if matched_document_count >= 2 and matched_term_count >= 2:
        return "STRONG"
    if matched_chunk_count >= 2 and matched_term_count >= 3:
        return "STRONG"
    return "WEAK"


def _diagnostic_notes(status: str, matched_term_count: int, matched_document_count: int) -> list[str]:
    if status == "STRONG":
        return [
            f"Found support across {matched_document_count} document(s).",
            f"Matched {matched_term_count} planned term(s) for this evidence group.",
        ]
    if status == "WEAK":
        return [
            "Some formal-corpus support was found, but breadth is limited.",
            "Refine retrieval or synthesis before widening Award Positions / Classifications claims.",
        ]
    return [
        "No useful formal-corpus support was found for this evidence group.",
        "Answers should state that the loaded formal corpus is insufficient for this group.",
    ]


def _count_active_documents(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(KnowledgeDocument).where(KnowledgeDocument.DocumentStatus == "ACTIVE")) or 0


def _count_active_chunks(db: Session) -> int:
    stmt = (
        select(func.count())
        .select_from(KnowledgeChunk)
        .join(KnowledgeDocument)
        .where(KnowledgeDocument.DocumentStatus == "ACTIVE")
    )
    return db.scalar(stmt) or 0


def scan_award_positions_classifications_corpus_coverage(
    db: Session,
    top_k_per_group: int = 10,
    tenant_id: str | None = None,
) -> AwardPositionsClassificationsCoverageReport:
    group_reports: list[AwardPositionsClassificationsGroupCoverage] = []
    coverage_counts = {"STRONG": 0, "WEAK": 0, "MISSING": 0}

    for group in AWARD_POSITIONS_CLASSIFICATIONS_DIAGNOSTIC_GROUPS:
        results = retrieve_relevant_chunks(
            db=db,
            query=" ".join(group.query_terms),
            tenant_id=tenant_id,
            top_k=top_k_per_group,
            source_types=list(group.preferred_source_types),
            include_samples=False,
        )
        useful_results = [
            result
            for result in results
            if any(_term_in_text(term, f"{result.title or ''}\n{result.chunk_text}") for term in group.required_terms_any)
        ]
        matched_terms = _matched_terms(group, useful_results)
        sources = _matched_sources(useful_results)
        status = _coverage_status(len(useful_results), len(sources), len(matched_terms))
        coverage_counts[status] += 1
        group_reports.append(
            AwardPositionsClassificationsGroupCoverage(
                group_key=group.group_id,
                group_label=group.label,
                search_terms_used=list(group.query_terms),
                matched_chunk_count=len(useful_results),
                matched_document_count=len(sources),
                matched_sources=sources,
                representative_matched_terms=matched_terms[:12],
                coverage_status=status,
                diagnostic_notes=_diagnostic_notes(status, len(matched_terms), len(sources)),
            )
        )

    return AwardPositionsClassificationsCoverageReport(
        plan_id=AWARD_POSITIONS_CLASSIFICATIONS_PLAN.plan_id,
        domain=AWARD_POSITIONS_CLASSIFICATIONS_PLAN.domain,
        generated_at_utc=datetime.now(UTC).isoformat(),
        total_evidence_groups=len(AWARD_POSITIONS_CLASSIFICATIONS_DIAGNOSTIC_GROUPS),
        coverage_counts=coverage_counts,
        corpus_document_count=_count_active_documents(db),
        corpus_chunk_count=_count_active_chunks(db),
        groups=group_reports,
    )
