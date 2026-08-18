from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44_100
DURATION_SECONDS = 168.0
BPM = 136.0
QUARTER_SECONDS = 60.0 / BPM
STEP_SECONDS = QUARTER_SECONDS / 4.0
BAR_SECONDS = QUARTER_SECONDS * 4.0
TOTAL_SAMPLES = int(DURATION_SECONDS * SAMPLE_RATE)
OUTPUT = Path("assets/audio/releases/ktd-main-single-fire-in-the-flood-beat-reference-fit-v3.wav")


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


def kick(length: float = 0.28) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    freq = 45.0 + 82.0 * np.exp(-t * 30.0)
    body = np.sin(2.0 * np.pi * freq * t) * np.exp(-t * 16.0)
    click = np.sin(2.0 * np.pi * 2_300.0 * t) * np.exp(-t * 100.0)
    return (0.92 * body + 0.055 * click).astype(np.float32)


def snare(length: float = 0.17, seed: int = 12) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    noise = np.random.default_rng(seed).normal(0.0, 1.0, n).astype(np.float32)
    tone = np.sin(2.0 * np.pi * 185.0 * t) * np.exp(-t * 24.0)
    return (0.34 * noise * np.exp(-t * 34.0) + 0.22 * tone).astype(np.float32)


def hat(length: float = 0.045, seed: int = 7) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    noise = np.random.default_rng(seed).normal(0.0, 1.0, n).astype(np.float32)
    shimmer = np.sin(2.0 * np.pi * 7_400.0 * t)
    return (0.11 * (0.72 * noise + 0.28 * shimmer) * np.exp(-t * 110.0)).astype(np.float32)


def open_hat(length: float = 0.12, seed: int = 21) -> np.ndarray:
    return hat(length, seed) * 0.72


def bass_note(freq: float, length: float = 0.62, slide: float = 0.0) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    glide = freq + slide * (1.0 - np.exp(-t * 12.0))
    phase = 2.0 * np.pi * np.cumsum(glide) / SAMPLE_RATE
    fundamental = np.sin(phase)
    harmonic = 0.22 * np.sin(phase * 2.0)
    grit = 0.08 * np.sin(phase * 3.0)
    envelope = np.minimum(1.0, t * 100.0) * np.exp(-t * 2.9)
    return ((fundamental + harmonic + grit) * envelope).astype(np.float32)


def piano_note(freq: float, length: float = 0.72) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    envelope = np.minimum(1.0, t * 80.0) * np.exp(-t * 3.2)
    signal = np.sin(2.0 * np.pi * freq * t)
    signal += 0.23 * np.sin(2.0 * np.pi * freq * 2.0 * t)
    signal += 0.09 * np.sin(2.0 * np.pi * freq * 3.0 * t)
    return (0.11 * signal * envelope).astype(np.float32)


def pad(length: float, root: float) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    notes = (root, root * 1.1892, root * 1.4983)
    signal = sum(np.sin(2.0 * np.pi * note * t + phase) for note, phase in zip(notes, (0.0, 1.1, 2.0)))
    fade = np.minimum(1.0, t * 0.7) * np.minimum(1.0, (length - t) * 0.7)
    return (0.018 * signal * np.maximum(fade, 0.0)).astype(np.float32)


def air_sweep(length: float = 0.33, seed: int = 0) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    noise = np.random.default_rng(seed).normal(0.0, 1.0, n).astype(np.float32)
    sweep = np.sin(2.0 * np.pi * (450.0 + 5_200.0 * t) * t)
    return (0.07 * (0.58 * noise + 0.42 * sweep) * np.exp(-t * 6.0)).astype(np.float32)


def section(bar: int) -> str:
    if bar < 4:
        return "intro"
    if bar < 22:
        return "verse1"
    if bar < 29:
        return "lift"
    if bar < 42:
        return "hook"
    if bar < 62:
        return "verse2"
    if bar < 69:
        return "short_hook"
    if bar < 82:
        return "bridge"
    if bar < 93:
        return "final"
    return "outro"


