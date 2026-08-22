from __future__ import annotations

import hashlib
import sqlite3
import json
from typing import Literal

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from kairos_core.social.algorithms import classify_comment
from kairos_core.social.contracts import ActionType, SocialPlatform, SocialRunRequest
from kairos_core.social.orchestrator import SocialOrchestrator
from kairos_core.social.scheduler import SocialScheduleStore
from kairos_core.social.platforms import PlatformError


class CommentTriageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2_200)


class SocialInteractionRequest(BaseModel):
    platform: SocialPlatform
    operation: Literal["fetch_comments", "reply_comment", "fetch_insights"]
    media_id: str = Field(min_length=1, max_length=200)
    comment_id: str | None = Field(default=None, max_length=200)
    message: str | None = Field(default=None, max_length=2_200)
    execute: bool = False


def build_social_router(
    orchestrator: SocialOrchestrator,
    schedule_store: SocialScheduleStore | None = None,
) -> APIRouter:
    router = APIRouter(prefix="/v1/social", tags=["social"])

    @router.get("/capabilities")
    def capabilities() -> dict[str, object]:
        return orchestrator.capabilities()

    @router.post("/run")
    def run(request: SocialRunRequest) -> dict[str, object]:
        try:
            return orchestrator.run(request).to_dict()
        except (ValueError, KeyError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @router.post("/schedules")
    def create_schedule(request: SocialRunRequest) -> dict[str, object]:
        if schedule_store is None:
            raise HTTPException(status_code=503, detail="Agenda social não configurada")
        try:
            return schedule_store.create(request)
        except (ValueError, sqlite3.IntegrityError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @router.get("/schedules")
    def list_schedules(status: str | None = None) -> dict[str, object]:
        if schedule_store is None:
            raise HTTPException(status_code=503, detail="Agenda social não configurada")
        return {"schedules": schedule_store.list(status=status)}

    @router.post("/community/triage")
    def community_triage(request: CommentTriageRequest) -> dict[str, object]:
        classification = classify_comment(request.text)
        return {
            "category": classification.category,
            "priority": classification.priority,
            "requires_escalation": classification.requires_escalation,
            "reasons": list(classification.reasons),
            "normalized_text": classification.normalized_text,
        }

    @router.post("/interaction")
    def interaction(request: SocialInteractionRequest) -> dict[str, object]:
        provider = orchestrator.providers.get(request.platform)
        if provider is None:
            raise HTTPException(status_code=404, detail="Plataforma não registrada")
        try:
            if request.operation == "fetch_comments":
                result = provider.fetch_comments(media_id=request.media_id)
                return {"status": result.status, "platform": result.platform.value, "payload": result.payload}
            if request.operation == "fetch_insights":
                result = provider.fetch_insights(media_id=request.media_id)
                return {"status": result.status, "platform": result.platform.value, "payload": result.payload}
            if not request.comment_id or not request.message:
                raise HTTPException(status_code=422, detail="comment_id e message são obrigatórios para reply_comment")
            policy = orchestrator.policy.evaluate(
                action_type=ActionType.REPLY_COMMENT,
                platform=request.platform,
                text=request.message,
                content_state="approved",
                autonomy_mode="autonomous",
            )
            if not policy.allowed:
                return {"status": "blocked", "policy": policy.model_dump(mode="json")}
            key = hashlib.sha256(
                f"{request.platform.value}:{request.comment_id}:{request.message}".encode()
            ).hexdigest()
            if not request.execute:
                return {
                    "status": "planned",
                    "policy": policy.model_dump(mode="json"),
                    "idempotency_key": key,
                }
            result = provider.reply_comment(
                comment_id=request.comment_id,
                message=request.message,
                idempotency_key=key,
            )
            return {
                "status": result.status,
                "platform": result.platform.value,
                "provider_id": result.provider_id,
                "payload": result.payload,
            }
        except PlatformError as exc:
            raise HTTPException(status_code=503 if exc.retryable else 409, detail={"code": exc.code, "message": str(exc)}) from exc

    @router.post("/webhooks/tiktok")
    async def tiktok_webhook(request: Request) -> dict[str, object]:
        provider = orchestrator.providers.get(SocialPlatform.TIKTOK)
        if provider is None or not hasattr(provider, "verify_webhook"):
            raise HTTPException(status_code=503, detail="TikTok provider não registrado")
        raw_body = await request.body()
        signature = request.headers.get("TikTok-Signature", "")
        try:
            valid = provider.verify_webhook(signature_header=signature, raw_body=raw_body)  # type: ignore[attr-defined]
        except PlatformError as exc:
            raise HTTPException(status_code=503, detail={"code": exc.code, "message": str(exc)}) from exc
        if not valid:
            raise HTTPException(status_code=401, detail="Webhook TikTok inválido")
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise HTTPException(status_code=400, detail="Webhook TikTok não é JSON válido") from exc
        return {"accepted": True, "event": payload.get("event"), "user_openid": payload.get("user_openid")}

    return router
