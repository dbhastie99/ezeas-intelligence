from collections import Counter
from typing import Any


APPROVAL_METADATA_FIELDS = [
    "approval_required",
    "approval_status",
    "approval_notes",
    "approved_file_count",
    "rejected_file_count",
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
