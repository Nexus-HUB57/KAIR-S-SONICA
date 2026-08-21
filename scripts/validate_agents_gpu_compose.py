from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        raise SystemExit(
            "usage: validate_agents_gpu_compose.py VIDEO AGENTS AGENTIC REQUIRE_NATIVE RUN_EXTERNAL_PROBES OUTPUT_DIR"
        )
    video = load(argv[1])
    agents = load(argv[2])
    agentic = load(argv[3])
    require_native = argv[4] == "true"
    run_external = argv[5] == "true"
    output_dir = Path(argv[6])

    native = video.get("backends", {}).get("native", {})
    if require_native and native.get("ready") is not True:
        raise SystemExit(f"native backend is not ready: {json.dumps(native, ensure_ascii=False)}")
    if agentic.get("enabled") is not True:
        raise SystemExit("agentic catalog is disabled on the GPU Compose API")
    catalog = {item.get("name"): item for item in agents.get("agents", [])}
    if catalog.get("skyreels-native", {}).get("enabled") is not True:
        raise SystemExit("skyreels-native is not enabled in the agent catalog")
    if run_external:
        probe = output_dir / "skyreels-space-probe.json"
        if not probe.is_file():
            raise SystemExit("external probes requested but SkyReels Space probe artifact is missing")
        payload = load(str(probe))
        if payload.get("agent") != "skyreels-space":
            raise SystemExit("SkyReels Space probe returned an unexpected agent")
        llamagen = output_dir / "llamagen-probe.json"
        if llamagen.is_file() and load(str(llamagen)).get("agent") != "llamagen":
            raise SystemExit("LlamaGen probe returned an unexpected agent")
    print(
        json.dumps(
            {
                "native_ready": native.get("ready", False),
                "native_runtime": native.get("runtime", False),
                "native_checkpoint": native.get("checkpoint", False),
                "agentic_enabled": agentic.get("enabled", False),
                "external_probes_executed": run_external,
                "catalog_agents": sorted(catalog),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
