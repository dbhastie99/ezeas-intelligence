from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True)
class JsonCompletion:
    content: str
    latency_ms: int


class OpenAICompatibleJsonClient:
    """One server-side, no-tools JSON client shared by governed Minerva paths."""

    def __init__(self, *, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def complete(
        self,
        *,
        system_instruction: str,
        user_payload: str,
        model: str,
        timeout_seconds: float,
        max_tokens: int,
        metadata: dict[str, str],
        response_schema: dict[str, Any] | None = None,
    ) -> JsonCompletion:
        del metadata  # Instruction identity is retained in the local audit, not sent as provider storage metadata.
        started = time.perf_counter()
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": model,
                "temperature": 0,
                "max_tokens": max_tokens,
                "response_format": (
                    {"type": "json_schema", "json_schema": response_schema}
                    if response_schema
                    else {"type": "json_object"}
                ),
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_payload},
                ],
            },
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        body: dict[str, Any] = response.json()
        content = body["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise ValueError("provider response content is not text")
        return JsonCompletion(
            content=content,
            latency_ms=max(0, round((time.perf_counter() - started) * 1000)),
        )


__all__ = ["JsonCompletion", "OpenAICompatibleJsonClient"]
