import io
import json
import time
import wave
from pathlib import Path

import numpy as np
from fastapi.testclient import TestClient

from services.api.main import app, settings


def wav_bytes(duration_seconds: float = 0.25, sample_rate: int = 8_000) -> bytes:
    samples = np.zeros(int(duration_seconds * sample_rate), dtype=np.int16)
    output = io.BytesIO()
    with wave.open(output, "wb") as wave_file:
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)
        wave_file.setframerate(sample_rate)
        wave_file.writeframes(samples.tobytes())
    return output.getvalue()


def wait_for_task(client: TestClient, task_id: str) -> dict:
    snapshot = {}
    for _ in range(80):
        snapshot = client.get(f"/v1/tasks/{task_id}").json()
        if snapshot.get("status") in {"SUCCEEDED", "FAILED"}:
            return snapshot
        time.sleep(0.05)
    return snapshot


def test_studio_upload_requires_configuration_and_bearer() -> None:
    original_token = settings.studio_upload_token
    settings.studio_upload_token = None
    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/studio/assets",
                files={"file": ("take.wav", wav_bytes(), "audio/wav")},
            )
        assert response.status_code == 503
    finally:
        settings.studio_upload_token = original_token


def test_studio_upload_validates_extension_and_size(tmp_path: Path) -> None:
    original_token = settings.studio_upload_token
    original_upload = settings.upload_dir
    original_max_bytes = settings.studio_upload_max_bytes
    settings.studio_upload_token = "studio-secret"
    settings.upload_dir = tmp_path / "uploads"
    settings.studio_upload_max_bytes = 64
    try:
        with TestClient(app) as client:
            unsupported = client.post(
                "/v1/studio/assets",
                headers={"Authorization": "Bearer studio-secret"},
                files={"file": ("take.txt", b"not-audio", "text/plain")},
            )
            oversized = client.post(
                "/v1/studio/assets",
                headers={"Authorization": "Bearer studio-secret"},
                files={"file": ("take.wav", wav_bytes(), "audio/wav")},
            )
        assert unsupported.status_code == 415
        assert oversized.status_code == 413
        assert not list(settings.upload_dir.rglob("*.part"))
    finally:
        settings.studio_upload_token = original_token
        settings.upload_dir = original_upload
        settings.studio_upload_max_bytes = original_max_bytes


def test_studio_upload_and_explicit_handoff_run_multimedia_pipeline(tmp_path: Path) -> None:
    original_token = settings.studio_upload_token
    original_upload = settings.upload_dir
    original_output = settings.output_dir
    original_max_duration = settings.studio_upload_max_duration_seconds
    settings.studio_upload_token = "studio-secret"
    settings.upload_dir = tmp_path / "uploads"
    settings.output_dir = tmp_path / "output"
    settings.studio_upload_max_duration_seconds = 2
    try:
        with TestClient(app) as client:
            upload = client.post(
                "/v1/studio/assets",
                headers={"Authorization": "Bearer studio-secret"},
                files={"file": ("Káiros Take 01.wav", wav_bytes(), "audio/wav")},
            )
            assert upload.status_code == 201
            asset = upload.json()
            assert asset["asset_id"].startswith("asset-")
            assert asset["audio_path"].startswith("studio/")
            uploaded_path = settings.upload_dir / asset["audio_path"]
            manifest_path = settings.upload_dir / "studio" / f"{asset['asset_id']}.json"
            assert uploaded_path.is_file()
            assert manifest_path.is_file()
            assert json.loads(manifest_path.read_text(encoding="utf-8"))["sha256"] == asset["sha256"]

            unauthorized = client.post(
                "/v1/studio/handoff",
                json={"asset_id": asset["asset_id"]},
            )
            assert unauthorized.status_code == 401

            handoff = client.post(
                "/v1/studio/handoff",
                headers={"Authorization": "Bearer studio-secret"},
                json={
                    "asset_id": asset["asset_id"],
                    "request": {
                        "prompt": "Avaliar take vocal do KTD",
                        "generate_audio": False,
                        "transcribe": False,
                        "analyze_audio": True,
                    },
                },
            )
            assert handoff.status_code == 202
            task_id = handoff.json()["task_id"]
            snapshot = wait_for_task(client, task_id)
            assert snapshot["status"] == "SUCCEEDED"
            metadata = client.get(f"/v1/metadata/{task_id}")
            assert metadata.status_code == 200
            assert asset["audio_path"] in metadata.text
    finally:
        settings.studio_upload_token = original_token
        settings.upload_dir = original_upload
        settings.output_dir = original_output
        settings.studio_upload_max_duration_seconds = original_max_duration
