from fastapi.testclient import TestClient
from kairos_core.config import Settings
from kairos_core.studio_master.frontier import AudiovisualFrontier, FrontierPlanRequest

from services.api.main import app


def test_frontier_capabilities_are_plan_first_and_governed() -> None:
    payload = AudiovisualFrontier(Settings()).capabilities()
    assert payload["harness"] == "PHD"
    assert payload["harness_meaning"] == "Preflight · Handoff · Determinism"
    assert payload["mode"] == "plan-first"
    assert payload["governance"]["human_approval_required"] is True
    assert payload["governance"]["auto_publish"] is False
    components = {item["component_id"]: item for item in payload["components"]}
    assert components["webcodecs-av1-opus"]["surface"] == "browser"
    assert components["ltx2-audio-video"]["status"] == "NOT_CONFIGURED"


def test_frontier_plan_selects_fallbacks_without_starting_jobs() -> None:
    plan = AudiovisualFrontier(Settings()).plan(
        FrontierPlanRequest(
            profile="audio_reactive_video",
            compute="webgpu",
            audio_backend="webcodecs",
            video_backend="ltx2_optional",
            approved_asset_id="asset-approved-001",
        )
    )
    assert plan.status == "READY_FOR_APPROVAL"
    assert plan.harness == "PHD"
    assert "webcodecs-av1-opus" in plan.selected_stack
    assert "webgpu-compute" in plan.selected_stack
    assert "ltx2-audio-video" in plan.selected_stack
    assert plan.handoff["target"] == "POST /v1/studio/handoff"
    assert plan.handoff["approval_required"] is True
    assert plan.handoff["submits_task"] is False
    assert any("LTX-2" in warning for warning in plan.warnings)


def test_frontier_api_exposes_capabilities_and_plan() -> None:
    with TestClient(app) as client:
        capabilities = client.get("/v1/studio-master/frontier/capabilities")
        plan = client.post(
            "/v1/studio-master/frontier/plan",
            json={"profile": "release_preflight", "video_backend": "browser_webcodecs"},
        )
    assert capabilities.status_code == 200
    assert capabilities.json()["harness"] == "PHD"
    assert plan.status_code == 200
    assert plan.json()["status"] == "READY_FOR_APPROVAL"
