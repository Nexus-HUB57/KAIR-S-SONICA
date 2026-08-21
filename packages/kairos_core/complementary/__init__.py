"""Núcleo complementar de planejamento audiovisual, sem substituir os pipelines existentes."""

from kairos_core.complementary.media import (
    MediaAsset,
    MediaCache,
    MediaProviderChain,
    MediaProviderError,
    PexelsProvider,
    UnsplashProvider,
    provider_chain_from_names,
)
from kairos_core.complementary.planner import (
    ComplementaryPlan,
    build_complementary_plan,
    complementary_capabilities,
)

__all__ = [
    "ComplementaryPlan",
    "MediaAsset",
    "MediaCache",
    "MediaProviderChain",
    "MediaProviderError",
    "PexelsProvider",
    "UnsplashProvider",
    "build_complementary_plan",
    "complementary_capabilities",
    "provider_chain_from_names",
]
