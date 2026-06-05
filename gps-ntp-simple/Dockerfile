FROM debian:bookworm-slim

# Avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
# python3-gps provides the 'import gps' module that ubxtool needs
RUN apt-get update && apt-get install -y \
    gpsd \
    gpsd-clients \
    chrony \
    bash \
    python3 \
    python3-gps \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

# Create directories for logs and config
RUN mkdir -p /etc/chrony /var/log/gpsntp

COPY run.sh /run.sh
COPY chrony.conf.template /etc/chrony.conf.template

RUN chmod +x /run.sh

# Chrony needs a specific user to run as in Debian
RUN touch /var/lib/chrony && chown chrony:chrony /var/lib/chrony

CMD ["/run.sh"]
