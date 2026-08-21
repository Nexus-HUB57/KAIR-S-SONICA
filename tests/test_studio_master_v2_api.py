from __future__ import annotations

from fastapi.testclient import TestClient
from kairos_core.config import Settings
from kairos_core.studio_master import (
    AutoRetrainGuard,
    CanonIndex,
    PerformanceController,
    ProductionHistoryStore,
    RepertoireCatalog,
    StudioMasterPlanner,
)

from services.api import main


def _patch_runtime(monkeypatch, tmp_path, *, enabled: bool = True, memory_enabled: bool = False) -> None:
    settings = Settings(
        task_db_path=tmp_path / "tasks.sqlite3",
        canon_index_path=main.Path("config/canon_index.yaml"),
        instrumentation_repertoire_path=main.Path("config/instrumentation_repertoire.yaml"),
        studio_master_analytics_path=tmp_path / "production_history.json",
        studio_master_memory_path=tmp_path / "artist-memory.jsonl",
        studio_master_enabled=enabled,
        studio_master_memory_enabled=memory_enabled,
    )
    monkeypatch.setattr(main, "settings", settings)
    canon = CanonIndex.load(settings.canon_index_path)
    repertoire = RepertoireCatalog.load(settings.instrumentation_repertoire_path)
    monkeypatch.setattr(main, "canon_index", canon)
    monkeypatch.setattr(main, "studio_master", StudioMasterPlanner(canon, repertoire))
    monkeypatch.setattr(main, "performance_controller", PerformanceController())
    monkeypatch.setattr(
        main,
        "auto_retrain_guard",
        AutoRetrainGuard(tmp_path / "retrain.json", enabled=False),
    )
    monkeypatch.setattr(
        main,
        "artist_memory",
        main.LocalArtistMemory(settings.studio_master_memory_path, enabled=memory_enabled),
    )
    monkeypatch.setattr(main, "production_history", ProductionHistoryStore(settings.studio_master_analytics_path))


def test_studio_master_v2_endpoints(monkeypatch, tmp_path) -> None:
    _patch_runtime(monkeypatch, tmp_path)
    with TestClient(main.app) as client:
        arrangement = client.post(
            "/v1/studio-master/arrangement",
            json={"style": "brazilian_funk_heavy", "total_bars": 40, "bpm": 142},
        )
        expression = client.post(
            "/v1/studio-master/expression",
            json={
                "bpm": 142,
                "notes": [{"pitch": 60, "time_beats": 0.25, "duration_beats": 1, "velocity": 80}],
                "seed": 1,
            },
        )
        sketch = client.post(
            "/v1/studio-master/hum-to-midi",
            json={
                "frames": [
                    {"time_seconds": 0.0, "frequency_hz": 440, "confidence": 0.9},
                    {"time_seconds": 0.1, "frequency_hz": 440, "confidence": 0.9},
                ]
            },
        )
        signature = client.post("/v1/studio-master/signature-plan", json={"intensity": 0.7})
        ducking = client.post(
            "/v1/studio-master/ducking/preview",
            json={"mix_bus": [1.0] * 32, "reference_track": [0.0] * 16 + [1.0] * 16},
        )
        perceptual = client.post("/v1/studio-master/perceptual/score", json={"samples": [0.1] * 64})
        adapters = client.get("/v1/studio-master/adapters")
        analytics = client.get("/v1/studio-master/analytics")
        retraining = client.get("/v1/studio-master/retraining")
        clip = client.post("/v1/studio-master/viral-clip-plan", json={})
        record_blocked = client.post(
            "/v1/studio-master/analytics/record",
            json={"task_id": "t-1", "genre": "funk", "approved": False},
        )
        record = client.post(
            "/v1/studio-master/analytics/record",
            json={"task_id": "t-1", "genre": "funk", "bpm": 142, "mos_score": 4.2, "approved": True},
        )
        feedback = client.post(
            "/v1/studio-master/memory/feedback",
            json={"context": "funk hook", "adjustments": {"swing": 0.64}},
        )

    assert arrangement.status_code == 200
    assert sum(section["bars"] for section in arrangement.json()["sections"]) == 40
    assert expression.status_code == 200
    assert expression.json()["method"] == "deterministic-expression/v1"
    assert sketch.status_code == 200
    assert sketch.json()["notes"][0]["midi_note"] == 69
    assert signature.status_code == 200
    assert signature.json()["guardrails"]["source_imitation"] is False
    assert ducking.status_code == 200
    assert ducking.json()["method"] == "numpy-rms-envelope/v1"
    assert perceptual.status_code == 200
    assert perceptual.json()["method"] == "technical-signal-health/v1"
    assert adapters.status_code == 200
    assert all(item["enabled"] is False for item in adapters.json()["adapters"])
    assert analytics.status_code == 200
    assert analytics.json()["source"] == "empty"
    assert record_blocked.status_code == 409
    assert record.status_code == 200
    assert record.json()["stored"] is True
    assert retraining.status_code == 200
    assert retraining.json()["status"] == "DISABLED"
    assert clip.status_code == 200
    assert clip.json()["render"]["automatic_publish"] is False
    assert feedback.status_code == 503


def test_studio_master_memory_feedback_is_opt_in(monkeypatch, tmp_path) -> None:
    _patch_runtime(monkeypatch, tmp_path, memory_enabled=True)
    with TestClient(main.app) as client:
        response = client.post(
            "/v1/studio-master/memory/feedback",
            json={"context": "boom bap verse", "adjustments": {"swing": 0.61}, "project_id": "p-1"},
        )

    assert response.status_code == 200
    assert response.json()["stored"] is True
    assert response.json()["metadata_only"] is True
