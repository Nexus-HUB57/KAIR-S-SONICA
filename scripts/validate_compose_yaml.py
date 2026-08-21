from __future__ import annotations

from pathlib import Path

import yaml

for name in ("docker-compose.yml", "docker-compose.gpu.yml", "docker-compose.agents.local.yml"):
    payload = yaml.safe_load(Path(name).read_text(encoding="utf-8"))
    assert isinstance(payload, dict) and "services" in payload
    print(f"{name}: YAML OK ({len(payload['services'])} services)")
