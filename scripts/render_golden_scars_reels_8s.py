#!/usr/bin/env python3
from pathlib import Path
import subprocess
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/video/aprovados/golden-scars-v1-frame-the-whole-picture-approved.mp4"
AUDIO = ROOT / "assets/audio/releases/ktd-third-single-golden-scars-trend-pre-release-v1.wav"
OUT = ROOT / "outputs/single_3/reels_8s"
OUT.mkdir(parents=True, exist_ok=True)

variants = [
    {
        "id": "reel01-bring-the-truth",
        "start": 33.0,
        "caption": "BRING THE TRUTH / BRING THE SCARS",
        "caption_lines": ["Bring the truth.", "Bring the scars."],
    },
    {
        "id": "reel02-bring-the-night",
        "start": 35.4,
        "caption": "BRING THE NIGHT INTO THE STARS",
        "caption_lines": ["Bring the night", "into the stars."],
    },
    {
        "id": "reel03-bring-both",
        "start": 37.9,
        "caption": "THEY WANT THE SHINE, NOT THE SCARS — I BRING BOTH",
        "caption_lines": ["They want the shine, not the scars.", "I bring both."],
    },
]


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def probe(path):
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate,channels,sample_rate",
        "-of", "json", str(path)
    ])
    return json.loads(raw)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def make_ass(path, lines):
    text = "\\N".join(lines).replace("&", "\\\\&")
    ass = f"""[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: KTD,Arial,54,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80101010,1,0,0,0,100,100,0,0,1,3,1,2,80,80,170,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\nDialogue: 0,0:00:00.35,0:00:07.55,KTD,,0,0,170,,{text}\n"""
    path.write_text(ass, encoding="utf-8")


manifest = {
    "project": "KAIR-S-SONICA",
    "single": 3,
    "title": "Golden Scars",
    "artist": "KTD",
    "status": "TECHNICAL_TEST",
    "source_video": str(SRC.relative_to(ROOT)),
    "source_audio": str(AUDIO.relative_to(ROOT)),
    "protocol": "docs/ktd-phd-audiovisual-production-protocol-v1.md",
    "format": {"width": 720, "height": 1280, "fps": 24, "duration_seconds": 8.0, "video_codec": "H.264", "audio_codec": "AAC", "audio_rate": 44100},
    "variants": [],
}

for v in variants:
    base = OUT / v["id"]
    clean = base.with_name(base.name + "-clean.mp4")
    captioned = base.with_name(base.name + "-captioned.mp4")
    thumb = base.with_name(base.name + "-thumbnail.jpg")
    ass = OUT / (v["id"] + ".ass")
    make_ass(ass, v["caption_lines"])

    common_video = [
        "-ss", "0", "-i", str(SRC), "-t", "8", "-map", "0:v:0",
        "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black",
        "-r", "24", "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", "-an", "-y", str(clean)
    ]
    run(["ffmpeg", "-v", "error"] + common_video)

    run([
        "ffmpeg", "-v", "error", "-i", str(clean), "-t", "8", "-ss", str(v["start"]), "-i", str(AUDIO),
        "-map", "0:v:0", "-map", "1:a:0", "-vf", f"ass={ass}",
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-af", "afade=t=in:st=0:d=0.10,afade=t=out:st=7.50:d=0.50",
        "-t", "8", "-movflags", "+faststart", "-metadata", f"title={v['caption']}", "-metadata", "artist=KTD", "-metadata", "album=Golden Scars", "-y", str(captioned)
    ])

    run([
        "ffmpeg", "-v", "error", "-i", str(clean), "-ss", "7.0", "-frames:v", "1", "-q:v", "2", "-y", str(thumb)
    ])

    for p in (clean, captioned, thumb):
        assert p.exists() and p.stat().st_size > 0
    manifest["variants"].append({
        "id": v["id"],
        "audio_start_seconds": v["start"],
        "lyric_hook": v["caption"],
        "clean": str(clean.relative_to(ROOT)),
        "captioned": str(captioned.relative_to(ROOT)),
        "thumbnail": str(thumb.relative_to(ROOT)),
        "sha256": {"clean": sha256(clean), "captioned": sha256(captioned), "thumbnail": sha256(thumb)},
        "probe": {"clean": probe(clean), "captioned": probe(captioned)},
    })

(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"output": str(OUT), "variants": len(variants)}, ensure_ascii=False))
