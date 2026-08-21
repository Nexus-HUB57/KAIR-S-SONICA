from __future__ import annotations

from fastapi.testclient import TestClient

from services.api.main import app

client = TestClient(app)


def test_real_adapter_capabilities_are_exposed_safely() -> None:
    response = client.get("/v1/studio-master/real-adapters/capabilities")

    assert response.status_code == 200
    payload = response.json()
    assert payload["gate_enabled"] is False
    assert len(payload["adapters"]) == 6
    assert {item["adapter_id"] for item in payload["adapters"]} == {
        "crepe",
        "pedalboard",
        "fluidsynth",
        "demucs",
        "mosnet",
        "moviepy",
    }
    assert all(item["operational_status"] == "FALLBACK_ONLY" for item in payload["adapters"])


def test_real_adapter_preflight_does_not_run_adapter() -> None:
    response = client.get("/v1/studio-master/real-adapters/moviepy/preflight")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "FALLBACK_ONLY"
    assert payload["capability"]["license"]["code_license"] == "MIT"
    assert payload["run_requires"]["fallback"] == "browser_canvas_clip_plan"


def test_unknown_real_adapter_returns_not_found() -> None:
    response = client.get("/v1/studio-master/real-adapters/unknown/preflight")

    assert response.status_code == 404
