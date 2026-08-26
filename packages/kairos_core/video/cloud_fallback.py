from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from kairos_core.config import Settings
from kairos_core.schemas import VideoRequest


class CloudFallbackError(RuntimeError):
    """Erro seguro e sem eco de segredos do adapter cloud."""


@dataclass(frozen=True, slots=True)
class CloudFallbackStatus:
    mode: str
    provider: str
    enabled: bool
    ready: bool
    reasons: tuple[str, ...]
    guardrails: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "provider": self.provider,
            "enabled": self.enabled,
            "ready": self.ready,
            "reasons": list(self.reasons),
            "guardrails": self.guardrails,
        }


class CloudVideoFallback:
    """Cliente HTTP JSON opt-in para um provider de vídeo escolhido pelo operador.

    O adapter não escolhe provider, não faz discovery, não baixa modelos e não é
    chamado por planners, preflight ou rotas locais. A rota de submit deve ser
    invocada explicitamente com confirmação humana e o preflight já aprovado.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def status(self) -> CloudFallbackStatus:
        settings = self.settings
        provider = settings.cloud_video_fallback_provider.strip() or "NOT_CONFIGURED"
        reasons: list[str] = []
        base_url = (settings.cloud_video_fallback_base_url or "").strip()
        parsed = urlparse(base_url)
        configured = provider != "NOT_CONFIGURED" and bool(base_url)
        if not configured:
            reasons.append("provider e base_url ainda não foram configurados")
        if base_url and parsed.scheme != "https":
            reasons.append("base_url cloud deve usar HTTPS")
        if not settings.cloud_video_fallback_allowed_providers:
            reasons.append("allowlist de providers está vazia")
        elif provider not in settings.cloud_video_fallback_allowed_providers:
            reasons.append("provider não está na allowlist aprovada")
        key_available = bool(os.getenv(settings.cloud_video_fallback_api_key_env))
        if not key_available:
            reasons.append("credencial cloud não está disponível no ambiente")
        if not settings.cloud_video_fallback_license_acknowledged:
            reasons.append("licença/termos do provider ainda não foram aceitos")
        if not settings.cloud_video_fallback_retention_acknowledged:
            reasons.append("política de retenção ainda não foi aprovada")
        if settings.cloud_video_fallback_spending_limit_cents <= 0:
            reasons.append("limite de gasto deve ser maior que zero")
        if settings.cloud_video_fallback_timeout_seconds <= 0:
            reasons.append("timeout deve ser maior que zero")
        if settings.cloud_video_fallback_max_upload_bytes <= 0:
            reasons.append("limite de upload deve ser maior que zero")
        if not settings.cloud_video_fallback_enabled:
            mode = "DISABLED"
        elif not configured:
            mode = "NOT_CONFIGURED"
        elif reasons:
            mode = "FALLBACK_ONLY"
        else:
            mode = "READY"
        guardrails = {
            "https_only": True,
            "allowlist_required": True,
            "license_acknowledged": settings.cloud_video_fallback_license_acknowledged,
            "retention_acknowledged": settings.cloud_video_fallback_retention_acknowledged,
            "spending_limit_cents": settings.cloud_video_fallback_spending_limit_cents,
            "timeout_seconds": settings.cloud_video_fallback_timeout_seconds,
            "max_upload_bytes": settings.cloud_video_fallback_max_upload_bytes,
            "credential_configured": key_available,
            "automatic_retry": False,
            "automatic_fallback": False,
            "preflight_required": True,
            "human_confirmation_required": True,
        }
        return CloudFallbackStatus(
            mode=mode,
            provider=provider,
            enabled=settings.cloud_video_fallback_enabled,
            ready=settings.cloud_video_fallback_enabled and not reasons,
            reasons=tuple(dict.fromkeys(reasons)),
            guardrails=guardrails,
        )

    def submit(self, request: VideoRequest, *, preflight_id: str) -> dict[str, Any]:
        status = self.status()
        if not status.ready:
            raise CloudFallbackError(
                f"Fallback cloud não está pronto ({status.mode}): "
                + "; ".join(status.reasons)
            )
        if request.image_path or request.end_image_path or request.video_path:
            raise CloudFallbackError(
                "O adapter HTTP JSON não aceita upload de image/video path; "
                "configure um contrato de transferência aprovado antes de usar I2V/extend/start_end"
            )
        base_url = (self.settings.cloud_video_fallback_base_url or "").rstrip("/")
        path = self.settings.cloud_video_fallback_submit_path.strip()
        if not path.startswith("/"):
            raise CloudFallbackError("cloud submit path deve começar com '/'")
        token = os.getenv(self.settings.cloud_video_fallback_api_key_env)
        if not token:
            raise CloudFallbackError("credencial cloud não está disponível no ambiente")
        payload = {
            "request": request.model_dump(mode="json"),
            "preflight": {
                "id": preflight_id,
                "decision": "READY_FOR_APPROVAL",
                "identity_lock": "immutable",
                "live_action_policy": "live-action-only-no-static-no-overlay",
            },
            "governance": {
                "human_confirmation": True,
                "spending_limit_cents": self.settings.cloud_video_fallback_spending_limit_cents,
                "retention_acknowledged": True,
            },
        }
        target = f"{base_url}{path}"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        http_request = Request(
            target,
            data=body,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            method="POST",
        )
        try:
            with urlopen(
                http_request,
                timeout=self.settings.cloud_video_fallback_timeout_seconds,
            ) as response:
                response_body = response.read()
                http_status = response.status
        except HTTPError as exc:
            exc.close()
            raise CloudFallbackError(
                f"provider cloud retornou HTTP {exc.code}; nenhuma nova tentativa automática foi feita"
            ) from exc
        except (OSError, URLError, TimeoutError) as exc:
            raise CloudFallbackError(
                "falha de comunicação com o provider cloud; nenhuma nova tentativa automática foi feita"
            ) from exc
        if http_status >= 400:
            raise CloudFallbackError(
                f"provider cloud retornou HTTP {http_status}; nenhuma nova tentativa automática foi feita"
            )
        try:
            response_payload = json.loads(response_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CloudFallbackError("provider cloud retornou JSON inválido") from exc
        if not isinstance(response_payload, dict):
            raise CloudFallbackError("provider cloud retornou um contrato inesperado")
        remote_task_id = (
            response_payload.get("remote_task_id")
            or response_payload.get("task_id")
            or response_payload.get("generation_id")
            or response_payload.get("id")
        )
        return {
            "provider": status.provider,
            "status": "SUBMITTED",
            "remote_task_id": str(remote_task_id) if remote_task_id is not None else None,
            "preflight_id": preflight_id,
            "preflight_decision": "READY_FOR_APPROVAL",
            "guardrails": status.guardrails,
        }


__all__ = ["CloudFallbackError", "CloudFallbackStatus", "CloudVideoFallback"]
