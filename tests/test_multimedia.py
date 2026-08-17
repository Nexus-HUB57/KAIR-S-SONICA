from pathlib import Path

import numpy as np
import pytest
from kairos_core.audio.orchestrator import MultimediaOrchestrator
from kairos_core.audio.processing import AudioProcessor
from kairos_core.audio.transcode import write_wav
from kairos_core.config import Settings
from kairos_core.schemas import MultimediaRequest


def _create_wav(path: Path, duration: float = 1.0) -> None:
    sample_rate = 8_000
    t = np.arange(round(sample_rate * duration), dtype=np.float32) / sample_rate
    audio = np.column_stack((0.2 * np.sin(2 * np.pi * 220 * t), 0.2 * np.sin(2 * np.pi * 220 * t)))
    write_wav(path, audio, sample_rate)


def test_audio_processor_analyzes_wav(tmp_path: Path) -> None:
    source = tmp_path / "reference.wav"
    _create_wav(source)
    analysis = AudioProcessor().analyze(source)
    assert analysis.sample_rate == 8_000
    assert analysis.channels == 2
    assert 0.99 < analysis.duration_seconds < 1.01
    assert analysis.peak_dbfs < 0


def test_multimedia_orchestrator_uses_sidecar_and_writes_artifacts(tmp_path: Path) -> None:
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "output"
    upload_dir.mkdir()
    source = upload_dir / "reference.wav"
    _create_wav(source)
    source.with_suffix(".txt").write_text("linha um\nlinha dois", encoding="utf-8")

    settings = Settings(output_dir=output_dir, upload_dir=upload_dir)
    request = MultimediaRequest(audio_path="reference.wav", duration_seconds=1, transcription_backend="sidecar")
    result = MultimediaOrchestrator(settings).run(request, task_id="multimedia-test")

    assert result.artifact_path is not None and result.artifact_path.is_file()
    assert result.transcript_path is not None and result.transcript_path.is_file()
    assert result.metadata_path.is_file()
    assert result.metadata["transcription"]["text"] == "linha um\nlinha dois"
    assert result.metadata["analysis"]["channels"] == 2


def test_multimedia_orchestrator_rejects_outside_path(tmp_path: Path) -> None:
    settings = Settings(output_dir=tmp_path / "output", upload_dir=tmp_path / "uploads")
    request = MultimediaRequest(audio_path="/etc/hosts", generate_audio=False, transcribe=False, analyze_audio=False)
    with pytest.raises(ValueError, match="data/uploads ou data/output"):
        MultimediaOrchestrator(settings).run(request, task_id="unsafe")
