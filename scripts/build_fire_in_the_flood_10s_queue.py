from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/releases/fire-in-the-flood-10s-scene-manifest-v1.json"
OUT = ROOT / "data/releases/fire-in-the-flood-10s-generation-queue-v1.json"

GLOBAL_ANCHOR = (
    "The same original fictional KTD: Black adult man, shaved head, long full beard, compact athletic build, "
    "left honey-amber eye and right pale clear-blue eye, restrained gold eyebrow slits, wet skin, direct intense gaze. "
    "Preserve the immutable tattoo map exactly: seven diamond-tipped claw marks arranged vertically down the upper chest "
    "from the sternum, with a symmetrical dragon-scale spine column running down the center of the abdomen ending in a dragon head at the navel, "
    "samurai armor on the left arm and shoulder, koi on the right arm, cherry blossoms integrated, per the immutable tattoo map of assets/persona/ktd-visual-master.png."
)

STYLE_ANCHOR = (
    "Cinematic live-action editorial rap music video, high-contrast chiaroscuro, charcoal black, cold steel blue, restrained amber and gold, "
    "real rain, moving water, vapor, cloth and practical light, realistic physical texture, no text, no logos, no watermark, no celebrity likeness. "
    "Every second must contain temporal movement and a readable action. This must not be a still image with zoom, slideshow, frozen portrait, face morph or montage."
)

VOCAL_PERFORMANCE_ANCHOR = (
    "KTD must actively perform and sing the exact lyric assigned to this scene into camera or toward a practical microphone. "
    "Make the mouth visibly form the correct phonemes and syllable timing of the supplied lyric, with clear jaw, lips and tongue motion; this is required phoneme-level lip-sync, not a closed-mouth mood performance. "
    "Show audible-looking breath preparation, consonant attacks, vowel sustain, throat and chest movement, eye focus, facial intention and hand gestures driven by the words. "
    "Keep the emotional arc specific to KTD: pressure held in the body, direct truth, controlled anger, resilience and release. "
    "Do not invent a different lyric, mumble, silently pose, stare with closed lips, or substitute walking for singing. Generate no audio; the original master v4 will be muxed later."
)

INSTRUMENTAL_PERFORMANCE_ANCHOR = (
    "This block is instrumental: KTD must not invent vocals or mouth unrelated words. Keep him physically present and emotionally expressive through breath, gaze, posture, hands and environment interaction. "
    "Use live action, real movement and a controlled release of the vocal arc without a silent frozen pose. Generate no audio; the original master v4 will be muxed later."
)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    queue = {
        "project": manifest["project"],
        "version": "performance-generation-queue-v1",
        "status": manifest.get("status", "queued"),
            "audio_alignment": manifest.get("alignment_review"),
            "performance_required": True,
            "performance_contract": {
                "must_sing_on_camera": True,
                "phoneme_level_lip_sync": True,
                "visible_breath_and_consonant_attacks": True,
                "emotion_and_gesture_driven_by_lyric": True,
                "silent_mood_performance_rejected": True
            },
            "duration_seconds": manifest["duration_seconds"],
        "model": "gemini-omni-flash-preview",
        "aspect_ratio": "portrait",
        "resolution": "720p",
        "generate_audio": False,
        "master_audio": manifest["master_audio"],
        "reference_rule": "Use the listed 9:16 performance keyframe when available; otherwise prepare a 9:16 KTD performance keyframe before video generation.",
        "scenes": [],
    }
    for scene in manifest["scenes"]:
        action = scene["action"]
        lyric = scene.get("lyric", "")
        is_instrumental = lyric.strip().lower().startswith("instrumental")
        performance_anchor = INSTRUMENTAL_PERFORMANCE_ANCHOR if is_instrumental else VOCAL_PERFORMANCE_ANCHOR
        lyric_instruction = (
            f"Instrumental block: no new vocal text; do not invent singing. "
            if is_instrumental
            else f"Exact lyric to sing on camera in this shot: {lyric} "
        )
        prompt = (
            f"Create a single uninterrupted {scene['duration']}-second cinematic live-action shot for {scene['id']} of Fire in the Flood. "
            f"{GLOBAL_ANCHOR} {STYLE_ANCHOR} {performance_anchor} "
            f"{lyric_instruction}"
            f"Scene action: {action} "
            "Use a continuous camera move appropriate to the action, preserve screen direction and physical causality, and end with a clear visual handoff to the next scene. "
            "No extra foreground characters, no invented tattoos, no fantasy armor, no text, no logos, no watermark."
        )
        queue["scenes"].append({
            "id": scene["id"],
            "start": scene["start"],
            "duration": scene["duration"],
            "section": scene["section"],
            "keyframe": scene["keyframe"],
            "output": scene["output"],
            "prompt": prompt,
            "status": "blocked_audio_alignment" if manifest.get("status") == "blocked_pending_authoritative_vocal_master" else "queued",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
