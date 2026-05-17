import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Any

from app.services.controlled_evidence_intake_dry_run_service import NO_ACTION_ATTESTATION


REVIEW_PACK_READY = "REVIEW_PACK_READY"
REVIEW_PACK_NEEDS_HUMAN_REVIEW = "REVIEW_PACK_NEEDS_HUMAN_REVIEW"
REVIEW_PACK_BLOCKED_MUTATION_OR_RUNTIME_CLAIM = (
    "REVIEW_PACK_BLOCKED_MUTATION_OR_RUNTIME_CLAIM"
)
REVIEW_PACK_UNKNOWN_REQUIRES_REVIEW = "REVIEW_PACK_UNKNOWN_REQUIRES_REVIEW"

RECOMMENDED_NEXT_SLICE = (
    "Controlled evidence intake review ledger / promotion criteria / no-corpus-mutation v0.1."
)

MUTATION_OR_RUNTIME_FLAG_FIELDS = (
    "ingestion_performed_any",
    "corpus_mutation_performed_any",
    "code_evidence_ingestion_performed_any",
    "db_write_performed_any",
    "live_retrieval_performed_any",
    "live_llm_performed_any",
    "final_answer_generation_performed_any",
)


@dataclass(frozen=True)
class ControlledEvidenceIntakeReviewPackResult:
    review_pack_id: str
    source_execution_id: str
    review_status: str
    fixture_count: int
    ready_count: int
    needs_review_count: int
    blocked_count: int
    all_non_mutating: bool
    safety_failures: tuple[str, ...]
    unexpected_outcome_failures: tuple[str, ...]
    mutation_failures: tuple[str, ...]
    required_human_review_items: tuple[str, ...]
    recommended_next_slice: str
    evidence_ingestion_authorised: bool
    corpus_mutation_authorised: bool
    code_evidence_ingestion_authorised: bool
    db_write_authorised: bool
    live_retrieval_authorised: bool
    live_llm_authorised: bool
    final_answer_generation_authorised: bool
    runtime_readiness_claim_permitted: bool
    production_readiness_claim_permitted: bool
    no_action_attestation: str
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_controlled_evidence_intake_review_pack(
    fixture_execution: dict[str, Any] | None,
    *,
    recommended_next_slice: str = RECOMMENDED_NEXT_SLICE,
) -> dict[str, Any]:
    execution = dict(fixture_execution or {})
    fixture_results = tuple(dict(result) for result in execution.get("fixture_results", ()))
    mutation_failures = _mutation_failures(execution)
    unexpected_outcome_failures = _unexpected_outcome_failures(fixture_results)
    safety_failures = _safety_failures(execution, mutation_failures)
    required_human_review_items = _required_human_review_items(
        fixture_results,
        mutation_failures,
        unexpected_outcome_failures,
    )
    review_status = _review_status(
        execution,
        mutation_failures,
        unexpected_outcome_failures,
        fixture_results,
    )

    material = {
        "source_execution_id": execution.get("execution_id", ""),
        "review_status": review_status,
        "fixture_count": int(execution.get("fixture_count", 0)),
        "ready_count": int(execution.get("ready_count", 0)),
        "needs_review_count": int(execution.get("needs_review_count", 0)),
        "blocked_count": int(execution.get("blocked_count", 0)),
        "all_non_mutating": bool(execution.get("all_non_mutating")),
        "safety_failures": safety_failures,
        "unexpected_outcome_failures": unexpected_outcome_failures,
        "mutation_failures": mutation_failures,
        "required_human_review_items": required_human_review_items,
        "recommended_next_slice": recommended_next_slice,
    }

    return ControlledEvidenceIntakeReviewPackResult(
        review_pack_id=_stable_id("controlled-evidence-intake-review-pack", material),
        source_execution_id=str(execution.get("execution_id", "")),
        review_status=review_status,
        fixture_count=int(execution.get("fixture_count", 0)),
        ready_count=int(execution.get("ready_count", 0)),
        needs_review_count=int(execution.get("needs_review_count", 0)),
        blocked_count=int(execution.get("blocked_count", 0)),
        all_non_mutating=bool(execution.get("all_non_mutating")),
        safety_failures=safety_failures,
        unexpected_outcome_failures=unexpected_outcome_failures,
        mutation_failures=mutation_failures,
        required_human_review_items=required_human_review_items,
        recommended_next_slice=recommended_next_slice,
        evidence_ingestion_authorised=False,
        corpus_mutation_authorised=False,
        code_evidence_ingestion_authorised=False,
        db_write_authorised=False,
        live_retrieval_authorised=False,
        live_llm_authorised=False,
        final_answer_generation_authorised=False,
        runtime_readiness_claim_permitted=False,
        production_readiness_claim_permitted=False,
        no_action_attestation=NO_ACTION_ATTESTATION,
        explanation=_explanation(review_status),
    ).to_dict()


