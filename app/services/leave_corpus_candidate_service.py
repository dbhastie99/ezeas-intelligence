import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from app.core.enums import SourceType
from app.services.document_extraction_service import extract_text
from app.services.document_metadata_service import extract_document_metadata


LEAVE_DOMAIN_TERMS = [
    "Annual Leave",
    "LeaveType",
    "LeaveTypeRule",
    "LeaveTypeKind",
    "Rule Cockpit",
    "LeaveLedger",
    "accrual",
    "TAKEN",
    "DeductsOnPublicHoliday",
    "public holiday",
    "valuation basis",
    "Worker Story",
    "Leave and Accrual Outcome",
    "PayRun",
    "Leave Source Model",
    "interpreter truth",
    "no fallback",
]
SUPPORTED_CANDIDATE_EXTENSIONS = {".txt", ".docx"}


@dataclass(frozen=True)
class LeaveCorpusCandidate:
    path: str
    score: int
    matched_terms: list[str]
    inferred_title: str
    source_type: str
    detected_document_date: str | None = None

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LeaveCorpusScanResult:
    candidates: list[LeaveCorpusCandidate]
    warnings: list[str]

    def model_dump(self) -> dict[str, Any]:
        return {
            "candidates": [candidate.model_dump() for candidate in self.candidates],
            "warnings": self.warnings,
        }


def score_leave_candidate_text(text: str, path: str | Path = "") -> tuple[int, list[str]]:
    haystack = f"{path}\n{text}".lower()
    matched_terms = [term for term in LEAVE_DOMAIN_TERMS if term.lower() in haystack]
    return len(matched_terms), matched_terms


def infer_source_type(path: str | Path, title: str | None = None) -> str:
    haystack = f"{path} {title or ''}".lower().replace("_", " ").replace("-", " ")
    if "hardening" in haystack:
        return SourceType.HARDENING_LOG.value
    if "platform doctrine" in haystack:
        return SourceType.PLATFORM_DOCTRINE.value
    if "doctrine" in haystack:
        return SourceType.OTHER.value
    if "developer log" in haystack or "dev log" in haystack or "developer_log" in haystack or "dev_log" in haystack:
        return SourceType.DEVELOPER_LOG.value
    return SourceType.DEVELOPER_LOG.value


def _candidate_from_path(path: Path) -> LeaveCorpusCandidate:
    text = extract_text(path.read_bytes(), path.name)
    source_type = infer_source_type(path)
    metadata = extract_document_metadata(text=text, file_name=path.name, source_type=source_type)
    source_type = infer_source_type(path, metadata.inferred_title)
    score, matched_terms = score_leave_candidate_text(text, path)
    detected_date = metadata.detected_document_date.isoformat() if metadata.detected_document_date else None
    return LeaveCorpusCandidate(
        path=str(path),
        score=score,
        matched_terms=matched_terms,
        inferred_title=metadata.inferred_title,
        source_type=source_type,
        detected_document_date=detected_date,
    )


def scan_leave_corpus_candidates(folder_path: str | Path, top: int | None = None) -> LeaveCorpusScanResult:
    root = Path(folder_path)
    if not root.exists() or not root.is_dir():
        raise ValueError("folder_path must be an existing directory.")

    candidates: list[LeaveCorpusCandidate] = []
    warnings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_CANDIDATE_EXTENSIONS:
            continue
        try:
            candidates.append(_candidate_from_path(path))
        except Exception as exc:
            warnings.append(f"{path}: {exc}")

    ranked = sorted(candidates, key=lambda item: (-item.score, item.path.lower()))
    if top is not None:
        ranked = ranked[:top]
    return LeaveCorpusScanResult(candidates=ranked, warnings=warnings)


def _manifest_path_for_candidate(candidate_path: Path, output_manifest_path: Path) -> str:
    try:
        return os.path.relpath(candidate_path, start=output_manifest_path.parent).replace("\\", "/")
    except ValueError:
        return str(candidate_path)


def build_leave_manifest_from_candidates(
    folder_path: str | Path,
    output_manifest_path: str | Path,
    min_score: int = 3,
) -> dict[str, Any]:
    output_path = Path(output_manifest_path)
    scan_result = scan_leave_corpus_candidates(folder_path)
    included = [candidate for candidate in scan_result.candidates if candidate.score >= min_score]
    skipped = [candidate for candidate in scan_result.candidates if candidate.score < min_score]
    documents = [
        {
            "path": _manifest_path_for_candidate(Path(candidate.path), output_path),
            "source_type": candidate.source_type,
            "capability_status": (
                "OUTSTANDING_HARDENING" if candidate.source_type == SourceType.HARDENING_LOG.value else "IMPLEMENTED"
            ),
            "title": candidate.inferred_title or Path(candidate.path).stem,
        }
        for candidate in included
    ]
    manifest = {
        "default_source_type": SourceType.DEVELOPER_LOG.value,
        "default_capability_status": "IMPLEMENTED",
        "default_tenant_id": None,
        "documents": documents,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {
        "manifest": manifest,
        "included_count": len(included),
        "skipped_count": len(skipped),
        "warnings": scan_result.warnings,
        "output_path": str(output_path),
    }
