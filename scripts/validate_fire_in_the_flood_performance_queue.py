#!/usr/bin/env python3
"""Validate the performance contract of the Fire in the Flood generation queue."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/releases/fire-in-the-flood-10s-generation-queue-v1.json"
MANIFEST = ROOT / "data/releases/fire-in-the-flood-10s-scene-manifest-v1.json"


def main() -> None:
    payload = json.loads(QUEUE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    lyrics_by_id = {scene["id"]: scene["lyric"] for scene in manifest["scenes"]}
    assert payload["version"] == "performance-generation-queue-v1"
    assert payload["performance_required"] is True
    assert payload["identity_fidelity_gate"] == "docs/ktd-fire-in-the-flood-identity-fidelity-gate-v1.md"
    contract = payload["performance_contract"]
    for key in (
        "must_sing_on_camera",
        "phoneme_level_lip_sync",
        "visible_breath_and_consonant_attacks",
        "emotion_and_gesture_driven_by_lyric",
        "silent_mood_performance_rejected",
    ):
        assert contract[key] is True, key

    scenes = payload["scenes"]
    assert len(scenes) == 17
    vocal = []
    instrumental = []
    for scene in scenes:
        prompt = scene["prompt"]
        lyric = lyrics_by_id[scene["id"]].strip().lower()
        if lyric.startswith("instrumental"):
            instrumental.append(scene["id"])
            assert "Instrumental block: no new vocal text" in prompt, scene["id"]
            assert "must not invent vocals" in prompt, scene["id"]
            assert "Exact lyric to sing on camera" not in prompt, scene["id"]
        else:
            vocal.append(scene["id"])
            assert "must actively perform and sing" in prompt, scene["id"]
            assert "phoneme-level lip-sync" in prompt, scene["id"]
            assert "visible breath" in prompt or "breath preparation" in prompt, scene["id"]
            assert "Exact lyric to sing on camera" in prompt, scene["id"]
            assert scene["duration"] in (8.0, 10.0)
            assert lyrics_by_id[scene["id"]].strip() in prompt

    assert vocal == [f"S{i:02d}" for i in range(1, 15)]
    assert instrumental == ["S15", "S16", "S17"]
    print(f"validated scenes={len(scenes)}")
    print(f"vocal_performance_scenes={','.join(vocal)}")
    print(f"instrumental_scenes={','.join(instrumental)}")
    print("identity_fidelity_gate=present")
    print("status=performance_contract_valid")


if __name__ == "__main__":
    main()
