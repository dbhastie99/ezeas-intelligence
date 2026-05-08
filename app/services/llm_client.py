from abc import ABC, abstractmethod

from app.services.answer_mode_service import AnswerMode, classify_answer_mode
from app.services.domain_retrieval_plan_service import detect_domain_retrieval_plan
from app.services.evidence_group_synthesis_service import EvidenceGroupSummary, synthesize_domain_plan_evidence
from app.services.knowledge_retrieval_service import RetrievalResult, classify_query_intent


def _safe_excerpt(text: str, max_length: int = 350) -> str:
    snippet = " ".join(text.split())
    if len(snippet) <= max_length:
        return snippet

    truncated = snippet[:max_length].rstrip()
    sentence_end = max(truncated.rfind("."), truncated.rfind("?"), truncated.rfind("!"))
    if sentence_end >= max_length // 2:
        return truncated[: sentence_end + 1]

    word_end = truncated.rfind(" ")
    if word_end > 0:
        return truncated[:word_end].rstrip() + "..."
    return truncated + "..."


def _coverage_label(strong_count: int, total_count: int) -> str:
    if strong_count == total_count and total_count > 0:
        return "complete"
    if strong_count >= max(1, total_count // 2):
        return "partial"
    return "weak"


def _evidence_basis_text(planned_chunks: list[RetrievalResult], strong_summaries: list[EvidenceGroupSummary]) -> str:
    source_parts: list[str] = []
    for result in planned_chunks:
        title = result.title or result.original_file_name
        source_part = f"{result.evidence_group_label}: {title} ({result.source_type})"
        if source_part not in source_parts:
            source_parts.append(source_part)
    group_text = ", ".join(summary.label for summary in strong_summaries) or "none"
    source_text = "; ".join(source_parts[:7]) if source_parts else "none"
    return f"Evidence groups used: {group_text}. Top source references: {source_text}."


class BaseLLMClient(ABC):
    model_name = "BASE_LLM"

    @abstractmethod
    def generate_answer(self, question: str, retrieved_chunks: list[RetrievalResult]) -> str:
        raise NotImplementedError


class StubLLMClient(BaseLLMClient):
    model_name = "STUB_LLM"

    def generate_answer(self, question: str, retrieved_chunks: list[RetrievalResult]) -> str:
        answer_mode = classify_answer_mode(question)
        if not retrieved_chunks:
            return (
                "I do not have retrieved Minerva knowledge evidence for that question. "
                "Minerva is advisory and does not calculate or change payroll truth."
            )

        intent = classify_query_intent(question)
        strong_chunks = [
            result
            for result in retrieved_chunks
            if result.score >= 18.0 and (result.match_ratio >= 0.45 or len(result.matched_tokens) >= 2 or result.matched_phrases)
        ]

        if intent and strong_chunks:
            if intent.name == "MINERVA_BOUNDARY_PROHIBITION":
                return (
                    "Minerva is not allowed to calculate payroll, determine entitlements, interpret awards at runtime, "
                    "approve exceptions, suppress warnings, override payroll outcomes, mutate configuration, finalise "
                    "PayRuns or become payroll calculation truth. It may search, retrieve, summarise, compare, explain "
                    "and interrogate evidence. Deterministic Ezeas services remain the source of payroll, award, leave, "
                    "tax, reconciliation and finalisation truth. Minerva is advisory and does not calculate or change "
                    "payroll truth."
                )
            if intent.name == "RBAC_BEFORE_LLM":
                return (
                    "RBAC-before-LLM means user permissions must be checked before evidence is retrieved into model "
                    "context. The model must not receive sensitive evidence that the user is not authorised to view. "
                    "Permission enforcement must happen before context construction, not after answer generation. "
                    "Minerva is advisory and does not calculate or change payroll truth."
                )
            if intent.name == "SEPARATE_DATABASE":
                return (
                    "Minerva uses a separate database so knowledge indexing, chat history, extracted facts, evidence "
                    "references and AI audit records are isolated from the operational payroll database. The operational "
                    "Ezeas database remains the authoritative source of payroll, leave, award, workforce and "
                    "reconciliation truth. Minerva is advisory and does not calculate or change payroll truth."
                )
            if intent.name == "NO_RAW_JSON_BY_DEFAULT":
                return (
                    "Raw JSON is not sent to the LLM by default because operational payroll evidence can contain "
                    "sensitive worker, payroll, tax, leave, bank/payment and correction data. It should be registered, "
                    "hashed, classified and extracted into facts or safe summaries first, then only the minimum "
                    "necessary evidence should be sent after tenant, RBAC and redaction controls. Minerva remains "
                    "read-only and advisory."
                )
            if intent.name == "SOURCE_AUTHORITY":
                return (
                    "Source authority matters because formal Platform Doctrine, Hardening Logs and Developer Logs "
                    "represent governed platform memory. Raw chat history and exploratory discussion can support an "
                    "answer, but must not override formal logged decisions, doctrine or implemented capability evidence. "
                    "Minerva remains read-only and advisory."
                )
            if intent.name == "DEVELOPER_LOGS_ROLE":
                return (
                    "Developer Logs are part of Minerva's formal knowledge corpus. They preserve implementation "
                    "decisions, rationale, current state, hardening commitments and operating model so Minerva can "
                    "explain how the platform works and why decisions were made. Minerva remains read-only and advisory."
                )
            if intent.name == "USER_GUIDE_RATIONALE":
                return (
                    "The User Guide / Rationale and Operating Model section exists to explain why the work matters, "
                    "how the feature should be understood, and how the platform should operate. It makes each thread's "
                    "reasoning easier for Minerva and future users to retrieve and explain later. Minerva remains "
                    "read-only and advisory."
                )
            if intent.name == "CHAT_HISTORY_AUTHORITY":
                return (
                    "Platform Doctrine is formal governed doctrine. Chat history is useful supporting material because "
                    "it may contain exploration, abandoned ideas, corrections and superseded thinking. Chat history "
                    "must not override Platform Doctrine, Hardening Logs or Developer Logs where they conflict. "
                    "Minerva remains read-only and advisory."
                )

        strong_chunks = [
            result
            for result in retrieved_chunks
            if result.score >= 18.0 and (result.match_ratio >= 0.45 or len(result.matched_tokens) >= 2)
        ]
        selected_chunks = (strong_chunks or retrieved_chunks)[:3]
        excerpts = [_safe_excerpt(result.chunk_text, max_length=260) for result in selected_chunks]

        if answer_mode == AnswerMode.PRODUCT_DOMAIN.value:
            domain_plan = detect_domain_retrieval_plan(question)
            planned_chunks = [result for result in retrieved_chunks if result.domain_plan_id]
            if domain_plan:
                summaries = synthesize_domain_plan_evidence(domain_plan, planned_chunks)
                strong_summaries = [summary for summary in summaries if not summary.is_weak]
                weak_summaries = [summary for summary in summaries if summary.is_weak]
                operation_points = [summary.sentence for summary in summaries]
                missing_groups = [summary.label for summary in weak_summaries]
                coverage = _coverage_label(len(strong_summaries), len(summaries))

                if coverage == "weak":
                    return (
                        "Direct summary\n"
                        "The retrieved formal corpus is not yet sufficient to answer this at the required rich-answer "
                        "standard.\n\n"
                        "How the system works\n"
                        "The loaded formal corpus does not yet contain enough retrieved evidence for the Annual Leave "
                        "management evidence groups.\n\n"
                        "Current implementation status\n"
                        "Unknown from the currently retrieved formal corpus.\n\n"
                        "What remains outstanding\n"
                        f"The loaded formal corpus does not yet contain enough retrieved evidence for: "
                        f"{', '.join(missing_groups)}.\n\n"
                        "Evidence basis\n"
                        "Use the returned source references as the evidence trail. Minerva is advisory and does not "
                        "calculate or change payroll truth."
                    )

                missing_text = (
                    "The loaded formal corpus does not yet contain enough retrieved evidence for: "
                    f"{', '.join(missing_groups)}."
                    if missing_groups
                    else "All planned evidence groups returned at least one source."
                )
                if coverage == "complete":
                    direct_summary = (
                        "Annual Leave is managed through configured leave policy, ledger-based accrual and TAKEN "
                        "movement, PayRun valuation/orchestration evidence, Worker Story explanation and tracked "
                        "hardening items. The system separates configuration, accrual, consumption, valuation, PayRun "
                        "processing and explanatory evidence rather than treating leave as a single opaque balance."
                    )
                    status_text = (
                        "The retrieved corpus shows this as an implemented or partially implemented platform area with "
                        "remaining hardening. It does not prove production completeness. Some mechanisms are implemented; "
                        "valuation, leave source modelling or production hardening may remain outstanding depending on "
                        "the specific sub-area."
                    )
                else:
                    direct_summary = (
                        "Annual Leave is partially described by the loaded formal corpus, but some planned evidence "
                        "groups are missing. The answer below is limited to the retrieved evidence and should be treated "
                        "as incomplete until the missing groups are covered."
                    )
                    status_text = (
                        "The retrieved corpus provides partial implementation evidence only. Missing groups should be "
                        "treated as unknown rather than inferred."
                    )
                evidence_basis = _evidence_basis_text(planned_chunks, strong_summaries)
                return (
                    "Direct summary\n"
                    f"{direct_summary}\n\n"
                    "How the system works\n"
                    f"{' '.join(operation_points)}\n\n"
                    "Current implementation status\n"
                    f"{status_text}\n\n"
                    "What remains outstanding\n"
                    f"{missing_text} Outstanding hardening remains wherever formal logs identify future work or where "
                    "an evidence group is weak.\n\n"
                    "Evidence basis\n"
                    f"{evidence_basis} Use the returned source references as the evidence trail. Minerva is advisory "
                    "and does not calculate or change payroll truth."
                )

            if not strong_chunks:
                return (
                    "The retrieved formal corpus is not yet sufficient to answer this at the required rich-answer "
                    "standard. The closest evidence says: "
                    f"{' '.join(excerpts[:2])} "
                    "Minerva is advisory and does not calculate or change payroll truth."
                )
            evidence = " ".join(excerpts[:3])
            return (
                "Direct summary\n"
                "Based on the retrieved formal Minerva knowledge sources, this product-domain answer is grounded in "
                "the strongest available evidence.\n\n"
                "How the system works\n"
                f"{evidence}\n\n"
                "Current implementation status\n"
                "The answer reflects only the retrieved formal corpus and does not infer operational payroll truth.\n\n"
                "What remains outstanding\n"
                "Any missing implementation status or hardening details should be treated as unknown until supported "
                "by formal doctrine, hardening logs or Developer Logs.\n\n"
                "Evidence basis\n"
                "Use the returned source references as the evidence trail. Minerva is advisory and does not calculate "
                "or change payroll truth."
            )

        if not strong_chunks:
            return (
                "The retrieved Minerva evidence is weak or mixed for this question. "
                f"The closest sources say: {' '.join(excerpts[:2])} "
                "Minerva is advisory and does not calculate or change payroll truth."
            )

        formatted_evidence = " ".join(excerpts)
        return (
            "Based on the retrieved Minerva knowledge sources, using the strongest matches, "
            f"{formatted_evidence} "
            "Minerva is advisory and does not calculate or change payroll truth."
        )
