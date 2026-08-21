from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load(path: str) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(paths: list[str]) -> None:
    if len(paths) != 5:
        raise SystemExit("usage: validate_agents_compose.py complementary-capabilities agents-capabilities space-probe llamagen-probe complementary-plan")
    complementary, agents, space, llamagen, plan = (load(path) for path in paths)

    assert complementary["name"] == "complementary-audiovisual-core"
    assert complementary["replaces_existing_core"] is False
    assert "prompt-to-scene-plan" in complementary["capabilities"]

    names = {agent["name"] for agent in agents["agents"]}
    assert {"skyreels-native", "skyreels-space", "llamagen"} <= names
    assert agents["enabled"] is True

    assert space["agent"] == "skyreels-space"
    assert "info" in space and "config" in space
    assert "generate_diffusion_forced_video" in json.dumps(space["config"])

    assert llamagen["agent"] == "llamagen"
    assert llamagen["health"]["status"] == "reachable"
    assert llamagen["health"]["reachable"] is True

    assert plan["architecture"] == "complementary-audiovisual-core.v1"
    assert plan["role"] == "planning-and-handoff"
    assert plan["handoff"]["video"] == "POST /v1/video/generate"
    assert len(plan["scenes"]) == 2
    assert all(scene["video_request_template"]["complementary_plan_id"] == plan["plan_id"] for scene in plan["scenes"])
    assert all("seed" in scene["video_request_template"] for scene in plan["scenes"])
    assert "local-compose-test-token" not in json.dumps((complementary, agents, space, llamagen, plan))


if __name__ == "__main__":
    main(sys.argv[1:])
