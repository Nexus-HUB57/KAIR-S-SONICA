from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from kairos_core.observability import get_logger, log_event

logger = get_logger(__name__)


class MediaProviderError(RuntimeError):
    """Falha normalizada de um provedor opcional de mídia."""


@dataclass(frozen=True, slots=True)
class MediaAsset:
    provider: str
    kind: str
    url: str
    width: int | None = None
    height: int | None = None
    duration_seconds: float | None = None


class MediaProvider(Protocol):
    name: str

    def search_images(self, query: str, *, per_page: int = 5) -> list[MediaAsset]: ...

    def search_videos(self, query: str, *, per_page: int = 5, orientation: str = "portrait") -> list[MediaAsset]: ...


class MediaCache:
    """Cache de download com chave SHA-256 e promoção atômica."""

    def __init__(self, directory: str | Path = "data/media-cache", *, max_bytes: int = 100 * 1024 * 1024) -> None:
        self.directory = Path(directory)
        self.max_bytes = max_bytes
        self.directory.mkdir(parents=True, exist_ok=True)

    def cache_key(self, url: str) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    def path_for(self, url: str, *, suffix: str | None = None) -> Path:
        extension = suffix or Path(urlparse(url).path).suffix or ".bin"
        if not extension.startswith("."):
            extension = "." + extension
        return self.directory / f"{self.cache_key(url)}{extension.lower()}"

    def get_or_download(
        self,
        url: str,
        *,
        timeout_seconds: int = 30,
        fetcher: Callable[[str], bytes] | None = None,
    ) -> Path:
        _validate_http_url(url)
        path = self.path_for(url)
        if path.is_file() and path.stat().st_size > 0:
            log_event(logger, 10, "media_cache_hit", cache_path=str(path), url_hash=self.cache_key(url))
            return path
        data = fetcher(url) if fetcher else _download_bytes(url, timeout_seconds=timeout_seconds, max_bytes=self.max_bytes)
        if not data:
            raise MediaProviderError("download de mídia retornou corpo vazio")
        if len(data) > self.max_bytes:
            raise MediaProviderError(f"mídia excede limite de {self.max_bytes} bytes")
        self.directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(prefix=".media-", dir=self.directory, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
        log_event(logger, 20, "media_cache_store", cache_path=str(path), size_bytes=len(data), url_hash=self.cache_key(url))
        return path


class PexelsProvider:
    name = "pexels"

    def __init__(self, *, api_key_env: str = "PEXELS_API_KEY", timeout_seconds: int = 10) -> None:
        self.api_key_env = api_key_env
        self.timeout_seconds = timeout_seconds

    def search_images(self, query: str, *, per_page: int = 5) -> list[MediaAsset]:
        key = os.getenv(self.api_key_env)
        if not key:
            log_event(logger, 10, "media_provider_disabled", provider=self.name, reason="missing_api_key")
            return []
        payload = _request_json(
            "https://api.pexels.com/v1/search",
            params={"query": query, "per_page": per_page},
            headers={"Authorization": key},
            timeout_seconds=self.timeout_seconds,
        )
        assets: list[MediaAsset] = []
        for photo in payload.get("photos", []):
            src = photo.get("src", {})
            url = src.get("large") or src.get("original")
            if url:
                assets.append(MediaAsset(provider=self.name, kind="image", url=url, width=photo.get("width"), height=photo.get("height")))
        return assets

    def search_videos(self, query: str, *, per_page: int = 5, orientation: str = "portrait") -> list[MediaAsset]:
        key = os.getenv(self.api_key_env)
        if not key:
            log_event(logger, 10, "media_provider_disabled", provider=self.name, reason="missing_api_key")
            return []
        payload = _request_json(
            "https://api.pexels.com/videos/search",
            params={"query": query, "per_page": per_page, "orientation": orientation},
            headers={"Authorization": key},
            timeout_seconds=self.timeout_seconds,
        )
        assets: list[MediaAsset] = []
        for video in payload.get("videos", []):
            files = sorted(video.get("video_files", []), key=lambda item: (item.get("width") or 0, item.get("height") or 0), reverse=True)
            selected = next((item for item in files if item.get("link")), None)
            if selected:
                assets.append(
                    MediaAsset(
                        provider=self.name,
                        kind="video",
                        url=selected["link"],
                        width=selected.get("width"),
                        height=selected.get("height"),
                        duration_seconds=video.get("duration"),
                    )
                )
        return assets


class UnsplashProvider:
    name = "unsplash"

    def __init__(self, *, api_key_env: str = "UNSPLASH_API_KEY", timeout_seconds: int = 10) -> None:
        self.api_key_env = api_key_env
        self.timeout_seconds = timeout_seconds

    def search_images(self, query: str, *, per_page: int = 5) -> list[MediaAsset]:
        key = os.getenv(self.api_key_env)
        if not key:
            log_event(logger, 10, "media_provider_disabled", provider=self.name, reason="missing_api_key")
            return []
        payload = _request_json(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "per_page": per_page},
            headers={"Authorization": f"Client-ID {key}"},
            timeout_seconds=self.timeout_seconds,
        )
        return [
            MediaAsset(provider=self.name, kind="image", url=photo["urls"].get("regular") or photo["urls"].get("full"))
            for photo in payload.get("results", [])
            if photo.get("urls")
        ]

    def search_videos(self, query: str, *, per_page: int = 5, orientation: str = "portrait") -> list[MediaAsset]:
        return []


