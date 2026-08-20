from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/releases/fire-in-the-flood-10s-scene-manifest-v1.json"
WORK = ROOT / "artifacts/video/dynamic-10s"
AUDIO = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav"
CONCAT = WORK / "concat.txt"
SILENT = WORK / "joined-silent.mp4"
OUT = ROOT / "artifacts/video/ktd-fire-in-the-flood-full-dynamic-10s-v1.mp4"
PROBE = ROOT / "artifacts/video/validation/ktd-fire-in-the-flood-full-dynamic-10s-v1-ffprobe.txt"


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scenes = manifest["scenes"]
    target_duration = float(manifest["duration_seconds"])
    tolerance = 0.08
    if len(scenes) != 17:
        raise RuntimeError(f"Expected 17 scenes, found {len(scenes)}")
    if abs(sum(float(s["duration"]) for s in scenes) - target_duration) > 1e-6:
        raise RuntimeError("Scene durations do not sum to the master duration")
    if not AUDIO.is_file():
        raise FileNotFoundError(AUDIO)

    missing = [s["output"] for s in scenes if not (ROOT / s["output"]).is_file()]
    if missing:
        print("MISSING_DYNAMIC_SCENES")
        for item in missing:
            print(item)
        raise SystemExit(2)

    WORK.mkdir(parents=True, exist_ok=True)
    PROBE.parent.mkdir(parents=True, exist_ok=True)
    normalized: list[Path] = []
    for scene in scenes:
        source = ROOT / scene["output"]
        expected = float(scene["duration"])
        actual = probe_duration(source)
        if abs(actual - expected) > tolerance:
            raise RuntimeError(f"Duration mismatch {scene['id']}: {actual:.3f}s vs {expected:.3f}s")
        destination = WORK / f"{scene['id']}-normalized.mp4"
        run([
            "ffmpeg", "-y", "-v", "error", "-i", str(source),
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                   "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=24,format=yuv420p",
            "-an", "-t", f"{expected:.3f}", "-c:v", "libx264", "-preset", "medium",
            "-crf", "18", "-pix_fmt", "yuv420p", str(destination),
        ])
        normalized.append(destination)

    CONCAT.write_text("\n".join(f"file '{p.resolve()}'" for p in normalized) + "\n", encoding="utf-8")
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(CONCAT),
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-t", f"{target_duration:.3f}", str(SILENT),
    ])
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(SILENT), "-i", str(AUDIO),
        "-t", f"{target_duration:.3f}", "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "44100",
        "-movflags", "+faststart", str(OUT),
    ])
    with PROBE.open("w", encoding="utf-8") as handle:
        subprocess.run([
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration:stream=codec_name,codec_type,width,height,sample_rate,channels,r_frame_rate,bit_rate",
            "-of", "default=noprint_wrappers=1", str(OUT),
        ], check=True, stdout=handle)
    print(OUT)
    print(PROBE)


if __name__ == "__main__":
    main()
