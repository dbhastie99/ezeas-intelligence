from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any


APPROVAL_METADATA_FIELDS = [
    "approval_required",
    "approval_status",
    "approval_notes",
    "approved_file_count",
    "rejected_file_count",
]
REQUIRED_APPROVAL_FILE_FIELDS = [
    "proposed_ingestion_action",
    "review_notes",
    "review_status",
]


def build_code_evidence_approval_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    excluded_reasons = Counter(item.get("reason") for item in payload.get("excluded_files", []) if item.get("reason"))
    return {
        "repo_name": payload.get("repo_name"),
        "repo_path": payload.get("repo_path"),
        "repository_metadata": payload.get("repository_metadata"),
        "safety_summary": payload.get("safety_summary"),
        "validation_result": payload.get("validation_result"),
        **{field: payload.get(field) for field in APPROVAL_METADATA_FIELDS},
        "included_count": payload.get("included_count", 0),
        "excluded_count": payload.get("excluded_count", 0),
        "excluded_file_summary": {
            "excluded_count": payload.get("excluded_count", 0),
            "counts_by_reason": dict(excluded_reasons),
            "top_exclusion_reasons": payload.get("top_exclusion_reasons", []),
        },
        "included_files": [dict(item) for item in payload.get("included_files", [])],
    }


@dataclass(frozen=True)
class CodeEvidenceApprovalManifestReviewResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    approval_status: str | None = None
    approval_required: bool | None = None
    total_included_files: int = 0
    approved_file_count: int = 0
    rejected_file_count: int = 0
    pending_review_count: int = 0
    counts_by_review_status: dict[str, int] = field(default_factory=dict)
    counts_by_proposed_ingestion_action: dict[str, int] = field(default_factory=dict)
    counts_by_source_type: dict[str, int] = field(default_factory=dict)
    counts_by_file_kind: dict[str, int] = field(default_factory=dict)
    counts_by_language: dict[str, int] = field(default_factory=dict)
    validation_status: bool | None = None
    safety_summary_flags: dict[str, Any] = field(default_factory=dict)

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


def review_code_evidence_approval_manifest(payload: dict[str, Any]) -> CodeEvidenceApprovalManifestReviewResult:
    errors: list[str] = []
    included_files = _included_files(payload, errors)
    safety_summary = payload.get("safety_summary")
    validation_result = payload.get("validation_result")

    _validate_approval_manifest_shape(payload, included_files, safety_summary, validation_result, errors)

    review_status_counts = Counter(item.get("review_status") for item in included_files)
    action_counts = Counter(item.get("proposed_ingestion_action") for item in included_files)
    source_type_counts = Counter(item.get("source_type") for item in included_files)
    file_kind_counts = Counter(item.get("file_kind") for item in included_files)
    language_counts = Counter(item.get("language") for item in included_files)

    safety_flags = _safety_summary_flags(safety_summary if isinstance(safety_summary, dict) else {})
    return CodeEvidenceApprovalManifestReviewResult(
        is_valid=not errors,
        errors=errors,
        approval_status=payload.get("approval_status"),
        approval_required=payload.get("approval_required"),
        total_included_files=len(included_files),
        approved_file_count=int(payload.get("approved_file_count") or 0),
        rejected_file_count=int(payload.get("rejected_file_count") or 0),
        pending_review_count=review_status_counts.get("PENDING_REVIEW", 0),
        counts_by_review_status=_counter_dict(review_status_counts),
        counts_by_proposed_ingestion_action=_counter_dict(action_counts),
        counts_by_source_type=_counter_dict(source_type_counts),
        counts_by_file_kind=_counter_dict(file_kind_counts),
        counts_by_language=_counter_dict(language_counts),
        validation_status=validation_result.get("is_valid") if isinstance(validation_result, dict) else None,
        safety_summary_flags=safety_flags,
    )


def _included_files(payload: dict[str, Any], errors: list[str]) -> list[dict[str, Any]]:
    included_files = payload.get("included_files", [])
    if not isinstance(included_files, list):
        errors.append("included_files must be a list.")
        return []
    valid_items = []
    for index, item in enumerate(included_files):
        if not isinstance(item, dict):
            errors.append(f"included_files[{index}] must be an object.")
            continue
        valid_items.append(item)
    return valid_items


def _validate_approval_manifest_shape(
    payload: dict[str, Any],
    included_files: list[dict[str, Any]],
    safety_summary: Any,
    validation_result: Any,
    errors: list[str],
) -> None:
    if not isinstance(payload.get("repository_metadata"), dict):
        errors.append("repository_metadata is required.")
    if not isinstance(safety_summary, dict):
        errors.append("safety_summary is required.")
    else:
        expected_safety_flags = {
            "code_content_captured": False,
            "included_code_content_bytes": 0,
            "database_ingestion_performed": False,
            "llm_exposure_performed": False,
        }
        for field_name, expected_value in expected_safety_flags.items():
            if safety_summary.get(field_name) != expected_value:
                errors.append(f"safety_summary.{field_name} must be {expected_value!r}.")
    if not isinstance(validation_result, dict):
        errors.append("validation_result is required.")

    for field_name in APPROVAL_METADATA_FIELDS:
        if field_name not in payload:
            errors.append(f"{field_name} is required.")

    for index, item in enumerate(included_files):
        for field_name in REQUIRED_APPROVAL_FILE_FIELDS:
            if field_name not in item:
                errors.append(f"included_files[{index}].{field_name} is required.")
        if "review_notes" in item and not isinstance(item.get("review_notes"), list):
            errors.append(f"included_files[{index}].review_notes must be a list.")


def _safety_summary_flags(safety_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "code_content_captured": safety_summary.get("code_content_captured"),
        "included_code_content_bytes": safety_summary.get("included_code_content_bytes"),
        "database_ingestion_performed": safety_summary.get("database_ingestion_performed"),
        "llm_exposure_performed": safety_summary.get("llm_exposure_performed"),
    }


def _counter_dict(counter: Counter) -> dict[str, int]:
    return {key: count for key, count in counter.items() if key is not None}
