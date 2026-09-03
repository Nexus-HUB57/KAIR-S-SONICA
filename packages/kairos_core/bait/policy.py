"""Tabela oficial de queima BAIT — segue o padrão de social/policy.py."""
from __future__ import annotations

import math

from kairos_core.bait.contracts import BurnTier, JobDecision, JobKind, JobRequest

# BAIT por unidade — imagem: por imagem; vídeo: por bloco de 10 segundos
BAIT_BURN_TABLE: dict[JobKind, dict[BurnTier, int]] = {
    JobKind.IMAGE: {BurnTier.SIMPLE: 1, BurnTier.COMPLEX: 2, BurnTier.REALISTIC: 3},
    JobKind.VIDEO: {BurnTier.SIMPLE: 1, BurnTier.COMPLEX: 2, BurnTier.REALISTIC: 3},
    JobKind.AUDIO: {BurnTier.SIMPLE: 2, BurnTier.COMPLEX: 3, BurnTier.REALISTIC: 4},
}

ONBOARDING_GRANT_BAIT = 100
FAUCET_DAILY_BAIT = 10
VIDEO_UNIT_SECONDS = 10
MAX_VIDEO_SECONDS = 60


class BaitPolicy:
    version = "bait-policy-v1"

    def evaluate(self, request: JobRequest, *, balance_bait: float) -> JobDecision:
        reasons: list[str] = []
        if not request.prompt.strip():
            return JobDecision(False, 0, 0, ["Prompt vazio."], route="rejected")
        if request.kind == JobKind.VIDEO:
            duration = request.duration_seconds or VIDEO_UNIT_SECONDS
            if duration < VIDEO_UNIT_SECONDS or duration > MAX_VIDEO_SECONDS or duration % VIDEO_UNIT_SECONDS:
                return JobDecision(False, 0, 0, ["Vídeo deve ser múltiplo de 10s, entre 10s e 60s."], route="rejected")
            units = duration // VIDEO_UNIT_SECONDS
        else:
            units = 1
        burn = BAIT_BURN_TABLE[request.kind][request.tier] * units
        if balance_bait < burn:
            reasons.append(f"Saldo insuficiente: {balance_bait:.0f} BAIT < {burn} BAIT. Faucet diário: {FAUCET_DAILY_BAIT} BAIT a cada 24h.")
            return JobDecision(False, burn, units, reasons, route="rejected")
        return JobDecision(True, burn, units, ["Queima aprovada pela tabela oficial."])

    def video_burn(self, tier: BurnTier, duration_seconds: int) -> int:
        units = max(1, math.ceil(duration_seconds / VIDEO_UNIT_SECONDS))
        return BAIT_BURN_TABLE[JobKind.VIDEO][tier] * units
