#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.agents.local.yml"
PROJECT_NAME="${COMPOSE_PROJECT_NAME:-kair-sonica-agents-local}"
API_URL="${KAIROS_LOCAL_API_URL:-http://127.0.0.1:${KAIR_LOCAL_API_PORT:-8001}}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker não está instalado/disponível neste host; execute este script no ambiente local com Docker Engine." >&2
  exit 78
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose v2 não está disponível neste host." >&2
  exit 78
fi

cleanup() {
  docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" down --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" up -d --build

for attempt in $(seq 1 30); do
  if curl --fail --silent --show-error "$API_URL/health" >/tmp/kair-agents-health.json; then
    break
  fi
  if [ "$attempt" -eq 30 ]; then
    docker compose -p "$PROJECT_NAME" -f "$COMPOSE_FILE" logs
    exit 1
  fi
  sleep 1
done

curl --fail --silent --show-error "$API_URL/v1/complementary/capabilities" >/tmp/kair-complementary-capabilities.json
curl --fail --silent --show-error "$API_URL/v1/agents/capabilities" >/tmp/kair-agents-capabilities.json
curl --fail --silent --show-error "$API_URL/v1/agents/skyreels-space/probe" >/tmp/kair-space-probe.json
curl --fail --silent --show-error "$API_URL/v1/agents/llamagen/probe" >/tmp/kair-llamagen-probe.json
curl --fail --silent --show-error \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"chuva cinematográfica em um videoclipe vertical","duration_seconds":10,"scene_seconds":5,"seed":42}' \
  "$API_URL/v1/complementary/plan" >/tmp/kair-complementary-plan.json

PYTHONPATH="$ROOT_DIR/packages" python3 "$ROOT_DIR/scripts/validate_agents_compose.py" \
  /tmp/kair-complementary-capabilities.json \
  /tmp/kair-agents-capabilities.json \
  /tmp/kair-space-probe.json \
  /tmp/kair-llamagen-probe.json \
  /tmp/kair-complementary-plan.json

echo "Docker Compose local agent discovery/probe test passed."
