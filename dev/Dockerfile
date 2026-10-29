# syntax=docker/dockerfile:1
FROM debian:bookworm-slim@sha256:99c0b25c46d0214d5a2091092e7908907dcaecd6a962cde0ac700acee222b6f3

# The session CA is supplied at build time and is never stored in an image layer.
RUN --mount=type=secret,id=proxy_ca,required=true \
    apt-get -o Acquire::https::CaInfo=/run/secrets/proxy_ca update \
    && DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::https::CaInfo=/run/secrets/proxy_ca install -y --no-install-recommends \
       build-essential ca-certificates clang cmake curl git libasound2-dev \
       libclang-dev libgbm-dev libgtk-3-dev libpam0g-dev libpulse-dev \
       libssl-dev libudev-dev libva-dev libvdpau-dev libxcb-randr0-dev \
       libxcb-shape0-dev libxcb-xfixes0-dev libxfixes-dev libxkbcommon-dev \
       libxrandr-dev libxtst-dev nasm ninja-build pkg-config protobuf-compiler \
       python3 python3-protobuf unzip zip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/lunar-remote
CMD ["bash"]
