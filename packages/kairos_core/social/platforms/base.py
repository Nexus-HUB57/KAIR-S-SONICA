from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from kairos_core.social.contracts import PlatformPackage, SocialPlatform


class PlatformError(RuntimeError):
    def __init__(self, message: str, *, code: str = "provider_error", retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


@dataclass(frozen=True, slots=True)
class ProviderResult:
    platform: SocialPlatform
    operation: str
    status: str
    provider_id: str | None = None
    payload: dict[str, Any] | None = None


class SocialProvider(ABC):
    platform: SocialPlatform

    @property
    @abstractmethod
    def configured(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def publish(self, package: PlatformPackage, *, idempotency_key: str) -> ProviderResult:
        raise NotImplementedError

    def fetch_comments(self, *, media_id: str) -> ProviderResult:
        raise PlatformError("Leitura de comentários não configurada", code="comments_not_supported")

    def reply_comment(self, *, comment_id: str, message: str, idempotency_key: str) -> ProviderResult:
        raise PlatformError("Resposta de comentários não configurada", code="comment_reply_not_supported")

    def fetch_insights(self, *, media_id: str | None = None) -> ProviderResult:
        raise PlatformError("Insights não configurados", code="insights_not_supported")
