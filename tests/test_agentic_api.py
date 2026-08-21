from __future__ import annotations

from fastapi.testclient import TestClient
from kairos_core.agentic import AgenticOrchestrator
from kairos_core.config import Settings

from services.api import main


def _patch_agentic_runtime(monkeypatch, tmp_path) -> None:
    settings = Settings(
        task_db_path=tmp_path / "tasks.sqlite3",
        agentic_memory_dir=tmp_path / "memory",
        worker_mode="queue",
    )
    monkeypatch.setattr(main, "settings", settings)
    monkeypatch.setattr(main, "store", main.TaskStore(settings.task_db_path))
    monkeypatch.setattr(main, "agentic_orchestrator", AgenticOrchestrator(settings))


def test_agentic_run_plans_without_creating_tasks(monkeypatch, tmp_path) -> None:
    _patch_agentic_runtime(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        response = client.post(
            "/v1/agentic/run",
            json={
                "prompt": "campanha vertical com chuva neon",
                "project_id": "api-test",
                "duration_seconds": 10,
                "scene_seconds": 5,
                "seed": 7,
                "submit_handoffs": False,
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "READY_FOR_APPROVAL"
    assert len(payload["roles"]) == 12
    assert len(payload["handoffs"]) == 3
    assert payload["submissions"] == []


def test_agentic_submission_requires_explicit_approval(monkeypatch, tmp_path) -> None:
    _patch_agentic_runtime(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        response = client.post(
            "/v1/agentic/run",
            json={"prompt": "teste", "submit_handoffs": True, "approve_handoffs": False},
        )

    assert response.status_code == 409
    assert "approve_handoffs" in response.json()["detail"]


def test_agentic_submission_reuses_task_store(monkeypatch, tmp_path) -> None:
    _patch_agentic_runtime(monkeypatch, tmp_path)

    with TestClient(main.app) as client:
        response = client.post(
            "/v1/agentic/run",
            json={
                "prompt": "campanha de produto em cidade futurista",
                "duration_seconds": 10,
                "scene_seconds": 5,
                "submit_handoffs": True,
                "approve_handoffs": True,
            },
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "SUBMITTED"
    assert len(payload["submissions"]) == 3
    for submission in payload["submissions"]:
        assert main.store.get(submission["task_id"]) is not None
    jobs = main.store.claim_recoverable_jobs("agentic-api-test")
    assert {kind for _, kind, _ in jobs} == {"video", "multimedia"}
