from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kairos_core.agentic.memory import ProjectMemory
from kairos_core.config import Settings
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
    SourceRef,
)
from kairos_core.social.llm import LLMRouter, LLMUnavailable
from kairos_core.social.platforms import (
    InstagramProvider,
    PlatformError,
    SocialProvider,
    TikTokProvider,
)
from kairos_core.social.peer import PeerCoordinator
from kairos_core.social.policy import SocialPolicy
from kairos_core.social.rag import SocialRagIndex


class SocialOrchestrator:
    """Coordena estratégia, RAG, LLM, QA, publicação e aprendizado social."""

    def __init__(
        self,
        settings: Settings,
        *,
        repo_root: str | Path = ".",
        memory: ProjectMemory | None = None,
        rag: SocialRagIndex | None = None,
        llm: LLMRouter | None = None,
        providers: dict[SocialPlatform, SocialProvider] | None = None,
        policy: SocialPolicy | None = None,
        peer_coordinator: PeerCoordinator | None = None,
    ) -> None:
        self.settings = settings
        self.repo_root = Path(repo_root)
        self.memory = memory or ProjectMemory(settings.agentic_memory_dir, "social")
        self.rag = rag or SocialRagIndex.from_repo(self.repo_root)
        self.llm = llm or LLMRouter()
        self.policy = policy or SocialPolicy()
        self.peer_coordinator = peer_coordinator or PeerCoordinator()
        self.providers = providers or {
            SocialPlatform.INSTAGRAM: InstagramProvider(),
            SocialPlatform.TIKTOK: TikTokProvider(),
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "name": "ktd-social-orchestrator",
            "mode": "hybrid-autonomy",
            "profiles": {
                "instagram": "@khairusktd_ofc",
                "tiktok": "@ktd_oficial",
            },
            "autonomy_modes": [mode.value for mode in AutonomyMode],
            "content_intents": [intent.value for intent in ContentIntent],
            "modules": [
                "strategy",
                "research_rag",
                "audience_pr",
                "copywriter",
                "creative_director",
                "platform_adapter",
                "community_manager",
                "analytics",
                "moderation_safety",
                "peer_delegate",
                "qa_delivery",
            ],
            "providers": {
                platform.value: {
                    "configured": provider.configured,
                    "operations": ["publish", "comments", "insights"],
                }
                for platform, provider in self.providers.items()
            },
            "llm": {
                "configured": self.llm.enabled,
                "execution_toggle": self._llm_allowed(),
                "catalog_discovered_at_runtime": True,
            },
            "safety": {
                "policy_version": self.policy.version,
                "publication_requires_approved_or_released_content": True,
                "sensitive_comments_escalate": True,
                "dm_proactive_default": False,
            },
        }

    def run(self, request: SocialRunRequest) -> SocialRunResult:
        run_id = hashlib.sha256(
            f"{request.campaign_id}:{request.objective}:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()[:24]
        evidence = self._evidence(request)
        strategy = self._strategy(request, evidence)
        warnings: list[str] = []
        if request.content_state not in {"approved", "released"}:
            warnings.append("Conteúdo ainda não está approved/released; publicação ficará bloqueada.")

        if request.include_llm and self._llm_allowed():
            try:
                strategy.update(self._llm_strategy(request, evidence))
            except LLMUnavailable as exc:
                warnings.append(str(exc))
        elif request.include_llm:
            warnings.append("LLM disponível por adapter, mas KTD_SOCIAL_LLM_ENABLED não está habilitado.")

        packages = [self._package(request, platform, strategy) for platform in request.platforms]
        peer_handoffs = [
            self.peer_coordinator.delegate(
                handoff,
                context={"objective": request.objective, "evidence": evidence.model_dump(mode="json")},
            )
            for handoff in self._peer_handoffs(request, evidence)
        ]
        strategy["peer_reconciliation"] = PeerCoordinator.reconcile(peer_handoffs)
        actions = [
            self._plan_publish_action(request, package, run_id)
            for package in packages
        ]
        if request.execute_actions and request.autonomy_mode != AutonomyMode.SIMULATE:
            for action in actions:
                self._execute_action(action)

        if request.peer_mode == "required" and peer_handoffs and strategy["peer_reconciliation"]["status"] != "completed":
            warnings.append("Peer obrigatório ainda não devolveu resultado; execução final aguarda reconciliação.")
            for action in actions:
                if action.status in {ActionStatus.PLANNED, ActionStatus.SIMULATED}:
                    action.status = ActionStatus.BLOCKED
                    action.error_code = "peer_result_required"

        status = self._status(request, actions, peer_handoffs)
        metrics = self._metrics(request)
        memory_entry = self.memory.append(
            run_id=run_id,
            role="social_orchestrator",
            kind="social_run",
            content={
                "campaign_id": request.campaign_id,
                "objective": request.objective,
                "status": status,
                "platforms": [platform.value for platform in request.platforms],
                "action_ids": [action.action_id for action in actions],
            },
        )
        return SocialRunResult(
            run_id=run_id,
            project_id=request.project_id,
            campaign_id=request.campaign_id,
            status=status,
            autonomy_mode=request.autonomy_mode,
            evidence=evidence,
            strategy=strategy,
            platform_packages=packages,
            actions=actions,
            peer_handoffs=peer_handoffs,
            metrics_plan=metrics,
            warnings=warnings,
            memory_writes=[memory_entry],
        )

    def _evidence(self, request: SocialRunRequest) -> EvidencePack:
        if not request.include_rag:
            return EvidencePack(query=request.objective, hits=[], retrieval_mode="disabled")
        hits = self.rag.search(request.objective, limit=8)
        for source in request.source_refs:
            hits.append(
                {
                    "source_id": source,
                    "locator": source,
                    "title": None,
                    "version": None,
                    "provenance": "user",
                    "score": 10.0,
                    "text_excerpt": "",
                    "metadata": {},
                }
            )
        unique: dict[str, SourceRef] = {}
        for hit in hits:
            unique[str(hit["source_id"])] = SourceRef(
                source_id=str(hit["source_id"]),
                locator=str(hit["locator"]),
                title=hit.get("title"),
                version=hit.get("version"),
                provenance=hit.get("provenance", "repo"),
                score=float(hit.get("score", 0.0)),
            )
        return EvidencePack(query=request.objective, hits=list(unique.values()))

    @staticmethod
    def _strategy(request: SocialRunRequest, evidence: EvidencePack) -> dict[str, Any]:
        return {
            "objective": request.objective,
            "campaign_id": request.campaign_id,
            "content_intent": request.content_intent.value,
            "audience": request.metadata.get("audience", "ouvintes de rap narrativo e comunidade de KTD"),
            "hypothesis": request.metadata.get(
                "hypothesis",
                "Performance autêntica e uma pergunta simples geram participação qualificada e retorno ao asset completo.",
            ),
            "funnel": ["discovery", "engagement", "conversion", "retention"],
            "evidence_count": len(evidence.hits),
            "llm_mode": "optional-structured-output",
        }

    def _llm_strategy(self, request: SocialRunRequest, evidence: EvidencePack) -> dict[str, Any]:
        schema = {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "hook": {"type": "string"},
                "cta": {"type": "string"},
                "risk_notes": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["message", "hook", "cta", "risk_notes"],
            "additionalProperties": False,
        }
        context = json.dumps([hit.model_dump(mode="json") for hit in evidence.hits[:6]], ensure_ascii=False)
        return self.llm.generate_json(
            task="creative",
            system=(
                "Você é o estrategista de mídias sociais de KTD. Preserve originalidade, identidade do artista,"
                " segurança e dignidade. Entregue apenas JSON compatível com o schema."
            ),
            user=f"Objetivo: {request.objective}\nEvidências: {context}",
            schema_name="social_strategy",
            schema=schema,
        )

    @staticmethod
    def _package(
        request: SocialRunRequest,
        platform: SocialPlatform,
        strategy: dict[str, Any],
    ) -> PlatformPackage:
        song_title = str(request.metadata.get("song_title", "I Won’t Waste This Life"))
        hook = str(strategy.get("hook", "I won’t waste this life."))
        cta = str(strategy.get("cta", "Watch, listen, and tell us what you refuse to waste."))
        base_caption = str(
            strategy.get(
                "message",
                f"{hook} KTD / Kháirus the Dragon. This is not a promise to the world; it is a decision to myself.",
            )
        )
        hashtags = request.metadata.get(
            "hashtags",
            ["#KTD", "#KhairusTheDragon", "#OldSchoolRap", "#BoomBap"],
        )
        media_ref = request.asset_refs[0] if request.asset_refs else None
        if platform == SocialPlatform.INSTAGRAM:
            return PlatformPackage(
                platform=platform,
                title=song_title,
                caption=f"{base_caption}\n\n{cta}\n\n" + " ".join(hashtags),
                hashtags=list(hashtags),
                cta=cta,
                media_ref=media_ref,
                alt_text=f"Kháirus the Dragon performing a narrative rap excerpt for {song_title}.",
                scheduled_at=request.schedule_at,
                notes=["Use a clean 9:16 master; preserve visible articulation and KTD identity."],
            )
        return PlatformPackage(
            platform=platform,
            title=f"{hook} — {song_title} | KTD",
            caption=f"{base_caption} {cta} " + " ".join(hashtags),
            hashtags=list(hashtags),
            cta=cta,
            media_ref=media_ref,
            cover_timestamp_ms=int(request.metadata.get("cover_timestamp_ms", 0)),
            scheduled_at=request.schedule_at,
            notes=["TikTok direct post requires creator authorization and a platform-accepted media source."],
        )

    def _peer_handoffs(self, request: SocialRunRequest, evidence: EvidencePack) -> list[PeerHandoff]:
        if request.peer_mode == "disabled":
            return []
        roles = ["pr-risk", "brand-guardian", "analytics"]
        return [
            PeerHandoff(
                peer_role=role,
                purpose=f"Revisar {request.content_intent.value} para {request.campaign_id} antes da próxima decisão.",
                context_refs=[hit.source_id for hit in evidence.hits[:4]],
            )
            for role in roles
        ]

    def _plan_publish_action(
        self,
        request: SocialRunRequest,
        package: PlatformPackage,
        run_id: str,
    ) -> SocialAction:
        serialized = json.dumps(package.model_dump(mode="json"), sort_keys=True, ensure_ascii=False)
        idempotency_key = hashlib.sha256(f"{run_id}:{serialized}".encode()).hexdigest()
        policy = self.policy.evaluate(
            action_type=ActionType.PUBLISH,
            platform=package.platform,
            text=f"{package.title}\n{package.caption}",
            content_state=request.content_state,
            autonomy_mode=request.autonomy_mode.value,
        )
        status = ActionStatus.PLANNED
        if not policy.allowed:
            status = ActionStatus.BLOCKED
        elif request.autonomy_mode == AutonomyMode.SIMULATE:
            status = ActionStatus.SIMULATED
        return SocialAction(
            idempotency_key=idempotency_key,
            action_type=ActionType.PUBLISH,
            platform=package.platform,
            package=package,
            policy=policy,
            status=status,
        )

    def _execute_action(self, action: SocialAction) -> None:
        if not action.policy.allowed:
            action.status = ActionStatus.BLOCKED
            action.error_code = "policy_block"
            return
        provider = self.providers[action.platform]
        if not provider.configured:
            action.status = ActionStatus.BLOCKED
            action.error_code = "provider_not_configured"
            action.error_message = f"{action.platform.value} sem credencial configurada."
            return
        try:
            result = provider.publish(action.package, idempotency_key=action.idempotency_key)  # type: ignore[arg-type]
            action.status = ActionStatus.EXECUTED if result.status in {"published", "processing"} else ActionStatus.FAILED
            action.provider_id = result.provider_id
            if result.status == "processing":
                action.error_code = "provider_processing"
        except PlatformError as exc:
            action.status = ActionStatus.FAILED if exc.retryable else ActionStatus.BLOCKED
            action.error_code = exc.code
            action.error_message = str(exc)

    @staticmethod
    def _status(request: SocialRunRequest, actions: list[SocialAction], peers: list[PeerHandoff]) -> str:
        if any(action.status == ActionStatus.BLOCKED for action in actions):
            return "PARTIAL" if any(action.status == ActionStatus.EXECUTED for action in actions) else "BLOCKED"
        if any(action.status == ActionStatus.FAILED for action in actions):
            return "PARTIAL" if any(action.status == ActionStatus.EXECUTED for action in actions) else "BLOCKED"
        if request.execute_actions and actions:
            return "PUBLISHED"
        if request.autonomy_mode == AutonomyMode.SIMULATE:
            return "SIMULATED"
        if peers and request.peer_mode == "required":
            return "BLOCKED"
        return "READY"

    @staticmethod
    def _metrics(request: SocialRunRequest) -> MetricsPlan:
        primary = ["qualified_comments", "shares", "profile_actions"]
        secondary = ["reach", "impressions", "views", "watch_time", "follows", "saves"]
        if SocialPlatform.INSTAGRAM in request.platforms:
            primary.append("instagram_engagement")
        if SocialPlatform.TIKTOK in request.platforms:
            primary.append("tiktok_completion_or_rewatch")
        return MetricsPlan(primary=primary, secondary=secondary)

    def _llm_allowed(self) -> bool:
        legacy_flag = os.getenv("KTD_SOCIAL_LLM_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
        return bool(self.settings.social_llm_enabled or legacy_flag)
