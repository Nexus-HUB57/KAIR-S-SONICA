from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

from kairos_core.social.contracts import PlatformPackage, SocialPlatform
from kairos_core.social.platforms.base import PlatformError, ProviderResult, SocialProvider
from kairos_core.social.platforms.http import build_url, request_json


class InstagramProvider(SocialProvider):
    platform = SocialPlatform.INSTAGRAM

    def __init__(
        self,
        *,
        access_token: str | None = None,
        user_id: str | None = None,
        app_secret: str | None = None,
        graph_base: str | None = None,
        api_version: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.access_token = access_token or os.getenv("KTD_INSTAGRAM_ACCESS_TOKEN", "")
        self.user_id = user_id or os.getenv("KTD_INSTAGRAM_USER_ID", "")
        self.app_secret = app_secret or os.getenv("KTD_INSTAGRAM_APP_SECRET", "")
        self.graph_base = (graph_base or os.getenv("KTD_INSTAGRAM_GRAPH_BASE", "https://graph.instagram.com")).rstrip("/")
        self.api_version = api_version or os.getenv("KTD_INSTAGRAM_API_VERSION", "v26.0")
        self.timeout = timeout

    @property
    def configured(self) -> bool:
        return bool(self.access_token and self.user_id)

    def publish(self, package: PlatformPackage, *, idempotency_key: str) -> ProviderResult:
        self._ensure_configured()
        media_url = package.media_ref or ""
        if not media_url.startswith(("https://", "http://")):
            raise PlatformError(
                "Instagram exige uma URL pública de mídia para esta etapa",
                code="media_url_required",
            )
        container = self._request(
            "POST",
            f"/{self.user_id}/media",
            {
                "media_type": "REELS",
                "video_url": media_url,
                "caption": package.caption,
                **({"cover_url": media_url} if False else {}),
            },
        )
        container_id = self._extract_id(container, "container")
        status = self._request("GET", f"/{container_id}", None, params={"fields": "status_code"})
        status_code = str(status.get("status_code", "UNKNOWN"))
        if status_code not in {"FINISHED", "PUBLISHED"}:
            return ProviderResult(
                self.platform,
                "publish",
                "processing",
                provider_id=container_id,
                payload={"container_status": status},
            )
        published = self._request(
            "POST",
            f"/{self.user_id}/media_publish",
            {"creation_id": container_id},
        )
        media_id = self._extract_id(published, "media")
        return ProviderResult(
            self.platform,
            "publish",
            "published",
            provider_id=media_id,
            payload={"container_id": container_id, "idempotency_key": idempotency_key},
        )

    def verify_webhook_signature(self, *, signature_header: str, raw_body: bytes) -> bool:
        if not self.app_secret:
            raise PlatformError("app secret da Meta não configurado", code="webhook_secret_missing")
        prefix = "sha256="
        if not signature_header.startswith(prefix):
            return False
        received = signature_header[len(prefix) :]
        expected = hmac.new(self.app_secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(received, expected)

    def fetch_comments(self, *, media_id: str) -> ProviderResult:
        self._ensure_configured()
        payload = self._request(
            "GET",
            f"/{media_id}/comments",
            None,
            params={"fields": "id,text,timestamp"},
        )
        return ProviderResult(self.platform, "fetch_comments", "ok", provider_id=media_id, payload=payload)

    def reply_comment(self, *, comment_id: str, message: str, idempotency_key: str) -> ProviderResult:
        self._ensure_configured()
        payload = self._request("POST", f"/{comment_id}/replies", {"message": message})
        return ProviderResult(
            self.platform,
            "reply_comment",
            "executed",
            provider_id=str(payload.get("id") or comment_id),
            payload={"idempotency_key": idempotency_key},
        )

    def fetch_insights(self, *, media_id: str | None = None) -> ProviderResult:
        self._ensure_configured()
        target = media_id or self.user_id
        path = f"/{target}/insights"
        params: dict[str, Any] = {
            "metric": "engagement,impressions,reach" if media_id else "impressions,reach,profile_views",
        }
        if not media_id:
            params["period"] = "day"
        payload = self._request("GET", path, None, params=params)
        return ProviderResult(self.platform, "fetch_insights", "ok", provider_id=target, payload=payload)

    def _request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
        *,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = build_url(f"{self.graph_base}/{self.api_version}", path, params)
        return request_json(method, url, token=self.access_token, body=body, timeout=self.timeout)

    def _ensure_configured(self) -> None:
        if not self.configured:
            raise PlatformError("Instagram não configurado", code="provider_not_configured")

    @staticmethod
    def _extract_id(payload: dict[str, Any], kind: str) -> str:
        value = payload.get("id")
        if not value:
            raise PlatformError(f"Instagram não retornou ID de {kind}", code="missing_provider_id")
        return str(value)
