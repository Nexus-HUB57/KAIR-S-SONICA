#!/usr/bin/env python3
"""Gera inventário SHA-256 e regras de não repetição visual do álbum."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}

RULES = {
    "GOLDEN_SCARS": {
        "status": "reserved",
        "blocked_for": ["UNLEASH_THE_DRAGON", "SIX_NAMES"],
        "restrictions": [
            "Não reutilizar corredor industrial, rua chuvosa, porta metálica ou sujeito central.",
            "Não reutilizar brilho azul nos olhos ou paleta cinza/preto/azul metálico.",
            "Não reutilizar a mesma composição, enquadramento ou movimento do MP4 aprovado.",
        ],
    },
    "UNLEASH_THE_DRAGON": {
        "status": "exclusive",
        "allowed_for": ["UNLEASH_THE_DRAGON"],
        "restrictions": [
            "Usar bastidor, porta de acesso ao palco, cabos, microfone, tênis e luz vermelho-âmbar.",
            "Não usar seis pratos, mesa doméstica, vela familiar ou chuva industrial.",
        ],
    },
    "SIX_NAMES": {
        "status": "exclusive",
        "allowed_for": ["SIX_NAMES"],
        "restrictions": [
            "Usar mesa doméstica, seis pratos, vela, mãos e memória familiar.",
            "Não usar palco, porta metálica, corredor industrial, água, chuva ou olhos azuis.",
        ],
    },
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def classify(path: Path) -> str:
    text = path.as_posix().lower()
    if "golden-scars" in text or "ktd-approved" in text or "initial-tour-01" in text:
        return "GOLDEN_SCARS"
    if "song1" in text or "unleash-the-dragon" in text:
        return "UNLEASH_THE_DRAGON"
    if "song2" in text or "six-names" in text:
        return "SIX_NAMES"
    return "UNASSIGNED"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    root = args.root.resolve()
    candidates = sorted(
        path for path in (root / "assets").rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
    )
    files = []
    for path in candidates:
        relative = path.relative_to(root).as_posix()
        category = classify(path)
        files.append({
            "path": relative,
            "extension": path.suffix.lower().lstrip("."),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
            "category": category,
            "status": RULES.get(category, {}).get("status", "unassigned"),
        })

    inventory = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "algorithm": "SHA-256",
        "scope": "assets visual e vídeos do catálogo KAIR-S-SONICA",
        "files": files,
        "rules": RULES,
        "limitations": [
            "SHA-256 detecta duplicatas binárias exatas; não substitui revisão perceptual de imagens semelhantes.",
            "Qualquer novo ativo deve ser classificado antes de entrar em um vídeo.",
            "Arquivos UNASSIGNED exigem decisão editorial antes do uso em qualquer faixa.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Inventário visual de não repetição",
        "",
        f"Gerado em UTC: `{inventory['generated_at_utc']}`  ",
        "Algoritmo: `SHA-256`",
        "",
        "## Regras por faixa",
        "",
    ]
    for category, rule in RULES.items():
        lines.append(f"### {category}")
        lines.append(f"Status: **{rule['status']}**")
        for key in ("allowed_for", "blocked_for"):
            if rule.get(key):
                lines.append(f"`{key}`: {', '.join(rule[key])}")
        for item in rule["restrictions"]:
            lines.append(f"- {item}")
        lines.append("")
    lines.extend([
        "## Arquivos inventariados",
        "",
        "| Caminho | Categoria | Estado | Bytes | SHA-256 |",
        "|---|---|---|---:|---|",
    ])
    for item in files:
        lines.append(f"| `{item['path']}` | {item['category']} | {item['status']} | {item['bytes']} | `{item['sha256']}` |")
    lines.extend([
        "",
        "## Limitações",
        "",
        "- SHA-256 identifica duplicata binária exata, mas não detecta automaticamente imagens visualmente parecidas.",
        "- Todo novo ativo deve ser classificado antes de ser usado em um MP4.",
        "- Arquivos `UNASSIGNED` exigem decisão editorial antes do uso.",
        "",
    ])
    args.output_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Inventário JSON: {args.output_json}")
    print(f"Inventário Markdown: {args.output_md}")
    print(f"Arquivos inventariados: {len(files)}")


if __name__ == "__main__":
    main()
