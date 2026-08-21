from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


class MockHandler(BaseHTTPRequestHandler):
    server_version = "KairLocalMock/1.0"

    @property
    def kind(self) -> str:
        return self.server.mock_kind  # type: ignore[attr-defined]

    def _json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _sse(self, payloads: list[dict[str, object]]) -> None:
        body = "".join(f"data: {json.dumps(payload)}\n\n" for payload in payloads).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            return self._json(200, {"status": "ok", "agent": self.kind})
        if self.kind == "space":
            if path == "/gradio_api/info":
                return self._json(
                    200,
                    {
                        "named_endpoints": {
                            "/generate_diffusion_forced_video": {
                                "parameters": [{"label": f"input-{index}"} for index in range(23)]
                            }
                        }
                    },
                )
            if path == "/config":
                return self._json(
                    200,
                    {
                        "dependencies": [
                            {
                                "api_name": "/generate_diffusion_forced_video",
                                "queue": True,
                                "inputs": [{"id": index} for index in range(23)],
                            }
                        ]
                    },
                )
        if self.kind == "llamagen" and path == "/v1/comics/generations/nonexistent":
            return self._json(404, {"error": "generation not found"})
        return self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        if self.kind == "space":
            if path == "/gradio_api/upload":
                return self._json(200, [{"path": "/tmp/mock-reference.png", "meta": {"_type": "gradio.FileData"}}])
            if path in {
                "/gradio_api/call/generate_diffusion_forced_video",
                "/gradio_api/call/v2/generate_diffusion_forced_video",
            }:
                return self._json(200, {"event_id": "mock-space-event"})
        if self.kind == "llamagen" and path == "/v1/comics/upload":
            return self._json(200, {"id": "mock-upload", "status": "uploaded"})
        return self._json(404, {"error": "not found"})

    def do_PATCH(self) -> None:
        self._json(200, {"id": "mock-generation", "status": "updated"})

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.end_headers()

    def do_GET_stream(self) -> None:
        self._sse(
            [
                {"msg": "process_completed", "success": True, "output": {"data": [{"path": "/tmp/mock-output.mp4"}]}},
            ]
        )


class StreamHandler(MockHandler):
    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if self.kind == "space" and path == "/gradio_api/call/generate_diffusion_forced_video/mock-space-event":
            return self._sse(
                [
                    {
                        "msg": "process_completed",
                        "success": True,
                        "output": {"data": [{"path": "/tmp/mock-output.mp4"}]},
                    }
                ]
            )
        return super().do_GET()


def main() -> None:
    parser = argparse.ArgumentParser(description="Mock local agent service for Compose tests")
    parser.add_argument("--kind", choices=("space", "llamagen"), required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("0.0.0.0", args.port), StreamHandler)
    server.mock_kind = args.kind  # type: ignore[attr-defined]
    print(f"mock {args.kind} listening on :{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
