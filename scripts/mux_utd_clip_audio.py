#!/usr/bin/env python3
"""Muxa um trecho do áudio de UNLEASH THE DRAGON com um clipe de vídeo real.

Extrai a janela [seg_start, seg_start+dur] do WAV, aplica fade-out final,
normaliza o vídeo para 720x1280 @24fps com o áudio AAC 192k e escreve o MP4.

Uso:
    python3 scripts/mux_utd_clip_audio.py <video_in.mp4> <out.mp4> \
        [seg_start=28.5] [dur=10.0] [fade_out=0.5]
"""
import subprocess
import sys

AUDIO = "assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav"


def main():
    video_in = sys.argv[1]
    out = sys.argv[2]
    seg_start = float(sys.argv[3]) if len(sys.argv) > 3 else 28.5
    dur = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0
    fade_out = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5

    fade_start = max(0.0, dur - fade_out)
    af = (
        f"[0:a]atrim=start={seg_start}:end={seg_start + dur},"
        f"asetpts=PTS-STARTPTS,"
        f"afade=t=in:st=0:d=0.3,"
        f"afade=t=out:st={fade_start:.3f}:d={fade_out}["
        f"fa];[1:v]fps=24,scale=720:1280:force_original_aspect_ratio=decrease,"
        f"pad=720:1280:(ow-iw)/2:(oh-ih)/2[v]"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", AUDIO,
        "-i", video_in,
        "-map", "[v]", "-map", "[fa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.3f}",
        out,
        "-filter_complex_script", "/dev/null",
    ]
    # ffmpeg aceita filter_complex com argumentos posicionais via -filter_complex
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", AUDIO,
        "-i", video_in,
        "-filter_complex", af,
        "-map", "[v]", "-map", "[fa]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.3f}",
        out,
    ]
    subprocess.run(cmd, check=True)
    print(f"Muxado: {out} (áudio {seg_start:.3f}–{seg_start + dur:.3f} s, fade-out {fade_out} s)")


if __name__ == "__main__":
    main()