def provider_chain_from_names(names: tuple[str, ...]) -> MediaProviderChain:
    providers: list[MediaProvider] = []
    for name in names:
        normalized = name.strip().lower()
        if normalized == "pexels":
            providers.append(PexelsProvider())
        elif normalized == "unsplash":
            providers.append(UnsplashProvider())
        else:
            log_event(logger, 30, "media_provider_unknown", provider=normalized)
    return MediaProviderChain(tuple(providers))


class MediaProviderChain:
    """Provedores em ordem de preferência, com fallback e sem estado global."""

    def __init__(self, providers: tuple[MediaProvider, ...] | None = None) -> None:
        self.providers = providers or (PexelsProvider(), UnsplashProvider())

    def search_images(self, query: str, *, per_page: int = 5) -> list[MediaAsset]:
        for provider in self.providers:
            try:
                assets = provider.search_images(query, per_page=per_page)
            except MediaProviderError as exc:
                log_event(logger, 30, "media_provider_failed", provider=provider.name, error=str(exc))
                continue
            if assets:
                log_event(logger, 20, "media_provider_selected", provider=provider.name, kind="image", count=len(assets))
                return assets
        return []

    def search_videos(self, query: str, *, per_page: int = 5, orientation: str = "portrait") -> list[MediaAsset]:
        for provider in self.providers:
            try:
                assets = provider.search_videos(query, per_page=per_page, orientation=orientation)
            except MediaProviderError as exc:
                log_event(logger, 30, "media_provider_failed", provider=provider.name, error=str(exc))
                continue
            if assets:
                log_event(logger, 20, "media_provider_selected", provider=provider.name, kind="video", count=len(assets))
                return assets
        return []


def _request_json(
    url: str,
    *,
    params: Mapping[str, Any],
    headers: Mapping[str, str],
    timeout_seconds: int,
) -> dict[str, Any]:
    query = urlencode({key: value for key, value in params.items() if value is not None})
    request = Request(f"{url}?{query}", headers={"Accept": "application/json", **headers}, method="GET")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        exc.close()
        raise MediaProviderError(f"GET {url} retornou HTTP {exc.code}") from exc
    except (OSError, URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MediaProviderError(f"falha ao consultar {url}: {exc}") from exc
    if not isinstance(payload, dict):
        raise MediaProviderError("resposta do provedor não é um objeto JSON")
    return payload


def _download_bytes(url: str, *, timeout_seconds: int, max_bytes: int) -> bytes:
    request = Request(url, headers={"Accept": "*/*"}, method="GET")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            content_type = response.headers.get_content_type()
            if content_type not in {"image/jpeg", "image/png", "image/webp", "video/mp4", "application/octet-stream"}:
                raise MediaProviderError(f"content-type não permitido: {content_type}")
            chunks: list[bytes] = []
            total = 0
            while chunk := response.read(1024 * 1024):
                total += len(chunk)
                if total > max_bytes:
                    raise MediaProviderError(f"mídia excede limite de {max_bytes} bytes")
                chunks.append(chunk)
            return b"".join(chunks)
    except HTTPError as exc:
        exc.close()
        raise MediaProviderError(f"download retornou HTTP {exc.code}") from exc
    except (OSError, URLError, TimeoutError) as exc:
        raise MediaProviderError(f"falha ao baixar mídia: {exc}") from exc


def _validate_http_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise MediaProviderError("URL de mídia deve usar http ou https")
