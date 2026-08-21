from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/releases/fire-in-the-flood-existing-materials-cut-v2.json"
WORK = ROOT / "artifacts/video/existing-materials-cut-v2-work"
NORMALIZED = WORK / "normalized"
CONCAT = WORK / "video_concat.mp4"
OUTPUT = ROOT / "artifacts/video/fire-in-the-flood-existing-materials-preview-v2.mp4"
REPORT = ROOT / "artifacts/video/validation/fire-in-the-flood-existing-materials-cut-v2-report.md"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    shots = manifest["shots"]
    if not shots:
        raise SystemExit("No shots configured")
    if any(Path(shot["source"]).suffix.lower() != ".mp4" for shot in shots):
        raise SystemExit("Static or non-MP4 source found; refusing assembly")
    expected = sum(float(shot["duration"]) for shot in shots)
    if abs(expected - float(manifest["duration_seconds"])) > 0.01:
        raise SystemExit(f"Manifest duration mismatch: {expected}")
    for shot in shots:
        source = ROOT / shot["source"]
        if not source.is_file():
            raise SystemExit(f"Missing source: {source}")

    NORMALIZED.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    normalized_files: list[Path] = []
    for index, shot in enumerate(shots, start=1):
        source = ROOT / shot["source"]
        target = NORMALIZED / f"{index:02d}-{shot['id']}.mp4"
        duration = float(shot["duration"])
        # Scale and crop landscape sources to the approved portrait canvas; portrait sources are preserved.
        vf = (
            "scale=720:1280:force_original_aspect_ratio=increase,"
            "crop=720:1280,setsar=1,fps=24,format=yuv420p"
        )
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(source), "-t", f"{duration:.3f}",
            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-r", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(target),
        ])
        normalized_files.append(target)

    concat_list = WORK / "concat.txt"
    concat_list.write_text("".join(f"file '{path.as_posix()}'\n" for path in normalized_files), encoding="utf-8")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(CONCAT)])

    audio = ROOT / manifest["audio_master"]
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(CONCAT), "-ss", "0", "-t", f"{expected:.3f}",
        "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0", "-t", f"{expected:.3f}",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "44100", "-ac", "2",
        "-shortest", "-movflags", "+faststart", str(OUTPUT),
    ])

    report = [
        "# FIRE IN THE FLOOD — corte com materiais existentes v2",
        "",
        f"- Saída: `{OUTPUT.relative_to(ROOT)}`",
        f"- Duração prevista: {expected:.3f} s",
        f"- Duração efetiva: {probe_duration(OUTPUT):.3f} s",
        f"- Fontes dinâmicas usadas: {len(shots)}",
        "- Áudio-fonte: master v4, recortada desde 00:00 e muxada como faixa única",
        "- Nenhuma imagem estática foi convertida em vídeo",
        "",
        "## Fontes",
        "",
        "| Ordem | ID | Duração | Origem | Tratamento |",
        "|---:|---|---:|---|---|",
    ]
    for index, shot in enumerate(shots, start=1):
        report.append(f"| {index} | {shot['id']} | {float(shot['duration']):.1f} s | `{shot['source']}` | {shot['source_type']} |")
    report.extend([
        "",
        "> Este arquivo é um preview editorial de materiais já existentes, agora com a cena de entrada anexada como M01. Ele não representa as cenas S02–S05 do roteiro v4 nem o videoclipe lyric-locked completo de 168 segundos.",
        "",
        "A entrada anexada ocupa os primeiros 8 segundos. S01 aparece em seguida como prova portrait existente; os demais planos são reels/provas existentes e entram aqui para demonstrar uma montagem dinâmica respeitando a cota, sem serem rebatizados como cenas novas.",
    ])
    REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(OUTPUT)
    print(REPORT)


if __name__ == "__main__":
    main()
