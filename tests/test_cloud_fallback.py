from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from kairos_core.config import Settings
from kairos_core.schemas import VideoRequest
from kairos_core.video.cloud_fallback import CloudFallbackError, CloudVideoFallback

import services.api.main as api_main
from services.api.main import app, settings


def _ready_settings(tmp_path: Path) -> Settings:
    return Settings(
        cloud_video_fallback_enabled=True,
        cloud_video_fallback_provider="test-provider",
        cloud_video_fallback_base_url="https://provider.example",
        cloud_video_fallback_submit_path="/v1/video/generations",
        cloud_video_fallback_api_key_env="TEST_CLOUD_KEY",
        cloud_video_fallback_allowed_providers=("test-provider",),
        cloud_video_fallback_license_acknowledged=True,
        cloud_video_fallback_retention_acknowledged=True,
        cloud_video_fallback_spending_limit_cents=100,
        cloud_video_fallback_timeout_seconds=10,
        cloud_video_fallback_max_upload_bytes=1024 * 1024,
        output_dir=tmp_path / "output",
        upload_dir=tmp_path / "uploads",
    )


def _request() -> VideoRequest:
    return VideoRequest(
        prompt="One uninterrupted live-action performance shot with continuous camera movement",
        mode="t2v",
        backend="cli",
        seed=42,
    )


