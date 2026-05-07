from abc import ABC, abstractmethod

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


class BaseLLMClient(ABC):
    model_name = "BASE_LLM"

    @abstractmethod
    def generate_answer(self, question: str, retrieved_chunks: list[RetrievalResult]) -> str:
        raise NotImplementedError


class StubLLMClient(BaseLLMClient):
    model_name = "STUB_LLM"

    def generate_answer(self, question: str, retrieved_chunks: list[RetrievalResult]) -> str:
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

        strong_chunks = [
            result
            for result in retrieved_chunks
            if result.score >= 18.0 and (result.match_ratio >= 0.45 or len(result.matched_tokens) >= 2)
        ]
        selected_chunks = (strong_chunks or retrieved_chunks)[:3]
        excerpts = [_safe_excerpt(result.chunk_text, max_length=260) for result in selected_chunks]

        if not strong_chunks:
            return (
                "The retrieved Minerva evidence is weak or mixed for this question. "
                f"The closest sources say: {' '.join(excerpts[:2])} "
                "Minerva is advisory and does not calculate or change payroll truth."
            )

        formatted_evidence = " ".join(f"Source {index + 1}: {excerpt}" for index, excerpt in enumerate(excerpts))
        return (
            "Based on the retrieved Minerva knowledge sources, using the strongest matches, "
            f"{formatted_evidence} "
            "Minerva is advisory and does not calculate or change payroll truth."
        )
