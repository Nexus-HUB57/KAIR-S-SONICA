from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kairos_core.config import Settings
from kairos_core.studio_master.auto_review import (
    CANONICAL_ARTIST_ID,
    CANONICAL_IDENTITY_PROFILE,
    CANONICAL_PHYSICAL_PROFILE,
    CANONICAL_TATTOO_MAP,
    CANONICAL_VOICE_REFERENCE,
    AutoReviewEngine,
)

SINGLE1_TITLE = "UNLEASH THE DRAGON"
SINGLE1_DECLARATION = Path("docs/ktd-debut-single-lyrics.md")
SINGLE1_CATALOG = Path("docs/singles/lyrics-catalog-bilingual.md")
SINGLE1_APPROVED_VIDEO = Path(
    "assets/video/aprovados/unleash-the-dragon-realgclip-01-dressing-room-10s-with-audio.mp4"
)
SINGLE1_REFERENCE_BPM = 102
SINGLE1_REFERENCE_KEY = "Fá menor"
SINGLE1_MIN_DURATION_SECONDS = 8.0
SINGLE1_MAX_DURATION_SECONDS = 10.0
SINGLE1_EXPECTED_WIDTH = 720
SINGLE1_EXPECTED_HEIGHT = 1280
SINGLE1_EXPECTED_FPS = 24


@dataclass(frozen=True, slots=True)
class Single1Declaration:
    title: str
    bpm: int
    key: str
    voice_reference: str
    source_path: str
    catalog_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "bpm": self.bpm,
            "key": self.key,
            "voice_reference": self.voice_reference,
            "source_path": self.source_path,
            "catalog_path": self.catalog_path,
        }


@dataclass(frozen=True, slots=True)
class CpuSimulationResult:
    declaration: dict[str, Any]
    asset: dict[str, Any]
    technical_gate_passed: bool
    technical_findings: tuple[str, ...]
    preflight_auto_repair_false: dict[str, Any]
    preflight_auto_repair_true: dict[str, Any]
    backend: dict[str, Any]
    operations: tuple[str, ...]
    overall_decision: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "simulation": "CPU_METADATA_ONLY",
            "declaration": self.declaration,
            "asset": self.asset,
            "technical_gate_passed": self.technical_gate_passed,
            "technical_findings": list(self.technical_findings),
            "preflight_auto_repair_false": self.preflight_auto_repair_false,
            "preflight_auto_repair_true": self.preflight_auto_repair_true,
            "backend": self.backend,
            "operations": list(self.operations),
            "overall_decision": self.overall_decision,
        }


def _read_required(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"Declaração canônica não encontrada: {path}")
    return path.read_text(encoding="utf-8")


def load_single1_declaration(repo_root: Path) -> Single1Declaration:
    root = repo_root.expanduser().resolve()
    declaration_path = root / SINGLE1_DECLARATION
    catalog_path = root / SINGLE1_CATALOG
    declaration_text = _read_required(declaration_path)
    catalog_text = _read_required(catalog_path)

    bpm_match = re.search(r"BPM de referência\s*\|\s*(\d+)", declaration_text, re.IGNORECASE)
    key_match = re.search(
        r"Tonalidade de referência\s*\|\s*([^|\n]+)", declaration_text, re.IGNORECASE
    )
    voice_match = re.search(
        r"Referência vocal\s*\|\s*`([^`]+)`", declaration_text, re.IGNORECASE
    )
    title_match = re.search(
        r"\|\s*1\s*\|\s*\*?Unleash the Dragon\*?\s*\|",
        catalog_text,
        re.IGNORECASE,
    )
    if not bpm_match or not key_match or not voice_match or not title_match:
        raise ValueError("A declaração canônica do Single 1 está incompleta ou inconsistente")

    declaration = Single1Declaration(
        title=SINGLE1_TITLE,
        bpm=int(bpm_match.group(1)),
        key=key_match.group(1).strip(),
        voice_reference=voice_match.group(1).strip(),
        source_path=declaration_path.relative_to(root).as_posix(),
        catalog_path=catalog_path.relative_to(root).as_posix(),
    )
    if declaration.bpm != SINGLE1_REFERENCE_BPM or declaration.key != SINGLE1_REFERENCE_KEY:
        raise ValueError("BPM ou tonalidade do Single 1 divergem da referência aprovada")
    if declaration.voice_reference != CANONICAL_VOICE_REFERENCE:
        raise ValueError("A referência vocal do Single 1 diverge do cânone imutável")
    return declaration


