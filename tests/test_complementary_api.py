from __future__ import annotations

from fastapi.testclient import TestClient

from services.api.main import app


def test_complementary_capabilities_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/v1/complementary/capabilities")

    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "complementary-audiovisual-core"
    assert payload["replaces_existing_core"] is False
    assert payload["enabled"] is True


def test_complementary_plan_is_synchronous_and_has_handoffs() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/v1/complementary/plan",
            json={
                "prompt": "KTD atravessa a chuva com luzes vermelhas",
                "duration_seconds": 10,
                "scene_seconds": 5,
                "seed": 42,
            },
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "planning-and-handoff"
    assert payload["duration_seconds"] == 10
    assert len(payload["scenes"]) == 2
    assert payload["scenes"][0]["video_request_template"]["backend"] == "native"
    assert "task_id" not in payload
    assert "status" not in payload
