import re
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path


@dataclass(frozen=True)
class DocumentMetadata:
    inferred_title: str
    detected_document_date: date | None = None
    detected_project: str | None = None
    detected_phase: str | None = None
    detected_developer: str | None = None
    source_label: str | None = None

    def model_dump(self) -> dict:
        data = asdict(self)
        if self.detected_document_date is not None:
            data["detected_document_date"] = self.detected_document_date.isoformat()
        return data


DATE_PATTERNS = [
    re.compile(r"^Date:\s*(?P<date>\d{1,2}\s+[A-Za-z]+\s+\d{4})$", re.IGNORECASE),
    re.compile(r"(Developer Log|Hardening Log|Platform Doctrine)\s+[-—]\s+Additive Entry\s+[-—]\s+(?P<date>\d{1,2}\s+[A-Za-z]+\s+\d{4})", re.IGNORECASE),
]


def _parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value.strip(), "%d %B %Y").date()
    except ValueError:
        try:
            return datetime.strptime(value.strip(), "%d %b %Y").date()
        except ValueError:
            return None


def _first_heading(text: str) -> str | None:
    for line in text.splitlines():
        candidate = line.strip().strip("#").strip()
        if candidate:
            return candidate[:255]
    return None


def _line_value(text: str, label: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(label)}:\s*(?P<value>.+)$", re.IGNORECASE)
    for line in text.splitlines():
        match = pattern.match(line.strip())
        if match:
            return match.group("value").strip()
    return None


def _detect_date(text: str) -> date | None:
    for line in text.splitlines():
        stripped = line.strip()
        for pattern in DATE_PATTERNS:
            match = pattern.search(stripped)
            if match:
                parsed = _parse_date(match.group("date"))
                if parsed:
                    return parsed
    return None


def _source_label(source_type: str | None, title: str | None, file_name: str) -> str | None:
    haystack = f"{source_type or ''} {title or ''} {file_name}".lower()
    if "developer log" in haystack or source_type == "DEVELOPER_LOG":
        return "Developer Log"
    if "hardening log" in haystack or source_type == "HARDENING_LOG":
        return "Hardening Log"
    if "platform doctrine" in haystack or source_type == "PLATFORM_DOCTRINE":
        return "Platform Doctrine"
    if source_type:
        return source_type
    return None


def extract_document_metadata(
    text: str,
    file_name: str,
    source_type: str | None = None,
    supplied_title: str | None = None,
) -> DocumentMetadata:
    inferred_title = supplied_title or Path(file_name).stem
    heading = _first_heading(text)
    if not supplied_title and heading and any(marker in heading.lower() for marker in ("developer log", "hardening log", "platform doctrine")):
        inferred_title = heading

    return DocumentMetadata(
        inferred_title=inferred_title,
        detected_document_date=_detect_date(text),
        detected_project=_line_value(text, "Project"),
        detected_phase=_line_value(text, "Phase"),
        detected_developer=_line_value(text, "Developer"),
        source_label=_source_label(source_type, supplied_title or heading, file_name),
    )
