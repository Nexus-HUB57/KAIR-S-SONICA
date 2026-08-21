#!/usr/bin/env python3
"""Localiza o trecho de 10 s de maior energia vocal/musical do áudio de UNLEASH THE DRAGON.

Calcula RMS por janela e escolhe a janela de 10 s com maior energia média,
excluindo os primeiros segundos de intro (reserva para buildup no clipe) e
garantindo que a janela termine antes do fim do arquivo.
"""
import sys

import numpy as np
import scipy.io.wavfile as wf

path = sys.argv[1] if len(sys.argv) > 1 else \
    "assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav"
window = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
skip = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0  # pula a intro

sr, data = wf.read(path)
if data.ndim > 1:
    data = data.mean(axis=1)
data = data.astype(np.float64) / (2**15 if data.dtype.kind == "i" else np.abs(data).max())
n = len(data)
dur = n / sr
print(f"Arquivo: {path}")
print(f"Duração: {dur:.3f} s | SR: {sr}")

hop = 0.5  # analisa a cada 0,5 s
rms = []
times = []
frame = int(0.2 * sr)
for i in range(0, n - frame, int(hop * sr)):
    seg = data[i:i + frame]
    rms.append(float(np.sqrt(np.mean(seg**2))))
    times.append(i / sr)
rms = np.array(rms)
times = np.array(times)

# janela de `window` segundos com maior RMS médio
best_start, best_rms = 0.0, -1.0
for t in times:
    if t < skip or t + window > dur:
        continue
    seg = rms[(times >= t) & (times < t + window)]
    if seg.mean() > best_rms:
        best_rms, best_start = float(seg.mean()), t

print(f"Janela de {window:.1f} s com maior energia: {best_start:.2f} s -> {best_start + window:.2f} s (RMS médio {best_rms:.4f})")

# top 5 alternativas para contexto
alts = []
for t in times:
    if t < skip or t + window > dur:
        continue
    seg = rms[(times >= t) & (times < t + window)]
    alts.append((float(seg.mean()), t))
alts.sort(reverse=True)
print("Top 5 janelas alternativas:")
for r, t in alts[:5]:
    print(f"  {t:6.2f} s -> {t + window:6.2f} s | RMS {r:.4f}")