def _fps_value(raw: str | None) -> float | None:
    if not raw:
        return None
    try:
        numerator, denominator = raw.split("/", 1)
        denominator_value = float(denominator)
        if denominator_value == 0:
            return None
        return float(numerator) / denominator_value
    except (TypeError, ValueError):
        return None


def probe_media(path: Path, ffprobe_bin: str = "ffprobe") -> dict[str, Any]:
    file_path = path.expanduser().resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"Asset do Single 1 não encontrado: {file_path}")
    command = [
        ffprobe_bin,
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate",
        "-of",
        "json",
        str(file_path),
    ]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"Não foi possível executar ffprobe para {file_path}") from exc
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "sem saída do ffprobe")[-2_000:]
        raise RuntimeError(f"ffprobe rejeitou o asset: {detail}")
    try:
        raw = json.loads(completed.stdout or "{}")
        streams = raw.get("streams", [])
        duration = float(raw.get("format", {}).get("duration", 0))
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise RuntimeError("Saída inválida do ffprobe para o asset do Single 1") from exc
    return {
        "path": str(file_path),
        "sha256": hashlib.sha256(file_path.read_bytes()).hexdigest(),
        "byte_size": file_path.stat().st_size,
        "duration_seconds": round(duration, 3),
        "streams": streams if isinstance(streams, list) else [],
    }


def _source_manifest(repo_root: Path, video_path: Path, asset: dict[str, Any]) -> dict[str, Any]:
    root = repo_root.expanduser().resolve()
    absolute = video_path.expanduser().resolve()
    try:
        relative = absolute.relative_to(root).as_posix()
    except ValueError:
        relative = str(absolute)
    return {
        "kind": "approved_reference_video",
        "path": relative,
        "sha256": asset["sha256"],
        "status": "APPROVED_REFERENCE",
        "license": "KTD-approved-repository-asset",
        "consent": "documented-in-repository",
        "identity_reference": CANONICAL_IDENTITY_PROFILE,
        "voice_reference": CANONICAL_VOICE_REFERENCE,
    }


def build_single1_payload(
    repo_root: Path,
    video_path: Path,
    asset: dict[str, Any],
    declaration: Single1Declaration,
    *,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "artist_id": CANONICAL_ARTIST_ID,
        "single_title": declaration.title,
        "bpm": declaration.bpm,
        "key": declaration.key,
        "physical_profile": CANONICAL_PHYSICAL_PROFILE,
        "tattoo_map": CANONICAL_TATTOO_MAP,
        "identity_profile": CANONICAL_IDENTITY_PROFILE,
        "identity_lock": "immutable",
        "tattoo_continuity": "exact-canonical-map",
        "voice_reference": declaration.voice_reference,
        "voice_lock": "immutable-canonical-reference",
        "vocal_profile": "medium-low-front-clear-controlled-aggression",
        "performance_profile": "syncopated-double-time-half-time",
        "prompt": (
            "Create one uninterrupted 10-second vertical 9:16 photorealistic live-action "
            "music-video take for UNLEASH THE DRAGON. Kháirus performs a physical action "
            "while the camera tracks continuously and the environment reacts in real time. "
            "No stills, no static image, no image overlay, no slideshow, and no pan/zoom over photo."
        ),
        "live_action_policy": "live-action-only-no-static-no-overlay",
        "video_policy": "live-action-only-no-static-no-overlay",
        "static_image_only": False,
        "image_overlay": False,
        "continuous_motion_required": True,
        "camera_motion": "continuous-motivated-tracking",
        "frame_review_required": True,
        "aspect_ratio": "9:16",
        "width": SINGLE1_EXPECTED_WIDTH,
        "height": SINGLE1_EXPECTED_HEIGHT,
        "fps": SINGLE1_EXPECTED_FPS,
        "duration_seconds": asset["duration_seconds"],
        "source_manifest": _source_manifest(repo_root, video_path, asset),
        "simulation_mode": "CPU_METADATA_ONLY",
        "render_request": False,
    }
    if overrides:
        payload.update(overrides)
    return payload


