FROM alpine:latest

# Install gpsd, chrony, and build tools
RUN apk add --no-cache \
    gpsd \
    gpsd-clients \
    chrony \
    bash \
    util-linux

# Create a directory for logs and config
RUN mkdir -p /etc/chrony && mkdir -p /var/log/gpsntp

COPY run.sh /run.sh
COPY chrony.conf.template /etc/chrony.conf.template

RUN chmod +x /run.sh

CMD ["/run.sh"]
