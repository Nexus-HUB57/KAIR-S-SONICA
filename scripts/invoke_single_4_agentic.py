#!/usr/bin/env python3
"""Invoca o planejamento agentic do quarto single old school.

O comando executa os contratos locais dos 12 papéis do estúdio, sem consultas
externas e sem submeter handoffs ao worker. O resultado é salvo para revisão.
"""

from __future__ import annotations

import json
from pathlib import Path

from kairos_core.agentic import AgenticOrchestrator, AgenticRunRequest
from kairos_core.config import Settings


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" / "single_4"
MEMORY_DIR = OUTPUT_DIR / "agentic_memory"
RESULT_PATH = OUTPUT_DIR / "single_4_agentic_run.json"

PROMPT = """Desenvolver o quarto single de rap old school de KTD sob coordenação do Maestro Layer Káiros. Este é um pacote inicial de composição e produção musical, não uma solicitação de vídeo final. A faixa deve usar linguagem old school: bateria marcada e humana, kick e snare presentes, baixo conversando com o bumbo, textura harmônica com caráter, espaço para rimas rápidas e vocal central com autoridade. O conceito precisa defender uma tese artística controversa e debatível, confrontando hipocrisia, pressão social, apagamento e exploração sem discurso de ódio, ameaça real, violência gráfica ou ataque a grupo protegido.

Prioridade absoluta: criar um refrão muito forte, polêmico, poderoso e inspirador. O refrão deve ter uma frase central memorável, resposta rítmica clara, imagens fortes, cadência coletiva e uma virada que transforme pressão em autonomia, dignidade e movimento. A composição deve usar rimas internas, aliteração, métrica controlada, contrastes de densidade e espaço para interpretação autoral de KTD em registro médio-grave, com ataque firme e presença frontal, sem imitar qualquer artista real.

Solicitar aos agentes: estratégia e tese do single; conceito e título provisório; refrão com alternativas; letra estruturada; análise de métrica e rimas; direção de beat old school; direção vocal e performance; plano de arranjo e mixagem; QA editorial, de segurança e de qualidade; memória de decisões e handoffs. Tratar o quarto single como uma nova obra autoral e manter todos os handoffs em READY_FOR_APPROVAL, sem criar tarefas de produção ainda."""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    settings = Settings(
        agentic_memory_dir=MEMORY_DIR,
        agentic_external_tools_enabled=False,
        agentic_core_enabled=True,
    )
    request = AgenticRunRequest(
        prompt=PROMPT,
        project_id="ktd-single-04-old-school-rap",
        duration_seconds=120.0,
        aspect_ratio="16:9",
        resolution="720P",
        fps=24,
        scene_seconds=30.0,
        audio_mode="old-school-rap-development",
        media_mode="no-external-media",
        seed=20260821,
        include_media_references=False,
        submit_handoffs=False,
        approve_handoffs=False,
        max_iterations=2,
    )
    result = AgenticOrchestrator(settings).run(request)
    payload = result.to_dict()
    payload["invocation"] = {
        "mode": "local-contract-first",
        "external_tools": False,
        "handoffs_submitted": False,
        "briefing_file": "docs/singles/single-4-old-school-briefing.md",
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "run_id": result.run_id,
        "project_id": result.project_id,
        "status": result.status,
        "roles": len(result.roles),
        "handoffs": len(result.handoffs),
        "artifacts": sorted(result.artifacts),
        "result_path": str(RESULT_PATH),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
