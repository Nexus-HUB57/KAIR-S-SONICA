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

import httpx


@dataclass(slots=True)
class RequestResult:
    index: int
    submit_status: int | None
    task_id: str | None
    submit_latency_ms: float
    total_latency_ms: float | None
    final_status: str
    error: str | None


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = min(len(ordered) - 1, round((len(ordered) - 1) * fraction))
    return round(ordered[position], 3)


async def run_one(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    index: int,
    args: argparse.Namespace,
) -> RequestResult:
    async with semaphore:
        payload: dict[str, Any] = {
            "prompt": args.prompt,
            "transcribe": False,
            "analyze_audio": bool(args.audio_path),
            "generate_audio": True,
            "genre": args.genre,
            "bpm": args.bpm,
            "key": args.key,
            "scale": args.scale,
            "duration_seconds": args.duration,
            "sample_rate": args.sample_rate,
            "output_format": args.output_format,
            "seed": index,
        }
        if args.audio_path:
            payload["audio_path"] = args.audio_path
        started = time.perf_counter()
        try:
            response = await client.post("/v1/orchestrate", json=payload)
            submit_latency_ms = (time.perf_counter() - started) * 1_000
            if response.status_code != 202:
                return RequestResult(index, response.status_code, None, round(submit_latency_ms, 3), None, "SUBMIT_FAILED", response.text[:500])
            task_id = response.json()["task_id"]
            deadline = time.perf_counter() + args.timeout
            final_status = "TIMEOUT"
            error = None
            while time.perf_counter() < deadline:
                snapshot_response = await client.get(f"/v1/tasks/{task_id}")
                if snapshot_response.status_code != 200:
                    final_status = "POLL_FAILED"
                    error = snapshot_response.text[:500]
                    break
                snapshot = snapshot_response.json()
                final_status = snapshot.get("status", "UNKNOWN")
                if final_status in {"SUCCEEDED", "FAILED"}:
                    error = snapshot.get("error")
                    break
                await asyncio.sleep(args.poll_interval)
            total_latency_ms = (time.perf_counter() - started) * 1_000 if final_status != "TIMEOUT" else None
            return RequestResult(index, response.status_code, task_id, round(submit_latency_ms, 3), round(total_latency_ms, 3) if total_latency_ms else None, final_status, error)
        except (httpx.HTTPError, asyncio.TimeoutError) as exc:
            submit_latency_ms = (time.perf_counter() - started) * 1_000
            return RequestResult(index, None, None, round(submit_latency_ms, 3), None, "CLIENT_ERROR", str(exc))


async def run_load(args: argparse.Namespace) -> dict[str, Any]:
    started = time.perf_counter()
    limits = httpx.Limits(max_connections=args.concurrency, max_keepalive_connections=args.concurrency)
    timeout = httpx.Timeout(args.request_timeout)
    semaphore = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient(base_url=args.base_url.rstrip("/"), limits=limits, timeout=timeout) as client:
        results = await asyncio.gather(*(run_one(client, semaphore, index, args) for index in range(args.requests)))
    elapsed_seconds = time.perf_counter() - started
    submit_latencies = [item.submit_latency_ms for item in results]
    total_latencies = [item.total_latency_ms for item in results if item.total_latency_ms is not None]
    succeeded = sum(item.final_status == "SUCCEEDED" for item in results)
    failed = len(results) - succeeded
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "configuration": {
            "base_url": args.base_url,
            "requests": args.requests,
            "concurrency": args.concurrency,
            "duration_seconds": args.duration,
            "sample_rate": args.sample_rate,
            "output_format": args.output_format,
            "audio_path": args.audio_path,
        },
        "summary": {
            "elapsed_seconds": round(elapsed_seconds, 3),
            "throughput_tasks_per_second": round(succeeded / elapsed_seconds, 3) if elapsed_seconds else 0,
            "submitted": len(results),
            "succeeded": succeeded,
            "failed_or_timeout": failed,
            "success_rate": round(succeeded / len(results), 4) if results else 0,
            "submit_latency_ms": {
                "mean": round(statistics.fmean(submit_latencies), 3) if submit_latencies else None,
                "p50": percentile(submit_latencies, 0.50),
                "p95": percentile(submit_latencies, 0.95),
                "p99": percentile(submit_latencies, 0.99),
            },
            "end_to_end_latency_ms": {
                "mean": round(statistics.fmean(total_latencies), 3) if total_latencies else None,
                "p50": percentile(total_latencies, 0.50),
                "p95": percentile(total_latencies, 0.95),
                "p99": percentile(total_latencies, 0.99),
            },
        },
        "results": [asdict(item) for item in results],
    }
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Teste de carga concorrente do endpoint /v1/orchestrate")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--requests", type=int, default=20)
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--duration", type=float, default=1.0)
    parser.add_argument("--sample-rate", type=int, default=8_000)
    parser.add_argument("--output-format", choices=("wav", "mp3"), default="wav")
    parser.add_argument("--audio-path", default=None, help="referência relativa em data/uploads ou data/output")
    parser.add_argument("--prompt", default="Teste de carga Káiros, Trap Soul instrumental")
    parser.add_argument("--genre", default="Trap Soul")
    parser.add_argument("--bpm", type=int, default=140)
    parser.add_argument("--key", default="C#")
    parser.add_argument("--scale", default="minor")
    parser.add_argument("--timeout", type=float, default=60.0, help="timeout de cada tarefa")
    parser.add_argument("--request-timeout", type=float, default=10.0, help="timeout de cada chamada HTTP")
    parser.add_argument("--poll-interval", type=float, default=0.05)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    if args.requests < 1 or args.concurrency < 1 or args.concurrency > args.requests:
        parser.error("--requests deve ser >= 1 e --concurrency deve ficar entre 1 e --requests")
    if args.output is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        args.output = Path("reports/load") / f"orchestrate-{stamp}.json"
    return args


def main() -> int:
    args = parse_args()
    report = asyncio.run(run_load(args))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = report["summary"]
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"report={args.output}")
    return 0 if summary["failed_or_timeout"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
