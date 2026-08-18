"""Render a new FIRE IN THE FLOOD mix with the rejected drum layer removed.

Preserved from the approved V1:
- vocal stem
- harmonic/melodic accompaniment (Demucs 'other' stem)

Replaced:
- old drums and bass are not used
- the new groove is generated independently on the V1's 94 BPM grid

The reference contributes only abstract groove/harmonic attributes documented in
this task: 4/4 stepping syncopation, light secondary swing, sparse dark minor
staccato stabs, kick-locked sub, and 8-bar density changes.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEM_DIR = ROOT / ".tmp/ktd-v1-four-stems/htdemucs/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1"
VOCAL = STEM_DIR / "vocals.wav"
MELODY_BED = STEM_DIR / "other.wav"
GROOVE = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-aligned-groove-v1.wav"
OUT_WAV = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.wav"
OUT_MP3 = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.mp3"
DURATION = 168


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-hide_banner", *args], check=True)


def render() -> None:
    OUT_WAV.parent.mkdir(parents=True, exist_ok=True)
    graph = (
        "[0:a]asplit=2[vraw_main][vraw_parallel];"
        "[vraw_main]highpass=f=65,lowpass=f=12500,"
        "acompressor=threshold=-21dB:ratio=2.0:attack=10:release=95:makeup=1.10,"
        "asoftclip=type=tanh:threshold=0.86:output=1.01:param=1.08:oversample=4,"
        "apad=whole_dur=168,atrim=0:168[vmain];"
        "[vraw_parallel]highpass=f=65,lowpass=f=12500,"
        "acompressor=threshold=-34dB:ratio=6:attack=5:release=130:makeup=1.35,"
        "volume=0.22,apad=whole_dur=168,atrim=0:168[vparallel];"
        "[vmain][vparallel]amix=inputs=2:weights='1 0.30':normalize=0[vocal_mix];"
        "[vocal_mix]asplit=2[vocal_key][vocal_main];"
        "[1:a]volume=0.96,highpass=f=95,lowpass=f=13500,"
        "equalizer=f=240:t=q:w=1.0:g=-1.3,"
        "apad=whole_dur=168,atrim=0:168[melody_bed];"
        "[2:a]volume=0.76,highpass=f=28,lowpass=f=14500,"
        "apad=whole_dur=168,atrim=0:168[groove_pre];"
        "[groove_pre][vocal_key]sidechaincompress="
        "threshold=0.075:ratio=1.55:attack=6:release=150:makeup=1:"
        "link=average:detection=rms[groove_ducked];"
        "[melody_bed][groove_ducked]amix=inputs=2:weights='1 0.88':normalize=0[instrumental];"
        "[instrumental][vocal_main]amix=inputs=2:weights='1 1.18':normalize=0,"
        "loudnorm=I=-14:TP=-1.0:LRA=7,alimiter=limit=0.95,"
        "aresample=44100[out]"
    )
    run_ffmpeg([
        "-i", str(VOCAL),
        "-i", str(MELODY_BED),
        "-i", str(GROOVE),
        "-filter_complex", graph,
        "-map", "[out]",
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
