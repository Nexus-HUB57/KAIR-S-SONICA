"""Generate an original, V1-grid-aligned groove for FIRE IN THE FLOOD.

The reference is translated only into abstract production attributes:
4/4, a stepping syncopation, light swing on secondary hits, sparse minor
staccato stabs, sub locked to kick, and 8-bar density changes. No source audio,
melody, lyric, sample, or performance is used.
"""

from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44_100
DURATION_SECONDS = 168.0
BPM = 94.0
BEAT_SECONDS = 60.0 / BPM
STEP_SECONDS = BEAT_SECONDS / 4.0
BAR_SECONDS = BEAT_SECONDS * 4.0
TOTAL_BARS = math.ceil(DURATION_SECONDS / BAR_SECONDS)
TOTAL_SAMPLES = int(DURATION_SECONDS * SAMPLE_RATE)
OUTPUT = Path("assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-aligned-groove-v1.wav")


def add_signal(audio: np.ndarray, start: int, signal: np.ndarray, gain: float, pan: float = 0.0) -> None:
    if start >= audio.shape[0]:
        return
    end = min(audio.shape[0], start + signal.shape[0])
    if end <= start:
        return
    usable = signal[: end - start] * gain
    left = 1.0 - max(0.0, pan)
    right = 1.0 + min(0.0, pan)
    audio[start:end, 0] += usable * left
    audio[start:end, 1] += usable * right


def envelope(length: int, attack: float, release: float) -> np.ndarray:
    t = np.arange(length, dtype=np.float32) / SAMPLE_RATE
    env = np.minimum(1.0, t / max(attack, 1e-4))
    env *= np.minimum(1.0, (length / SAMPLE_RATE - t) / max(release, 1e-4))
    return np.maximum(env, 0.0)


def kick(length: float = 0.30) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    freq = 46.0 + 76.0 * np.exp(-t * 27.0)
    phase = 2.0 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    body = np.sin(phase) * np.exp(-t * 13.0)
    click = np.sin(2.0 * np.pi * 2_200.0 * t) * np.exp(-t * 95.0)
    return (0.86 * body + 0.05 * click).astype(np.float32)


def snare(length: float = 0.19, seed: int = 7) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    noise = np.random.default_rng(seed).normal(0.0, 1.0, n).astype(np.float32)
    tone = np.sin(2.0 * np.pi * 190.0 * t) * np.exp(-t * 22.0)
    return (0.30 * noise * np.exp(-t * 28.0) + 0.24 * tone).astype(np.float32)


def hat(length: float = 0.055, seed: int = 13) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    noise = np.random.default_rng(seed).normal(0.0, 1.0, n).astype(np.float32)
    bright = np.sin(2.0 * np.pi * 7_300.0 * t)
    return (0.075 * (0.7 * noise + 0.3 * bright) * np.exp(-t * 88.0)).astype(np.float32)


def perc(length: float = 0.10, seed: int = 31) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    noise = np.random.default_rng(seed).normal(0.0, 1.0, n).astype(np.float32)
    tone = np.sin(2.0 * np.pi * 740.0 * t) * np.exp(-t * 38.0)
    return (0.075 * noise * np.exp(-t * 42.0) + 0.07 * tone).astype(np.float32)


def bass_note(freq: float, length: float = 0.52) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    phase = 2.0 * np.pi * freq * t
    env = np.minimum(1.0, t * 90.0) * np.exp(-t * 3.9)
    return ((np.sin(phase) + 0.18 * np.sin(phase * 2.0) + 0.06 * np.sin(phase * 3.0)) * env).astype(np.float32)


def harmonic_stab(root: float, length: float = 0.24) -> np.ndarray:
    """Short D-minor/Phrygian-color stab, not a lead melody."""
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    env = envelope(n, attack=0.006, release=0.11) * np.exp(-t * 10.0)
    chord = (
        0.50 * np.sin(2.0 * np.pi * root * t)
        + 0.34 * np.sin(2.0 * np.pi * root * 1.1892 * t)
        + 0.28 * np.sin(2.0 * np.pi * root * 1.4983 * t)
        + 0.12 * np.sin(2.0 * np.pi * root * 2.0 * t)
    )
    return (0.10 * chord * env).astype(np.float32)


