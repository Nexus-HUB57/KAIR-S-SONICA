from fastapi.testclient import TestClient
from kairos_core.config import Settings
from kairos_core.studio_master.auto_review import (
    CANONICAL_ARTIST_ID,
    CANONICAL_VOICE_REFERENCE,
    AutoReviewEngine,
)

from services.api.main import app


def test_audio_request_is_normalized_to_kairos_canon(tmp_path) -> None:
    engine = AutoReviewEngine(Settings(studio_master_preflight_dir=tmp_path))
    result = engine.review("audio", {"prompt": "boom bap vocal"})

    assert result.decision == "READY_FOR_APPROVAL"
    assert result.normalized_payload["artist_id"] == CANONICAL_ARTIST_ID
    assert result.normalized_payload["voice_reference"] == CANONICAL_VOICE_REFERENCE
    assert "identity-lock-artist-id" in result.repairs_applied
    assert "audio-lock-reference" in result.repairs_applied
    assert result.final_approval_required is True
    assert result.auto_publish is False


def test_wrong_voice_reference_is_hard_blocked(tmp_path) -> None:
    engine = AutoReviewEngine(Settings(studio_master_preflight_dir=tmp_path))
    result = engine.review("audio", {"voice_reference": "audio/other-voice.wav"})

    assert result.decision == "REJECTED"
    assert any(finding.code == "AUD-VOICE-01" for finding in result.findings)
    assert any(item.requires_human_approval for item in result.roadmap)


def test_identity_modification_is_hard_blocked(tmp_path) -> None:
    engine = AutoReviewEngine(Settings(studio_master_preflight_dir=tmp_path))
    result = engine.review(
        "image",
        {
            "artist_id": CANONICAL_ARTIST_ID,
            "identity_modification_requested": True,
        },
    )

    assert result.decision == "REJECTED"
    assert any(finding.code == "IMG-IMMUTABLE-01" for finding in result.findings)
    assert any(item.repair_id == "identity-modification-approval" for item in result.roadmap)


def test_static_or_overlay_video_is_hard_blocked(tmp_path) -> None:
    engine = AutoReviewEngine(Settings(studio_master_preflight_dir=tmp_path))
    result = engine.review(
        "video",
        {
            "prompt": "static image with image overlay and Ken Burns pan/zoom",
        },
    )

    assert result.decision == "REJECTED"
    assert any(finding.code == "VID-POLICY-01" for finding in result.findings)


def test_video_brief_gets_safe_live_action_constraint(tmp_path) -> None:
    engine = AutoReviewEngine(Settings(studio_master_preflight_dir=tmp_path))
    result = engine.review("video", {"prompt": "Kháirus performs in a dark studio"})

    assert result.decision == "READY_FOR_APPROVAL"
    assert "video-live-action-constraint" in result.repairs_applied
    assert result.normalized_payload["continuous_motion_required"] is True
    assert "Live-action contínuo" in result.normalized_payload["prompt"]


def test_audit_only_does_not_mutate_payload(tmp_path) -> None:
    engine = AutoReviewEngine(Settings(studio_master_preflight_dir=tmp_path))
    payload = {"prompt": "Kháirus studio brief"}
    result = engine.review("video", payload, auto_repair=False)

    assert result.decision == "READY_FOR_APPROVAL"
    assert result.normalized_payload == payload
    assert result.repairs_applied == []
    assert any(finding.code == "VID-POLICY-02" for finding in result.findings)


def test_preflight_api_returns_blocked_audit() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/studio-master/preflight",
            json={
                "media_kind": "image",
                "payload": {"identity_modification_requested": True},
            },
        )

    assert response.status_code == 200
    assert response.json()["decision"] == "REJECTED"
    assert any(item["code"] == "IMG-IMMUTABLE-01" for item in response.json()["findings"])


def test_generation_endpoint_blocks_other_artist_before_queueing() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/generate",
            json={"prompt": "test", "artist_id": "other.artist"},
        )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["code"] == "AUTO_REVIEW_BLOCKED"
    assert detail["audit"]["decision"] == "REJECTED"
