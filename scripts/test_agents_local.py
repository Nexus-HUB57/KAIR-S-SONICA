from __future__ import annotations

import json
import os
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "packages"))

from kairos_core.agents import AgentAggregator, LlamaGenClient, SkyReelsSpaceClient
from kairos_core.config import Settings

from tools.mock_external_agent import StreamHandler


def start_mock(kind: str, port: int) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), StreamHandler)
    server.mock_kind = kind  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main() -> None:
    space_server = start_mock("space", 17860)
    llamagen_server = start_mock("llamagen", 18090)
    os.environ["LLAMAGEN_API_KEY"] = "local-test-token"
    settings = Settings(
        agent_aggregator_enabled=True,
        skyreels_space_enabled=True,
        skyreels_space_base_url="http://127.0.0.1:17860",
        skyreels_space_timeout_seconds=5,
        llamagen_enabled=True,
        llamagen_base_url="http://127.0.0.1:18090",
    )
    try:
        aggregator = AgentAggregator(settings)
        space_probe = aggregator.probe("skyreels-space")
        llamagen_probe = aggregator.probe("llamagen")
        generated = SkyReelsSpaceClient(settings).generate(
            prompt="local smoke test",
            poll_seconds=0.01,
        )
        direct_health = LlamaGenClient(settings).health()
        result = {
            "space_probe": space_probe,
            "llamagen_probe": llamagen_probe,
            "space_generate_status": generated["status"],
            "llamagen_health": direct_health["status"],
        }
        assert result["space_generate_status"] == "completed"
        assert result["llamagen_health"] == "reachable"
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        space_server.shutdown()
        llamagen_server.shutdown()


if __name__ == "__main__":
    main()
