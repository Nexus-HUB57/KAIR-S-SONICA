from __future__ import annotations

from kairos_core.artistic_island import (
    ALGORITHM_REGISTRY,
    InstrumentAtlas,
    MixPlanRequest,
    SkillGenerator,
)


def test_atlas_loads_starter_profiles_and_algorithms() -> None:
    atlas = InstrumentAtlas.load()

    assert atlas.source_status == "yaml"
    assert len(atlas.profiles) >= 15
    assert {"kick", "lead_vocal", "backing_vocal", "synth_pad"}.issubset(atlas.profiles)
    assert len(ALGORITHM_REGISTRY) == 12


def test_skill_generator_builds_vocal_chain_with_optional_steps() -> None:
    plan = SkillGenerator().generate_chain(
        MixPlanRequest(
            instrument="backing_vocal",
            context="vocal",
            prompt="backing vocal noturno com largura controlada",
            reference_id="ref-001",
        )
    )

    names = [step.algorithm for step in plan.chain]
    assert plan.profile_found is True
    assert 5 <= len(names) <= 12
    assert names[:2] == ["pitch_corrector", "deesser"]
    assert "formant_shifter" in names
    assert "stereo_widener" in names
    assert plan.master_bus["integrated_lufs_target"] == -14
    assert plan.provenance["external_plugin_execution"] is False


def test_skill_generator_is_deterministic_and_limits_chain() -> None:
    request = MixPlanRequest(instrument="strings", context="orchestra", max_steps=5, seed=None)
    first = SkillGenerator().generate_chain(request).model_dump(mode="json")
    second = SkillGenerator().generate_chain(request).model_dump(mode="json")

    assert first == second
    assert len(first["chain"]) == 5
    assert first["chain"][0]["order"] == 1


def test_unknown_instrument_is_rejected() -> None:
    try:
        SkillGenerator().generate_chain(MixPlanRequest(instrument="unknown-instrument"))
    except ValueError as error:
        assert "Instrumento não encontrado" in str(error)
    else:
        raise AssertionError("unknown instrument should be rejected")
