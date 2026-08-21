#!/usr/bin/env python3
"""Monta clipes reais verticais de UNLEASH THE DRAGON sem muxagem de áudio.

O pipeline v2 abandona slides/Ken Burns como produto final e concatena clipes
com movimento físico contínuo. Cada entrada é normalizada para 720x1280 @24
fps, os cortes são secos e o arquivo final não contém faixa de áudio até que a
nova mixagem oficial seja aprovada editorialmente.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


WIDTH = 720
HEIGHT = 1280
FPS = 24


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration,size:stream=index,codec_name,codec_type,width,height,r_frame_rate,pix_fmt",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clips", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--fps", type=int, default=FPS)
    parser.add_argument("--width", type=int, default=WIDTH)
    parser.add_argument("--height", type=int, default=HEIGHT)
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def validate_inputs(clips: list[Path], output: Path, force: bool) -> None:
    if len(clips) < 2:
        raise SystemExit("A montagem v2 exige pelo menos dois clipes reais.")
    for path in clips:
        if not path.is_file():
            raise SystemExit(f"Clipe não encontrado: {path}")
    if output.exists() and not force:
        raise SystemExit(
            f"Destino já existe; use --force somente se a substituição for intencional: {output}"
        )


def build_filtergraph(count: int, width: int, height: int, fps: int) -> str:
    labels: list[str] = []
    parts: list[str] = []
    for index in range(count):
        label = f"v{index}"
        labels.append(f"[{label}]")
        parts.append(
            f"[{index}:v:0]fps={fps},"
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"format=yuv420p,setsar=1[{label}]"
        )
    parts.append("".join(labels) + f"concat=n={count}:v=1:a=0[vout]")
    return ";".join(parts)


def assemble(args: argparse.Namespace) -> dict[str, Any]:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    filtergraph = build_filtergraph(len(args.clips), args.width, args.height, args.fps)
    command = ["ffmpeg", "-y"]
    for clip in args.clips:
        command.extend(["-i", str(clip)])
    command.extend(
        [
            "-filter_complex",
            filtergraph,
            "-map",
            "[vout]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            str(args.crf),
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(args.fps),
            "-movflags",
            "+faststart",
            str(args.output),
        ]
    )
    subprocess.run(command, check=True)

    output_probe = probe(args.output)
    manifest = {
        "title": "UNLEASH THE DRAGON — real clips v2 work-in-progress",
        "status": "technical preview; pending editorial approval and approved mix",
        "audio": "intentionally omitted",
        "format": {
            "width": args.width,
            "height": args.height,
            "fps": args.fps,
            "video_codec": "H.264",
            "pixel_format": "yuv420p",
            "crf": args.crf,
        },
        "inputs": [
            {
                "path": str(path),
                "sha256": sha256(path),
                "probe": probe(path),
            }
            for path in args.clips
        ],
        "output": {
            "path": str(args.output),
            "sha256": sha256(args.output),
            "probe": output_probe,
        },
    }
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return manifest


def main() -> None:
    args = parse_args()
    validate_inputs(args.clips, args.output, args.force)
    manifest = assemble(args)
    duration = manifest["output"]["probe"]["format"].get("duration", "unknown")
    print(f"Montagem concluída: {args.output}")
    print(f"Duração: {duration}s | clipes: {len(args.clips)} | áudio: omitido")


if __name__ == "__main__":
    main()
