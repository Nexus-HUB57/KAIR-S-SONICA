from __future__ import annotations

import sys
from pathlib import Path

from scripts import provision_skyreels


def test_provision_local_checkpoint_is_idempotent(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "SkyReels-V2"
    repo.mkdir()
    (repo / "generate_video.py").write_text("# fixture", encoding="utf-8")
    (repo / "generate_video_df.py").write_text("# fixture", encoding="utf-8")
    model = tmp_path / "models" / "Skywork" / "SkyReels-V2-DF-1.3B-540P-Diffusers"
    for relative in provision_skyreels.REQUIRED_NATIVE_FILES:
        path = model / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")
    manifest = tmp_path / "models" / "kairos-skyreels-manifest.json"
    argv = [
        "provision_skyreels.py",
        "--repo",
        str(repo),
        "--models-root",
        str(tmp_path / "models"),
        "--native-model-id",
        "Skywork/SkyReels-V2-DF-1.3B-540P-Diffusers",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    assert provision_skyreels.main() == 0
    first_manifest = manifest.read_text(encoding="utf-8")
    assert "HF_TOKEN" not in first_manifest
    assert "model_index.json" in first_manifest
    assert provision_skyreels.main() == 0
    assert manifest.is_file()
    assert manifest.read_text(encoding="utf-8") != first_manifest


def test_provision_dry_run_does_not_create_files(tmp_path: Path, monkeypatch) -> None:
    repo = tmp_path / "SkyReels-V2"
    repo.mkdir()
    (repo / "generate_video_df.py").write_text("# fixture", encoding="utf-8")
    models_root = tmp_path / "models"
    argv = [
        "provision_skyreels.py",
        "--repo",
        str(repo),
        "--models-root",
        str(models_root),
        "--dry-run",
    ]
    monkeypatch.setattr(sys, "argv", argv)

    assert provision_skyreels.main() == 0
    assert not (models_root / "kairos-skyreels-manifest.json").exists()
