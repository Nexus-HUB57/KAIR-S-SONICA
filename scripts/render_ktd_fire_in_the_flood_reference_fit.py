from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BED = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-beat-reference-fit-v3.wav"
VOCAL = ROOT / "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3"
OUT_WAV = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-fit-v1.wav"
OUT_MP3 = ROOT / "assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-fit-v1.mp3"
DURATION = 168


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", *args], check=True)


def render() -> None:
    OUT_WAV.parent.mkdir(parents=True, exist_ok=True)
    graph = (
        "[0:a]volume=0.42,apad=whole_dur=168,atrim=0:168,aresample=44100[bed];"
        "[1:a]asplit=2[vraw_main][vraw_parallel];"
        "[vraw_main]highpass=f=65,lowpass=f=12500,"
        "acompressor=threshold=-19dB:ratio=2.2:attack=8:release=90:makeup=1.08,"
        "asoftclip=type=tanh:threshold=0.82:output=1.02:param=1.15:oversample=4,"
        "apad=whole_dur=168,atrim=0:168[vmain];"
        "[vraw_parallel]highpass=f=65,lowpass=f=12500,"
        "acompressor=threshold=-32dB:ratio=8:attack=3:release=120:makeup=1.5,"
        "volume=0.32,apad=whole_dur=168,atrim=0:168[vparallel];"
        "[vmain][vparallel]amix=inputs=2:weights='1 0.35':normalize=0[vmix];"
        "[vmix]asplit=2[vocal_sc][vocal_main];"
        "[bed][vocal_sc]sidechaincompress=threshold=0.08:ratio=1.6:attack=4:release=120:makeup=1:link=average:detection=rms[duckedbed];"
        "[duckedbed][vocal_main]amix=inputs=2:weights='1 1':normalize=0,"
        "loudnorm=I=-14:TP=-1.0:LRA=7,alimiter=limit=0.95,aresample=44100[out]"
    )
    run_ffmpeg([
        "-i", str(BED),
        "-i", str(VOCAL),
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
