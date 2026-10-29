#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
unset DOCKER_HOST DOCKER_CONTEXT DOCKER_TLS DOCKER_TLS_VERIFY DOCKER_CERT_PATH
docker_cmd=(docker --host=unix:///var/run/docker.sock)
project="lunar-smoke-${RANDOM}-$$"
compose=("${docker_cmd[@]}" compose -p "$project" -f "$project_root/infra/server/compose.yaml")
export LUNAR_RELAY_HOST=hbbr:21117
export LUNAR_BIND_ADDRESS=127.0.0.1

# Use a fresh private Docker network and data volume for each test. A dedicated
# override removes published ports so the probe cannot collide with a real VPS.
override="$(mktemp)"
cat > "$override" <<'YAML'
services:
  hbbs:
    ports: !reset []
  hbbr:
    ports: !reset []
YAML
compose+=(-f "$override")
cleanup() {
  "${compose[@]}" down -v --remove-orphans
  rm -f -- "$override" "${override}.pub" "${override}.after.pub"
}
trap cleanup EXIT

"${compose[@]}" config --quiet
"${compose[@]}" up -d --wait --wait-timeout 45
"${docker_cmd[@]}" run --rm \
  --network "${project}_default" \
  --mount "type=bind,src=$project_root,dst=/src,readonly" \
  --mount "type=volume,src=${project}_server-data,dst=/data,readonly" \
  -w /tmp lunar-remote-dev:bookworm sh -ec '
    protoc -I /src/libs/hbb_common/protos --python_out=/tmp /src/libs/hbb_common/protos/rendezvous.proto
    PYTHONPATH=/tmp python3 /src/infra/server/smoke.py
  '

# Restart services with retained data and prove the public identity is stable.
"${compose[@]}" cp hbbs:/data/id_ed25519.pub "${override}.pub"
"${compose[@]}" restart hbbs hbbr
"${compose[@]}" cp hbbs:/data/id_ed25519.pub "${override}.after.pub"
cmp -- "${override}.pub" "${override}.after.pub"
echo 'Server public identity preserved after restart.'
"${docker_cmd[@]}" run --rm \
  --network "${project}_default" \
  --mount "type=bind,src=$project_root,dst=/src,readonly" \
  --mount "type=volume,src=${project}_server-data,dst=/data,readonly" \
  -w /tmp lunar-remote-dev:bookworm sh -ec '
    protoc -I /src/libs/hbb_common/protos --python_out=/tmp /src/libs/hbb_common/protos/rendezvous.proto
    PYTHONPATH=/tmp python3 /src/infra/server/smoke.py
  '
