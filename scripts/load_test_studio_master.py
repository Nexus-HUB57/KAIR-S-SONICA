from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx


@dataclass(slots=True)
class ProbeResult:
    kind: str
    route: str
    status_code: int | None
    latency_ms: float
    ok: bool
    error: str | None = None


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((len(ordered) - 1) * fraction))
    return round(ordered[index], 3)


def payloads() -> tuple[tuple[str, str, dict[str, Any]], ...]:
    return (
        ("GET", "/v1/studio-master/capabilities", {}),
        ("GET", "/v1/studio-master/canon", {}),
        ("GET", "/v1/studio-master/repertoire", {}),
        ("GET", "/v1/studio-master/real-adapters/capabilities", {}),
        ("GET", "/v1/studio-master/analytics", {}),
        ("GET", "/v1/studio-master/retraining", {}),
        (
            "POST",
            "/v1/studio-master/arrangement",
            {"style": "boom_bap", "mood": "focused", "bpm": 92, "total_bars": 32, "key": "C#"},
        ),
        (
            "POST",
            "/v1/studio-master/signature-plan",
            {"intensity": 0.65, "vocal_presence": 0.8, "low_end_focus": 0.7, "spatial_depth": 0.35, "target": "mix_bus"},
        ),
        (
            "POST",
            "/v1/studio-master/viral-clip-plan",
            {"title": "Káiros stress probe", "duration_seconds": 15, "aspect_ratio": "9:16", "platform": "generic", "audio_asset_id": None},
        ),
        (
            "POST",
            "/v1/studio-master/responsive-plan",
            {"style": "boom_bap", "canon_id": None, "repertoire_id": None, "bpm": 92, "swing_ratio": 0.58, "grid_follow": True, "flow": None},
        ),
        (
            "POST",
            "/v1/studio-master/ducking/preview",
            {"mix_bus": [0.0, 0.1, -0.1, 0.0] * 16, "reference_track": [0.0, 0.2, -0.2, 0.0] * 16, "strength": 0.35, "window_size": 16},
        ),
        (
            "POST",
            "/v1/studio-master/perceptual/score",
            {"samples": [0.0, 0.1, -0.1, 0.0] * 16, "target_score": 4.0},
        ),
    )


async def one_http_probe(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    method: str,
    route: str,
    body: dict[str, Any],
) -> ProbeResult:
    async with semaphore:
        started = time.perf_counter()
        try:
            response = await client.request(method, route, json=body or None)
            latency = (time.perf_counter() - started) * 1000
            return ProbeResult("http", route, response.status_code, round(latency, 3), response.is_success, response.text[:300] if not response.is_success else None)
        except (httpx.HTTPError, asyncio.TimeoutError) as exc:
            latency = (time.perf_counter() - started) * 1000
            return ProbeResult("http", route, None, round(latency, 3), False, str(exc))


async def one_websocket_probe(base_url: str, timeout: float) -> ProbeResult:
    route = "/ws/studio-master/{session_id}/performance"
    session_id = f"stress-{uuid4()}"
    ws_url = base_url.rstrip("/").replace("https://", "wss://").replace("http://", "ws://")
    ws_url = f"{ws_url}/ws/studio-master/{session_id}/performance"
    started = time.perf_counter()
    try:
        import websockets

        async with asyncio.timeout(timeout):
            async with websockets.connect(ws_url, max_size=1_000_000) as socket:
                initial = json.loads(await socket.recv())
                if initial.get("event") != "performance_state":
                    raise RuntimeError("handshake sem performance_state")
                await socket.send(json.dumps({"action": "SET_BPM", "bpm": 96}))
                update = json.loads(await socket.recv())
                if update.get("event") != "performance_state":
                    raise RuntimeError("update sem performance_state")
        latency = (time.perf_counter() - started) * 1000
        return ProbeResult("websocket", route, 101, round(latency, 3), True)
    except (ImportError, OSError, RuntimeError, TimeoutError, TypeError, ValueError) as exc:
        latency = (time.perf_counter() - started) * 1000
        return ProbeResult("websocket", route, None, round(latency, 3), False, str(exc))


async def run_stress(args: argparse.Namespace) -> dict[str, Any]:
    started = time.perf_counter()
    requests = [payload for _ in range(args.rounds) for payload in payloads()]
    limits = httpx.Limits(max_connections=args.concurrency, max_keepalive_connections=args.concurrency)
    semaphore = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient(base_url=args.base_url.rstrip("/"), timeout=args.request_timeout, limits=limits) as client:
        http_results = await asyncio.gather(
            *(one_http_probe(client, semaphore, method, route, body) for method, route, body in requests)
        )
    websocket_results = await asyncio.gather(
        *(one_websocket_probe(args.base_url, args.websocket_timeout) for _ in range(args.websocket_clients))
    )
    results = [*http_results, *websocket_results]
    elapsed = time.perf_counter() - started
    grouped: dict[str, list[ProbeResult]] = {}
    for item in results:
        grouped.setdefault(item.route, []).append(item)
    route_summary = {}
    for route, items in grouped.items():
        latencies = [item.latency_ms for item in items]
        route_summary[route] = {
            "requests": len(items),
            "successes": sum(item.ok for item in items),
            "failures": sum(not item.ok for item in items),
            "p50_ms": percentile(latencies, 0.50),
            "p95_ms": percentile(latencies, 0.95),
            "p99_ms": percentile(latencies, 0.99),
            "max_ms": round(max(latencies), 3) if latencies else None,
        }
    successful = sum(item.ok for item in results)
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "configuration": {
            "base_url": args.base_url,
            "rounds": args.rounds,
            "concurrency": args.concurrency,
            "websocket_clients": args.websocket_clients,
            "request_timeout": args.request_timeout,
            "websocket_timeout": args.websocket_timeout,
        },
        "summary": {
            "elapsed_seconds": round(elapsed, 3),
            "probes": len(results),
            "successes": successful,
            "failures": len(results) - successful,
            "success_rate": round(successful / len(results), 4) if results else 0,
            "throughput_probes_per_second": round(len(results) / elapsed, 3) if elapsed else 0,
            "latency_ms": {
                "mean": round(statistics.fmean(item.latency_ms for item in results), 3) if results else None,
                "p50": percentile([item.latency_ms for item in results], 0.50),
                "p95": percentile([item.latency_ms for item in results], 0.95),
                "p99": percentile([item.latency_ms for item in results], 0.99),
            },
        },
        "routes": route_summary,
        "results": [asdict(item) for item in results],
    }
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stress test HTTP/WebSocket do Command Deck StudioMaster 2.0")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--websocket-clients", type=int, default=5)
    parser.add_argument("--request-timeout", type=float, default=10.0)
    parser.add_argument("--websocket-timeout", type=float, default=10.0)
    parser.add_argument("--output", type=Path, default=Path("/tmp/studio-master-command-deck-stress.json"))
    args = parser.parse_args()
    if args.rounds < 1 or args.concurrency < 1 or args.websocket_clients < 1:
        parser.error("rounds, concurrency e websocket-clients devem ser positivos")
    return args


def main() -> int:
    args = parse_args()
    report = asyncio.run(run_stress(args))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"report={args.output}")
    return 0 if report["summary"]["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
