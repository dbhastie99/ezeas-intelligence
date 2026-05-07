from abc import ABC, abstractmethod

from app.services.knowledge_retrieval_service import RetrievalResult


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
            snippet = " ".join(result.chunk_text.split())
            excerpts.append(snippet[:350])
        evidence_summary = " ".join(excerpts)
        return (
            "Based on the retrieved Minerva knowledge sources, "
            f"{evidence_summary} "
            "Minerva is advisory and does not calculate or change payroll truth."
        )
