from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
IMAGE = ROOT / "assets/reels/single-17-princess-no-more/single-17-lyric-card-03-freedom-v5.png"
AUDIO = ROOT / "assets/audio/proofs/single-17-princess-come-back/single-17-princess-come-back-proof-g-chorus-harmony-v1-24s.mp3"
OUT = ROOT / "outputs/single_17/reels_8s/single-17-princess-no-more-reel-08s-freedom-fallback-v1.mp4"
OUT.parent.mkdir(parents=True, exist_ok=True)

cmd = [
    "ffmpeg", "-y", "-loop", "1", "-i", str(IMAGE), "-i", str(AUDIO),
    "-t", "8", "-map", "0:v:0", "-map", "1:a:0",
    "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,format=yuv420p",
    "-r", "24", "-c:v", "libx264", "-profile:v", "high", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
    "-af", "afade=t=in:st=0:d=0.12,afade=t=out:st=7.45:d=0.55",
    "-movflags", "+faststart", "-metadata", "title=Princess, No More — Reel 08s",
    "-metadata", "artist=Kháirus The Dragon (KTD)",
    "-metadata", "comment=TECHNICAL_TEST; procedural still fallback; AI video generation unavailable",
    str(OUT),
]
subprocess.run(cmd, check=True)
print(OUT)
