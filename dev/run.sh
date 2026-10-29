#!/usr/bin/env bash
set -euo pipefail
project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
workspace_root="$(dirname -- "$project_root")"
ca_bundle="${LUNAR_CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}"

# Preserve Docker's registry credentials and proxy configuration. Only select
# the managed local daemon, never a saved remote Docker context.
unset DOCKER_HOST DOCKER_CONTEXT DOCKER_TLS DOCKER_TLS_VERIFY DOCKER_CERT_PATH
docker --host=unix:///var/run/docker.sock info >/dev/null
docker --host=unix:///var/run/docker.sock build \
  --secret "id=proxy_ca,src=$ca_bundle" \
  -t lunar-remote-dev:bookworm -f "$project_root/dev/Dockerfile" "$project_root/dev"

if (( $# == 0 )); then
  set -- bash
fi
# Run as the checkout owner; generated files must not become root-owned.
docker --host=unix:///var/run/docker.sock run --rm -i \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$project_root,dst=/workspace/lunar-remote" \
  --mount "type=bind,src=$workspace_root/toolchains,dst=/workspace/toolchains" \
  --mount "type=bind,src=$ca_bundle,dst=/run/session-ca.pem,readonly" \
  -e HOME=/tmp \
  -e CARGO_HOME=/workspace/toolchains/cargo \
  -e RUSTUP_HOME=/workspace/toolchains/rustup \
  -e PATH=/workspace/toolchains/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  -e SSL_CERT_FILE=/run/session-ca.pem \
  -e CURL_CA_BUNDLE=/run/session-ca.pem \
  -e GIT_SSL_CAINFO=/run/session-ca.pem \
  -e CARGO_HTTP_CAINFO=/run/session-ca.pem \
  -w /workspace/lunar-remote \
  lunar-remote-dev:bookworm "$@"
