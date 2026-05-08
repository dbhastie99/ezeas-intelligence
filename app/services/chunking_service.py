from dataclasses import dataclass
import re


@dataclass(frozen=True)
class TextChunk:
    index: int
    text: str
    token_estimate: int
    source_section: str | None = None


HEADING_PATTERNS = [
    re.compile(r"^platform doctrine\b", re.IGNORECASE),
    re.compile(r".*\bdoctrine$", re.IGNORECASE),
    re.compile(r".*\bhardening$", re.IGNORECASE),
    re.compile(r".*\bdecision$", re.IGNORECASE),
    re.compile(r".*\bobjectives$", re.IGNORECASE),
    re.compile(r".*\bwork completed$", re.IGNORECASE),
    re.compile(r".*\bissues encountered$", re.IGNORECASE),
    re.compile(r".*\bcurrent state$", re.IGNORECASE),
    re.compile(r".*\bstill to do / do not lose$", re.IGNORECASE),
    re.compile(r".*\buser guide / rationale and operating model$", re.IGNORECASE),
    re.compile(r".*\bdeveloper log\b.*", re.IGNORECASE),
    re.compile(r".*\bhardening log\b.*", re.IGNORECASE),
]


def is_heading_like(line: str) -> bool:
    candidate = line.strip().strip("#").strip()
    if not candidate or len(candidate) > 180:
        return False
    return any(pattern.match(candidate) for pattern in HEADING_PATTERNS)


def detect_heading_positions(text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        clean_line = line.strip().strip("#").strip()
        if is_heading_like(clean_line):
            headings.append((offset, clean_line))
        offset += len(line)
    return headings


def source_section_for_range(headings: list[tuple[int, str]], start: int, end: int) -> str | None:
    section = None
    for position, heading in headings:
        if position > end:
            break
        if position <= end:
            section = heading
    return section


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 150) -> list[TextChunk]:
    normalized = text.strip()
    if not normalized:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be zero or greater and less than chunk_size")

    chunks: list[TextChunk] = []
    headings = detect_heading_positions(normalized)
    start = 0
    index = 0
    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(
                TextChunk(
                    index=index,
                    text=chunk,
                    token_estimate=max(1, len(chunk) // 4),
                    source_section=source_section_for_range(headings, start, end),
                )
            )
            index += 1
        if end == len(normalized):
            break
        start = end - overlap
    return chunks
