from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from kairos_core.config import Settings
from kairos_core.social import AutonomyMode, PeerMode, SocialPlatform, SocialRunRequest, SocialOrchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Executa o KTD Social Orchestrator dentro de um GitHub Actions runner.")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--asset-url", required=True)
    parser.add_argument("--content-state", default="candidate", choices=["draft", "candidate", "approved", "released"])
    parser.add_argument("--autonomy-mode", default="autonomous", choices=[mode.value for mode in AutonomyMode])
    parser.add_argument("--peer-mode", default="optional", choices=[mode.value for mode in PeerMode])
    parser.add_argument("--execute-actions", action="store_true")
    parser.add_argument("--include-llm", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.execute_actions:
        if args.content_state not in {"approved", "released"}:
            print("execution blocked: content-state must be approved or released", file=sys.stderr)
            return 2
        if os.getenv("GITHUB_REF") not in {"", "refs/heads/main"}:
            print("execution blocked: real publishing is allowed only from main", file=sys.stderr)
            return 2
        if os.getenv("GITHUB_EVENT_NAME") not in {"", "workflow_dispatch"}:
            print("execution blocked: real publishing requires workflow_dispatch", file=sys.stderr)
            return 2

    settings = Settings.from_env()
    repo_root = Path(__file__).resolve().parents[1]
    orchestrator = SocialOrchestrator(settings, repo_root=repo_root)
    request = SocialRunRequest(
        objective=args.objective,
        campaign_id=args.campaign_id,
        autonomy_mode=AutonomyMode(args.autonomy_mode),
        peer_mode=PeerMode(args.peer_mode),
        content_state=args.content_state,
        include_llm=args.include_llm,
        execute_actions=args.execute_actions,
        asset_refs=[args.asset_url],
        metadata={
            "song_title": "I Won’t Waste This Life",
            "source": "github-actions",
        },
    )
    result = orchestrator.run(request)
    summary = {
        "run_id": result.run_id,
        "campaign_id": result.campaign_id,
        "status": result.status,
        "autonomy_mode": result.autonomy_mode.value,
        "actions": [
            {
                "platform": action.platform.value,
                "status": action.status.value,
                "provider_id": action.provider_id,
                "error_code": action.error_code,
            }
            for action in result.actions
        ],
        "peer_reconciliation": result.strategy.get("peer_reconciliation"),
        "warnings": result.warnings,
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    if os.getenv("GITHUB_STEP_SUMMARY"):
        Path(os.environ["GITHUB_STEP_SUMMARY"]).write_text(
            "# KTD Social Orchestrator\n\n```json\n"
            + json.dumps(summary, ensure_ascii=False, indent=2)
            + "\n```\n",
            encoding="utf-8",
        )
    if args.execute_actions and result.status not in {"PUBLISHED", "PARTIAL"}:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
