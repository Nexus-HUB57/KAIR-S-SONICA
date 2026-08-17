from kairos_core.audio.groove import build_groove_grid
from kairos_core.schemas import GrooveSettings


def test_swing_delays_offbeats() -> None:
    events = build_groove_grid(120, 2, GrooveSettings(swing=0.6, humanize_ms=0), seed=1)
    assert events[0].beat == 0
    assert events[1].beat > 0.25
    assert all(event.beat < 2 for event in events)
