from abc import ABC, abstractmethod

from app.services.knowledge_retrieval_service import RetrievalResult


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

        excerpts = []
        for result in retrieved_chunks[:3]:
            excerpts.append(_safe_excerpt(result.chunk_text))
        evidence_summary = " ".join(excerpts)
        return (
            "Based on the retrieved Minerva knowledge sources, "
            f"{evidence_summary} "
            "Minerva is advisory and does not calculate or change payroll truth."
        )
