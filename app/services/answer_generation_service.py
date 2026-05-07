from app.schemas.common import SourceReference
from app.services.knowledge_retrieval_service import RetrievalResult
from app.services.llm_client import BaseLLMClient, StubLLMClient


PROMPT_POLICY = "MINERVA_V0_GROUNDED_READ_ONLY"


def build_source_references(results: list[RetrievalResult]) -> list[SourceReference]:
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
        )
        for result in results
    ]


def generate_grounded_answer(
    question: str,
    retrieved_chunks: list[RetrievalResult],
    llm_client: BaseLLMClient | None = None,
) -> tuple[str, list[SourceReference], str, str]:
    client = llm_client or StubLLMClient()
    sources = build_source_references(retrieved_chunks)
    response_text = client.generate_answer(question, retrieved_chunks)
    return response_text, sources, client.model_name, PROMPT_POLICY
