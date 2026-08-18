from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "ktd" / "asset-inventory.json"
DIRECTORIES = [ROOT / "assets" / "persona", ROOT / "assets" / "audio"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_metadata(path: Path) -> dict[str, object]:
    try:
        with Image.open(path) as image:
            return {"width": image.width, "height": image.height, "format": image.format}
    except (OSError, UnidentifiedImageError):
        return {}


def audio_metadata(path: Path) -> dict[str, object]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-show_entries",
        "stream=codec_name,sample_rate,channels",
        "-of",
        "json",
        str(path),
    ]
    try:
        payload = json.loads(subprocess.check_output(command, text=True))
        streams = payload.get("streams", [])
        stream = streams[0] if streams else {}
        format_data = payload.get("format", {})
        result: dict[str, object] = {
            "codec": stream.get("codec_name"),
            "sample_rate": int(stream["sample_rate"]) if stream.get("sample_rate") else None,
            "channels": int(stream["channels"]) if stream.get("channels") else None,
        }
        if format_data.get("duration"):
            result["duration_seconds"] = round(float(format_data["duration"]), 6)
        return result
    except (OSError, subprocess.SubprocessError, ValueError, json.JSONDecodeError, KeyError, TypeError):
        return {}


def classify(path: Path) -> str:
    name = path.name.lower()
    approved_release_markers = (
        "ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3",
    )
    rejected_release_markers = (
        "ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1",
        "ktd-main-single-fire-in-the-flood-v1-rebeat-v1",
    )
    if any(marker in name for marker in approved_release_markers):
        return "approved_audio_release"
    if (
        any(marker in name for marker in rejected_release_markers)
        or "rejected" in name
        or "rough" in name
        or "old-school-boom-bap-beat-v1" in name
    ):
        return "rejected_or_audit"
    if "visual-master" in name or "physical-turnaround" in name or "expression-" in name or "artista-principal-diamante" in name:
        return "official_visual_reference"
    if "kairos-rapid-rap-flow-demo-en-v3" in name:
        return "official_vocal_reference"
    if "reference-aligned-groove-v1" in name or "vocal-isolated-stem-v1" in name:
        return "candidate_audio_source"
    if "releases" in path.parts:
        return "candidate_audio_release"
    if "trials" in path.parts or "bed" in name:
        return "candidate_audio_source"
    return "historical_or_supporting"


def main() -> None:
    records: list[dict[str, object]] = []
    for directory in DIRECTORIES:
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            record: dict[str, object] = {
                "path": relative,
                "category": classify(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                record.update(image_metadata(path))
            elif path.suffix.lower() in {".wav", ".mp3", ".flac", ".m4a"}:
                record.update(audio_metadata(path))
            records.append(record)
    output = {
        "schema_version": "1.0.0",
        "generated_by": "scripts/build_ktd_asset_inventory.py",
        "persona": "kairos.khairus_the_dragon",
        "official_voice_reference": "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3",
        "records": records,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
