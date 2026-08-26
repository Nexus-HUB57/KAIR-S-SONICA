#!/usr/bin/env python3
"""Simula o Preflight PHD do Single 1 sem renderizar ou enviar mídia.

Por padrão, a simulação é offline e usa o mesmo AutoReviewEngine. Com
``--base-url`` informado explicitamente, também chama o endpoint local em duas
passagens, auto_repair=false e auto_repair=true. Nenhuma rota de geração é
chamada por este script.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "packages"
if str(PACKAGES) not in sys.path:
    sys.path.insert(0, str(PACKAGES))

from kairos_core.config import Settings
from kairos_core.studio_master.cpu_preflight import (
    SINGLE1_APPROVED_VIDEO,
    build_single1_payload,
    load_single1_declaration,
    probe_media,
    simulate_single1_cpu,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--video", type=Path, default=None)
    parser.add_argument("--base-url", default=None, help="URL local explícita, por exemplo http://127.0.0.1:8000")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/home/ubuntu/kairus-workspace/single1-cpu-preflight-report.json"),
    )
    parser.add_argument("--summary-output", type=Path, default=None)
    return parser.parse_args()


def post_preflight(base_url: str, payload: dict[str, object], auto_repair: bool) -> dict[str, object]:
    body = json.dumps(
        {"media_kind": "multimedia", "payload": payload, "auto_repair": auto_repair},
        ensure_ascii=False,
    ).encode("utf-8")
    request = Request(
        f"{base_url.rstrip('/')}/v1/studio-master/preflight",
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            response_body = response.read()
            status = response.status
    except HTTPError as exc:
        response_body = exc.read()
        status = exc.code
    except (OSError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Falha ao chamar preflight local: {exc}") from exc
    try:
        parsed = json.loads(response_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Preflight local retornou JSON inválido") from exc
    if status >= 400:
        raise RuntimeError(f"Preflight local retornou HTTP {status}: {parsed}")
    if not isinstance(parsed, dict):
        raise TypeError("Preflight local retornou um payload inesperado")
    return parsed


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.expanduser().resolve()
    video_path = (args.video or (repo_root / SINGLE1_APPROVED_VIDEO)).expanduser().resolve()
    settings = Settings.from_env()
    declaration = load_single1_declaration(repo_root)
    asset = probe_media(video_path, settings.ffprobe_bin)
    payload = build_single1_payload(repo_root, video_path, asset, declaration)
    offline = simulate_single1_cpu(settings, repo_root, video_path)
    report = offline.to_dict()
    report["transport"] = "offline-engine"
    if args.base_url:
        report["transport"] = "local-http-and-offline-cross-check"
        report["preflight_http_auto_repair_false"] = post_preflight(
            args.base_url, payload, auto_repair=False
        )
        report["preflight_http_auto_repair_true"] = post_preflight(
            args.base_url, payload, auto_repair=True
        )
        report["http_contract"] = {
            "endpoint": f"{args.base_url.rstrip('/')}/v1/studio-master/preflight",
            "generation_endpoint_called": False,
        }
    report["cli"] = {
        "repo_root": str(repo_root),
        "video_path": str(video_path),
        "base_url": args.base_url,
        "render_started": False,
        "cloud_call_started": False,
    }

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.summary_output:
        summary = {
            "overall_decision": report["overall_decision"],
            "technical_gate_passed": report["technical_gate_passed"],
            "technical_findings": report["technical_findings"],
            "offline_preflight_decision": report["preflight_auto_repair_false"]["decision"],
            "local_gpu": report["backend"]["local_gpu"],
            "render_started": report["cli"]["render_started"],
            "cloud_call_started": report["cli"]["cloud_call_started"],
        }
        summary_path = args.summary_output.expanduser().resolve()
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "overall_decision": report["overall_decision"],
        "technical_gate_passed": report["technical_gate_passed"],
        "preflight_decision": report["preflight_auto_repair_false"]["decision"],
        "local_gpu": report["backend"]["local_gpu"],
        "transport": report["transport"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
