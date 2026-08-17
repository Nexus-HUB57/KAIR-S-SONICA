from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class StemSeparationUnavailable(RuntimeError):
    pass


class DemucsSeparator:
    """Adaptador explícito para o CLI Demucs, sem instalação/download implícito."""

    def separate(self, input_path: Path, output_dir: Path, model: str = "htdemucs") -> dict[str, Path]:
        executable = shutil.which("demucs")
        if not executable:
            raise StemSeparationUnavailable("Demucs não está instalado; instale a dependência opcional antes de separar stems")
        output_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run([executable, "-n", model, "-o", str(output_dir), str(input_path)], check=True)
        stem_root = output_dir / model / input_path.stem
        return {path.stem: path for path in stem_root.glob("*.wav")}
