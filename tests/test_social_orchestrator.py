from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path

from kairos_core.config import Settings
from kairos_core.social import (
    AutonomyMode,
    RagDocument,
    SocialOrchestrator,
    SocialPlatform,
    SocialRagIndex,
    SocialRunRequest,
)
from kairos_core.social.platforms.tiktok import TikTokProvider


def make_orchestrator(tmp_path: Path) -> SocialOrchestrator:
    settings = Settings(agentic_memory_dir=tmp_path / "memory")
    rag = SocialRagIndex(
        [
            RagDocument(
                source_id="ktd-canon",
                text="KTD é rapper de rap narrativo old school, com performance vocal visível.",
                locator="docs/ktd-visual-bible.md",
            )
        ]
    )
    return SocialOrchestrator(settings, repo_root=tmp_path, rag=rag)


def test_social_orchestrator_simulates_both_platforms(tmp_path: Path) -> None:
    result = make_orchestrator(tmp_path).run(
        SocialRunRequest(
            objective="lançar um trecho de rap old school com performance de KTD",
            campaign_id="single-11",
            autonomy_mode=AutonomyMode.SIMULATE,
            content_state="approved",
            include_llm=False,
            asset_refs=["https://cdn.example.test/ktd-short.mp4"],
        )
    )

    assert result.status == "SIMULATED"
    assert {package.platform for package in result.platform_packages} == {
        SocialPlatform.INSTAGRAM,
        SocialPlatform.TIKTOK,
    }
    assert all(action.status.value == "simulated" for action in result.actions)
    assert result.evidence.hits[0].source_id == "ktd-canon"


def test_pending_content_cannot_be_published(tmp_path: Path) -> None:
    result = make_orchestrator(tmp_path).run(
        SocialRunRequest(
            objective="publicar prova ainda pendente",
            content_state="candidate",
            execute_actions=True,
            include_llm=False,
        )
    )

    assert result.status == "BLOCKED"
    assert all(action.status.value == "blocked" for action in result.actions)
    assert "approved/released" in result.warnings[0]


def test_tiktok_webhook_signature_is_verified() -> None:
    secret = "test-secret"
    timestamp = 1_700_000_000
    body = json.dumps({"event": "post.publish.complete"}).encode()
    signed = f"{timestamp}.{body.decode()}".encode()
    signature = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    provider = TikTokProvider(access_token="token", client_secret=secret)

    assert provider.verify_webhook(
        signature_header=f"t={timestamp},s={signature}",
        raw_body=body,
        now=timestamp,
    )
    assert not provider.verify_webhook(
        signature_header="t=1700000000,s=invalid",
        raw_body=body,
        now=timestamp,
    )
