#!/usr/bin/env python3
"""Inspeciona elegibilidade para auto-retraining sem treinar ou promover checkpoints.

O treino real deve ser executado em um host configurado pelo operador, com manifesto,
revisão humana, split de validação e promoção atômica após os testes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from kairos_core.studio_master.retraining import AutoRetrainGuard


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("data/studio-master/retrain-manifest.json"))
    parser.add_argument("--enabled", action="store_true", help="apenas inspeciona o gate como habilitado")
    args = parser.parse_args()
    guard = AutoRetrainGuard(args.manifest, enabled=args.enabled)
    print(json.dumps(guard.execution_plan(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
