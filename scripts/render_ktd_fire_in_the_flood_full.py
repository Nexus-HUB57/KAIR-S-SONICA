from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO_SRC = Path('/home/ubuntu/upload/ktd-main-single-fire-in-the-flood-v1-reference-ali.mp3')
AUDIO_LOCAL = ROOT / 'assets/audio/references/ktd-main-single-fire-in-the-flood-v1-reference-ali.mp3'
OUT = ROOT / 'artifacts/video/ktd-fire-in-the-flood-full-v1.mp4'
DURATION = 168
FPS = 24
W, H = 1920, 1080

SCENES = [
    (14, ROOT/'assets/persona/artista-principal-diamante.png', 'cool'),
    (14, ROOT/'assets/persona/ktd-visual-master.png', 'cool'),
    (14, ROOT/'assets/persona/ktd-expression-rooftop.png', 'cool'),
    (14, ROOT/'assets/persona/ktd-expression-street.png', 'wet'),
    (14, ROOT/'assets/persona/ktd-expression-stage.png', 'fire'),
    (14, ROOT/'assets/persona/ktd-expression-studio.png', 'warm'),
    (14, ROOT/'assets/persona/ktd-expression-stage.png', 'fire'),
    (14, ROOT/'assets/persona/ktd-expression-rooftop.png', 'cool'),
    (14, ROOT/'assets/persona/ktd-visual-master.png', 'shadow'),
    (14, ROOT/'assets/persona/ktd-expression-street.png', 'wet'),
    (14, ROOT/'assets/persona/ktd-expression-stage.png', 'fire'),
    (14, ROOT/'assets/persona/artista-principal-diamante.png', 'final'),
]


def run(args: list[str]) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    AUDIO_LOCAL.parent.mkdir(parents=True, exist_ok=True)
    if AUDIO_SRC.exists() and AUDIO_SRC.resolve() != AUDIO_LOCAL.resolve():
        shutil.copy2(AUDIO_SRC, AUDIO_LOCAL)
    if not AUDIO_LOCAL.exists():
        raise FileNotFoundError(f'Faixa não encontrada: {AUDIO_LOCAL}')

    inputs: list[str] = []
    filters: list[str] = []
    for idx, (dur, image, mood) in enumerate(SCENES):
        inputs += ['-loop', '1', '-t', str(dur), '-i', str(image)]
        grade = {
            'cool': 'eq=contrast=1.06:saturation=0.82:brightness=-0.02,colorbalance=bs=.08:gs=.02:rs=-.02',
            'wet': 'eq=contrast=1.10:saturation=0.90:brightness=-0.04,colorbalance=bs=.05:rs=.03',
            'fire': 'eq=contrast=1.12:saturation=1.08:brightness=0.01,colorbalance=rs=.10:gs=.03:bs=-.05',
            'warm': 'eq=contrast=1.06:saturation=0.98:brightness=0.00,colorbalance=rs=.06:gs=.02:bs=-.02',
            'shadow': 'eq=contrast=1.18:saturation=0.72:brightness=-0.08,colorbalance=bs=.05:rs=-.02',
            'final': 'eq=contrast=1.08:saturation=0.92:brightness=-0.01,colorbalance=rs=.04:bs=.02',
        }[mood]
        filters.append(
            f'[{idx}:v]scale={W}:{H}:force_original_aspect_ratio=increase,'
            f'crop={W}:{H},setsar=1,'
            f'{grade},format=yuv420p,fade=t=in:st=0:d=0.7,fade=t=out:st={dur-0.7}:d=0.7[v{idx}]'
        )

    # Concatenate the 12 timed chapters; each chapter already carries in/out fades.
    concat_inputs = ''.join(f'[v{i}]' for i in range(len(SCENES)))
    filters.append(f'{concat_inputs}concat=n={len(SCENES)}:v=1:a=0[vconcat]')
    current = 'vconcat'

    filters.append(
        f'[{current}]drawtext=fontcolor=white:fontsize=58:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:'
        "text='FIRE IN THE FLOOD':x=90:y=850:enable='between(t,1,5)':alpha='if(lt(t,2),t-1,if(gt(t,4),5-t,1))',"
        "drawtext=fontcolor=white:fontsize=28:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
        "text='KHÁIRUS THE DRAGON  /  KTD':x=94:y=920:enable='between(t,2,5)':alpha='if(lt(t,3),t-2,if(gt(t,4),5-t,1))',"
        "drawtext=fontcolor=white:fontsize=52:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "text='KTD  —  FIRE IN THE FLOOD':x=(w-text_w)/2:y=820:enable='between(t,160,167)':alpha='if(lt(t,162),t-160,if(gt(t,166),167-t,1))'[vout]"
    )
    filter_complex = ';'.join(filters)
    args = ['ffmpeg', '-y'] + inputs + ['-i', str(AUDIO_LOCAL), '-filter_complex', filter_complex,
        '-map', '[vout]', '-map', f'{len(SCENES)}:a', '-t', str(DURATION),
        '-af', 'aresample=48000, loudnorm=I=-14:TP=-1.0:LRA=7,afade=t=out:st=167.3:d=0.7',
        '-r', str(FPS), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', str(OUT)]
    run(args)
    print(OUT)


if __name__ == '__main__':
    main()
