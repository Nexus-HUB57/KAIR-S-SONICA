from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from kairos_core.config import Settings
from kairos_core.schemas import VideoRequest
from kairos_core.video.adapter import SkyReelsVideoAdapter, VideoBackendError


def _settings(tmp_path: Path, *, enabled: bool = True) -> Settings:
    repo = tmp_path / "SkyReels-V2"
    repo.mkdir()
    (repo / "generate_video.py").write_text("# fixture", encoding="utf-8")
    (repo / "generate_video_df.py").write_text("# fixture", encoding="utf-8")
    model = tmp_path / "model"
    model.mkdir()
    return Settings(
        output_dir=tmp_path / "output",
        upload_dir=tmp_path / "uploads",
        enable_skyreels=enabled,
        skyreels_repo=repo,
        skyreels_model_id=str(model),
    )


def test_video_request_defaults_are_portable() -> None:
    request = VideoRequest(prompt="A moving cinematic shot")
    assert request.mode == "t2v"
    assert request.engine == "diffusion_forcing"
    assert request.resolution == "540P"
    assert request.num_frames is None
    assert request.offload is True


def test_build_df_t2v_command_uses_resolution_frame_defaults(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    adapter = SkyReelsVideoAdapter(settings)
    request = VideoRequest(prompt="A moving cinematic shot", resolution="720P", seed=42)

    command = adapter.build_command(request, "task-1", tmp_path / "staging")

    assert command[1].endswith("generate_video_df.py")
    assert "--num_frames" in command
    assert command[command.index("--num_frames") + 1] == "121"
    assert command[command.index("--seed") + 1] == "42"
    assert "--overlap_history" not in command


def test_build_i2v_command_resolves_upload_reference(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    settings.upload_dir.mkdir()
    image = settings.upload_dir / "keyframe.png"
    image.write_bytes(b"not-a-real-image-for-command-test")
    adapter = SkyReelsVideoAdapter(settings)
    request = VideoRequest(prompt="Animate the keyframe", mode="i2v", image_path="keyframe.png")

    command = adapter.build_command(request, "task-2", tmp_path / "staging")

    assert command[command.index("--image") + 1] == str(image.resolve())


def test_extend_defaults_overlap_and_rejects_missing_video(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    settings.upload_dir.mkdir()
    video = settings.upload_dir / "prefix.mp4"
    video.write_bytes(b"prefix")
    adapter = SkyReelsVideoAdapter(settings)

    request = VideoRequest(prompt="Continue the shot", mode="extend", video_path="prefix.mp4")
    command = adapter.build_command(request, "task-3", tmp_path / "staging")
    assert command[command.index("--overlap_history") + 1] == "17"
    assert command[command.index("--video_path") + 1] == str(video.resolve())

    with pytest.raises(ValueError, match="modo extend exige video_path"):
        adapter.build_command(
            VideoRequest(prompt="Continue the shot", mode="extend"),
            "task-4",
            tmp_path / "staging-2",
        )

    with pytest.raises(ValueError, match="modo i2v não aceita end_image_path"):
        adapter.build_command(
            VideoRequest(
                prompt="Animate the keyframe",
                mode="i2v",
                image_path="prefix.mp4",
                end_image_path="prefix.mp4",
            ),
            "task-4b",
            tmp_path / "staging-3",
        )


def test_media_path_outside_allowed_roots_is_rejected(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    adapter = SkyReelsVideoAdapter(settings)
    outside = tmp_path / "outside.mp4"
    outside.write_bytes(b"outside")

    with pytest.raises(ValueError, match="caminho de mídia"):
        adapter.build_command(
            VideoRequest(prompt="Unsafe", mode="i2v", image_path=str(outside)),
            "task-5",
            tmp_path / "staging",
        )


def test_run_requires_explicit_backend_enablement(tmp_path: Path) -> None:
    adapter = SkyReelsVideoAdapter(_settings(tmp_path, enabled=False))

    with pytest.raises(VideoBackendError, match="SkyReels está desabilitado"):
        adapter.run(VideoRequest(prompt="A shot"), "task-6")


def test_run_promotes_mp4_and_writes_metadata_without_overwrite(tmp_path: Path, monkeypatch) -> None:
    settings = _settings(tmp_path)
    adapter = SkyReelsVideoAdapter(settings)

    def fake_run(command, cwd=None, check=False, capture_output=False, text=False, timeout=None):
        if command[0] == settings.ffprobe_bin:
            return SimpleNamespace(
                returncode=0,
                stdout=json.dumps({"format": {"duration": "2.0"}, "streams": [{"codec_type": "video"}]}),
                stderr="",
            )
        outdir = Path(command[command.index("--outdir") + 1])
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "generated.mp4").write_bytes(b"mp4")
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("kairos_core.video.adapter.subprocess.run", fake_run)
    request = VideoRequest(prompt="A shot", seed=7)
    result = adapter.run(request, "task-7")

    assert result.artifact_path == settings.output_dir / "task-7.mp4"
    assert result.artifact_path.read_bytes() == b"mp4"
    assert result.metadata_path.is_file()
    assert result.metadata["backend"] == "skyreels-v2"

    with pytest.raises(FileExistsError, match="Saída já existe"):
        adapter.run(request, "task-7")
