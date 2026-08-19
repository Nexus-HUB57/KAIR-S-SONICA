#!/usr/bin/env python3
"""Renderiza um teaser vertical dinâmico de UNLEASH THE DRAGON sem usar vídeo generativo.

Este script segue o mesmo pipeline híbrido validado em `render_ktd_six_names_hybrid.py`,
adaptado ao roteiro exclusivo da faixa de estreia: bastidor de palco, travessia de
cabos, microfone vintage e palco iluminado. A paleta usa carvão, bronze, vermelho
queimado e âmbar — sem azul elétrico, néon frio ou chuva, conforme o inventário de
não repetição visual do álbum.

O áudio é muxado no final por FFmpeg; hashes proibidos (GOLDEN SCARS) são bloqueados
pelo manifesto; nenhuma imagem pode se repetir dentro do mesmo teaser.
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

# Paleta exclusiva de UNLEASH THE DRAGON (carvão, bronze, vermelho queimado, âmbar).
WARM_OVERLAY = (92, 30, 12)


@dataclass(frozen=True)
class Shot:
    image: Path
    start: float
    end: float
    motion: str
    direction: int


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image-dir", type=Path)
    parser.add_argument("--image", type=Path, action="append", dest="images",
                        help="Imagem exclusiva da faixa; pode ser repetido.")
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--duration", type=float, default=8.0)
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
    hashes: set[str] = set()
    for item in data.get("files", []):
        value = item.get("sha256")
        category = item.get("category")
        if value and category == "GOLDEN_SCARS":
            hashes.add(value)
    return hashes


def discover_images(image_dir: Path | None, explicit: list[Path] | None,
                    forbidden: set[str]) -> list[Path]:
    if explicit:
        images = [path for path in explicit]
    elif image_dir:
        images = sorted(
            path
            for path in image_dir.iterdir()
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        )
    else:
        raise SystemExit("Informe --image-dir ou pelo menos quatro ocorrências de --image.")
    if not images:
        raise SystemExit(f"Nenhuma imagem encontrada em {image_dir}")
    seen: set[str] = set()
    for path in images:
        digest = sha256(path)
        if digest in forbidden:
            raise SystemExit(f"Imagem bloqueada pelo manifesto (GOLDEN SCARS): {path}")
        if digest in seen:
            raise SystemExit(f"Imagem duplicada no conjunto de entrada: {path}")
        seen.add(digest)
    if len(images) < 4:
        raise SystemExit("UNLEASH THE DRAGON requer pelo menos 4 imagens exclusivas distintas.")
    return images


def build_shots(images: list[Path], duration: float, bpm: float) -> list[Shot]:
    """Distribui os planos ao longo da duração com movimentos distintos.

    A grade usa o BPM da faixa para alinhar os cortes aos downbeats: para 102 BPM
    o beat é ~0,588 s e cada plano cobre ~3,36 beats (2 s), mantendo hard cuts em
    múltiplos do beat. O roteiro de oito segundos alterna push-in (preparação),
    planos de travessia e um pull-out de recompensa final.
    """
    if len(images) < 4:
        raise SystemExit("O teaser exige pelo menos quatro imagens distintas e sem repetição.")
    beat = 60.0 / bpm
    shot_duration = 2.0
    if len(images) * shot_duration > duration:
        shot_duration = duration / len(images)
    motions = ["push_in", "pan_right", "push_in", "pull_out"]
    shots: list[Shot] = []
    for index, image in enumerate(images):
        start = index * shot_duration
        end = duration if index == len(images) - 1 else (index + 1) * shot_duration
        shots.append(
            Shot(
                image=image,
                start=start,
                end=end,
                motion=motions[index % len(motions)],
                direction=1 if index % 2 == 0 else -1,
            )
        )
    return shots


def animated_frame(source: Image.Image, progress: float, motion: str,
                   direction: int, size: tuple[int, int]) -> Image.Image:
    width, height = size
    source = ImageOps.exif_transpose(source).convert("RGB")
    source_ratio = source.width / source.height
    target_ratio = width / height
    if source_ratio > target_ratio:
        crop_height = source.height
        crop_width = int(crop_height * target_ratio)
    else:
        crop_width = source.width
        crop_height = int(crop_width / target_ratio)

    scale = 1.04 + 0.10 * progress if motion in {"push_in"} else 1.08
    if motion == "pull_out":
        scale = 1.16 - 0.08 * progress
    crop_width = min(source.width, int(crop_width / scale))
    crop_height = min(source.height, int(crop_height / scale))
    max_x = source.width - crop_width
    max_y = source.height - crop_height

    if motion in {"pan_right", "pan_left"}:
        x_progress = progress if direction > 0 else 1.0 - progress
        x = int(max_x * x_progress)
        y = int(max_y * (0.42 + 0.08 * math.sin(progress * math.pi)))
    elif motion == "tilt_up":
        x = int(max_x * 0.5)
        y = int(max_y * (1.0 - progress))
    elif motion == "pull_out":
        x = int(max_x * (0.45 + 0.10 * progress))
        y = int(max_y * (0.50 - 0.10 * progress))
    else:
        x = int(max_x * (0.50 + 0.08 * (progress - 0.5)))
        y = int(max_y * 0.50)

    frame = source.crop((x, y, x + crop_width, y + crop_height)).resize((width, height),
                                                                         Image.Resampling.LANCZOS)
    pulse = 1.0 + 0.035 * math.sin(progress * math.pi * 4.0)
    frame = ImageEnhance.Brightness(frame).enhance(pulse)
    frame = ImageEnhance.Contrast(frame).enhance(1.04)

    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((-width * 0.20, -height * 0.10, width * 1.20, height * 1.10), fill=220)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=width * 0.12))
    dark = Image.new("RGB", (width, height), (12, 5, 3))
    frame = Image.composite(frame, dark, mask)

    warm = Image.new("RGB", (width, height), WARM_OVERLAY)
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
            frame = animated_frame(source, progress, shot.motion, shot.direction, size)
            frame.save(temp_dir / f"frame_{frame_index:06d}.jpg", quality=94, subsampling=0)
            frame_index += 1


def mux_video(temp_dir: Path, audio: Path, output: Path, fps: int, duration: float) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-y", "-framerate", str(fps), "-i", str(temp_dir / "frame_%06d.jpg"),
        "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0", "-t", f"{duration:.3f}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
        str(output),
    ]
    subprocess.run(command, check=True)


def main() -> None:
    args = parse_args()
    if args.output.exists() and not args.force:
        raise SystemExit(f"Destino já existe; use --force somente se a substituição "
                         f"for intencional: {args.output}")
    if not args.audio.is_file():
        raise SystemExit(f"Áudio não encontrado: {args.audio}")
    forbidden = load_forbidden_hashes(args.forbidden_manifest)
    images = discover_images(args.image_dir, args.images, forbidden)
    shots = build_shots(images, args.duration, args.bpm)
    with tempfile.TemporaryDirectory(prefix="ktd_unleash_the_dragon_") as work:
        temp_dir = Path(work)
        render_frames(shots, temp_dir, args.fps, (args.width, args.height))
        mux_video(temp_dir, args.audio, args.output, args.fps, args.duration)
    print(f"Render concluído: {args.output}")
    print("Planos sem repetição:")
    for shot in shots:
        print(f"  {shot.start:05.2f}-{shot.end:05.2f}s | {shot.motion:9s} | {shot.image.name}")


if __name__ == "__main__":
    main()
