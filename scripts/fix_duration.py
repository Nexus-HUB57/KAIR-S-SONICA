#!/usr/bin/env python3
"""Reenquadra um teaser para durar exatamente a duração alvo.

O ffmpeg com `-shortest` pode encerrar o vídeo ligeiramente antes dos 8 s se o
áudio tiver uma granularidade menor que o último quadro. Este script reencode o
trailer com `-t <duracao>` no lugar de `-shortest`, garantindo o encerramento
exato sem alterar quadros.
"""
import subprocess
import sys

src = sys.argv[1]
out = sys.argv[2]
duration = sys.argv[3] if len(sys.argv) > 3 else "8.000"

cmd = [
    "ffmpeg", "-y", "-i", src, "-t", duration,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out,
]
subprocess.run(cmd, check=True)
print("Reenquadramento concluído:", out)
