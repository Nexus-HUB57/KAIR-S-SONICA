from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class LLMUnavailable(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ModelInfo:
    model_id: str
    pricing: dict[str, Any]
    capabilities: dict[str, Any]


class LLMRouter:
    """Roteia tarefas sociais para o catálogo built-in sem expor credenciais."""

    def __init__(self, *, api_base: str | None = None, api_key: str | None = None, timeout: int = 60) -> None:
        self.api_base = (api_base or os.getenv("OPENAI_API_BASE", "")).rstrip("/")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.timeout = timeout
        self._catalog: tuple[ModelInfo, ...] | None = None

    @property
    def enabled(self) -> bool:
        return bool(self.api_base and self.api_key)

    def catalog(self, *, refresh: bool = False) -> tuple[ModelInfo, ...]:
        if self._catalog is not None and not refresh:
            return self._catalog
        payload = self._request("GET", "/models")
        items = payload.get("data", payload if isinstance(payload, list) else [])
        self._catalog = tuple(
            ModelInfo(
                model_id=str(item.get("id", "")),
                pricing=dict(item.get("pricing", {})),
                capabilities=dict(item.get("capabilities", {})),
            )
            for item in items
            if item.get("id")
        )
        return self._catalog

    def choose(self, task: str) -> str | None:
        if not self.enabled:
            return None
        catalog = {item.model_id: item for item in self.catalog()}
        preferred = {
            "bulk": ("gpt-5-mini", "gpt-5-nano", "claude-haiku-4-5"),
            "creative": ("claude-sonnet-4-6", "gpt-5", "gemini-3.1-pro-preview"),
            "safety": ("claude-opus-4-7", "gpt-5.5", "gemini-3.1-pro-preview"),
            "vision": ("gemini-3-flash-preview", "gemini-3.1-pro-preview", "gpt-5"),
        }.get(task, ("gpt-5-mini", "gpt-5", "claude-sonnet-4-6"))
        return next((model_id for model_id in preferred if model_id in catalog), next(iter(catalog), None))

    def generate_json(
        self,
        *,
        task: str,
        system: str,
        user: str,
        schema_name: str,
        schema: dict[str, Any],
        model: str | None = None,
    ) -> dict[str, Any]:
        selected_model = model or self.choose(task)
        if not selected_model:
            raise LLMUnavailable("LLM built-in não configurado")
        payload: dict[str, Any] = {
            "model": selected_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                },
            },
        }
        model_info = next((item for item in self.catalog() if item.model_id == selected_model), None)
        if model_info and model_info.capabilities.get("thinking_param") == "reasoning":
            payload["max_completion_tokens"] = 4_000
            payload["reasoning"] = {"effort": "low"}
        elif model_info and model_info.capabilities.get("thinking_param") == "thinking":
            payload["max_tokens"] = 4_096
            payload["thinking"] = {"type": "enabled", "budget_tokens": 1_024}
        response = self._request("POST", "/chat/completions", payload)
        try:
            content = response["choices"][0]["message"]["content"]
            result = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMUnavailable("LLM retornou saída não parseável") from exc
        if not isinstance(result, dict):
            raise LLMUnavailable("LLM retornou JSON fora do contrato")
        return result

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.enabled:
            raise LLMUnavailable("LLM built-in não configurado")
        request = urllib.request.Request(
            f"{self.api_base}{path}",
            method=method,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps(body).encode("utf-8") if body is not None else None,
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise LLMUnavailable(f"LLM indisponível: {type(exc).__name__}") from exc
