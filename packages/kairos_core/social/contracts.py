from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class SocialPlatform(str, Enum):
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"


class AutonomyMode(str, Enum):
    AUTONOMOUS = "autonomous"
    COLLABORATIVE = "collaborative"
    SIMULATE = "simulate"


class PeerMode(str, Enum):
    DISABLED = "disabled"
    OPTIONAL = "optional"
    REQUIRED = "required"


class ContentIntent(str, Enum):
    LAUNCH = "launch"
    EVERGREEN = "evergreen"
    COMMUNITY = "community"
    PR = "pr"
    ANALYTICS = "analytics"


class ActionType(str, Enum):
    DRAFT = "draft"
    SCHEDULE = "schedule"
    PUBLISH = "publish"
    REPLY_COMMENT = "reply_comment"
    HIDE_COMMENT = "hide_comment"
    COLLECT_INSIGHTS = "collect_insights"


class ActionStatus(str, Enum):
    PLANNED = "planned"
    SIMULATED = "simulated"
    EXECUTED = "executed"
    BLOCKED = "blocked"
    FAILED = "failed"


class SocialRunRequest(BaseModel):
    objective: str = Field(min_length=1, max_length=4_000)
    campaign_id: str = Field(default="ktd-social", min_length=1, max_length=160)
    platforms: list[SocialPlatform] = Field(
        default_factory=lambda: [SocialPlatform.INSTAGRAM, SocialPlatform.TIKTOK],
        min_length=1,
        max_length=2,
    )
    autonomy_mode: AutonomyMode = AutonomyMode.AUTONOMOUS
    peer_mode: PeerMode = PeerMode.OPTIONAL
    content_intent: ContentIntent = ContentIntent.LAUNCH
    asset_refs: list[str] = Field(default_factory=list, max_length=40)
    source_refs: list[str] = Field(default_factory=list, max_length=40)
    schedule_at: datetime | None = None
    execute_actions: bool = False
    include_llm: bool = True
    include_rag: bool = True
    project_id: str = Field(default="default", min_length=1, max_length=120)
    content_state: Literal["draft", "candidate", "approved", "released"] = "draft"
    metadata: dict[str, Any] = Field(default_factory=dict)


class SourceRef(BaseModel):
    source_id: str
    locator: str
    title: str | None = None
    version: str | None = None
    provenance: Literal["repo", "official_api_docs", "user", "external"] = "repo"
    score: float = 0.0


class EvidencePack(BaseModel):
    query: str
    hits: list[SourceRef] = Field(default_factory=list)
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retrieval_mode: str = "lexical-metadata"
    provenance_required: bool = True


class PlatformPackage(BaseModel):
    platform: SocialPlatform
    title: str = Field(max_length=300)
    caption: str = Field(max_length=2_200)
    hashtags: list[str] = Field(default_factory=list, max_length=30)
    cta: str = Field(max_length=240)
    media_ref: str | None = None
    cover_timestamp_ms: int | None = Field(default=None, ge=0)
    alt_text: str | None = Field(default=None, max_length=1_000)
    scheduled_at: datetime | None = None
    related_content: list[str] = Field(default_factory=list, max_length=10)
    notes: list[str] = Field(default_factory=list, max_length=20)


class PolicyDecision(BaseModel):
    allowed: bool
    decision: Literal["allow", "block", "escalate"]
    reasons: list[str] = Field(default_factory=list)
    policy_version: str = "social-policy-v1"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class SocialAction(BaseModel):
    action_id: str = Field(default_factory=lambda: uuid4().hex)
    idempotency_key: str
    action_type: ActionType
    platform: SocialPlatform
    package: PlatformPackage | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    policy: PolicyDecision
    status: ActionStatus = ActionStatus.PLANNED
    provider_id: str | None = None
    error_code: str | None = None
    error_message: str | None = None


class PeerHandoff(BaseModel):
    handoff_id: str = Field(default_factory=lambda: uuid4().hex)
    peer_role: str
    purpose: str
    context_refs: list[str] = Field(default_factory=list)
    result: dict[str, Any] | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    status: Literal["planned", "completed", "escalated"] = "planned"


class MetricsPlan(BaseModel):
    primary: list[str] = Field(default_factory=list)
    secondary: list[str] = Field(default_factory=list)
    attribution_window_hours: int = Field(default=72, ge=1, le=720)
    next_decision_rule: str = "Comparar retenção, comentários qualificados e conversão por plataforma antes de ampliar o pacote."


class SocialRunResult(BaseModel):
    run_id: str = Field(default_factory=lambda: uuid4().hex)
    project_id: str
    campaign_id: str
    status: Literal["DRAFT", "READY", "SIMULATED", "SCHEDULED", "PUBLISHED", "PARTIAL", "BLOCKED"]
    autonomy_mode: AutonomyMode
    evidence: EvidencePack
    strategy: dict[str, Any]
    platform_packages: list[PlatformPackage] = Field(default_factory=list)
    actions: list[SocialAction] = Field(default_factory=list)
    peer_handoffs: list[PeerHandoff] = Field(default_factory=list)
    metrics_plan: MetricsPlan
    warnings: list[str] = Field(default_factory=list)
    memory_writes: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
