ARG BUILD_FROM=ghcr.io/hassio-addons/base:21.0.0
# hadolint ignore=DL3006
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    gpsd=3.27.3-r1 \
    gpsd-clients=3.27.3-r1 \
    chrony=4.8-r6 \
    tzdata=2026b-r0

# Copy data for app
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]