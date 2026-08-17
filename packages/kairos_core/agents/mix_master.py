from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from kairos_core.audio.dsp import master_audio


@dataclass(frozen=True, slots=True)
class MixMasterAgent:
    """Fachada musical para o estágio DSP; mantém o processamento testável."""

    target_peak_dbfs: float = -1.0
    target_rms_dbfs: float = -14.0

    def process(self, audio: np.ndarray) -> np.ndarray:
        return master_audio(audio, target_peak_dbfs=self.target_peak_dbfs, target_rms_dbfs=self.target_rms_dbfs)
