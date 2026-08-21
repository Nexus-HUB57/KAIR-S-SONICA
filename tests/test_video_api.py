from __future__ import annotations

import time
from pathlib import Path

from fastapi.testclient import TestClient

from services.api.main import app, settings


def test_video_endpoint_fails_explicitly_when_backend_is_disabled(tmp_path: Path) -> None:
    original_output = settings.output_dir
    original_upload = settings.upload_dir
    original_enabled = settings.enable_skyreels
    settings.output_dir = tmp_path / "output"
    settings.upload_dir = tmp_path / "uploads"
    settings.enable_skyreels = False

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/video/generate",
                json={"prompt": "A cinematic moving shot", "seed": 42},
            )
            assert response.status_code == 202
            task_id = response.json()["task_id"]
            snapshot = None
            for _ in range(60):
                snapshot = client.get(f"/v1/tasks/{task_id}").json()
                if snapshot["status"] in {"SUCCEEDED", "FAILED"}:
                    break
                time.sleep(0.05)
            assert snapshot is not None
            assert snapshot["status"] == "FAILED"
            assert "SkyReels está desabilitado" in snapshot["error"]
            assert client.get(f"/v1/video/{task_id}").status_code == 409
    finally:
        settings.output_dir = original_output
        settings.upload_dir = original_upload
        settings.enable_skyreels = original_enabled
