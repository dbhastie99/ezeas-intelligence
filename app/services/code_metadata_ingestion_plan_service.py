from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.services.code_evidence_approval_manifest_service import review_code_evidence_approval_manifest


CONTENT_LIKE_FIELDS = {"content", "file_content", "raw_content", "source_code", "text"}
PLANNED_ITEM_FIELDS = [
    "repo_name",
    "repo_path",
    "branch",
    "commit",
    "file_path",
    "source_type",
    "language",
    "file_kind",
    "is_test",
    "is_generated",
    "classification_reason",
    "review_status",
    "proposed_ingestion_action",
    "review_notes",
]


@dataclass(frozen=True)
class CodeMetadataIngestionPlanValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)

    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


def build_code_metadata_ingestion_plan(
    approval_manifest: dict[str, Any],
    source_approval_manifest: str | Path,
) -> tuple[dict[str, Any] | None, CodeMetadataIngestionPlanValidationResult]:
    approval_review = review_code_evidence_approval_manifest(approval_manifest)
    if not approval_review.is_valid:
        return None, CodeMetadataIngestionPlanValidationResult(is_valid=False, errors=approval_review.errors)

    approved_files = [
        item
        for item in approval_manifest.get("included_files", [])
        if item.get("review_status") == "APPROVED" and item.get("proposed_ingestion_action") == "INGEST_METADATA_ONLY"
    ]
    planned_items = [_planned_item(item) for item in approved_files]
    plan = {
        "plan_type": "CODE_METADATA_ONLY_INGESTION_PLAN",
        "plan_status": "READY_FOR_REVIEW" if planned_items else "NO_APPROVED_FILES",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "repository_metadata": approval_manifest.get("repository_metadata"),
        "safety_summary": approval_manifest.get("safety_summary"),
        "source_approval_manifest": str(source_approval_manifest),
        "approved_file_count": len(planned_items),
        "code_content_included": False,
        "code_content_bytes": 0,
        "db_ingestion_performed": False,
        "llm_exposure_performed": False,
        "execution_performed": False,
        "planned_items": planned_items,
    }
    validation_result = validate_code_metadata_ingestion_plan(plan)
    return plan, validation_result


def validate_code_metadata_ingestion_plan(plan: dict[str, Any]) -> CodeMetadataIngestionPlanValidationResult:
    errors: list[str] = []
    expected_flags = {
        "code_content_included": False,
        "code_content_bytes": 0,
        "db_ingestion_performed": False,
        "llm_exposure_performed": False,
        "execution_performed": False,
    }
    for field_name, expected_value in expected_flags.items():
        if plan.get(field_name) != expected_value:
            errors.append(f"{field_name} must be {expected_value!r}.")

    planned_items = plan.get("planned_items")
    if not isinstance(planned_items, list):
        errors.append("planned_items must be a list.")
        planned_items = []

    if plan.get("approved_file_count") != len(planned_items):
        errors.append("planned_items count must equal approved_file_count.")

    for index, item in enumerate(planned_items):
        if not isinstance(item, dict):
            errors.append(f"planned_items[{index}] must be an object.")
            continue
        if item.get("review_status") != "APPROVED":
            errors.append(f"planned_items[{index}].review_status must be 'APPROVED'.")
        if item.get("proposed_ingestion_action") != "INGEST_METADATA_ONLY":
            errors.append(f"planned_items[{index}].proposed_ingestion_action must be 'INGEST_METADATA_ONLY'.")
        for field_name in CONTENT_LIKE_FIELDS:
            if field_name in item:
                errors.append(f"planned_items[{index}] must not contain content-like field {field_name!r}.")

    return CodeMetadataIngestionPlanValidationResult(is_valid=not errors, errors=errors)


def summarize_code_metadata_ingestion_plan(plan: dict[str, Any]) -> dict[str, Any]:
    planned_items = [item for item in plan.get("planned_items", []) if isinstance(item, dict)]
    return {
        "plan_path": None,
        "plan_status": plan.get("plan_status"),
        "approved_file_count": plan.get("approved_file_count", 0),
        "counts_by_source_type": _counts(planned_items, "source_type"),
        "counts_by_file_kind": _counts(planned_items, "file_kind"),
        "counts_by_language": _counts(planned_items, "language"),
    }


def _planned_item(item: dict[str, Any]) -> dict[str, Any]:
    planned = {field_name: item.get(field_name) for field_name in PLANNED_ITEM_FIELDS}
    planned["review_notes"] = list(item.get("review_notes") or [])
    return planned


def _counts(items: list[dict[str, Any]], field_name: str) -> dict[str, int]:
    return {key: count for key, count in Counter(item.get(field_name) for item in items).items() if key is not None}
