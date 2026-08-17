import wave

from kairos_core.audio.pipeline import AudioPipeline
from kairos_core.config import Settings
from kairos_core.schemas import TrackRequest


def test_pipeline_writes_valid_wav(tmp_path) -> None:
    settings = Settings(output_dir=tmp_path)
    request = TrackRequest(prompt="demo", duration_seconds=1, output_format="wav")
    result = AudioPipeline(settings).run(request, request_id="pipeline-test")
    assert result.artifact_path.exists()
    with wave.open(str(result.artifact_path), "rb") as handle:
        assert handle.getnchannels() == 2
        assert handle.getframerate() == request.sample_rate
        assert handle.getnframes() > 0
