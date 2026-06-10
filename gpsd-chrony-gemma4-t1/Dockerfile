ARG BUILD_FROM=ghcr.io/homeassistant/armv7-debian:bookworm
FROM $BUILD_FROM

RUN apt-get update && \
    apt-get install -y --no-install-recommends gpsd gpsd-clients chrony && \
    rm -rf /var/lib/apt/lists/*

COPY rootfs/ /

CMD ["start.sh"]