"""Orquestrador social híbrido de KTD para TikTok e Instagram."""

from kairos_core.social.algorithms import (
    CommentClassification,
    NextAction,
    choose_next_action,
    classify_comment,
    content_fingerprint,
    rank_comments,
    summarize_signals,
)
from kairos_core.social.contracts import (
    ActionStatus,
    ActionType,
    AutonomyMode,
    ContentIntent,
    EvidencePack,
    MetricsPlan,
    PeerHandoff,
    PlatformPackage,
    PolicyDecision,
    SocialAction,
    SocialPlatform,
    SocialRunRequest,
    SocialRunResult,
)
from kairos_core.social.llm import LLMRouter, LLMUnavailable, ModelInfo
from kairos_core.social.orchestrator import SocialOrchestrator
from kairos_core.social.peer import PeerCoordinator
from kairos_core.social.policy import SocialPolicy
from kairos_core.social.rag import RagDocument, SocialRagIndex
from kairos_core.social.scheduler import SocialScheduleStore

__all__ = [
    "ActionStatus",
    "CommentClassification",
    "ActionType",
    "AutonomyMode",
    "ContentIntent",
    "choose_next_action",
    "classify_comment",
    "content_fingerprint",
    "EvidencePack",
    "LLMRouter",
    "LLMUnavailable",
    "MetricsPlan",
    "NextAction",
    "ModelInfo",
    "PeerHandoff",
    "PeerCoordinator",
    "PlatformPackage",
    "PolicyDecision",
    "RagDocument",
    "rank_comments",
    "SocialAction",
    "SocialOrchestrator",
    "SocialPlatform",
    "summarize_signals",
    "SocialPolicy",
    "SocialScheduleStore",
    "SocialRagIndex",
    "SocialRunRequest",
    "SocialRunResult",
]
