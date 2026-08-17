from __future__ import annotations

import argparse
import json
from pathlib import Path

from kairos_core.audio.pipeline import AudioPipeline
from kairos_core.config import Settings
from kairos_core.persona import DEFAULT_PERSONA
from kairos_core.schemas import TrackRequest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kairos", description="CLI do Agente Káiros")
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="normaliza prompt e imprime plano JSON")
    plan.add_argument("--prompt", required=True)
    plan.add_argument("--genre", default="Trap Soul")
    plan.add_argument("--bpm", type=int, default=140)
    plan.add_argument("--key", default="C#")
    plan.add_argument("--scale", default="minor")
    demo = sub.add_parser("demo", help="gera um WAV procedural")
    demo.add_argument("--duration", type=float, default=8.0)
    demo.add_argument("--output", type=Path, default=Path("data/output/demo.wav"))
    persona = sub.add_parser("persona", help="inspeciona a persona operacional Káiros")
    persona.add_argument("--format", choices=("json", "prompt"), default="json")
    persona.add_argument("--context", default=None, help="contexto opcional anexado ao prompt")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "persona":
        if args.format == "prompt":
            print(DEFAULT_PERSONA.prompt_with_context(args.context))
        else:
            print(json.dumps(DEFAULT_PERSONA.to_dict(), ensure_ascii=False, indent=2))
        return 0

    request = TrackRequest(prompt=getattr(args, "prompt", "Demo Káiros"), genre=getattr(args, "genre", "Trap Soul"), bpm=getattr(args, "bpm", 140), key=getattr(args, "key", "C#"), scale=getattr(args, "scale", "minor"), duration_seconds=getattr(args, "duration", 8.0))
    settings = Settings(output_dir=Path("data/output"))
    if args.command == "plan":
        print(json.dumps(AudioPipeline(settings).maestro.build_plan(request).model_dump(), ensure_ascii=False, indent=2))
        return 0
    result = AudioPipeline(settings).run(request, request_id="cli-demo")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if result.artifact_path != args.output:
        args.output.write_bytes(result.artifact_path.read_bytes())
    print(result.artifact_path)
    return 0
