from __future__ import annotations

import json

import pytest
from kairos_core.complementary import build_complementary_plan, complementary_capabilities


def test_complementary_plan_is_deterministic_and_non_replacing() -> None:
    first = build_complementary_plan(
        prompt="chuva neon em videoclipe vertical",
        duration_seconds=10,
        scene_seconds=5,
        seed=42,
    ).to_dict()
    second = build_complementary_plan(
        prompt="  chuva   neon em videoclipe vertical ",
        duration_seconds=10,
        scene_seconds=5,
        seed=42,
    ).to_dict()

    assert first == second
    assert first["architecture"] == "complementary-audiovisual-core.v1"
    assert first["role"] == "planning-and-handoff"
    assert first["guardrails"]
    assert first["handoff"]["video"] == "POST /v1/video/generate"
    assert len(first["scenes"]) == 2
    assert all(scene["agent_handoff"] == ["skyreels-native", "skyreels-space"] for scene in first["scenes"])
    assert all(scene["video_request_template"]["complementary_plan_id"] == first["plan_id"] for scene in first["scenes"])
    assert "PEXELS_API_KEY" in json.dumps(first)


def test_complementary_capabilities_do_not_enable_external_agents() -> None:
    payload = complementary_capabilities()

    assert payload["replaces_existing_core"] is False
    assert payload["optional_adapters"]["pexels"]["enabled_by_default"] is False
    assert payload["optional_adapters"]["tts"]["enabled_by_default"] is False
    assert payload["optional_adapters"]["musicgen"]["enabled_by_default"] is False


def test_complementary_plan_rejects_empty_prompt() -> None:
    with pytest.raises(ValueError, match="prompt"):
        build_complementary_plan(prompt=" ")
