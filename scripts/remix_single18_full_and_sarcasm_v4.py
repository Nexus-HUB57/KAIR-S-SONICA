#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path('/home/ubuntu/KAIR-S-SONICA')
OUT = ROOT / 'outputs/single_18/audio'
OUT.mkdir(parents=True, exist_ok=True)
STEMS = Path('/tmp/single18_stems/htdemucs/single-18-the-chain-came-home-v2-aggressive-ktd-proof')
VOCALS = STEMS / 'vocals.wav'
BED = STEMS / 'no_vocals.wav'
PV = Path('/tmp/single18_v4_processed_vocal.wav')
SFX = Path('/tmp/single18_v4_sharp_impact.wav')
MIX = OUT / 'single-18-the-chain-came-home-v4-full-local-remix.wav'
MP3 = OUT / 'single-18-the-chain-came-home-v4-full-local-remix.mp3'
SAR = OUT / 'single-18-the-chain-came-home-v4-tiktok-sarcasm-edit.wav'
SAR_MP3 = OUT / 'single-18-the-chain-came-home-v4-tiktok-sarcasm-edit.mp3'

def run(args):
    subprocess.run(args, check=True)

run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(VOCALS),'-af','highpass=f=85,acompressor=threshold=-22dB:ratio=10:attack=1:release=45:makeup=6,equalizer=f=1600:t=q:w=0.9:g=4,equalizer=f=3300:t=q:w=0.9:g=3,acrusher=bits=15:mix=0.18,aecho=0.8:0.86:48:0.10,volume=2.2dB,alimiter=limit=0.96','-c:a','pcm_s24le',str(PV)])

run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','lavfi','-i','anoisesrc=color=white:amplitude=0.9:duration=0.24:sample_rate=44100','-f','lavfi','-i','sine=frequency=72:duration=0.34:sample_rate=44100','-filter_complex','[0:a]highpass=f=1100,lowpass=f=9500, equalizer=f=3000:t=q:w=1.2:g=4,afade=t=out:st=0.012:d=0.228,volume=0.78[n];[1:a]afade=t=out:st=0.012:d=0.328,volume=0.52[b];[n][b]amix=inputs=2:duration=longest,alimiter=limit=0.96','-ac','2','-ar','44100','-c:a','pcm_s24le',str(SFX)])

# Full version: the original accompaniment is retained; the vocal treatment matches the approved hook v4.
# Sharp impacts are placed in the first attack verse while preserving the complete song duration.
run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(BED),'-i',str(PV),'-i',str(SFX),'-i',str(SFX),'-filter_complex','[0:a]volume=0.94[bed];[1:a]volume=1.22[v];[2:a]adelay=56000|56000,volume=1.08[hit1];[3:a]adelay=58500|58500,volume=1.02[hit2];[bed][v][hit1][hit2]amix=inputs=4:duration=first:dropout_transition=0,alimiter=limit=0.95:level_in=1.0','-ar','44100','-ac','2','-c:a','pcm_s24le',str(MIX)])
run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(MIX),'-c:a','libmp3lame','-b:a','320k','-ar','44100','-ac','2','-metadata','artist=KTD','-metadata','title=The Chain Came Home - Full Local Remix v4','-metadata','comment=Approved hook treatment applied to full version; sharper attack effects','-y',str(MP3)])

# Sarcasm edit: final lines from “The tree did not chase him” through “my breath”.
run(['ffmpeg','-y','-hide_banner','-loglevel','error','-ss','138.1','-t','11.6','-i',str(MIX),'-af','afade=t=in:st=0:d=0.10,afade=t=out:st=11.15:d=0.45,loudnorm=I=-12:TP=-1.0:LRA=5','-ar','44100','-ac','2','-c:a','pcm_s24le',str(SAR)])
run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(SAR),'-c:a','libmp3lame','-b:a','320k','-ar','44100','-ac','2','-metadata','artist=KTD','-metadata','title=The Chain Came Home - TikTok Sarcasm Edit','-metadata','comment=Final tree and motorcycle consequence verse; original vocal performance preserved','-y',str(SAR_MP3)])
print(MIX)
print(MP3)
print(SAR)
print(SAR_MP3)
