from __future__ import annotations

import math
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44_100
BPM = 100
BEAT = 60.0 / BPM
STEP = BEAT / 4.0
BAR = BEAT * 4.0
DURATION = 130.0
TOTAL = int(DURATION * SAMPLE_RATE)
OUTPUT = Path("assets/audio/ktd-conscious-aggressive-trap-proof-bed-v1.wav")


def add(audio: np.ndarray, start: int, signal: np.ndarray, gain: float, pan: float = 0.0) -> None:
    end = min(audio.shape[0], start + signal.shape[0])
    if start >= end:
        return
    usable = signal[: end - start] * gain
    left = 1.0 - max(0.0, pan)
    right = 1.0 + min(0.0, pan)
    audio[start:end, 0] += usable * left
    audio[start:end, 1] += usable * right


def tone(freq: float, length: float, level: float = 1.0, bright: bool = False) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    wobble = freq * (1.0 + 0.02 * np.exp(-t * 8.0))
    s = np.sin(2 * np.pi * wobble * t)
    if bright:
        s += 0.18 * np.sin(2 * np.pi * wobble * 2.0 * t)
    env = np.minimum(1.0, t * 90.0) * np.exp(-t * (4.0 if bright else 2.0))
    return (s * env * level).astype(np.float32)


def noise(length: float, seed: int, decay: float) -> np.ndarray:
    n = int(length * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float32) / SAMPLE_RATE
    rng = np.random.default_rng(seed)
    return (rng.normal(0.0, 1.0, n).astype(np.float32) * np.exp(-t * decay)).astype(np.float32)


def section(bar: int) -> str:
    if bar < 4:
        return "intro"
    if bar < 16:
        return "verse"
    if bar < 24:
        return "hook"
    if bar < 36:
        return "verse2"
    if bar < 44:
        return "bridge"
    return "final"


def main() -> None:
    audio = np.zeros((TOTAL, 2), dtype=np.float32)
    root_cycle = [55.0, 65.41, 73.42, 82.41]  # A, C, D, E in the lower register.
    hook_melody = [220.0, 261.63, 293.66, 261.63, 220.0, 196.0, 220.0, 164.81]
    kick_body = tone(54.0, 0.42, 0.92)
    kick_click = tone(1_800.0, 0.06, 0.08, True)
    kick = kick_body + np.pad(kick_click, (0, kick_body.shape[0] - kick_click.shape[0]))
    snare_body = noise(0.22, 71, 28.0) * 0.28
    snare_tone = tone(185.0, 0.20, 0.18)
    snare = snare_body + np.pad(snare_tone, (0, snare_body.shape[0] - snare_tone.shape[0]))
    bars = math.ceil(DURATION / BAR)

    for bar in range(bars):
        mode = section(bar)
        bar_time = bar * BAR
        root = root_cycle[(bar // 2) % len(root_cycle)]
        # Dark chord bed, more open in the bridge.
        chord = tone(root, 2.0, 0.035) + tone(root * 1.1892, 2.0, 0.025) + tone(root * 1.4983, 2.0, 0.022)
        if mode != "bridge":
            add(audio, int(bar_time * SAMPLE_RATE), chord, 1.0, pan=-0.12 if bar % 2 else 0.12)

        if bar in (4, 16, 24, 36, 44):
            sweep = noise(0.55, bar, 4.0) * 0.07 + tone(300.0 + bar * 10, 0.55, 0.04, True)
            add(audio, int(bar_time * SAMPLE_RATE), sweep, 1.0, pan=-0.25 if bar % 2 else 0.25)

        for step in range(16):
            t = bar_time + step * STEP
            start = int(t * SAMPLE_RATE)
            if mode == "intro":
                if step in (0, 8) and bar >= 2:
                    add(audio, start, kick, 0.58)
                continue
            if mode == "bridge":
                if step in (4, 12) and bar % 2 == 0:
                    add(audio, start, snare, 0.38, pan=0.05)
                if step in (0, 8) and bar % 2:
                    add(audio, start, tone(root * 0.5, 0.55, 0.48), 1.0)
                if step in (0, 4, 8, 12):
                    add(audio, start, noise(0.06, bar * 16 + step, 80.0), 0.07, pan=0.3 if step % 8 else -0.3)
                continue

            kick_steps = {0, 5, 7, 8, 11, 14} if mode in ("hook", "final") else {0, 7, 8, 14}
            if step in kick_steps:
                add(audio, start, kick, 0.72 if step in (0, 8) else 0.55)
            if step in (4, 12):
                add(audio, start, snare, 0.78 if mode in ("hook", "final") else 0.66, pan=0.04)
            if step % 2 == 0 or mode == "final":
                hat = noise(0.055, bar * 16 + step, 88.0) * 0.11
                add(audio, start, hat, 0.82, pan=-0.35 if step % 4 else 0.3)
            if mode == "final" and step % 2 == 1:
                add(audio, start, noise(0.035, 1000 + bar * 16 + step, 120.0), 0.065, pan=0.25)
            if step == 10 and mode in ("hook", "final"):
                add(audio, start, noise(0.16, 3000 + bar, 25.0), 0.13, pan=0.2)

            if step in ({0, 5, 8, 12} if mode in ("hook", "final") else {0, 8, 14}):
                glide_root = root * (0.5 if step in (5, 12) else 1.0)
                add(audio, start, tone(glide_root, 0.62, 0.7), 0.78)

        # Melodic hook motif and restrained final reprise.
        if mode == "hook" or (mode == "final" and bar % 2 == 0):
            for note_index, freq in enumerate(hook_melody):
                note_time = bar_time + note_index * (BEAT / 2.0)
                if note_time >= DURATION:
                    break
                add(audio, int(note_time * SAMPLE_RATE), tone(freq, 0.30, 0.12, True), 1.0, pan=-0.2 if note_index % 2 else 0.2)

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
