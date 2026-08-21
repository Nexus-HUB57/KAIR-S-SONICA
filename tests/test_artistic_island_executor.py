from __future__ import annotations

import numpy as np
import pytest
from kairos_core.artistic_island import MixPlanRequest, NumpyChainExecutor, SkillGenerator


def test_numpy_executor_applies_supported_steps_and_reports_contract_steps() -> None:
    plan = SkillGenerator().generate_chain(MixPlanRequest(instrument="lead_vocal", context="vocal"))
    audio = np.zeros((4800, 2), dtype=np.float32)
    audio[0, :] = 0.8

    output, report = NumpyChainExecutor().apply(audio, 48_000, plan)

    assert output.shape == audio.shape
    assert output.dtype == np.float32
    assert report.applied
    assert "dynamic_eq" in report.skipped
    assert report.peak_before == pytest.approx(0.8)
    assert report.peak_after <= 1.0
    assert "adapter DSP explícito" in " ".join(report.warnings)


def test_numpy_executor_is_deterministic_for_mono_audio() -> None:
    plan = SkillGenerator().generate_chain(MixPlanRequest(instrument="kick", context="beat"))
    audio = np.linspace(-0.8, 0.8, 1024, dtype=np.float32)

    first, first_report = NumpyChainExecutor().apply(audio, 44_100, plan)
    second, second_report = NumpyChainExecutor().apply(audio, 44_100, plan)

    assert np.array_equal(first, second)
    assert first_report.to_dict() == second_report.to_dict()
    assert first.shape == (1024, 1)


def test_numpy_executor_rejects_invalid_audio() -> None:
    plan = SkillGenerator().generate_chain(MixPlanRequest(instrument="kick"))

    with pytest.raises(ValueError, match="não pode ser vazio"):
        NumpyChainExecutor().apply(np.empty((0,)), 44_100, plan)

    with pytest.raises(ValueError, match="NaN"):
        NumpyChainExecutor().apply(np.array([np.nan], dtype=np.float32), 44_100, plan)

    with pytest.raises(ValueError, match="shape"):
        NumpyChainExecutor().apply(np.zeros((2, 3, 4)), 44_100, plan)