def validate_technical_metadata(asset: dict[str, Any], payload: dict[str, Any]) -> tuple[bool, tuple[str, ...]]:
    findings: list[str] = []
    duration = float(asset.get("duration_seconds") or 0)
    if not SINGLE1_MIN_DURATION_SECONDS <= duration <= SINGLE1_MAX_DURATION_SECONDS:
        findings.append("Duração do take aprovado deve estar entre 8 e 10 segundos")
    video_streams = [
        stream for stream in asset.get("streams", []) if stream.get("codec_type") == "video"
    ]
    audio_streams = [
        stream for stream in asset.get("streams", []) if stream.get("codec_type") == "audio"
    ]
    if not video_streams:
        findings.append("Asset sem stream de vídeo")
    else:
        stream = video_streams[0]
        if stream.get("width") != SINGLE1_EXPECTED_WIDTH or stream.get("height") != SINGLE1_EXPECTED_HEIGHT:
            findings.append("Formato deve ser vertical 720x1280")
        fps = _fps_value(stream.get("avg_frame_rate") or stream.get("r_frame_rate"))
        if fps is None or abs(fps - SINGLE1_EXPECTED_FPS) > 0.01:
            findings.append("Taxa de quadros deve ser 24 fps")
    if not audio_streams:
        findings.append("Asset aprovado precisa conter referência de áudio para o handoff")
    if payload.get("voice_reference") != CANONICAL_VOICE_REFERENCE:
        findings.append("referência vocal divergente do cânone imutável")
    if payload.get("aspect_ratio") != "9:16":
        findings.append("aspect_ratio divergente de 9:16")
    if payload.get("fps") != SINGLE1_EXPECTED_FPS:
        findings.append("fps declarado divergente de 24")
    manifest = payload.get("source_manifest")
    required_manifest = {"path", "sha256", "status", "license", "consent", "identity_reference"}
    if not isinstance(manifest, dict) or not required_manifest.issubset(manifest):
        findings.append("source_manifest incompleto")
    if payload.get("live_action_policy") != "live-action-only-no-static-no-overlay":
        findings.append("política live-action não está explicitamente fixada")
    if payload.get("static_image_only") is True or payload.get("image_overlay") is True:
        findings.append("pedido contém still ou overlay proibido")
    if payload.get("render_request") is not False:
        findings.append("simulação CPU não pode ser tratada como pedido de renderização")
    return not findings, tuple(findings)


