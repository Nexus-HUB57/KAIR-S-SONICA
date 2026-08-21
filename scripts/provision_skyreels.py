#!/usr/bin/env python3
"""Provisiona clone e checkpoint SkyReels-V2 de forma idempotente e auditável."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_NATIVE_FILES = (
    "model_index.json",
    "vae/config.json",
    "transformer/config.json",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("/opt/models/SkyReels-V2"))
    parser.add_argument("--models-root", type=Path, default=Path("/models"))
    parser.add_argument(
        "--native-model-id",
        default="Skywork/SkyReels-V2-DF-1.3B-540P-Diffusers",
        help="ID Hugging Face ou caminho local do checkpoint Diffusers",
    )
    parser.add_argument(
        "--native-model-dir",
        type=Path,
        help="Destino local opcional; por default usa models-root/ID",
    )
    parser.add_argument(
        "--cli-model-id",
        help="ID/caminho opcional do checkpoint do CLI original",
    )
    parser.add_argument(
        "--revision",
        help="Revisão imutável do checkpoint no Hub; recomendado para produção",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Permite acesso ao Hub e download; sem esta flag somente valida arquivos locais",
    )
    parser.add_argument(
        "--hf-token-env",
        default="HF_TOKEN",
        help="Nome da variável que contém o token opcional do Hub; o valor nunca é gravado",
    )
    parser.add_argument("--skip-repo-check", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def model_dir(args: argparse.Namespace) -> Path:
    if args.native_model_dir:
        return args.native_model_dir.expanduser().resolve()
    model_name = args.native_model_id.rstrip("/").split("/")[-1]
    return (args.models_root / "Skywork" / model_name).expanduser().resolve()


def validate_repo(repo: Path) -> dict[str, Any]:
    checks = {
        "directory": repo.is_dir(),
        "df_entrypoint": (repo / "generate_video_df.py").is_file(),
        "standard_entrypoint": (repo / "generate_video.py").is_file(),
    }
    if not checks["directory"] or not checks["df_entrypoint"]:
        missing = [key for key, value in checks.items() if not value]
        raise SystemExit(f"Clone SkyReels inválido em {repo}: {', '.join(missing)}")
    return checks


def validate_native_model(path: Path) -> dict[str, Any]:
    checks = {relative: (path / relative).is_file() for relative in REQUIRED_NATIVE_FILES}
    checks["directory"] = path.is_dir()
    checks["files"] = sum(value for key, value in checks.items() if key != "directory")
    if not checks["directory"] or checks["files"] != len(REQUIRED_NATIVE_FILES):
        missing = [relative for relative, value in checks.items() if relative in REQUIRED_NATIVE_FILES and not value]
        raise SystemExit(
            f"Checkpoint Diffusers incompleto em {path}; faltam: {', '.join(missing)}"
        )
    return checks


def download_model(model_id: str, target: Path, revision: str | None, token_env: str) -> None:
    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise SystemExit(
            "Download solicitado, mas huggingface_hub não está instalado; "
            "instale-o somente no ambiente CUDA autorizado"
        ) from exc
    token = os.getenv(token_env) or None
    target.parent.mkdir(parents=True, exist_ok=True)
    kwargs: dict[str, Any] = {
        "repo_id": model_id,
        "local_dir": str(target),
        "token": token,
        "resume_download": True,
    }
    if revision:
        kwargs["revision"] = revision
    snapshot_download(**kwargs)


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    if temporary.exists():
        raise SystemExit(f"Manifesto temporário já existe e não será reutilizado: {temporary}")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def main() -> int:
    args = parse_args()
    if args.download and not args.revision:
        raise SystemExit(
            "--revision é obrigatório com --download para garantir um checkpoint reproduzível"
        )
    repo = args.repo.expanduser().resolve()
    target = model_dir(args)
    manifest = args.models_root.expanduser().resolve() / "kairos-skyreels-manifest.json"
    lock_path = args.models_root.expanduser().resolve() / ".kairos-skyreels.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        repo_checks = {} if args.skip_repo_check else validate_repo(repo)
        local_before = target.is_dir()
        if args.download and not args.dry_run and not (
            target.is_dir() and all((target / relative).is_file() for relative in REQUIRED_NATIVE_FILES)
        ):
            download_model(args.native_model_id, target, args.revision, args.hf_token_env)
        if not args.dry_run:
            model_checks = validate_native_model(target)
        else:
            model_checks = {"directory": target.is_dir(), "dry_run": True}

        payload: dict[str, Any] = {
            "schema_version": 1,
            "configured_at": datetime.now(timezone.utc).isoformat(),
            "repo": str(repo),
            "native": {
                "model_id": args.native_model_id,
                "model_dir": str(target),
                "revision": args.revision,
                "checks": model_checks,
            },
            "cli_model_id": args.cli_model_id,
            "repo_checks": repo_checks,
            "download_requested": args.download,
            "local_model_preexisting": local_before,
            "download_token_env": args.hf_token_env if args.download else None,
        }
        if not args.dry_run:
            atomic_write(manifest, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
