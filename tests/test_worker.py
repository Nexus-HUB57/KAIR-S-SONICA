from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest
from kairos_core.config import Settings
from kairos_core.schemas import VideoRequest

import services.api.main as api_main
from scripts.run_worker import Worker
from services.api.main import TaskStore


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="FFmpeg é requisito do perfil de produção")
def test_persistent_worker_claims_and_completes_video_job(tmp_path: Path) -> None:
    original_store = api_main.store
    original_settings = api_main.settings
    repo = tmp_path / "SkyReels-V2"
    repo.mkdir()
    for name in ("generate_video.py", "generate_video_df.py"):
        (repo / name).write_text(
            """import argparse\nimport subprocess\nfrom pathlib import Path\n\nparser = argparse.ArgumentParser()\nparser.add_argument('--outdir', required=True)\nargs, _ = parser.parse_known_args()\noutdir = Path(args.outdir)\noutdir.mkdir(parents=True, exist_ok=True)\nsubprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=black:s=32x32:d=1', '-y', str(outdir / 'generated.mp4')], check=True)\n""",
            encoding="utf-8",
        )
    model = tmp_path / "model"
    model.mkdir()
    settings = Settings(
        output_dir=tmp_path / "output",
        upload_dir=tmp_path / "uploads",
        task_db_path=tmp_path / "tasks.sqlite3",
        enable_skyreels=True,
        skyreels_repo=repo,
        skyreels_model_id=str(model),
        skyreels_python=sys.executable,
        ffprobe_bin=shutil.which("ffprobe") or "ffprobe",
        worker_mode="queue",
    )
    store = TaskStore(settings.task_db_path)
    request = VideoRequest(prompt="queue smoke", seed=7)
    store.create("queue-video", job_kind="video", payload=request.model_dump(mode="json"))
    api_main.store = store
    api_main.settings = settings

    try:
        Worker(store, poll_seconds=0.1).run(once=True)
        snapshot = store.get("queue-video")
        assert snapshot is not None
        assert snapshot.status == "SUCCEEDED", snapshot
        assert snapshot.artifact_url == "/v1/video/queue-video"
        assert (settings.output_dir / "queue-video.mp4").is_file()
        assert (settings.output_dir / "queue-video.metadata.json").is_file()
        assert store.claim_recoverable_jobs("second-worker") == []
    finally:
        api_main.store = original_store
        api_main.settings = original_settings