def backend_state(settings: Settings) -> dict[str, Any]:
    torch_available = importlib.util.find_spec("torch") is not None
    diffusers_available = importlib.util.find_spec("diffusers") is not None
    cuda_available = False
    if torch_available and settings.skyreels_device.startswith("cuda"):
        try:
            torch = __import__("torch")
            cuda_available = bool(torch.cuda.is_available())
        except (ImportError, AttributeError, RuntimeError):
            cuda_available = False
    elif torch_available:
        cuda_available = True
    model = settings.skyreels_native_model_id
    model_path = Path(model).expanduser() if model else None
    checkpoint_ready = bool(
        model_path
        and model_path.is_dir()
        and all((model_path / item).is_file() for item in ("model_index.json", "vae/config.json", "transformer/config.json"))
    )
    local_ready = bool(
        settings.enable_skyreels
        and settings.skyreels_native_api
        and torch_available
        and diffusers_available
        and cuda_available
        and checkpoint_ready
    )
    return {
        "local_gpu": "READY" if local_ready else "BLOCKED",
        "local_gpu_reason": (
            "CUDA runtime, PyTorch, Diffusers e checkpoint prontos"
            if local_ready
            else "GPU local não provisionada; simulação não habilita renderização"
        ),
        "skyreels_enabled": settings.enable_skyreels,
        "native_api_enabled": settings.skyreels_native_api,
        "torch_available": torch_available,
        "diffusers_available": diffusers_available,
        "cuda_available": cuda_available,
        "checkpoint_ready": checkpoint_ready,
        "render_called": False,
    }


def simulate_single1_cpu(
    settings: Settings,
    repo_root: Path,
    video_path: Path,
    *,
    overrides: dict[str, Any] | None = None,
    probe: Callable[[Path, str], dict[str, Any]] = probe_media,
) -> CpuSimulationResult:
    root = repo_root.expanduser().resolve()
    asset_path = video_path.expanduser().resolve()
    declaration = load_single1_declaration(root)
    asset = probe(asset_path, settings.ffprobe_bin)
    payload = build_single1_payload(root, asset_path, asset, declaration, overrides=overrides)
    technical_passed, technical_findings = validate_technical_metadata(asset, payload)

    engine = AutoReviewEngine(settings)
    review_without_repair = engine.review(
        "multimedia", dict(payload), auto_repair=False, persist=False
    )
    review_with_repair = engine.review(
        "multimedia", dict(payload), auto_repair=True, persist=False
    )
    overall = (
        "READY_FOR_APPROVAL"
        if technical_passed
        and review_without_repair.decision == "READY_FOR_APPROVAL"
        and review_with_repair.decision == "READY_FOR_APPROVAL"
        else "REJECTED"
    )
    return CpuSimulationResult(
        declaration=declaration.to_dict(),
        asset=asset,
        technical_gate_passed=technical_passed,
        technical_findings=technical_findings,
        preflight_auto_repair_false=review_without_repair.model_dump(mode="json"),
        preflight_auto_repair_true=review_with_repair.model_dump(mode="json"),
        backend=backend_state(settings),
        operations=(
            "read canonical Single 1 declaration",
            "ffprobe approved reference asset",
            "sha256 approved reference asset",
            "POST /v1/studio-master/preflight (auto_repair=false) when explicitly requested",
            "POST /v1/studio-master/preflight (auto_repair=true) when explicitly requested",
            "no POST /v1/video/generate",
            "no render, upload, cloud call, or publication",
        ),
        overall_decision=overall,
    )


def summarize_review(result: dict[str, Any]) -> dict[str, Any]:
    """Keep reports useful without exposing full duplicated payloads."""
    review = result.get("preflight_auto_repair_false") or {}
    return {
        "overall_decision": result.get("overall_decision"),
        "technical_gate_passed": result.get("technical_gate_passed"),
        "technical_findings": result.get("technical_findings", []),
        "preflight_decision": review.get("decision"),
        "hard_gate_passed": review.get("hard_gate_passed"),
        "repairs_applied_with_auto_repair": len(
            result.get("preflight_auto_repair_true", {}).get("repairs_applied", [])
        ),
        "local_gpu": result.get("backend", {}).get("local_gpu"),
    }


__all__ = [
    "SINGLE1_APPROVED_VIDEO",
    "SINGLE1_DECLARATION",
    "SINGLE1_TITLE",
    "CpuSimulationResult",
    "backend_state",
    "build_single1_payload",
    "load_single1_declaration",
    "probe_media",
    "simulate_single1_cpu",
    "summarize_review",
    "validate_technical_metadata",
]
