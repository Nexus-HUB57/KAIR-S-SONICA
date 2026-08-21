from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/releases/fire-in-the-flood-10s-scene-manifest-v1.json"
QUEUE = ROOT / "data/releases/fire-in-the-flood-10s-generation-queue-v1.json"
LYRICS = ROOT / "docs/ktd-main-single-rework-lyrics.md"
SCRIPT = ROOT / "docs/ktd-fire-in-the-flood-10s-scene-script-v4.md"

LEGACY_LINES = ("Water at the window", "Fire in the chest", "Grandma kept a candle")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    if manifest["status"] != "aligned_to_v4_transcription":
        raise SystemExit("manifest is not aligned_to_v4_transcription")
    if manifest["alignment_review"]["audio_lyrics_match"] is not True:
        raise SystemExit("audio_lyrics_match is not true")
    if len(manifest["scenes"]) != 17:
        raise SystemExit("manifest must contain 17 scenes")
    total = sum(float(scene["duration"]) for scene in manifest["scenes"])
    if abs(total - 168.0) > 1e-9:
        raise SystemExit(f"duration sum is {total}, expected 168.0")
    if queue["status"] != "aligned_to_v4_transcription":
        raise SystemExit("queue is not aligned_to_v4_transcription")
    if not all(scene["status"] == "queued" for scene in queue["scenes"]):
        raise SystemExit("not all queue scenes are queued")
    active_lyrics = "\n".join(scene["lyric"] for scene in manifest["scenes"])
    canonical_text = LYRICS.read_text(encoding="utf-8")
    for legacy in LEGACY_LINES:
        if legacy in active_lyrics:
            raise SystemExit(f"legacy lyric found in active manifest lyric fields: {legacy}")
    if "I hear the lock click" not in active_lyrics or "I hear the clock tick" not in active_lyrics:
        raise SystemExit("v4 opening is missing from manifest lyric fields")
    if "I hear the lock click" not in canonical_text or "I hear the clock tick" not in canonical_text:
        raise SystemExit("v4 opening is missing from canonical lyrics")
    if "instrumental final" not in SCRIPT.read_text(encoding="utf-8").lower():
        raise SystemExit("instrumental tail is missing from the v4 script")
    print("manifest_status=", manifest["status"])
    print("queue_status=", queue["status"])
    print("scenes=", len(manifest["scenes"]))
    print("duration=", total)
    print("opening=", manifest["scenes"][0]["lyric"])
    print("instrumental_tail=", manifest["alignment_review"]["instrumental_tail"])
    print("legacy_lyrics_absent_from_active_lyric_fields=true")


if __name__ == "__main__":
    main()
