from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44_100
DURATION_SECONDS = 138.0
BPM = 102
BEAT_SECONDS = 60.0 / BPM
STEP_SECONDS = BEAT_SECONDS / 4.0
BAR_SECONDS = BEAT_SECONDS * 4.0
TOTAL_SAMPLES = int(DURATION_SECONDS * SAMPLE_RATE)

OUTPUT = Path("assets/audio/ktd-modern-trap-comparison-bed-v1.wav")


def add_signal(audio: np.ndarray, start: int, signal: np.ndarray, gain: float, pan: float = 0.0) -> None:
    if start >= audio.shape[0]:
        return
    end = min(audio.shape[0], start + signal.shape[0])
    if end <= start:
        return
    usable = signal[: end - start] * gain
    left = (1.0 - max(0.0, pan)) if pan >= 0 else 1.0
    right = (1.0 + min(0.0, pan)) if pan <= 0 else 1.0
    audio[start:end, 0] += usable * left
    audio[start:end, 1] += usable * right


def kick(length: float = 0.42) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    freq = 46.0 + 78.0 * np.exp(-t * 24.0)
    body = np.sin(2 * np.pi * freq * t) * np.exp(-t * 9.0)
    click = np.sin(2 * np.pi * 1_900.0 * t) * np.exp(-t * 75.0)
    return (0.9 * body + 0.08 * click).astype(np.float32)


def snare(length: float = 0.22, seed: int = 0) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 1.0, n).astype(np.float32)
    tone = np.sin(2 * np.pi * 190.0 * t) * np.exp(-t * 18.0)
    return (0.32 * noise * np.exp(-t * 28.0) + 0.22 * tone).astype(np.float32)


def hat(length: float = 0.055, seed: int = 0) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 1.0, n).astype(np.float32)
    shimmer = np.sin(2 * np.pi * 7_200.0 * t)
    return (0.12 * (noise * 0.75 + shimmer * 0.25) * np.exp(-t * 85.0)).astype(np.float32)


def open_hat(length: float = 0.18, seed: int = 0) -> np.ndarray:
    return hat(length, seed) * 0.72


def bass_note(freq: float, length: float = 0.62) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    glide = freq * (1.08 - 0.08 * np.exp(-t * 14.0))
    fundamental = np.sin(2 * np.pi * glide * t)
    harmonic = 0.28 * np.sin(2 * np.pi * glide * 2.0 * t)
    envelope = np.minimum(1.0, t * 90.0) * np.exp(-t * 2.6)
    return ((fundamental + harmonic) * envelope).astype(np.float32)


def pad(length: float = 2.3, root: float = 43.65) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    notes = [root, root * 1.1892, root * 1.4983]
    signal = sum(np.sin(2 * np.pi * f * t + phase) for f, phase in zip(notes, (0.0, 1.3, 2.1)))
    envelope = np.minimum(1.0, t * 0.8) * np.minimum(1.0, (length - t) * 0.8)
    return (0.026 * signal * np.maximum(envelope, 0.0)).astype(np.float32)


def transition_noise(length: float = 0.42, seed: int = 0) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 1.0, n).astype(np.float32)
    sweep = np.sin(2 * np.pi * (600.0 + 5_000.0 * t) * t)
    return (0.08 * (noise * 0.55 + sweep * 0.45) * np.exp(-t * 5.0)).astype(np.float32)


def section(bar: int) -> str:
    if bar < 4:
        return "intro"
    if bar < 16:
        return "verse"
    if bar < 24:
        return "hook"
    if bar < 38:
        return "verse2"
    if bar < 46:
        return "bridge"
    return "final"


def main() -> None:
    audio = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    kick_sig = kick()
    snare_sig = snare(seed=17)
    bass_roots = [43.65, 51.91, 65.41, 58.27]  # F, Ab, C, Bb in the lower register.

    total_bars = math.ceil(DURATION_SECONDS / BAR_SECONDS)
    for bar in range(total_bars):
        mode = section(bar)
        bar_start = bar * BAR_SECONDS
        pad_root = bass_roots[(bar // 2) % len(bass_roots)]
        pad_start = int(bar_start * SAMPLE_RATE)
        add_signal(audio, pad_start, pad(root=pad_root), 1.0, pan=-0.12 if bar % 2 else 0.12)

        if bar in (4, 16, 24, 38, 46):
            add_signal(audio, pad_start, transition_noise(seed=bar), 1.0, pan=-0.3 if bar % 2 else 0.3)

        for step in range(16):
            step_start = bar_start + step * STEP_SECONDS
            sample_start = int(step_start * SAMPLE_RATE)
            if mode == "intro":
                if step in (0, 8) and bar >= 2:
                    add_signal(audio, sample_start, kick_sig, 0.62)
                continue
            if mode == "bridge":
                if step in (4, 12) and bar % 2 == 0:
                    add_signal(audio, sample_start, snare_sig, 0.44, pan=0.02)
                if step in (0, 8) and bar % 2 == 1:
                    add_signal(audio, sample_start, bass_note(bass_roots[bar % len(bass_roots)], 0.48), 0.55)
                if step % 4 == 0:
                    add_signal(audio, sample_start, hat(seed=bar * 16 + step), 0.32, pan=-0.25 if step % 8 else 0.25)
                continue

            kick_steps = {0, 6, 8, 11, 14} if mode in ("hook", "final") else {0, 7, 8, 14}
            if step in kick_steps:
                velocity = 0.74 if step in (0, 8) else 0.57
                add_signal(audio, sample_start, kick_sig, velocity)
            if step in (4, 12):
                snare_velocity = 0.72 if mode in ("hook", "final") else 0.62
                add_signal(audio, sample_start, snare_sig, snare_velocity, pan=0.02)
            if step % 2 == 0 or (mode == "final" and step in (1, 3, 5, 7, 9, 11, 13, 15)):
                hat_velocity = 0.34 if step % 4 else 0.46
                if mode == "hook":
                    hat_velocity *= 1.1
                add_signal(audio, sample_start, hat(seed=bar * 16 + step), hat_velocity, pan=-0.35 if step % 4 else 0.3)
            if step == 10 and bar % 2 == 1 and mode in ("hook", "final"):
                add_signal(audio, sample_start, open_hat(seed=bar), 0.42, pan=0.22)

            bass_step = step in ({0, 6, 8, 12} if mode in ("hook", "final") else {0, 8, 14})
            if bass_step:
                note = bass_roots[(bar + (step // 8)) % len(bass_roots)]
                add_signal(audio, sample_start, bass_note(note), 0.68 if mode == "final" else 0.58)

    fade = int(0.08 * SAMPLE_RATE)
    audio[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)[:, None]
    audio[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)[:, None]
    peak = float(np.max(np.abs(audio)))
    if peak > 0.92:
        audio *= 0.92 / peak
    pcm = (np.clip(audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUTPUT), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