def test_cloud_status_is_fallback_only_when_provider_lacks_credential(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("TEST_CLOUD_KEY", raising=False)
    cloud = CloudVideoFallback(_ready_settings(tmp_path))

    status = cloud.status()

    assert status.mode == "FALLBACK_ONLY"
    assert status.ready is False
    assert "credencial cloud não está disponível no ambiente" in status.reasons


def test_cloud_submit_does_not_call_network_when_not_ready(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv("TEST_CLOUD_KEY", raising=False)
    cloud = CloudVideoFallback(_ready_settings(tmp_path))
    called = False

    def fail_network(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("network must not be called")

    monkeypatch.setattr("kairos_core.video.cloud_fallback.urlopen", fail_network)
    with pytest.raises(CloudFallbackError, match="não está pronto"):
        cloud.submit(_request(), preflight_id="audit-test")
    assert called is False


def test_cloud_submit_is_explicit_and_does_not_return_secret(monkeypatch, tmp_path: Path) -> None:
    secret = "test-secret-that-must-not-appear-in-result"
    monkeypatch.setenv("TEST_CLOUD_KEY", secret)
    cloud = CloudVideoFallback(_ready_settings(tmp_path))
    captured: dict[str, object] = {}

    class FakeResponse:
        status = 202

        def read(self) -> bytes:
            return b'{"task_id":"remote-123"}'

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["headers"] = dict(request.headers)
        captured["body"] = json.loads(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr("kairos_core.video.cloud_fallback.urlopen", fake_urlopen)
    result = cloud.submit(_request(), preflight_id="audit-test")

    assert result["remote_task_id"] == "remote-123"
    assert secret not in json.dumps(result)
    assert captured["url"] == "https://provider.example/v1/video/generations"
    assert captured["timeout"] == 10
    assert secret not in json.dumps(captured["body"])
    assert "Authorization" in captured["headers"]


def test_cloud_route_requires_human_confirmation_and_stays_disabled_by_default() -> None:
    original_enabled = settings.cloud_video_fallback_enabled
    original_provider = settings.cloud_video_fallback_provider
    try:
        settings.cloud_video_fallback_enabled = False
        settings.cloud_video_fallback_provider = "NOT_CONFIGURED"
        with TestClient(app) as client:
            missing_confirmation = client.post(
                "/v1/video/cloud-submit",
                json={"request": {"prompt": "live-action shot"}},
            )
            assert missing_confirmation.status_code == 409
            assert missing_confirmation.json()["detail"]["code"] == "CLOUD_CONFIRMATION_REQUIRED"

            disabled = client.post(
                "/v1/video/cloud-submit",
                json={
                    "request": {
                        "prompt": "One uninterrupted live-action performance with continuous camera movement",
                    },
                    "identity_metadata": {
                        "artist_id": "kairos.khairus_the_dragon",
                        "physical_profile": "ktd-physical-spec-v1",
                        "tattoo_map": "dragon-diamond-v1",
                        "identity_profile": "ktd-visual-canon-v1",
                        "voice_reference": "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3",
                        "source_manifest": {"path": "approved.mp4"},
                    },
                    "confirm_cloud_submit": True,
                    "human_approved": True,
                },
            )
            assert disabled.status_code == 503
            assert disabled.json()["detail"]["code"] == "CLOUD_FALLBACK_DISABLED"
    finally:
        settings.cloud_video_fallback_enabled = original_enabled
        settings.cloud_video_fallback_provider = original_provider


def test_cloud_route_runs_preflight_before_submit(monkeypatch) -> None:
    original_enabled = settings.cloud_video_fallback_enabled
    original_fallback = api_main.cloud_video_fallback
    called: dict[str, object] = {}

    class FakeCloudFallback:
        def submit(self, request: VideoRequest, *, preflight_id: str) -> dict[str, object]:
            called["prompt"] = request.prompt
            called["preflight_id"] = preflight_id
            return {
                "provider": "test-provider",
                "status": "SUBMITTED",
                "remote_task_id": "remote-1",
                "preflight_id": preflight_id,
                "preflight_decision": "READY_FOR_APPROVAL",
                "guardrails": {"preflight_required": True},
            }

        def status(self):
            return type("Status", (), {"mode": "READY"})()

    settings.cloud_video_fallback_enabled = True
    api_main.cloud_video_fallback = FakeCloudFallback()
    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/video/cloud-submit",
                json={
                    "request": {
                        "prompt": "One uninterrupted live-action performance with continuous camera movement",
                        "mode": "t2v",
                        "seed": 42,
                    },
                    "identity_metadata": {
                        "artist_id": "kairos.khairus_the_dragon",
                        "physical_profile": "ktd-physical-spec-v1",
                        "tattoo_map": "dragon-diamond-v1",
                        "identity_profile": "ktd-visual-canon-v1",
                        "voice_reference": "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3",
                        "aspect_ratio": "9:16",
                        "fps": 24,
                        "source_manifest": {
                            "path": "approved.mp4",
                            "sha256": "a" * 64,
                            "status": "APPROVED_REFERENCE",
                            "license": "approved",
                            "consent": "documented",
                            "identity_reference": "ktd-visual-canon-v1",
                        },
                        "live_action_policy": "live-action-only-no-static-no-overlay",
                        "static_image_only": False,
                        "image_overlay": False,
                    },
                    "confirm_cloud_submit": True,
                    "human_approved": True,
                },
            )
        assert response.status_code == 202, response.text
        payload = response.json()
        assert payload["status"] == "SUBMITTED"
        assert payload["remote_task_id"] == "remote-1"
        assert called["prompt"].startswith("One uninterrupted")
        assert str(called["preflight_id"]).startswith("audit-")
    finally:
        settings.cloud_video_fallback_enabled = original_enabled
        api_main.cloud_video_fallback = original_fallback


def test_cloud_route_rejects_identity_mismatch_before_submit() -> None:
    original_enabled = settings.cloud_video_fallback_enabled
    original_fallback = api_main.cloud_video_fallback
    called = False

    class FailIfCalled:
        def submit(self, request: VideoRequest, *, preflight_id: str):
            nonlocal called
            called = True
            raise AssertionError("identity mismatch must block before provider call")

    settings.cloud_video_fallback_enabled = True
    api_main.cloud_video_fallback = FailIfCalled()
    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/video/cloud-submit",
                json={
                    "request": {
                        "prompt": "One uninterrupted live-action performance with continuous camera movement",
                    },
                    "identity_metadata": {
                        "artist_id": "kairos.khairus_the_dragon",
                        "physical_profile": "unauthorized-profile",
                        "tattoo_map": "dragon-diamond-v1",
                        "identity_profile": "ktd-visual-canon-v1",
                        "voice_reference": "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3",
                        "source_manifest": {"path": "approved.mp4"},
                    },
                    "confirm_cloud_submit": True,
                    "human_approved": True,
                },
            )
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "AUTO_REVIEW_BLOCKED"
        assert called is False
    finally:
        settings.cloud_video_fallback_enabled = original_enabled
        api_main.cloud_video_fallback = original_fallback


def test_video_capabilities_exposes_cloud_fallback_state() -> None:
    with TestClient(app) as client:
        payload = client.get("/v1/video/capabilities").json()
    assert "cloud_fallback" in payload
    assert payload["explicit_cloud_submit_endpoint"] == "/v1/video/cloud-submit"
