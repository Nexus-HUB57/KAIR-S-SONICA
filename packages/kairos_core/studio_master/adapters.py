from __future__ import annotations

from importlib.util import find_spec


class OptionalAdapterRegistry:
    """Catálogo de capacidade; a consulta não inicializa nenhum backend."""

    _specs: tuple[tuple[str, str, str], ...] = (
        ("neural-groove-extractor", "torch", "model checkpoint configured by operator"),
        ("pitch-tracking", "crepe", "audio adapter configured by operator"),
        ("spectral-ducking", "pedalboard", "sidechain multiband adapter"),
        ("reference-mastering", "matchering", "operator-supplied reference required"),
        ("artist-memory-vector", "chromadb", "metadata-only vector adapter"),
        ("perceptual-mos", "torchaudio", "MOS model checkpoint configured by operator"),
        ("midi-renderer", "fluidsynth", "soundfont path configured by operator"),
        ("viral-clip-renderer", "moviepy", "audio/video renderer configured by operator"),
    )

    def capabilities(self) -> list[dict[str, object]]:
        return [
            {
                "name": name,
                "dependency": dependency,
                "available": find_spec(dependency) is not None,
                "enabled": False,
                "reason": reason,
            }
            for name, dependency, reason in self._specs
        ]

    def enabled_names(self) -> list[str]:
        return []
