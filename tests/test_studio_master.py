from __future__ import annotations

import numpy as np
from kairos_core.agents.rhythm import RhythmEvent
from kairos_core.studio_master import (
    CanonIndex,
    DeterministicGrooveExtractor,
    PerformanceCommand,
    PerformanceController,
    RepertoireCatalog,
    ResponsivePlanRequest,
    StudioMasterPlanner,
    apply_flow_to_events,
)


def _catalogs() -> tuple[CanonIndex, RepertoireCatalog]:
    return CanonIndex.load("config/canon_index.yaml"), RepertoireCatalog.load(
        "config/instrumentation_repertoire.yaml"
    )


def test_canon_and_repertoire_load_versioned_metadata() -> None:
    canon, repertoire = _catalogs()

    assert len(canon.entries()) >= 8
    assert canon.get("br_funk_mandelao").region == "BRAZIL"
    assert len(repertoire.profiles()) >= 4
    assert repertoire.get(style="brazilian_funk_heavy").id == "brazilian_funk_heavy_kit"
    assert repertoire.mixing_chain("brazilian_funk_heavy")["id"] == "brazilian_funk_heavy"


def test_groove_extractor_is_deterministic_and_returns_canon_match() -> None:
    sample_rate = 8_000
    samples = np.zeros(sample_rate * 2, dtype=np.float32)
    for second in (0.0, 0.25, 0.52, 0.75, 1.0, 1.25, 1.51, 1.75):
        index = int(second * sample_rate)
        samples[index : index + 24] = np.hanning(24)
    canon, _ = _catalogs()
    extractor = DeterministicGrooveExtractor(canon)

    first = extractor.extract(samples, sample_rate=sample_rate, bpm=120)
    second = extractor.extract(samples, sample_rate=sample_rate, bpm=120)

    assert first.model_dump() == second.model_dump()
    assert first.method == "deterministic-onset-energy/v1"
    assert first.onsets
    assert first.canon_match
    assert sum(item.probability for item in first.culture) == 1


def test_flow_follow_moves_offbeat_without_mutating_source_events() -> None:
    canon, _ = _catalogs()
    groove = DeterministicGrooveExtractor(canon).extract(
        np.ones(8_000, dtype=np.float32), sample_rate=8_000, bpm=120
    )
    events = [RhythmEvent(name="hat", beat=0.125, velocity=0.42)]

    adjusted = apply_flow_to_events(events, groove, bpm=120, grid_follow=True)

    assert events[0].beat == 0.125
    assert adjusted[0].beat >= events[0].beat


def test_responsive_plan_contains_audio_handoff_and_style_chain() -> None:
    canon, repertoire = _catalogs()
    planner = StudioMasterPlanner(canon, repertoire)

    plan = planner.responsive_plan(
        ResponsivePlanRequest(
            style="brazilian_funk_heavy",
            canon_id="br_funk_mandelao",
            repertoire_id="brazilian_funk_heavy_kit",
            bpm=140,
            swing_ratio=0.55,
        )
    )

    assert plan.status == "READY_FOR_APPROVAL"
    assert plan.canon["id"] == "br_funk_mandelao"
    assert plan.repertoire["id"] == "brazilian_funk_heavy_kit"
    assert plan.timing["grid_follow"] is True
    assert plan.handoff["target"] == "POST /v1/orchestrate"
    assert plan.handoff["approval_required"] is True


def test_performance_commands_are_validated_and_push_is_proposal_only() -> None:
    controller = PerformanceController()
    state = controller.apply("session-1", PerformanceCommand(action="SET_SWING", value="65%"))
    assert state.swing_ratio == 0.65
    assert state.swing_ms > 0

    state = controller.apply("session-1", PerformanceCommand(action="SET_GRID_FOLLOW", value=False))
    assert state.grid_follow is False

    state = controller.apply(
        "session-1",
        PerformanceCommand(action="PUSH_TO_LIBRARY", reference_id="manual-ref"),
    )
    assert state.status == "PENDING_APPROVAL"
    assert state.proposal["metadata_only"] is True
    assert "persistida" in " ".join(state.warnings)
