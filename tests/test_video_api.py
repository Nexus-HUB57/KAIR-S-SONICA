from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.api.main import app, settings


def test_readiness_checks_skyreels_runtime(tmp_path: Path) -> None:
    original_enabled = settings.enable_skyreels
    original_repo = settings.skyreels_repo
    original_model = settings.skyreels_model_id
    repo = tmp_path / "SkyReels-V2"
    repo.mkdir()
    (repo / "generate_video_df.py").write_text("# fixture", encoding="utf-8")
    model = tmp_path / "model"
    model.mkdir()
    settings.enable_skyreels = True
    settings.skyreels_repo = repo
    settings.skyreels_model_id = str(model)

    try:
        with TestClient(app) as client:
            response = client.get("/ready")
            assert response.status_code == 200
            assert response.json()["checks"]["skyreels_entrypoint"] == "ok"
            assert response.json()["checks"]["skyreels_model"] == "ok"
    finally:
        settings.enable_skyreels = original_enabled
        settings.skyreels_repo = original_repo
        settings.skyreels_model_id = original_model


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="FFmpeg é requisito do perfil de produção")
def test_video_endpoint_completes_end_to_end_with_local_fake_backend(tmp_path: Path) -> None:
    original = {
        "output_dir": settings.output_dir,
        "upload_dir": settings.upload_dir,
        "enable_skyreels": settings.enable_skyreels,
        "skyreels_repo": settings.skyreels_repo,
        "skyreels_model_id": settings.skyreels_model_id,
        "skyreels_python": settings.skyreels_python,
        "ffprobe_bin": settings.ffprobe_bin,
    }
    settings.output_dir = tmp_path / "output"
    settings.upload_dir = tmp_path / "uploads"
    settings.enable_skyreels = True
    settings.skyreels_repo = tmp_path / "SkyReels-V2"
    settings.skyreels_repo.mkdir()
    settings.skyreels_model_id = str(tmp_path / "model")
    Path(settings.skyreels_model_id).mkdir()
    settings.skyreels_python = sys.executable
    settings.ffprobe_bin = shutil.which("ffprobe") or "ffprobe"
    fake_backend = settings.skyreels_repo / "generate_video_df.py"
    fake_backend.write_text(
        """import argparse\nimport subprocess\nfrom pathlib import Path\n\nparser = argparse.ArgumentParser()\nparser.add_argument('--outdir', required=True)\nargs, _ = parser.parse_known_args()\noutdir = Path(args.outdir)\noutdir.mkdir(parents=True, exist_ok=True)\nsubprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=black:s=32x32:d=1', '-y', str(outdir / 'generated.mp4')], check=True)\n""",
        encoding="utf-8",
    )

    try:
        with TestClient(app) as client:
            response = client.post(
                "/v1/video/generate",
                json={"prompt": "A local production smoke shot", "seed": 42},
            )
            assert response.status_code == 202
            task_id = response.json()["task_id"]
            snapshot = None
            for _ in range(100):
                snapshot = client.get(f"/v1/tasks/{task_id}").json()
                if snapshot["status"] in {"SUCCEEDED", "FAILED"}:
                    break
                time.sleep(0.05)
            assert snapshot is not None
            assert snapshot["status"] == "SUCCEEDED", snapshot
            assert snapshot["artifact_url"] == f"/v1/video/{task_id}"
            video = client.get(f"/v1/video/{task_id}")
            assert video.status_code == 200
            assert video.headers["content-type"].startswith("video/mp4")
            assert len(video.content) > 0
            metadata = client.get(f"/v1/metadata/{task_id}")
            assert metadata.status_code == 200
            assert metadata.json()["duration_seconds"] > 0
    finally:
        for key, value in original.items():
            setattr(settings, key, value)


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


def test_video_capabilities_exposes_native_backend() -> None:
    original_enabled = settings.enable_skyreels
    original_native = settings.skyreels_native_api
    settings.enable_skyreels = True
    settings.skyreels_native_api = True

    try:
        with TestClient(app) as client:
            response = client.get("/v1/video/capabilities")
            assert response.status_code == 200
            payload = response.json()
            assert payload["backends"]["native"]["enabled"] is True
            assert payload["modes"] == ["t2v", "i2v", "extend", "start_end"]
            assert payload["default_backend"] == "cli"
    finally:
        settings.enable_skyreels = original_enabled
        settings.skyreels_native_api = original_native


def test_native_readiness_requires_model_and_runtime(tmp_path: Path, monkeypatch) -> None:
    original = {
        "enable_skyreels": settings.enable_skyreels,
        "skyreels_native_api": settings.skyreels_native_api,
        "skyreels_native_model_id": settings.skyreels_native_model_id,
        "skyreels_device": settings.skyreels_device,
    }
    settings.enable_skyreels = True
    settings.skyreels_native_api = True
    settings.skyreels_native_model_id = str(tmp_path / "native-model")
    settings.skyreels_device = "cpu"

    try:
        with TestClient(app) as client:
            response = client.get("/ready")
            assert response.status_code == 503
            assert response.json()["detail"]["checks"]["skyreels_native_model"] == "missing"

        native_model = Path(settings.skyreels_native_model_id)
        for relative in ("model_index.json", "vae/config.json", "transformer/config.json"):
            path = native_model / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}", encoding="utf-8")
        monkeypatch.setattr(
            "services.api.main.importlib.util.find_spec",
            lambda name: object(),
        )
        with TestClient(app) as client:
            response = client.get("/ready")
            assert response.status_code == 200
            assert response.json()["checks"]["skyreels_native_model"] == "ok"
            assert response.json()["checks"]["skyreels_native_runtime"] == "ok"
    finally:
        for key, value in original.items():
            setattr(settings, key, value)
