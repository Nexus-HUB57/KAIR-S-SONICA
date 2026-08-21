from __future__ import annotations

from fastapi.testclient import TestClient
from kairos_core.config import Settings
from kairos_core.studio_master import (
    CanonIndex,
    PerformanceController,
    RepertoireCatalog,
    StudioMasterPlanner,
)

from services.api import main


def _patch_runtime(monkeypatch, tmp_path, enabled: bool = True) -> None:
    settings = Settings(
        task_db_path=tmp_path / "tasks.sqlite3",
        canon_index_path=main.Path("config/canon_index.yaml"),
        instrumentation_repertoire_path=main.Path("config/instrumentation_repertoire.yaml"),
        studio_master_enabled=enabled,
    )
    monkeypatch.setattr(main, "settings", settings)
    canon = CanonIndex.load(settings.canon_index_path)
    repertoire = RepertoireCatalog.load(settings.instrumentation_repertoire_path)
    monkeypatch.setattr(main, "canon_index", canon)
    monkeypatch.setattr(main, "studio_master", StudioMasterPlanner(canon, repertoire))
    monkeypatch.setattr(main, "performance_controller", PerformanceController())


def test_studio_master_catalog_analyze_and_plan(monkeypatch, tmp_path) -> None:
    _patch_runtime(monkeypatch, tmp_path)
    samples = [0.0] * 400
    for index in (20, 100, 205, 300):
        samples[index : index + 12] = [0.9, 0.8, 0.6, 0.4] + [0.0] * 8

    with TestClient(main.app) as client:
        capabilities = client.get("/v1/studio-master/capabilities")
        canon = client.get("/v1/studio-master/canon")
        repertoire = client.get("/v1/studio-master/repertoire")
        analysis = client.post(
            "/v1/studio-master/groove/analyze",
            json={"samples": samples, "sample_rate": 8_000, "bpm": 140},
        )
        plan = client.post(
            "/v1/studio-master/responsive-plan",
            json={
                "style": "brazilian_funk_heavy",
                "canon_id": "br_funk_mandelao",
                "repertoire_id": "brazilian_funk_heavy_kit",
                "bpm": 140,
                "swing_ratio": 0.55,
            },
        )
        state = client.get("/v1/studio-master/performance/session-http")

    assert capabilities.status_code == 200
    assert capabilities.json()["enabled"] is True
    assert capabilities.json()["canon_entries"] >= 8
    assert len(canon.json()["entries"]) >= 8
    assert len(repertoire.json()["profiles"]) >= 4
    assert analysis.status_code == 200
    assert analysis.json()["method"] == "deterministic-onset-energy/v1"
    assert plan.status_code == 200
    assert plan.json()["handoff"]["approval_required"] is True
    assert state.status_code == 200
    assert state.json()["session_id"] == "session-http"


def test_studio_master_websocket_accepts_performance_commands(monkeypatch, tmp_path) -> None:
    _patch_runtime(monkeypatch, tmp_path)

    with TestClient(main.app) as client, client.websocket_connect(
        "/ws/studio-master/session-ws/performance"
    ) as socket:
        initial = socket.receive_json()
        socket.send_json({"action": "SET_SWING", "value": "65%"})
        swing = socket.receive_json()
        socket.send_json({"action": "SET_GRID_FOLLOW", "value": False})
        grid = socket.receive_json()
        socket.send_json({"action": "PUSH_TO_LIBRARY", "reference_id": "ref-01"})
        proposal = socket.receive_json()

    assert initial["event"] == "performance_state"
    assert swing["state"]["swing_ratio"] == 0.65
    assert grid["state"]["grid_follow"] is False
    assert proposal["state"]["status"] == "PENDING_APPROVAL"


def test_studio_master_can_be_disabled(monkeypatch, tmp_path) -> None:
    _patch_runtime(monkeypatch, tmp_path, enabled=False)

    with TestClient(main.app) as client:
        capabilities = client.get("/v1/studio-master/capabilities")
        canon = client.get("/v1/studio-master/canon")
        analysis = client.post(
            "/v1/studio-master/groove/analyze",
            json={"samples": [0.0], "sample_rate": 8_000, "bpm": 140},
        )

    assert capabilities.status_code == 200
    assert capabilities.json()["enabled"] is False
    assert canon.status_code == 503
    assert analysis.status_code == 503
