from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from typing import Any

from kairos_core.social.contracts import PlatformPackage, SocialPlatform
from kairos_core.social.platforms.base import PlatformError, ProviderResult, SocialProvider
from kairos_core.social.platforms.http import build_url, request_json


class TikTokProvider(SocialProvider):
    platform = SocialPlatform.TIKTOK
    api_base = "https://open.tiktokapis.com"

    def __init__(
        self,
        *,
        access_token: str | None = None,
        client_secret: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.access_token = access_token or os.getenv("KTD_TIKTOK_ACCESS_TOKEN", "")
        self.client_secret = client_secret or os.getenv("KTD_TIKTOK_CLIENT_SECRET", "")
        self.timeout = timeout

    @property
    def configured(self) -> bool:
        return bool(self.access_token)

    def creator_info(self) -> ProviderResult:
        self._ensure_configured()
        payload = request_json(
            "POST",
            build_url(self.api_base, "/v2/post/publish/creator_info/query/"),
            token=self.access_token,
            body={},
            timeout=self.timeout,
        )
        return ProviderResult(self.platform, "creator_info", "ok", payload=payload)

    def publish(self, package: PlatformPackage, *, idempotency_key: str) -> ProviderResult:
        self._ensure_configured()
        media_url = package.media_ref or ""
        if not media_url.startswith(("https://", "http://")):
            raise PlatformError(
                "TikTok exige uma URL pública e verificada para PULL_FROM_URL nesta etapa",
                code="verified_media_url_required",
            )
        creator = self.creator_info().payload or {}
        creator_data = creator.get("data", {}) if isinstance(creator, dict) else {}
        options = creator_data.get("privacy_level_options") or ["SELF_ONLY"]
        requested_privacy = os.getenv("KTD_TIKTOK_PRIVACY_LEVEL", "PUBLIC_TO_EVERYONE")
        privacy = requested_privacy if requested_privacy in options else options[0]
        body = {
            "post_info": {
                "title": package.caption,
                "privacy_level": privacy,
                "disable_duet": True,
                "disable_stitch": True,
                "disable_comment": False,
                **(
                    {"video_cover_timestamp_ms": package.cover_timestamp_ms}
                    if package.cover_timestamp_ms is not None
                    else {}
                ),
            },
            "source_info": {"source": "PULL_FROM_URL", "video_url": media_url},
        }
        initialized = request_json(
            "POST",
            build_url(self.api_base, "/v2/post/publish/video/init/"),
            token=self.access_token,
            body=body,
            timeout=self.timeout,
        )
        data = initialized.get("data", {})
        publish_id = data.get("publish_id")
        if not publish_id:
            raise PlatformError("TikTok não retornou publish_id", code="missing_publish_id")
        status = self.fetch_status(str(publish_id))
        status_data = (status.payload or {}).get("data", {})
        status_name = str(status_data.get("status", "PROCESSING"))
        final = status_name == "PUBLISH_COMPLETE"
        return ProviderResult(
            self.platform,
            "publish",
            "published" if final else "processing",
            provider_id=str(publish_id),
            payload={
                "idempotency_key": idempotency_key,
                "privacy_level": privacy,
                "status": status.payload,
            },
        )

    def fetch_status(self, publish_id: str) -> ProviderResult:
        self._ensure_configured()
        payload = request_json(
            "POST",
            build_url(self.api_base, "/v2/post/publish/status/fetch/"),
            token=self.access_token,
            body={"publish_id": publish_id},
            timeout=self.timeout,
        )
        return ProviderResult(self.platform, "fetch_status", "ok", provider_id=publish_id, payload=payload)

    def fetch_comments(self, *, media_id: str) -> ProviderResult:
        raise PlatformError(
            "A consulta pública documentada pertence ao Research API e não é tratada como gerenciamento normal de comentários",
            code="comments_capability_not_authorized",
        )

    def fetch_insights(self, *, media_id: str | None = None) -> ProviderResult:
        raise PlatformError(
            "Insights TikTok não configurados neste adapter inicial",
            code="insights_capability_not_configured",
        )

    def verify_webhook(self, *, signature_header: str, raw_body: bytes, now: int | None = None, tolerance_seconds: int = 300) -> bool:
        if not self.client_secret:
            raise PlatformError("client_secret do TikTok não configurado", code="webhook_secret_missing")
        parts = dict(
            item.split("=", 1)
            for item in signature_header.split(",")
            if "=" in item
        )
        timestamp = parts.get("t")
        signature = parts.get("s")
        if not timestamp or not signature:
            return False
        try:
            timestamp_int = int(timestamp)
        except ValueError:
            return False
        current = int(now if now is not None else time.time())
        if abs(current - timestamp_int) > tolerance_seconds:
            return False
        signed = f"{timestamp}.{raw_body.decode('utf-8')}".encode("utf-8")
        expected = hmac.new(self.client_secret.encode("utf-8"), signed, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def _ensure_configured(self) -> None:
        if not self.configured:
            raise PlatformError("TikTok não configurado", code="provider_not_configured")
