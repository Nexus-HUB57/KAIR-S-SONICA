from __future__ import annotations

from fastapi.testclient import TestClient
from kairos_core.artistic_island import SkillGenerator
from kairos_core.config import Settings

from services.api import main


def _patch_island_runtime(monkeypatch, tmp_path, enabled: bool = True) -> None:
    settings = Settings(
        task_db_path=tmp_path / "tasks.sqlite3",
        instrument_atlas_path=main.Path("config/instrument_atlas.yaml"),
        artistic_island_enabled=enabled,
    )
    monkeypatch.setattr(main, "settings", settings)
    monkeypatch.setattr(main, "artistic_island", SkillGenerator(atlas_path=settings.instrument_atlas_path))


def test_artistic_island_catalog_and_mix_plan(monkeypatch, tmp_path) -> None:
    _patch_island_runtime(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        capabilities = client.get("/v1/artistic-island/capabilities")
        instruments = client.get("/v1/artistic-island/instruments")
        plan = client.post(
            "/v1/artistic-island/mix-plan",
            json={"instrument": "lead_vocal", "context": "vocal", "prompt": "lead limpo e presente"},
        )

    assert capabilities.status_code == 200
    assert capabilities.json()["enabled"] is True
    assert capabilities.json()["replaces_existing_core"] is False
    assert instruments.status_code == 200
    assert len(instruments.json()["instruments"]) >= 15
    assert plan.status_code == 200
    assert plan.json()["instrument"] == "lead_vocal"
    assert plan.json()["chain"]


def test_artistic_island_returns_422_for_unknown_instrument(monkeypatch, tmp_path) -> None:
    _patch_island_runtime(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        response = client.post("/v1/artistic-island/mix-plan", json={"instrument": "not-in-atlas"})

    assert response.status_code == 422
    assert "Instrumento não encontrado" in response.json()["detail"]


def test_artistic_island_can_be_disabled(monkeypatch, tmp_path) -> None:
    _patch_island_runtime(monkeypatch, tmp_path, enabled=False)

    with TestClient(main.app) as client:
        capabilities = client.get("/v1/artistic-island/capabilities")
        response = client.get("/v1/artistic-island/instruments")

    assert capabilities.status_code == 200
    assert capabilities.json()["enabled"] is False
    assert response.status_code == 503
