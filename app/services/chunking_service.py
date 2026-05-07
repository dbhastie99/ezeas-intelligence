from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    token_estimate: int


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 150) -> list[TextChunk]:
    normalized = text.strip()
    if not normalized:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be zero or greater and less than chunk_size")

    chunks: list[TextChunk] = []
    start = 0
    index = 0
    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(TextChunk(index=index, text=chunk, token_estimate=max(1, len(chunk) // 4)))
            index += 1
        if end == len(normalized):
            break
        start = end - overlap
    return chunks
