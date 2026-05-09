from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


REQUIRED_INCLUDED_FILE_FIELDS = {
    "classification_reason",
    "file_kind",
    "file_path",
    "language",
    "repo_name",
    "repo_path",
    "source_type",
}
UNSAFE_PATH_FRAGMENTS = {
    ".env",
    ".git",
    ".venv",
    "__pycache__",
    "credential",
    "key",
    "node_modules",
    "private",
    "secret",
    "token",
    "venv",
}


@dataclass(frozen=True)
class CodeEvidenceManifestValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_at_utc: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    included_file_count: int = 0
    excluded_file_count: int = 0

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


def validate_code_evidence_manifest(payload: dict[str, Any]) -> CodeEvidenceManifestValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    included_files = _list_field(payload, "included_files", errors)
    excluded_files = _list_field(payload, "excluded_files", errors)

    if "repository_metadata" not in payload or not isinstance(payload.get("repository_metadata"), dict):
        errors.append("repository_metadata is required.")

    safety_summary = payload.get("safety_summary")
    if not isinstance(safety_summary, dict):
        errors.append("safety_summary is required.")
    else:
        _validate_safety_summary(safety_summary, errors)

    _validate_included_files(included_files, errors)
    _validate_counts(payload, included_files, errors)

    return CodeEvidenceManifestValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=warnings,
        included_file_count=len(included_files),
        excluded_file_count=len(excluded_files),
    )


def _list_field(payload: dict[str, Any], field_name: str, errors: list[str]) -> list[dict[str, Any]]:
    value = payload.get(field_name, [])
    if not isinstance(value, list):
        errors.append(f"{field_name} must be a list.")
        return []
    invalid_indexes = [index for index, item in enumerate(value) if not isinstance(item, dict)]
    for index in invalid_indexes:
        errors.append(f"{field_name}[{index}] must be an object.")
    return [item for item in value if isinstance(item, dict)]


def _validate_safety_summary(safety_summary: dict[str, Any], errors: list[str]) -> None:
    expected_values = {
        "code_content_captured": False,
        "included_code_content_bytes": 0,
        "database_ingestion_performed": False,
        "llm_exposure_performed": False,
    }
    for field_name, expected_value in expected_values.items():
        if safety_summary.get(field_name) != expected_value:
            errors.append(f"safety_summary.{field_name} must be {expected_value!r}.")


def _validate_included_files(included_files: list[dict[str, Any]], errors: list[str]) -> None:
    for index, item in enumerate(included_files):
        missing_fields = sorted(field for field in REQUIRED_INCLUDED_FILE_FIELDS if not item.get(field))
        for field_name in missing_fields:
            errors.append(f"included_files[{index}].{field_name} is required.")

        file_path = str(item.get("file_path", ""))
        unsafe_fragment = _unsafe_path_fragment(file_path)
        if unsafe_fragment is not None:
            errors.append(f"included_files[{index}].file_path contains unsafe fragment: {unsafe_fragment}.")


def _validate_counts(payload: dict[str, Any], included_files: list[dict[str, Any]], errors: list[str]) -> None:
    expected_counts = {
        "counts_by_source_type": Counter(item.get("source_type") for item in included_files),
        "counts_by_language": Counter(item.get("language") for item in included_files),
        "counts_by_file_kind": Counter(item.get("file_kind") for item in included_files),
    }
    for field_name, counter in expected_counts.items():
        actual = payload.get(field_name)
        expected = {key: count for key, count in counter.items() if key}
        if actual != expected:
            errors.append(f"{field_name} does not reconcile with included_files.")


def _unsafe_path_fragment(file_path: str) -> str | None:
    normalized = file_path.replace("\\", "/").lower()
    for fragment in sorted(UNSAFE_PATH_FRAGMENTS):
        if fragment in normalized:
            return fragment
    return None
