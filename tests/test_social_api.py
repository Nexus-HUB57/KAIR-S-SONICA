from __future__ import annotations

from fastapi.testclient import TestClient

from services.api.main import app


def test_social_capabilities_expose_hybrid_mode() -> None:
    with TestClient(app) as client:
        response = client.get("/v1/social/capabilities")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "ktd-social-orchestrator"
    assert payload["mode"] == "hybrid-autonomy"
    assert payload["profiles"]["instagram"] == "@khairusktd_ofc"
    assert payload["profiles"]["tiktok"] == "@ktd_oficial"


def test_social_run_does_not_publish_by_default() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/social/run",
            json={
                "objective": "planejar trecho de rap old school para a campanha KTD",
                "campaign_id": "smoke-test",
                "include_llm": False,
                "content_state": "approved",
                "asset_refs": ["https://cdn.example.test/ktd.mp4"],
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "READY"
    assert all(action["status"] == "planned" for action in payload["actions"])


def test_social_comment_reply_is_planned_without_execute() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/social/interaction",
            json={
                "platform": "instagram",
                "operation": "reply_comment",
                "media_id": "media-1",
                "comment_id": "comment-1",
                "message": "Thank you for listening.",
                "execute": False,
            },
        )

    assert response.status_code == 200
    assert response.json()["status"] == "planned"


def test_social_community_triage_escalates_privacy_signal() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/social/community/triage",
            json={"text": "Please contact me on WhatsApp, my phone number is 555-1234."},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["category"] == "privacy"
    assert payload["requires_escalation"] is True
