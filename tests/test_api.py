import time

from fastapi.testclient import TestClient

from services.api.main import app, settings


def test_health_and_plan() -> None:
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        response = client.post("/v1/plan", json={"prompt": "92 BPM D minor"})
        assert response.status_code == 200
        assert response.json()["bpm"] == 92


def test_generate_task_completes(tmp_path) -> None:
    original = settings.output_dir
    settings.output_dir = tmp_path
    try:
        with TestClient(app) as client:
            response = client.post("/v1/generate", json={"prompt": "demo", "duration_seconds": 1})
            assert response.status_code == 202
            task_id = response.json()["task_id"]
            for _ in range(40):
                snapshot = client.get(f"/v1/tasks/{task_id}").json()
                if snapshot["status"] in {"SUCCEEDED", "FAILED"}:
                    break
                time.sleep(0.05)
            assert snapshot["status"] == "SUCCEEDED"
            assert client.get(f"/v1/audio/{task_id}").status_code == 200
    finally:
        settings.output_dir = original
