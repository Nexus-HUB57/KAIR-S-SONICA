#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-$ROOT_DIR/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ -e "$VENV_DIR" ] && [ ! -x "$VENV_DIR/bin/python" ]; then
  echo "VENV_DIR existe mas não parece um virtualenv: $VENV_DIR" >&2
  exit 2
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -e "$ROOT_DIR[dev]"

if command -v npm >/dev/null 2>&1 && [ -f "$ROOT_DIR/web-client/package-lock.json" ]; then
  npm ci --prefix "$ROOT_DIR/web-client"
fi

cat <<EOF
Ambiente pronto em: $VENV_DIR
Ative com: source "$VENV_DIR/bin/activate"
Valide com: make lint && make test
EOF