def main() -> None:
    audio = np.zeros((TOTAL_SAMPLES, 2), dtype=np.float32)
    kick_sig = kick()
    snare_sig = snare()
    root_notes = [36.71, 43.65, 51.91, 48.999]  # D, F, G#, G in the low register.
    piano_pattern = [73.42, 87.31, 98.00, 87.31]
    total_bars = 95

    for bar in range(total_bars):
        mode = section(bar)
        bar_start = bar * BAR_SECONDS
        start = int(bar_start * SAMPLE_RATE)
        root = root_notes[(bar // 2) % len(root_notes)]

        if mode in {"intro", "lift", "hook", "short_hook", "bridge", "final", "outro"}:
            pad_gain = 1.35 if mode in {"hook", "final"} else 0.85
            add_signal(audio, start, pad(BAR_SECONDS * 1.02, root), pad_gain, pan=-0.16 if bar % 2 else 0.16)

        if mode in {"intro", "lift", "bridge", "outro"}:
            piano_steps = (0, 6, 10, 14) if mode != "bridge" else (0, 8, 12)
            for step in piano_steps:
                note = piano_pattern[(bar + step // 4) % len(piano_pattern)]
                add_signal(audio, int((bar_start + step * STEP_SECONDS) * SAMPLE_RATE), piano_note(note), 0.78, pan=-0.1 if step % 8 else 0.1)

        if bar in (4, 22, 29, 42, 62, 69, 82, 93):
            add_signal(audio, start, air_sweep(seed=bar), 0.8, pan=-0.25 if bar % 2 else 0.25)

        for step in range(16):
            event_time = bar_start + step * STEP_SECONDS
            sample_start = int(event_time * SAMPLE_RATE)
            if mode == "intro":
                continue
            if mode == "bridge":
                if bar >= 78 and step in (0, 8) and bar % 2 == 0:
                    add_signal(audio, sample_start, kick_sig, 0.20)
                if step in (4, 12) and bar >= 79 and bar % 2 == 0:
                    add_signal(audio, sample_start, snare_sig, 0.17)
                continue
            if mode == "outro":
                continue

            if mode in {"hook", "final"}:
                kick_steps = {0, 3, 6, 8, 10, 13}
                hat_steps = {0, 2, 4, 6, 8, 10, 12, 14}
                bass_steps = {0, 3, 6, 8, 10, 13}
            elif mode == "lift":
                kick_steps = {0, 8, 13}
                hat_steps = {0, 4, 8, 12}
                bass_steps = {0, 8}
            else:
                kick_steps = {0, 6, 8, 13}
                hat_steps = {0, 4, 8, 12}
                bass_steps = {0, 8}

            if step in kick_steps:
                velocity = 0.70 if step in (0, 8) else 0.48
                add_signal(audio, sample_start, kick_sig, velocity)
            if step == 8:
                add_signal(audio, sample_start, snare_sig, 0.66 if mode in {"hook", "final"} else 0.56, pan=0.02)
            if step in hat_steps:
                hat_gain = 0.25 if mode not in {"hook", "final"} else 0.31
                add_signal(audio, sample_start, hat(seed=bar * 16 + step), hat_gain, pan=-0.22 if step % 4 else 0.22)
            if mode in {"hook", "final"} and step == 15 and bar % 2 == 1:
                add_signal(audio, sample_start, open_hat(seed=bar), 0.28, pan=0.2)
            if step in bass_steps:
                note = root_notes[(bar + step // 8) % len(root_notes)]
                slide = 11.0 if mode in {"hook", "final"} and step in (6, 13) else 0.0
                add_signal(audio, sample_start, bass_note(note, slide=slide), 0.43 if mode == "verse1" else 0.52)

    fade = int(0.12 * SAMPLE_RATE)
    audio[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)[:, None]
    audio[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)[:, None]
    peak = float(np.max(np.abs(audio)))
    if peak > 0.88:
        audio *= 0.88 / peak
    pcm = (np.clip(audio, -1.0, 1.0) * 32767.0).astype(np.int16)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUTPUT), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(pcm.tobytes())


if __name__ == "__main__":
    main()
