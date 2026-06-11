# Garnet CLI image — S166–S178 distribution-band draft (NOT published anywhere).
# Unlike the winget/scoop drafts, this recipe is REAL today: it pins the published
# v0.8.1 Linux .deb by its official SHA256 (from the release's signed SHA256SUMS).
# Build:  docker build -t garnet:0.8.1 .
# Smoke:  docker run --rm garnet:0.8.1 --version
# Image publication (Docker Hub / GHCR) is Jon-owned and out of scope.

FROM debian:bookworm-slim

ARG GARNET_DEB_URL=https://github.com/Island-Dev-Crew/garnet/releases/download/v0.8.1/garnet_0.8.1-1_amd64.deb
ARG GARNET_DEB_SHA256=ca35ebf881cc1d16f288f850eb767305c590112a05966c6778e5fa3d2a42e0cc

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ca-certificates curl; \
    curl -fsSL -o /tmp/garnet.deb "$GARNET_DEB_URL"; \
    echo "$GARNET_DEB_SHA256  /tmp/garnet.deb" | sha256sum -c -; \
    dpkg -i /tmp/garnet.deb; \
    rm -f /tmp/garnet.deb; \
    apt-get purge -y curl; \
    apt-get autoremove -y; \
    rm -rf /var/lib/apt/lists/*; \
    garnet --version

ENTRYPOINT ["garnet"]
CMD ["--help"]
