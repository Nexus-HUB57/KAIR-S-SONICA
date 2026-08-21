from __future__ import annotations

import json
import logging

from kairos_core.complementary.media import (
    MediaAsset,
    MediaCache,
    MediaProviderChain,
    PexelsProvider,
    UnsplashProvider,
)
from kairos_core.observability import JsonFormatter


class _EmptyProvider:
    name = "empty"

    def search_images(self, query: str, *, per_page: int = 5) -> list[MediaAsset]:
        return []

    def search_videos(self, query: str, *, per_page: int = 5, orientation: str = "portrait") -> list[MediaAsset]:
        return []


class _FallbackProvider:
    name = "fallback"

    def search_images(self, query: str, *, per_page: int = 5) -> list[MediaAsset]:
        return [MediaAsset(provider=self.name, kind="image", url="https://cdn.test/fallback.jpg")]

    def search_videos(self, query: str, *, per_page: int = 5, orientation: str = "portrait") -> list[MediaAsset]:
        return []


def test_media_cache_uses_atomic_file_and_second_call_is_cache_hit(tmp_path) -> None:
    calls: list[str] = []
    cache = MediaCache(tmp_path)

    def fetcher(url: str) -> bytes:
        calls.append(url)
        return b"image-bytes"

    first = cache.get_or_download("https://cdn.test/image.png", fetcher=fetcher)
    second = cache.get_or_download("https://cdn.test/image.png", fetcher=fetcher)

    assert first == second
    assert first.read_bytes() == b"image-bytes"
    assert calls == ["https://cdn.test/image.png"]
    assert not list(tmp_path.glob(".media-*"))


def test_provider_chain_falls_back_without_network() -> None:
    chain = MediaProviderChain((_EmptyProvider(), _FallbackProvider()))

    assets = chain.search_images("rain")

    assert assets[0].provider == "fallback"
    assert assets[0].url.endswith("fallback.jpg")


def test_real_providers_are_disabled_without_keys(monkeypatch) -> None:
    monkeypatch.delenv("PEXELS_API_KEY", raising=False)
    monkeypatch.delenv("UNSPLASH_API_KEY", raising=False)

    assert PexelsProvider().search_images("rain") == []
    assert PexelsProvider().search_videos("rain") == []
    assert UnsplashProvider().search_images("rain") == []
    assert UnsplashProvider().search_videos("rain") == []


def test_json_formatter_redacts_secret_fields() -> None:
    logger = logging.getLogger("test.observability")
    record = logger.makeRecord(
        logger.name,
        logging.INFO,
        __file__,
        1,
        "provider selected",
        (),
        None,
        extra={"event": "provider_selected", "token": "never-print", "provider": "pexels"},
    )

    payload = json.loads(JsonFormatter().format(record))

    assert payload["event"] == "provider_selected"
    assert payload["provider"] == "pexels"
    assert "token" not in payload
    assert "never-print" not in json.dumps(payload)
