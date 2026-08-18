from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BED = ROOT / "assets/audio/releases/ktd-debut-single-unleash-the-dragon-bed-v1.wav"
VOICE = ROOT / "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3"
OUT_WAV = ROOT / "assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav"
OUT_MP3 = ROOT / "assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3"

FILTER = (
    "[0:a]atrim=duration=150,apad=whole_dur=150,volume=0.58,asetpts=N/SR/TB[bed];"
    "[1:a]atrim=duration=150,apad=whole_dur=150,"
    "highpass=f=65,lowpass=f=12500,"
    "acompressor=threshold=-19dB:ratio=2.2:attack=8:release=90:makeup=1.08,"
    "asplit=2[vmain][vpar];"
    "[vpar]acompressor=threshold=-32dB:ratio=8:attack=3:release=120:makeup=1.5,"
    "volume=0.32[vparc];"
    "[vmain][vparc]amix=inputs=2:duration=longest:weights=1 0.35:normalize=0[voice];"
    "[bed][voice]amix=inputs=2:duration=longest:weights=1 1.15:normalize=0,"
    "atrim=duration=150,loudnorm=I=-14:TP=-1.0:LRA=7,alimiter=limit=0.95[out]"
)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def main() -> None:
    OUT_WAV.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(BED),
            "-i",
            str(VOICE),
            "-filter_complex",
            FILTER,
            "-map",
            "[out]",
            "-ar",
            "44100",
            "-ac",
            "2",
            "-c:a",
            "pcm_s16le",
            str(OUT_WAV),
        ]
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(OUT_WAV),
            "-codec:a",
            "libmp3lame",
            "-b:a",
            "320k",
            str(OUT_MP3),
        ]
    )


if __name__ == "__main__":
    main()
