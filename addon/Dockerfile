FROM ghcr.io/home-assistant/amd64-base:latest

RUN apk add --no-cache \
    gpsd gpsd-clients \
    chrony \
    python3 py3-pip \
    mosquitto-clients \
    udev jq \
    bash \
    socat \
    tzdata \
    build-base

RUN pip install fastapi uvicorn[standard] paho-mqtt psutil

COPY rootfs /

RUN chmod -R +x /etc/services.d /etc/cont-init.d /usr/bin
