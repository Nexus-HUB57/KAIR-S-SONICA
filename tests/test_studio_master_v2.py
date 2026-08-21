from __future__ import annotations

import numpy as np
from kairos_core.studio_master import (
    ArrangementArchitect,
    ArrangementRequest,
    AutoRetrainGuard,
    ExpressiveNote,
    HumanExpressionEngine,
    HumanExpressionRequest,
    HumPitchFrame,
    HumToMidiRequest,
    HumToMidiSketcher,
    KairosSignaturePlanner,
    LocalArtistMemory,
    OptionalAdapterRegistry,
    PerceptualValidator,
    SignatureModeRequest,
    SpectralDucker,
    ViralClipPlanner,
    ViralClipPlanRequest,
)


def test_arrangement_architect_respects_bar_budget_and_adds_automation() -> None:
    plan = ArrangementArchitect().build(
        ArrangementRequest(style="brazilian_funk_heavy", mood="energetic", total_bars=40, bpm=142)
    )

    assert plan.status == "READY_FOR_APPROVAL"
    assert sum(section.bars for section in plan.sections) == 40
    assert plan.sections[-1].id == "outro"
    assert plan.sections[0].automation["filter_cutoff_hz"] < plan.sections[3].automation["filter_cutoff_hz"]


def test_human_expression_is_seeded_and_does_not_mutate_input() -> None:
    request = HumanExpressionRequest(
        bpm=142,
        swing_ratio=0.65,
        humanize_ms=2,
        seed=7,
        energy_map={0: 0.9},
        notes=[
            ExpressiveNote(pitch=60, time_beats=0, duration_beats=1, velocity=80),
            ExpressiveNote(pitch=64, time_beats=0.25, duration_beats=1, velocity=80),
        ],
    )

    first = HumanExpressionEngine().apply(request)
    second = HumanExpressionEngine().apply(request)

    assert first.model_dump() == second.model_dump()
    assert request.notes[1].time_beats == 0.25
    assert first.notes[1].time_beats > request.notes[1].time_beats
    assert first.max_timing_shift_ms <= 10


def test_hum_to_midi_sketch_groups_contour_and_keeps_export_optional() -> None:
    result = HumToMidiSketcher().convert(
        HumToMidiRequest(
            frames=[
                HumPitchFrame(time_seconds=0.0, frequency_hz=440, confidence=0.9),
                HumPitchFrame(time_seconds=0.1, frequency_hz=440, confidence=0.95),
                HumPitchFrame(time_seconds=0.2, frequency_hz=440, confidence=0.9),
                HumPitchFrame(time_seconds=0.3, frequency_hz=493.883, confidence=0.9),
                HumPitchFrame(time_seconds=0.4, frequency_hz=493.883, confidence=0.9),
            ]
        )
    )

    assert [note.midi_note for note in result.notes] == [69, 71]
    assert result.notes[0].end_seconds == 0.2
    assert result.midi_export == "not-generated"


def test_signature_plan_is_parametric_and_has_source_imitation_guardrail() -> None:
    plan = KairosSignaturePlanner().plan(SignatureModeRequest(intensity=0.8, target="mix_bus"))

    assert plan.status == "READY_FOR_APPROVAL"
    assert plan.guardrails["source_imitation"] is False
    assert plan.guardrails["automatic_file_write"] is False
    assert plan.chain[-1]["parameters"]["ceiling_db"] == -1.0


def test_ducking_preview_and_signal_validator_are_deterministic() -> None:
    mix = np.ones(64, dtype=np.float32)
    reference = np.zeros(64, dtype=np.float32)
    reference[20:32] = 1.0
    preview = SpectralDucker().preview(mix, reference, strength=0.8, window_size=8)
    report = PerceptualValidator().predict(preview.audio)

    assert preview.method == "numpy-rms-envelope/v1"
    assert preview.audio.shape == mix.shape
    assert float(preview.audio[25]) < float(preview.audio[0])
    assert 0 <= report.score <= 5
    assert report.method == "technical-signal-health/v1"


def test_artist_memory_is_opt_in_and_metadata_only(tmp_path) -> None:
    disabled = LocalArtistMemory(tmp_path / "disabled.jsonl", enabled=False)
    assert disabled.store_feedback("funk, 140 bpm", {"swing": 0.62})["stored"] is False

    memory = LocalArtistMemory(tmp_path / "memory.jsonl", enabled=True)
    stored = memory.store_feedback("funk, 140 bpm, hook", {"swing": 0.64}, project_id="p-1")
    assert stored["metadata_only"] is True
    assert memory.recall_similar("funk 140 bpm") == {"swing": 0.64}


def test_viral_clip_plan_is_bounded_and_not_published() -> None:
    plan = ViralClipPlanner().plan(ViralClipPlanRequest(audio_asset_id=None))

    assert plan["status"] == "READY_FOR_APPROVAL"
    assert plan["canvas"] == {"width": 1080, "height": 1920, "fps": 24}
    assert plan["render"]["automatic_publish"] is False
    assert plan["audio"]["required"] is True


def test_auto_retrain_guard_requires_manifest_and_approval(tmp_path) -> None:
    disabled = AutoRetrainGuard(tmp_path / "missing.json", enabled=False).status()
    assert disabled.status == "DISABLED"
    assert disabled.ready is False

    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        '{"approved_samples": 24, "operator_approval": "approved", '
        '"license_provenance": "manifest-1", "validation_split": "split-1"}',
        encoding="utf-8",
    )
    ready = AutoRetrainGuard(manifest, enabled=True).status()
    assert ready.status == "READY_FOR_APPROVAL"
    assert ready.ready is True


def test_adapter_registry_does_not_enable_optional_backends() -> None:
    adapters = OptionalAdapterRegistry().capabilities()

    assert adapters
    assert all(item["enabled"] is False for item in adapters)
    assert all(item["reason"] for item in adapters)
