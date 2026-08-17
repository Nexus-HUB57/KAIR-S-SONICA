from kairos_core.agents.maestro import MaestroAgent
from kairos_core.schemas import TrackRequest


def test_maestro_extracts_bpm_and_key_from_prompt() -> None:
    request = TrackRequest(prompt="Boom bap a 92 BPM em D minor", bpm=140, key="C#", scale="major")
    plan = MaestroAgent().build_plan(request, request_id="test")
    assert plan.bpm == 92
    assert plan.key.lower() == "d"
    assert plan.scale == "minor"
    assert plan.sections[-1].end_seconds == request.duration_seconds
