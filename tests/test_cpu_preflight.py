from __future__ import annotations

from pathlib import Path

from kairos_core.config import Settings
from kairos_core.studio_master.auto_review import CANONICAL_VOICE_REFERENCE
from kairos_core.studio_master.cpu_preflight import (
    SINGLE1_APPROVED_VIDEO,
    load_single1_declaration,
    simulate_single1_cpu,
)


def _fake_probe(path: Path, ffprobe_bin: str) -> dict[str, object]:
    del ffprobe_bin
    return {
        "path": str(path),
        "sha256": "a" * 64,
        "byte_size": 123,
        "duration_seconds": 10.0,
        "streams": [
            {
                "index": 0,
                "codec_type": "video",
                "codec_name": "h264",
                "width": 720,
                "height": 1280,
                "avg_frame_rate": "24/1",
            },
            {"index": 1, "codec_type": "audio", "codec_name": "aac"},
        ],
    }


def test_load_single1_declaration_is_canonical() -> None:
    root = Path(__file__).resolve().parents[1]
    declaration = load_single1_declaration(root)

    assert declaration.title == "UNLEASH THE DRAGON"
    assert declaration.bpm == 102
    assert declaration.key == "Fá menor"
    assert declaration.voice_reference == CANONICAL_VOICE_REFERENCE


def test_cpu_simulation_validates_metadata_without_rendering() -> None:
    root = Path(__file__).resolve().parents[1]
    video_path = root / SINGLE1_APPROVED_VIDEO
    result = simulate_single1_cpu(
        Settings(), root, video_path, probe=_fake_probe
    ).to_dict()

    assert result["simulation"] == "CPU_METADATA_ONLY"
    assert result["technical_gate_passed"] is True
    assert result["overall_decision"] == "READY_FOR_APPROVAL"
    assert result["preflight_auto_repair_false"]["decision"] == "READY_FOR_APPROVAL"
    assert result["preflight_auto_repair_true"]["decision"] == "READY_FOR_APPROVAL"
    assert result["backend"]["local_gpu"] == "BLOCKED"
    assert result["backend"]["render_called"] is False
    assert "no POST /v1/video/generate" in result["operations"]


def test_cpu_simulation_rejects_incorrect_voice_reference() -> None:
    root = Path(__file__).resolve().parents[1]
    video_path = root / SINGLE1_APPROVED_VIDEO
    result = simulate_single1_cpu(
        Settings(),
        root,
        video_path,
        overrides={"voice_reference": "assets/audio/not-the-canonical-reference.mp3"},
        probe=_fake_probe,
    ).to_dict()

    assert result["overall_decision"] == "REJECTED"
    assert result["preflight_auto_repair_false"]["decision"] == "REJECTED"
    assert any(
        finding["code"] == "AUD-VOICE-01"
        for finding in result["preflight_auto_repair_false"]["findings"]
    )


def test_cpu_simulation_rejects_incomplete_source_manifest() -> None:
    root = Path(__file__).resolve().parents[1]
    video_path = root / SINGLE1_APPROVED_VIDEO
    result = simulate_single1_cpu(
        Settings(),
        root,
        video_path,
        overrides={"source_manifest": {"path": "unverified.mp4"}},
        probe=_fake_probe,
    ).to_dict()

    assert result["technical_gate_passed"] is False
    assert "source_manifest incompleto" in result["technical_findings"]
    assert result["overall_decision"] == "REJECTED"
