"""Contratos do módulo BAIT — ponte b'AI'tcoin × organismo KAIR-S-SONICA.

Protocolos (decisão do titular 2026-09):
1. Cadastro via endereço BAIT (agentes AI e peers humanos)
2. Produção paga em tokens BAIT
3. Primeiro acesso: 100 BAIT de boas-vindas
4. Faucet: 10 BAIT a cada 24h (renovação 00:01 UTC)
5. Queima por complexidade da tarefa (tabela em policy.py)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class JobKind(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class BurnTier(str, Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"
    REALISTIC = "realistic"


@dataclass(frozen=True, slots=True)
class WalletSession:
    address: str
    balance_bait: float
    onboarded: bool
    last_faucet_claim_utc: str | None = None


@dataclass(frozen=True, slots=True)
class JobRequest:
    wallet_address: str
    kind: JobKind
    tier: BurnTier
    prompt: str
    duration_seconds: int | None = None  # vídeo: cobrado por bloco de 10s
    artist_policy: str = "ktd-immutable-identity"


@dataclass(frozen=True, slots=True)
class JobDecision:
    allowed: bool
    burn_bait: float
    units: int
    reasons: list[str] = field(default_factory=list)
    route: Literal["pipeline", "rejected"] = "pipeline"
