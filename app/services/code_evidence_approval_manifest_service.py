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
VALID_REVIEW_STATUSES = {"APPROVED", "PENDING_REVIEW", "REJECTED"}
VALID_PROPOSED_INGESTION_ACTIONS = {"DO_NOT_INGEST_YET", "INGEST_METADATA_ONLY"}


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


@dataclass(frozen=True)
class CodeEvidenceApprovalManifestUpdateResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    file_path: str | None = None
    review_status: str | None = None
    proposed_ingestion_action: str | None = None
    approved_file_count: int = 0
    rejected_file_count: int = 0
    pending_review_count: int = 0
    approval_status: str | None = None

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


def update_code_evidence_approval_manifest(
    payload: dict[str, Any],
    file_path: str,
    review_status: str,
    proposed_ingestion_action: str,
    notes: list[str] | None = None,
) -> tuple[dict[str, Any], CodeEvidenceApprovalManifestUpdateResult]:
    errors = _update_request_errors(review_status, proposed_ingestion_action)
    review_result = review_code_evidence_approval_manifest(payload)
    errors.extend(review_result.errors)
    if errors:
        return payload, CodeEvidenceApprovalManifestUpdateResult(is_valid=False, errors=errors)

    matching_files = [item for item in payload.get("included_files", []) if item.get("file_path") == file_path]
    if len(matching_files) != 1:
        return payload, CodeEvidenceApprovalManifestUpdateResult(
            is_valid=False,
            errors=[f"Expected exactly one included file matching file_path {file_path!r}; found {len(matching_files)}."],
        )

    updated_payload = _deep_copy(payload)
    updated_file = next(item for item in updated_payload["included_files"] if item.get("file_path") == file_path)
    updated_file["review_status"] = review_status
    updated_file["proposed_ingestion_action"] = proposed_ingestion_action
    updated_file["review_notes"] = list(updated_file.get("review_notes") or [])
    updated_file["review_notes"].extend(notes or [])

    approved_count, rejected_count, pending_count = _review_counts(updated_payload["included_files"])
    approval_status = "PENDING_REVIEW" if pending_count else "REVIEWED"
    updated_payload["approved_file_count"] = approved_count
    updated_payload["rejected_file_count"] = rejected_count
    updated_payload["approval_status"] = approval_status

    return updated_payload, CodeEvidenceApprovalManifestUpdateResult(
        is_valid=True,
        file_path=file_path,
        review_status=review_status,
        proposed_ingestion_action=proposed_ingestion_action,
        approved_file_count=approved_count,
        rejected_file_count=rejected_count,
        pending_review_count=pending_count,
        approval_status=approval_status,
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


def _update_request_errors(review_status: str, proposed_ingestion_action: str) -> list[str]:
    errors = []
    if review_status not in VALID_REVIEW_STATUSES:
        errors.append(f"review_status must be one of {sorted(VALID_REVIEW_STATUSES)}.")
    if proposed_ingestion_action not in VALID_PROPOSED_INGESTION_ACTIONS:
        errors.append(f"proposed_ingestion_action must be one of {sorted(VALID_PROPOSED_INGESTION_ACTIONS)}.")
    if proposed_ingestion_action == "INGEST_METADATA_ONLY" and review_status != "APPROVED":
        errors.append("INGEST_METADATA_ONLY requires review_status APPROVED.")
    if review_status == "REJECTED" and proposed_ingestion_action != "DO_NOT_INGEST_YET":
        errors.append("REJECTED files must use proposed_ingestion_action DO_NOT_INGEST_YET.")
    return errors


def _review_counts(included_files: list[dict[str, Any]]) -> tuple[int, int, int]:
    review_status_counts = Counter(item.get("review_status") for item in included_files)
    return (
        review_status_counts.get("APPROVED", 0),
        review_status_counts.get("REJECTED", 0),
        review_status_counts.get("PENDING_REVIEW", 0),
    )


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


def _deep_copy(payload: dict[str, Any]) -> dict[str, Any]:
    copied = dict(payload)
    copied["included_files"] = [dict(item) for item in payload.get("included_files", [])]
    for item in copied["included_files"]:
        if isinstance(item.get("review_notes"), list):
            item["review_notes"] = list(item["review_notes"])
    return copied
