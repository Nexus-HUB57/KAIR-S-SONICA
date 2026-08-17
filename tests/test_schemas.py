from kairos_core.schemas import TrackRequest
from pydantic import ValidationError


def test_track_request_normalizes_scale_alias() -> None:
    request = TrackRequest(prompt="teste", scale="m")
    assert request.scale == "minor"


def test_track_request_rejects_invalid_bpm() -> None:
    try:
        TrackRequest(prompt="teste", bpm=300)
    except ValidationError as exc:
        assert "bpm" in str(exc).lower()
    else:
        raise AssertionError("bpm inválido deveria ser rejeitado")