def _review_status(
    execution: dict[str, Any],
    mutation_failures: tuple[str, ...],
    unexpected_outcome_failures: tuple[str, ...],
    fixture_results: tuple[dict[str, Any], ...],
) -> str:
    if mutation_failures:
        return REVIEW_PACK_BLOCKED_MUTATION_OR_RUNTIME_CLAIM
    if unexpected_outcome_failures:
        return REVIEW_PACK_NEEDS_HUMAN_REVIEW
    if not execution or int(execution.get("fixture_count", 0)) != len(fixture_results):
        return REVIEW_PACK_UNKNOWN_REQUIRES_REVIEW
    if not bool(execution.get("all_non_mutating")):
        return REVIEW_PACK_BLOCKED_MUTATION_OR_RUNTIME_CLAIM
    return REVIEW_PACK_READY


def _mutation_failures(execution: dict[str, Any]) -> tuple[str, ...]:
    return tuple(
        field
        for field in MUTATION_OR_RUNTIME_FLAG_FIELDS
        if bool(execution.get(field))
    )


def _unexpected_outcome_failures(
    fixture_results: tuple[dict[str, Any], ...],
) -> tuple[str, ...]:
    failures: list[str] = []
    for result in fixture_results:
        if not bool(result.get("passed_expected_outcome")):
            fixture_id = str(result.get("fixture_id", "unknown-fixture"))
            result_failures = tuple(str(item) for item in result.get("failures", ()))
            if result_failures:
                failures.extend(f"{fixture_id}: {failure}" for failure in result_failures)
            else:
                failures.append(f"{fixture_id}: expected outcome failed")
    return tuple(sorted(failures))


def _safety_failures(
    execution: dict[str, Any],
    mutation_failures: tuple[str, ...],
) -> tuple[str, ...]:
    failures = list(mutation_failures)
    if bool(execution.get("evidence_ingestion_authorised")):
        failures.append("evidence_ingestion_authorised")
    if bool(execution.get("corpus_mutation_authorised")):
        failures.append("corpus_mutation_authorised")
    return tuple(sorted(failures))


def _required_human_review_items(
    fixture_results: tuple[dict[str, Any], ...],
    mutation_failures: tuple[str, ...],
    unexpected_outcome_failures: tuple[str, ...],
) -> tuple[str, ...]:
    items: list[str] = []
    items.extend(f"mutation_or_runtime_flag:{failure}" for failure in mutation_failures)
    items.extend(f"unexpected_outcome:{failure}" for failure in unexpected_outcome_failures)
    for result in fixture_results:
        decision = str(result.get("dry_run_decision", ""))
        if decision != "DRY_RUN_READY_FOR_FUTURE_INTAKE":
            items.append(f"fixture_review:{result.get('fixture_id')}:{decision}")
    return tuple(sorted(dict.fromkeys(items)))


def _explanation(review_status: str) -> str:
    if review_status == REVIEW_PACK_READY:
        return (
            "Fixture execution matched checked-in expectations and remained "
            "non-mutating; the pack is ready for controlled review without "
            "authorising ingestion or runtime claims."
        )
    if review_status == REVIEW_PACK_BLOCKED_MUTATION_OR_RUNTIME_CLAIM:
        return (
            "The review pack detected a prohibited mutation, execution, or runtime "
            "flag and authorises no further action."
        )
    if review_status == REVIEW_PACK_NEEDS_HUMAN_REVIEW:
        return (
            "The review pack found unexpected fixture outcomes that require human "
            "review before any later intake decision."
        )
    return "The review pack input is incomplete or unknown and requires controlled review."


def _stable_id(prefix: str, material: dict[str, Any]) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), default=str)
    return prefix + "-" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]
