from __future__ import annotations

import sys
from pathlib import Path

from kairos_core.config import Settings
from kairos_core.studio_master.adapters_real import RealAdapterRegistry
from kairos_core.studio_master.adapters_real.crepe_adapter import CrepeAdapter
from kairos_core.studio_master.adapters_real.demucs_adapter import DemucsAdapter
from kairos_core.studio_master.adapters_real.fluidsynth_adapter import FluidSynthAdapter
from kairos_core.studio_master.adapters_real.mosnet_adapter import MosnetAdapter
from kairos_core.studio_master.adapters_real.moviepy_adapter import MoviePyAdapter
from kairos_core.studio_master.adapters_real.pedalboard_adapter import PedalboardAdapter

ROOT = Path(__file__).resolve().parents[1]


def test_real_registry_is_safe_by_default() -> None:
    settings = Settings(
        studio_master_adapter_licenses_path=ROOT / "config/studio_master_adapter_licenses.yaml"
    )
    registry = RealAdapterRegistry(settings)
    capabilities = registry.capabilities()

    assert {item["adapter_id"] for item in capabilities} == {
        "crepe",
        "pedalboard",
        "fluidsynth",
        "demucs",
        "mosnet",
        "moviepy",
    }
    assert all(item["enabled"] is False for item in capabilities)
    assert all(item["operational_status"] == "FALLBACK_ONLY" for item in capabilities)
    assert all(item["license_status"] == "pending" for item in capabilities)
    assert all(item["license"]["source_url"] for item in capabilities)


def test_real_adapters_fallback_without_gate_or_heavy_imports() -> None:
    settings = Settings(
        studio_master_adapter_licenses_path=ROOT / "config/studio_master_adapter_licenses.yaml"
    )
    samples = [0.0, 0.1, -0.1, 0.0]
    results = [
        CrepeAdapter(settings).run(samples, 44_100),
        PedalboardAdapter(settings).run(samples, 44_100),
        FluidSynthAdapter(settings).run(
            [{"pitch": 60, "velocity": 90, "duration_seconds": 0.1}],
            44_100,
            soundfont_path="missing.sf2",
        ),
        DemucsAdapter(settings).run("missing.wav"),
        MosnetAdapter(settings).run(samples, 44_100, model_path="missing.h5"),
        MoviePyAdapter(settings).run("missing.wav", "clip.mp4"),
    ]

    assert all(result.status == "FALLBACK" for result in results)
    assert all(result.fallback_used for result in results)
    assert "tensorflow" not in sys.modules
    assert "crepe" not in sys.modules
    assert "pedalboard" not in sys.modules
    assert "demucs" not in sys.modules
    assert "moviepy" not in sys.modules


def test_registry_preflight_exposes_license_and_fallback() -> None:
    settings = Settings(
        studio_master_adapter_licenses_path=ROOT / "config/studio_master_adapter_licenses.yaml"
    )
    preflight = RealAdapterRegistry(settings).preflight("moviepy")

    assert preflight["status"] == "FALLBACK_ONLY"
    assert preflight["capability"]["license"]["code_license"] == "MIT"
    assert preflight["run_requires"]["fallback"] == "browser_canvas_clip_plan"