def section(bar: int) -> str:
    if bar < 4:
        return "intro"
    if bar < 20:
        return "verse"
    if bar < 28:
        return "lift"
    if bar < 40:
        return "hook"
    if bar < 60:
        return "verse2"
    if bar < 68:
        return "bridge"
    return "outro"


def event_time(bar_start: float, step: int, swung: bool = False) -> float:
    # Only secondary off-beats move; anchors remain exactly on the V1 grid.
    shift = 0.012 if swung and step % 2 == 1 else 0.0
    return bar_start + step * STEP_SECONDS + shift


def main() -> None:
    audio = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    kick_sig = kick()
    snare_sig = snare()
    bass_roots = [36.71, 43.65, 46.25, 41.20]  # D2, F2, F#2 color, E2.
    stab_roots = [146.83, 174.61, 184.99, 164.81]  # D4/F4/F#4/E4 colors.

    for bar in range(TOTAL_BARS):
        mode = section(bar)
        bar_start = bar * BAR_SECONDS
        root_idx = (bar // 2) % len(bass_roots)
        root = bass_roots[root_idx]
        stab_root = stab_roots[(bar // 2) % len(stab_roots)]
        swung = mode not in {"intro", "bridge", "outro"}

        if mode == "intro":
            continue
        if mode == "outro":
            continue

        # The reference-inspired architecture is sparse and 8-bar based.
        if mode == "bridge":
            if bar % 2 == 0:
                add_signal(audio, int(event_time(bar_start, 0) * SAMPLE_RATE), kick_sig, 0.22)
            if bar % 2 == 1:
                add_signal(audio, int(event_time(bar_start, 8) * SAMPLE_RATE), snare_sig, 0.16)
            if bar % 2 == 0:
                add_signal(audio, int(event_time(bar_start, 6, swung=True) * SAMPLE_RATE), harmonic_stab(stab_root), 0.46, pan=-0.12)
            continue

        kick_steps = {0, 3, 6, 8, 11, 14} if mode in {"hook"} else {0, 3, 6, 8, 13}
        if bar % 4 == 3:
            kick_steps = {0, 6, 8, 11}
        snare_steps = {4, 12}
        hat_steps = {0, 2, 4, 6, 8, 10, 12, 14}
        bass_steps = {0, 3, 8, 11} if mode == "hook" else {0, 8}
        stab_steps = {2, 7, 10, 15} if mode == "hook" else {3, 11}

        for step in range(16):
            t = event_time(bar_start, step, swung)
            sample_start = int(t * SAMPLE_RATE)
            if step in kick_steps:
                gain = 0.64 if step in {0, 8} else 0.40
                add_signal(audio, sample_start, kick_sig, gain)
            if step in snare_steps:
                add_signal(audio, sample_start, snare_sig, 0.47 if mode == "hook" else 0.40, pan=0.01)
            if step in hat_steps and (mode == "hook" or step % 2 == 0):
                add_signal(audio, sample_start, hat(seed=bar * 32 + step), 0.20 if mode == "hook" else 0.14, pan=-0.18 if step % 4 else 0.18)
            if step in {3, 10} and bar % 2 == 0:
                add_signal(audio, sample_start, perc(seed=bar * 16 + step), 0.36, pan=-0.20 if step == 3 else 0.20)
            if step in bass_steps:
                add_signal(audio, sample_start, bass_note(root), 0.34 if mode == "hook" else 0.28)
            if step in stab_steps:
                add_signal(audio, sample_start, harmonic_stab(stab_root), 0.52 if mode == "hook" else 0.38, pan=-0.16 if step % 2 else 0.16)

    fade = int(0.10 * SAMPLE_RATE)
    audio[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)[:, None]
    audio[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)[:, None]
    peak = float(np.max(np.abs(audio)))
    if peak > 0.82:
        audio *= 0.82 / peak
    pcm = (np.clip(audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUTPUT), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
