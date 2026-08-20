from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/releases/fire-in-the-flood-dynamic-shot-manifest-v1.json"
AUDIO = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav"
WORK = ROOT / "artifacts/video/dynamic-shots"
OUT = ROOT / "artifacts/video/ktd-fire-in-the-flood-dynamic-v1.mp4"
CONCAT = ROOT / "artifacts/video/validation/fire-in-the-flood-dynamic-concat.txt"
PROBE = ROOT / "artifacts/video/validation/fire-in-the-flood-dynamic-v1-ffprobe.txt"


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    shots = manifest["shots"]
    missing = [shot["output"] for shot in shots if not (ROOT / shot["output"]).is_file()]
    if missing:
        print("MISSING_DYNAMIC_SHOTS")
        for item in missing:
            print(item)
        raise SystemExit(2)
    if not AUDIO.is_file():
        raise FileNotFoundError(AUDIO)

    CONCAT.parent.mkdir(parents=True, exist_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for shot in shots:
        path = (ROOT / shot["output"]).resolve()
        lines.append(f"file '{path}'")
    CONCAT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Normalize every generated shot to the delivery canvas while preserving real
    # temporal motion. The source clips are expected to be continuous video; this
    # stage only handles technical matching and audio replacement.
    video_filter = (
        "scale=1920:1080:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,"
        "setsar=1,fps=24,format=yuv420p"
    )
    temp = WORK / "_dynamic_joined_silent.mp4"
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(CONCAT),
        "-vf", video_filter, "-an", "-t", "168", "-c:v", "libx264",
        "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(temp)
    ])
    run([
        "ffmpeg", "-y", "-i", str(temp), "-i", str(AUDIO), "-t", "168",
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
        "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", str(OUT)
    ])
    with PROBE.open("w", encoding="utf-8") as handle:
        subprocess.run([
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration:stream=codec_name,codec_type,width,height,sample_rate,channels,r_frame_rate,bit_rate",
            "-of", "default=noprint_wrappers=1", str(OUT)
        ], check=True, stdout=handle)
    print(OUT)
    print(PROBE)


if __name__ == "__main__":
    main()
