#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.gpu.yml"
PROJECT_NAME="${COMPOSE_PROJECT_NAME:-kair-sonica-gpu-agents}"
API_URL="${KAIROS_GPU_API_URL:-http://127.0.0.1:${KAIR_API_PORT:-8000}}"
RUN_EXTERNAL_PROBES="${KAIROS_RUN_EXTERNAL_PROBES:-false}"
REQUIRE_NATIVE="${KAIROS_REQUIRE_NATIVE_READY:-true}"
REQUIRE_LLAMAGEN="${KAIROS_REQUIRE_LLAMAGEN_PROBE:-false}"
TMP_DIR="${TMPDIR:-/tmp}/kair-sonica-gpu-agents-${PROJECT_NAME}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker não está disponível neste host GPU." >&2
  exit 78
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 não está disponível neste host GPU." >&2
  exit 78
fi
if ! command -v nvidia-smi >/dev/null 2>&1; then
  echo "nvidia-smi não está disponível; este teste exige host NVIDIA CUDA." >&2
  exit 78
fi
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader

docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" config --quiet
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

cleanup() {
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

for attempt in $(seq 1 120); do
  if curl --fail --silent --show-error "$API_URL/ready" >"$TMP_DIR/ready.json"; then
    break
  fi
  if [ "$attempt" -eq 120 ]; then
    docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" logs --tail=200
    exit 1
  fi
  sleep 2
done

curl --fail --silent --show-error "$API_URL/health" >"$TMP_DIR/health.json"
curl --fail --silent --show-error "$API_URL/v1/video/capabilities" >"$TMP_DIR/video-capabilities.json"
curl --fail --silent --show-error "$API_URL/v1/agents/capabilities" >"$TMP_DIR/agent-capabilities.json"
curl --fail --silent --show-error "$API_URL/v1/agentic/capabilities" >"$TMP_DIR/agentic-capabilities.json"

if [ "$RUN_EXTERNAL_PROBES" = "true" ]; then
  if [ "${KAIROS_AGENT_AGGREGATOR_ENABLED:-false}" != "true" ] || [ "${KAIROS_SKYREELS_SPACE_ENABLED:-false}" != "true" ]; then
    echo "Probes externos solicitados, mas os gates do SkyReels Space não estão ambos em true." >&2
    exit 2
  fi
  curl --fail --silent --show-error "$API_URL/v1/agents/skyreels-space/probe" >"$TMP_DIR/skyreels-space-probe.json"

  if [ "${KAIROS_AGENT_AGGREGATOR_ENABLED:-false}" = "true" ] && [ "${KAIROS_LLAMAGEN_ENABLED:-false}" = "true" ] && [ -n "${LLAMAGEN_API_KEY:-}" ]; then
    curl --fail --silent --show-error "$API_URL/v1/agents/llamagen/probe" >"$TMP_DIR/llamagen-probe.json"
  elif [ "$REQUIRE_LLAMAGEN" = "true" ]; then
    echo "LlamaGen obrigatório, mas o gate ou LLAMAGEN_API_KEY não está disponível." >&2
    exit 2
  else
    echo "LlamaGen probe skipped: gate/chave não habilitados neste teste."
  fi
else
  echo "External probes skipped: use KAIROS_RUN_EXTERNAL_PROBES=true após revisar gates e credenciais."
fi

PYTHONPATH="$ROOT_DIR/packages" python3 "$ROOT_DIR/scripts/validate_agents_gpu_compose.py" \
  "$TMP_DIR/video-capabilities.json" \
  "$TMP_DIR/agent-capabilities.json" \
  "$TMP_DIR/agentic-capabilities.json" \
  "$REQUIRE_NATIVE" \
  "$RUN_EXTERNAL_PROBES" \
  "$TMP_DIR"

echo "Docker Compose GPU discovery/readiness test passed."
