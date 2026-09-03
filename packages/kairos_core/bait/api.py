"""Router /v1/bait — mesmo padrão de kairos_core.social.api (build_router)."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from kairos_core.bait.contracts import BurnTier, JobKind, JobRequest
from kairos_core.bait.orchestrator import BaitOrchestrator


class OnboardRequest(BaseModel):
    address: str = Field(min_length=8, max_length=128)


class ProduceRequest(BaseModel):
    wallet_address: str = Field(min_length=8, max_length=128)
    kind: JobKind
    tier: BurnTier = BurnTier.SIMPLE
    prompt: str = Field(min_length=1, max_length=4_000)
    duration_seconds: int | None = None


def build_bait_router(orchestrator: BaitOrchestrator) -> APIRouter:
    router = APIRouter(prefix="/v1/bait", tags=["bait"])

    @router.get("/capabilities")
    def capabilities() -> dict:
        return orchestrator.capabilities()

    @router.post("/wallet/onboard")
    def onboard(request: OnboardRequest) -> dict:
        try:
            s = orchestrator.onboard(request.address)
            return {"address": s.address, "balance_bait": s.balance_bait, "onboarded": s.onboarded}
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @router.get("/wallet/{address}")
    def wallet(address: str) -> dict:
        try:
            s = orchestrator.session(address)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if s is None:
            raise HTTPException(status_code=404, detail="Carteira não cadastrada")
        return {"address": s.address, "balance_bait": s.balance_bait, "last_faucet_claim_utc": s.last_faucet_claim_utc}

    @router.post("/faucet/claim")
    def faucet(request: OnboardRequest) -> dict:
        try:
            s = orchestrator.claim_faucet(request.address)
            return {"address": s.address, "balance_bait": s.balance_bait}
        except (ValueError, KeyError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @router.post("/produce")
    def produce(request: ProduceRequest) -> dict:
        job = JobRequest(
            wallet_address=request.wallet_address,
            kind=request.kind,
            tier=request.tier,
            prompt=request.prompt,
            duration_seconds=request.duration_seconds,
        )
        try:
            return orchestrator.burn_and_dispatch(job)
        except (ValueError, KeyError) as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return router
