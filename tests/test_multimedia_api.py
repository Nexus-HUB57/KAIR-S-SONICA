import time
from pathlib import Path

import numpy as np
from fastapi.testclient import TestClient
from kairos_core.audio.transcode import write_wav

from services.api.main import app, settings


def test_orchestrate_endpoint_returns_multimedia_result(tmp_path: Path) -> None:
    original_output = settings.output_dir
    original_upload = settings.upload_dir
    settings.output_dir = tmp_path / "output"
    settings.upload_dir = tmp_path / "uploads"
    settings.upload_dir.mkdir()
    t = np.arange(8_000, dtype=np.float32) / 8_000
    source = settings.upload_dir / "reference.wav"
    write_wav(source, np.column_stack((0.1 * np.sin(2 * np.pi * 220 * t),) * 2), 8_000)
    source.with_suffix(".txt").write_text("referência vocal", encoding="utf-8")

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/orchestrate",
                json={
                    "audio_path": "reference.wav",
                    "transcribe": True,
                    "transcription_backend": "sidecar",
                    "analyze_audio": True,
                    "generate_audio": True,
                    "duration_seconds": 1,
                },
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
            assert snapshot["status"] == "SUCCEEDED"
            assert snapshot["result"]["transcript_url"] == f"/v1/transcript/{task_id}"
            assert client.get(f"/v1/audio/{task_id}").status_code == 200
            assert client.get(f"/v1/transcript/{task_id}").status_code == 200
            assert client.get(f"/v1/metadata/{task_id}").status_code == 200
    finally:
        settings.output_dir = original_output
        settings.upload_dir = original_upload
