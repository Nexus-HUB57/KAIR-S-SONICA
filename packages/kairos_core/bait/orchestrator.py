"""Orquestrador BAIT — sessões de carteira, faucet e despacho para o pipeline real.

Sem estado externo nesta versão: sessões em memória + store SQLite opcional.
A produção entra no AgenticOrchestrator / AutoReviewEngine existentes — este
módulo NÃO gera mídia; ele valida identidade, saldo e queima, e despacha.
"""
from __future__ import annotations

import sqlite3
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from kairos_core.bait.contracts import JobDecision, JobRequest, WalletSession
from kairos_core.bait.policy import FAUCET_DAILY_BAIT, ONBOARDING_GRANT_BAIT, BaitPolicy


class BaitOrchestrator:
    def __init__(self, db_path: str | Path | None = None) -> None:
        self.policy = BaitPolicy()
        self._db: sqlite3.Connection | None = None
        if db_path is not None:
            self._db = sqlite3.connect(str(db_path), check_same_thread=False)
            self._db.execute(
                "CREATE TABLE IF NOT EXISTS wallets (address TEXT PRIMARY KEY, balance REAL NOT NULL, last_faucet TEXT)"
            )
            self._db.commit()

    # ---- identidade / cadastro -------------------------------------------------
    def onboard(self, address: str) -> WalletSession:
        self._validate_address(address)
        existing = self._get(address)
        if existing is not None:
            return existing
        session = WalletSession(address=address, balance_bait=float(ONBOARDING_GRANT_BAIT), onboarded=True)
        self._put(session)
        return session

    def session(self, address: str) -> WalletSession | None:
        self._validate_address(address)
        return self._get(address)

    # ---- faucet diário ---------------------------------------------------------
    def claim_faucet(self, address: str) -> WalletSession:
        session = self._require(address)
        now = datetime.now(timezone.utc)
        if session.last_faucet_claim_utc:
            last = datetime.fromisoformat(session.last_faucet_claim_utc)
            if now - last < timedelta(hours=24):
                nxt = (last + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M UTC")
                raise ValueError(f"Faucet em cooldown. Próximo resgate: {nxt}.")
        updated = WalletSession(address, session.balance_bait + FAUCET_DAILY_BAIT, True, now.isoformat())
        self._put(updated)
        return updated

    # ---- produção (queima + despacho) -----------------------------------------
    def evaluate_job(self, request: JobRequest) -> JobDecision:
        session = self._require(request.wallet_address)
        return self.policy.evaluate(request, balance_bait=session.balance_bait)

    def burn_and_dispatch(self, request: JobRequest) -> dict:
        """Valida, queima e devolve o envelope para o pipeline KAIR-S-SONICA.

        O caller (services/api) injeta o envelope no AgenticOrchestrator /
        AutoReviewEngine — a identidade KTD é auditada ANTES de qualquer worker.
        """
        session = self._require(request.wallet_address)
        decision = self.policy.evaluate(request, balance_bait=session.balance_bait)
        if not decision.allowed:
            return {"decision": asdict(decision), "dispatched": False}
        self._put(WalletSession(session.address, session.balance_bait - decision.burn_bait, True, session.last_faucet_claim_utc))
        envelope = {
            "kind": request.kind.value,
            "tier": request.tier.value,
            "prompt": request.prompt,
            "duration_seconds": request.duration_seconds,
            "artist_policy": request.artist_policy,
            "burn_bait": decision.burn_bait,
            "requires_auto_review": True,  # PHD Gate obrigatório — padrão do sistema
        }
        return {"decision": asdict(decision), "dispatched": True, "pipeline_envelope": envelope}

    def capabilities(self) -> dict:
        return {
            "module": "kairos_core.bait",
            "policy_version": self.policy.version,
            "onboarding_grant_bait": ONBOARDING_GRANT_BAIT,
            "faucet_daily_bait": FAUCET_DAILY_BAIT,
            "burn_table": {k.value: {t.value: v for t, v in tiers.items()} for k, tiers in __import__("kairos_core.bait.policy", fromlist=["BAIT_BURN_TABLE"]).BAIT_BURN_TABLE.items()},
            "video_unit_seconds": 10,
        }

    # ---- store -----------------------------------------------------------------
    @staticmethod
    def _validate_address(address: str) -> None:
        if not address or len(address.strip()) < 8:
            raise ValueError("Endereço BAIT inválido.")

    def _require(self, address: str) -> WalletSession:
        session = self._get(address)
        if session is None:
            raise KeyError("Carteira não cadastrada. Faça onboard primeiro (100 BAIT de boas-vindas).")
        return session

    def _get(self, address: str) -> WalletSession | None:
        if self._db is None:
            return getattr(self, "_mem", {}).get(address)
        row = self._db.execute("SELECT address, balance, last_faucet FROM wallets WHERE address = ?", (address,)).fetchone()
        return WalletSession(row[0], row[1], True, row[2]) if row else None

    def _put(self, session: WalletSession) -> None:
        if self._db is None:
            if not hasattr(self, "_mem"):
                self._mem = {}
            self._mem[session.address] = session
            return
        self._db.execute(
            "INSERT INTO wallets (address, balance, last_faucet) VALUES (?,?,?) "
            "ON CONFLICT(address) DO UPDATE SET balance=excluded.balance, last_faucet=excluded.last_faucet",
            (session.address, session.balance_bait, session.last_faucet_claim_utc),
        )
        self._db.commit()
