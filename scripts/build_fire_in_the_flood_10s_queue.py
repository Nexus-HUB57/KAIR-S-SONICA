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


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    queue = {
        "project": manifest["project"],
        "version": "generation-queue-v1",
        "duration_seconds": manifest["duration_seconds"],
        "model": "gemini-omni-flash-preview",
        "aspect_ratio": "landscape",
        "resolution": "720p",
        "generate_audio": False,
        "master_audio": manifest["master_audio"],
        "reference_rule": "Use the listed 16:9 keyframe when available; otherwise use the canonical KTD visual master after preparing a 16:9 keyframe.",
        "scenes": [],
    }
    for scene in manifest["scenes"]:
        action = scene["action"]
        prompt = (
            f"Create a single uninterrupted {scene['duration']}-second cinematic live-action shot for {scene['id']} of Fire in the Flood. "
            f"{GLOBAL_ANCHOR} {STYLE_ANCHOR} Scene action: {action} "
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
            "status": "queued",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
