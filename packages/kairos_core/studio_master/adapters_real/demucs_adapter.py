from __future__ import annotations

import re
from pathlib import Path
from typing import Any, ClassVar

from kairos_core.studio_master.adapters_real.base import (
    AdapterContext,
    AdapterResult,
    AdapterSpec,
    AdapterUnavailable,
)

SPEC = AdapterSpec(
    adapter_id="demucs",
    package="demucs",
    import_module="demucs",
    code_license="MIT",
    code_license_url="https://pypi.org/project/demucs/",
    source_url="https://github.com/facebookresearch/demucs",
    model_artifact_policy="checkpoint_and_dataset_provenance_required",
    requires_gpu=False,
    requires_external_asset=False,
    fallback="approved_stem_handoff",
    risk_level="model_and_dataset_review",
)


class DemucsAdapter:
    adapter_id = SPEC.adapter_id
    _models: ClassVar[set[str]] = {"htdemucs", "htdemucs_ft", "htdemucs_6s", "hdemucs_mmi", "mdx", "mdx_extra"}

    def __init__(self, settings: Any) -> None:
        self.context = AdapterContext(settings, SPEC)

    def capability(self):
        return self.context.capability()

    def run(
        self,
        audio_path: str,
        *,
        model: str = "htdemucs",
        two_stems: str | None = None,
        run_id: str = "separation",
        fallback: bool = True,
    ) -> AdapterResult:
        try:
            self.context.require_ready()
            if not getattr(self.context.settings, "studio_master_adapter_allow_model_download", False):
                raise AdapterUnavailable("download de checkpoint Demucs está desligado")
            audio = self.context.approved_asset(audio_path)
            if model not in self._models:
                raise AdapterUnavailable(f"modelo Demucs não permitido: {model}")
            if two_stems not in {None, "vocals", "drums", "bass", "other"}:
                raise AdapterUnavailable("two_stems inválido")
            safe_id = re.sub(r"[^a-zA-Z0-9_-]+", "-", run_id).strip("-")[:80] or "separation"
            root = Path(self.context.settings.studio_master_adapter_output_dir).expanduser().resolve()
            output_dir = root / "demucs" / safe_id
            if output_dir.exists():
                raise AdapterUnavailable("diretório de separação existente não será sobrescrito")
            output_dir.mkdir(parents=True, exist_ok=False)
            import demucs.separate  # type: ignore[import-not-found]

            args = ["-n", model, "-o", str(output_dir), "-d", "cpu"]
            if two_stems:
                args.extend(["--two-stems", two_stems])
            args.append(str(audio))
            try:
                demucs.separate.main(args)
            except SystemExit as exc:
                if exc.code not in {None, 0}:
                    raise AdapterUnavailable(f"Demucs encerrou com código {exc.code}") from exc
            stems = sorted(str(path) for path in output_dir.rglob("*.wav"))
            if not stems:
                raise AdapterUnavailable("Demucs terminou sem stems WAV")
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="demucs.separate/v1",
                status="SUCCEEDED",
                output=stems,
                metadata={"model": model, "two_stems": two_stems, "output_dir": str(output_dir)},
            )
        except (AdapterUnavailable, ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
            if not fallback:
                raise
            return AdapterResult(
                adapter_id=self.adapter_id,
                method="approved-stem-handoff/fallback-v1",
                status="FALLBACK",
                output={"audio_path": audio_path},
                warnings=[f"Demucs indisponível: {exc}"],
                metadata={"fallback": self.context.spec.fallback},
                fallback_used=True,
            )
