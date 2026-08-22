from __future__ import annotations

import re
from pathlib import Path

import yaml


WORKFLOWS = (
    Path(".github/workflows/social-dry-run.yml"),
    Path(".github/workflows/social-publish.yml"),
    Path(".github/workflows/social-token-health.yml"),
)


def main() -> int:
    for path in WORKFLOWS:
        content = path.read_text(encoding="utf-8")
        document = yaml.safe_load(content)
        if not isinstance(document, dict):
            raise SystemExit(f"{path}: YAML root is not a mapping")
        if "on" not in document:
            raise SystemExit(f"{path}: missing on trigger")
        if "jobs" not in document:
            raise SystemExit(f"{path}: missing jobs")
        if re.search(r"(?:Bearer\s+[A-Za-z0-9_./+=-]{24,}|(?:ACCESS_TOKEN|CLIENT_SECRET|APP_SECRET|REFRESH_TOKEN)=\S+)", content):
            raise SystemExit(f"{path}: possible secret literal")
    publish = yaml.safe_load(Path(".github/workflows/social-publish.yml").read_text(encoding="utf-8"))
    job = publish["jobs"]["publish"]
    if job.get("environment") != "production-social":
        raise SystemExit("social-publish.yml: production environment missing")
    if "workflow_dispatch" not in publish["on"]:
        raise SystemExit("social-publish.yml: publish workflow must be manual")
    if any(event in publish["on"] for event in ("push", "pull_request")):
        raise SystemExit("social-publish.yml: automatic push/PR trigger is not allowed")
    print("social workflows valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
