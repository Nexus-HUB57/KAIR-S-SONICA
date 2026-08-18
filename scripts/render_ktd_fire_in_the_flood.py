"""Render the FIRE IN THE FLOOD arrangement proof with KTD's approved vocal reference."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BED = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-bed-v1.wav"
VOCAL = ROOT / "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3"
OUT_WAV = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.wav"
OUT_MP3 = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.mp3"
DURATION = 168


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True)


def render() -> None:
    OUT_WAV.parent.mkdir(parents=True, exist_ok=True)
    filter_complex = (
        "[0:a]volume=0.52,apad=whole_dur=168,atrim=0:168[bed];"
        "[1:a]highpass=f=65,lowpass=f=12500,"
        "acompressor=threshold=-19dB:ratio=2.2:attack=8:release=90:makeup=1.08,"
        "asoftclip=type=tanh:threshold=0.82:output=1.02:param=1.15:oversample=4[vc];"
        "[1:a]highpass=f=65,lowpass=f=12500,"
        "acompressor=threshold=-32dB:ratio=8:attack=3:release=120:makeup=1.5,"
        "volume=0.32[vp];"
        "[vc][vp]amix=inputs=2:weights='1 0.35':normalize=0,"
        "apad=whole_dur=168,atrim=0:168[vocal];"
        "[bed][vocal]amix=inputs=2:weights='1 1':normalize=0,"
        "loudnorm=I=-14:TP=-1.0:LRA=7,alimiter=limit=0.95,"
        "aresample=44100[a]"
    )
    run_ffmpeg([
        "-i", str(BED),
        "-i", str(VOCAL),
        "-filter_complex", filter_complex,
        "-map", "[a]",
        "-t", str(DURATION),
        "-c:a", "pcm_s16le",
        str(OUT_WAV),
    ])
    run_ffmpeg([
        "-i", str(OUT_WAV),
        "-codec:a", "libmp3lame",
        "-b:a", "320k",
        str(OUT_MP3),
    ])


if __name__ == "__main__":
    render()
