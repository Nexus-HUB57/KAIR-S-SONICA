from __future__ import annotations

import json
from pathlib import Path

import pytest
from kairos_core.agents.clients import ExternalAgentError, LlamaGenClient, SkyReelsSpaceClient
from kairos_core.agents.registry import AgentAggregator
from kairos_core.config import Settings


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        output_dir=tmp_path / "output",
        upload_dir=tmp_path / "uploads",
        agent_aggregator_enabled=True,
        skyreels_space_enabled=True,
        llamagen_enabled=True,
    )


def test_space_generate_maps_agents_md_inputs_and_polls(tmp_path: Path, monkeypatch) -> None:
    client = SkyReelsSpaceClient(_settings(tmp_path))
    captured: dict[str, object] = {}

    def submit(inputs: list[object]) -> dict[str, str]:
        captured["inputs"] = inputs
        return {"event_id": "evt-1"}

    monkeypatch.setattr(client, "_submit", submit)
    monkeypatch.setattr(
        client,
        "_request",
        lambda method, path, **kwargs: (
            200,
            b'data: {"msg":"process_completed","success":true,"output":{"data":[{"path":"/tmp/out.mp4"}]}}\n',
            {"Content-Type": "text/event-stream"},
        ),
    )

    result = client.generate(prompt="Rain-soaked rap shot", seed=42)

    inputs = captured["inputs"]
    assert isinstance(inputs, list)
    assert inputs[0] == "Rain-soaked rap shot"
    assert inputs[3] == "Skywork/SkyReels-V2-DF-1.3B-540P"
    assert inputs[5] == 97
    assert inputs[18] == 42
    assert result["status"] == "completed"
    assert result["data"][0]["path"] == "/tmp/out.mp4"


def test_llamagen_requires_environment_secret(tmp_path: Path, monkeypatch) -> None:
    client = LlamaGenClient(_settings(tmp_path))
    monkeypatch.delenv("LLAMAGEN_API_KEY", raising=False)

    with pytest.raises(ExternalAgentError, match="LLAMAGEN_API_KEY"):
        client.create_generation({"prompt": "A storyboard"})


def test_llamagen_health_classifies_unauthorized_without_exposing_token(tmp_path: Path, monkeypatch) -> None:
    client = LlamaGenClient(_settings(tmp_path))
    monkeypatch.setenv("LLAMAGEN_API_KEY", "sk-test-only")

    def unauthorized(*args, **kwargs):
        raise ExternalAgentError("GET /v1/comics/generations/nonexistent retornou HTTP 403: invalid token")

    monkeypatch.setattr(client, "_request", unauthorized)
    result = client.health()

    assert result["status"] == "unauthorized"
    assert result["reachable"] is True
    assert "sk-test-only" not in json.dumps(result)


def test_agent_catalog_is_disabled_by_default(tmp_path: Path) -> None:
    settings = _settings(tmp_path)
    settings.agent_aggregator_enabled = False
    payload = AgentAggregator(settings).catalog()

    assert payload["enabled"] is False
    assert {agent["name"] for agent in payload["agents"]} == {
        "skyreels-native",
        "skyreels-space",
        "llamagen",
    }
    assert all(agent["enabled"] is False for agent in payload["agents"] if agent["name"] != "skyreels-native")
