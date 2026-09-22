#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path('/home/ubuntu/KAIR-S-SONICA')
STEMS = Path('/tmp/single18_stems/htdemucs/single-18-the-chain-came-home-v2-aggressive-ktd-proof')
OUT = ROOT / 'outputs/single_18/audio'
OUT.mkdir(parents=True, exist_ok=True)
VOCALS = STEMS / 'vocals.wav'
INSTRUMENTAL = STEMS / 'no_vocals.wav'
PROCESSED_VOCAL = Path('/tmp/single18_processed_vocal.wav')
SFX = Path('/tmp/single18_cinematic_impacts.wav')
MIX = OUT / 'single-18-the-chain-came-home-v3-local-remix-master.wav'
MP3 = OUT / 'single-18-the-chain-came-home-v3-local-remix-conference.mp3'
HOOK_WAV = OUT / 'single-18-the-chain-came-home-v3-tiktok-hook-15s.wav'
HOOK_MP3 = OUT / 'single-18-the-chain-came-home-v3-tiktok-hook-15s.mp3'

def run(args):
    subprocess.run(args, check=True)

# Front-of-mix KTD treatment: presence, aggressive compression, controlled saturation and short room reflection.
run([
    'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(VOCALS),
    '-af', 'highpass=f=85,acompressor=threshold=-23dB:ratio=6:attack=2:release=70:makeup=6,equalizer=f=1700:t=q:w=1.0:g=4,equalizer=f=3600:t=q:w=1.0:g=3,acrusher=bits=15:mix=0.16,aecho=0.8:0.86:48:0.10,alimiter=limit=0.95',
    '-c:a', 'pcm_s24le', str(PROCESSED_VOCAL)
])

# Short, stylized cinematic impact: bright crack plus low transient, deliberately non-graphic.
run([
    'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
    '-f', 'lavfi', '-i', 'anoisesrc=color=white:amplitude=0.8:duration=0.22:sample_rate=44100',
    '-f', 'lavfi', '-i', 'sine=frequency=78:duration=0.32:sample_rate=44100',
    '-filter_complex',
    '[0:a]highpass=f=900,lowpass=f=8500,afade=t=out:st=0.015:d=0.205,volume=0.62[n];[1:a]afade=t=out:st=0.015:d=0.305,volume=0.48[b];[n][b]amix=inputs=2:duration=longest,alimiter=limit=0.95',
    '-ac', '2', '-ar', '44100', '-c:a', 'pcm_s24le', str(SFX)
])

# Mix original accompaniment with treated KTD vocal. Place two impacts in the attack passage.
run([
    'ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
    '-i', str(INSTRUMENTAL), '-i', str(PROCESSED_VOCAL), '-i', str(SFX), '-i', str(SFX),
    '-filter_complex',
    '[0:a]volume=0.94[bed];[1:a]volume=1.22[v];[2:a]adelay=56000|56000,volume=0.92[hit1];[3:a]adelay=58500|58500,volume=0.86[hit2];[bed][v][hit1][hit2]amix=inputs=4:duration=first:dropout_transition=0,alimiter=limit=0.95:level_in=1.0',
    '-ar', '44100', '-ac', '2', '-c:a', 'pcm_s24le', str(MIX)
])

# Conference MP3 and a 15-second hook cut centered on the already recorded chorus.
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(MIX), '-c:a', 'libmp3lame', '-b:a', '320k', '-ar', '44100', '-ac', '2', '-metadata', 'artist=KTD', '-metadata', 'title=The Chain Came Home - Local Remix', '-metadata', 'comment=Local vocal mix refinement; original performance preserved', str(MP3)])
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-ss', '26.7', '-t', '15', '-i', str(MIX), '-af', 'afade=t=in:st=0:d=0.08,afade=t=out:st=14.65:d=0.35,loudnorm=I=-14:TP=-1.2:LRA=7', '-ar', '44100', '-ac', '2', '-c:a', 'pcm_s24le', str(HOOK_WAV)])
run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(HOOK_WAV), '-c:a', 'libmp3lame', '-b:a', '320k', '-ar', '44100', '-ac', '2', '-metadata', 'artist=KTD', '-metadata', 'title=The Chain Came Home - TikTok Hook Edit', '-metadata', 'comment=15-second hook cut from original chorus; no new voice generated', str(HOOK_MP3)])
print(MIX)
print(MP3)
print(HOOK_WAV)
print(HOOK_MP3)
