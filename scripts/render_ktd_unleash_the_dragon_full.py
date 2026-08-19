#!/usr/bin/env python3
"""Renderiza o vídeo clipe completo vertical de UNLEASH THE DRAGON (padrão do cânone KTD).

O script transforma keyframes líricas em planos com movimento procedural,
cortes alinhados à grade de BPM (102 BPM, beat = 0,588 s), variação de luz e
vignette, aplicando a gramática do cânone aprovado: push-in predominante,
hard cuts no downbeat, planos longos de recompensa e fade final a preto no
último golpe. O áudio oficial é muxado ao final por FFmpeg com a duração
exata da faixa (150,000 s).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


@dataclass(frozen=True)
class Shot:
    image: Path
    start: float
    end: float
    motion: str
    direction: int
    pulse: bool = True


BEAT = 60.0 / 102.0  # 0,588235 s


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", type=Path, nargs="+", required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration", type=float, default=150.0)
    parser.add_argument("--bpm", type=float, default=102.0)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--width", type=int, default=720)
    parser.add_argument("--height", type=int, default=1280)
    parser.add_argument("--forbidden-manifest", type=Path)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def load_forbidden_hashes(manifest: Path | None) -> set[str]:
    if not manifest:
        return set()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    return {
        item["sha256"] for item in data.get("files", [])
        if item.get("sha256") and item.get("category") == "GOLDEN_SCARS"
    }


def resolve_shots(images: list[Path], forbidden: set[str]) -> list[Path]:
    seen: set[str] = set()
    resolved: list[Path] = []
    for path in images:
        if not path.is_file():
            raise SystemExit(f"Imagem não encontrada: {path}")
        digest = sha256(path)
        if digest in forbidden:
            raise SystemExit(f"Imagem bloqueada pelo manifesto (GOLDEN_SCARS): {path}")
        if digest in seen:
            raise SystemExit(f"Imagem duplicada: {path}")
        seen.add(digest)
        resolved.append(path)
    if len(resolved) < 6:
        raise SystemExit("O clipe completo exige pelo menos 6 keyframes distintas.")
    return resolved


def build_shots(images: list[Path], duration: float, bpm: float) -> list[Shot]:
    """Constrói a grade de planos: barras de 4 batidas (~2,353 s), com cortes
    acelerados nos hooks e planos longos de recompensa."""
    beat = 60.0 / bpm
    bar = beat * 4.0
    n = len(images)
    # Distribuição ponderada: plano final (microfone solitário + fade) recebe
    # um pouco mais de espaço para o encerramento.
    weights = [1.0] * n
    weights[-1] = 1.6
    total = sum(weights)
    shots: list[Shot] = []
    cursor = 0.0
    motions = [
        "push_in", "tracking_right", "push_in", "cut_push", "tilt_up",
        "push_in", "push_in", "pull_out", "tracking_right", "tracking_left",
        "push_in", "pull_out_fade",
    ]
    for index, (image, weight) in enumerate(zip(images, weights)):
        span = duration * weight / total
        # Alinha o fim do plano à grade de barras, exceto o último.
        if index < n - 1:
            span = max(bar, round(span / bar) * bar)
        start = cursor
        cursor += span
        end = duration if index == n - 1 else cursor
        shots.append(Shot(
            image=image, start=start, end=end,
            motion=motions[index % len(motions)],
            direction=1 if index % 2 == 0 else -1,
            pulse=index != n - 1,
        ))
    return shots


def animated_frame(source: Image.Image, progress: float, motion: str,
                   direction: int, size: tuple[int, int]) -> Image.Image:
    width, height = size
    source = ImageOps.exif_transpose(source).convert("RGB")
    source_ratio = source.width / source.height
    target_ratio = width / height
    if source_ratio > target_ratio:
        crop_width = int(source.height * target_ratio)
        crop_height = source.height
    else:
        crop_width = source.width
        crop_height = int(crop_width / target_ratio)

    if motion in {"push_in", "cut_push"}:
        scale = 1.04 + 0.10 * progress
    elif motion == "pull_out" or motion == "pull_out_fade":
        scale = 1.12 - 0.08 * progress
    else:
        scale = 1.08

    crop_width = min(source.width, int(crop_width / scale))
    crop_height = min(source.height, int(crop_height / scale))
    max_x = source.width - crop_width
    max_y = source.height - crop_height

    if motion in {"tracking_right", "tracking_left"}:
        x_progress = progress if direction > 0 else 1.0 - progress
        x = int(max_x * x_progress)
        y = int(max_y * (0.42 + 0.08 * math.sin(progress * math.pi)))
    elif motion == "tilt_up":
        x = int(max_x * 0.5)
        y = int(max_y * (1.0 - progress))
    elif motion == "pull_out_fade":
        x = int(max_x * (0.45 + 0.10 * progress))
        y = int(max_y * (0.50 - 0.10 * progress))
    else:
        x = int(max_x * (0.50 + 0.08 * (progress - 0.5)))
        y = int(max_y * 0.50)

    frame = source.crop((x, y, x + crop_width, y + crop_height)).resize((width, height), Image.Resampling.LANCZOS)
    if motion == "pull_out_fade":
        fade = max(0.0, 1.0 - ((progress - 0.55) / 0.45)) if progress > 0.55 else 1.0
        frame = ImageEnhance.Brightness(frame).enhance(fade)
    else:
        pulse = 1.0 + 0.035 * math.sin(progress * math.pi * 4.0)
        frame = ImageEnhance.Brightness(frame).enhance(pulse)
    frame = ImageEnhance.Contrast(frame).enhance(1.04)

    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((-width * 0.20, -height * 0.10, width * 1.20, height * 1.10), fill=220)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=width * 0.12))
    dark = Image.new("RGB", (width, height), (12, 5, 3))
    frame = Image.composite(frame, dark, mask)

    warm = Image.new("RGB", (width, height), (86, 38, 16))
    warm_alpha = int(22 + 12 * math.sin(progress * math.pi * 2.0))
    frame = Image.blend(frame, warm, warm_alpha / 255.0)
    return frame


def render_frames(shots: list[Shot], temp_dir: Path, fps: int,
                  size: tuple[int, int]) -> None:
    cache: dict[Path, Image.Image] = {}
    frame_index = 0
    for shot in shots:
        source = cache.setdefault(shot.image, Image.open(shot.image))
        frame_count = max(1, int(round((shot.end - shot.start) * fps)))
        for local_index in range(frame_count):
            progress = local_index / max(1, frame_count - 1)
            frame = animated_frame(source, progress, shot.motion,
                                   shot.direction, size)
            frame.save(temp_dir / f"frame_{frame_index:06d}.jpg",
                       quality=94, subsampling=0)
            frame_index += 1


def mux_video(temp_dir: Path, audio: Path, output: Path, fps: int,
              duration: float) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", str(temp_dir / "frame_%06d.jpg"), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0", "-t", f"{duration:.3f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output),
    ]
    subprocess.run(command, check=True)


def main() -> None:
    args = parse_args()
    if args.output.exists() and not args.force:
        raise SystemExit(f"Destino já existe; use --force somente se a substituição for intencional: {args.output}")
    if not args.audio.is_file():
        raise SystemExit(f"Áudio não encontrado: {args.audio}")
    forbidden = load_forbidden_hashes(args.forbidden_manifest)
    images = resolve_shots(args.images, forbidden)
    shots = build_shots(images, args.duration, args.bpm)
    with tempfile.TemporaryDirectory(prefix="ktd_utd_full_") as work:
        temp_dir = Path(work)
        render_frames(shots, temp_dir, args.fps, (args.width, args.height))
        mux_video(temp_dir, args.audio, args.output, args.fps, args.duration)
    print(f"Render concluído: {args.output}")
    for shot in shots:
        print(f"  {shot.start:06.2f}-{shot.end:06.2f}s | {shot.motion:14s} | {shot.image.name}")


if __name__ == "__main__":
    main()
