from __future__ import annotations

from typing import Protocol

import httpx
from pydantic import ValidationError

from app.core.config import get_settings
from app.schemas.award_execution_minerva import AwardRuntimeDecisionEvidenceV1


class AwardExecutionEvidenceNotFound(LookupError):
    pass


class AwardExecutionExactVersionMismatch(ValueError):
    pass


class AwardExecutionEvidenceUnavailable(RuntimeError):
    pass


class AwardExecutionEvidenceInvalid(ValueError):
    pass


class AwardExecutionEvidenceProvider(Protocol):
    def fetch(
        self,
        calc_interpreter_line_id: str,
        award_version_id: str,
        account_id: str,
    ) -> AwardRuntimeDecisionEvidenceV1: ...


class WorkforceAwardExecutionEvidenceClient:
    def __init__(self, *, base_url: str, timeout_seconds: float, service_token: str | None = None) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds
        self._service_token = service_token

    def fetch(
        self,
        calc_interpreter_line_id: str,
        award_version_id: str,
        account_id: str,
    ) -> AwardRuntimeDecisionEvidenceV1:
        headers = {"Accept": "application/json"}
        if self._service_token:
            headers["Authorization"] = f"Bearer {self._service_token}"
        url = (
            f"{self._base_url}/api/v1/interpreter-results/calc-interpreter-lines/"
            f"{calc_interpreter_line_id}/award-decision-evidence"
        )
        try:
            response = httpx.get(
                url,
                params={"award_version_id": award_version_id, "account_id": account_id},
                headers=headers,
                timeout=self._timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise AwardExecutionEvidenceUnavailable("Workforce decision-evidence service is unavailable") from exc
        if response.status_code == 404:
            raise AwardExecutionEvidenceNotFound("no stored Award decision evidence exists for this pay line")
        if response.status_code == 409:
            raise AwardExecutionExactVersionMismatch(
                "Workforce rejected stored execution evidence because exact-version or stored-hash integrity "
                "validation failed"
            )
        if response.status_code == 422:
            raise AwardExecutionEvidenceInvalid(
                "Workforce rejected invalid stored Award decision evidence"
            )
        if response.status_code != 200:
            raise AwardExecutionEvidenceUnavailable(
                f"Workforce decision-evidence service returned HTTP {response.status_code}"
            )
        try:
            return AwardRuntimeDecisionEvidenceV1.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise AwardExecutionEvidenceInvalid(
                "Workforce returned decision evidence that does not satisfy the durable execution contract"
            ) from exc


def get_award_execution_evidence_provider() -> AwardExecutionEvidenceProvider:
    settings = get_settings()
    if settings.workforce_base_url is None:
        raise AwardExecutionEvidenceUnavailable(
            "Workforce decision-evidence endpoint is not configured for Minerva"
        )
    return WorkforceAwardExecutionEvidenceClient(
        base_url=settings.workforce_base_url,
        timeout_seconds=settings.workforce_evidence_timeout_seconds,
        service_token=settings.workforce_service_token,
    )


__all__ = [
    "AwardExecutionEvidenceInvalid",
    "AwardExecutionEvidenceNotFound",
    "AwardExecutionEvidenceProvider",
    "AwardExecutionEvidenceUnavailable",
    "AwardExecutionExactVersionMismatch",
    "WorkforceAwardExecutionEvidenceClient",
    "get_award_execution_evidence_provider",
]
