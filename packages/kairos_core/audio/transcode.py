from __future__ import annotations

import shutil
import subprocess
import wave
from pathlib import Path

import numpy as np


def write_wav(path: Path, audio: np.ndarray, sample_rate: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = np.clip(audio, -1.0, 1.0)
    pcm = (pcm * 32767.0).astype(np.int16)
    if pcm.ndim == 1:
        pcm = pcm[:, None]
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(pcm.shape[1])
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(pcm.tobytes())
    return path


def transcode_to_mp3(wav_path: Path, mp3_path: Path, ffmpeg_bin: str = "ffmpeg") -> Path:
    executable = shutil.which(ffmpeg_bin)
    if not executable:
        raise RuntimeError("FFmpeg não encontrado; instale-o para solicitar output_format=mp3")
    mp3_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([executable, "-y", "-i", str(wav_path), "-codec:a", "libmp3lame", "-b:a", "320k", str(mp3_path)], check=True, capture_output=True)
    return mp3_path
