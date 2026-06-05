FROM alpine:latest

# Install gpsd, chrony, bash, AND python3
# we add python3 specifically because ubxtool is a python script
RUN apk add --no-cache \
    gpsd \
    gpsd-clients \
    chrony \
    bash \
    util-linux \
    python3 \
    py3-pip

# Ensure the system knows where python3 is 
# Some versions of ubxtool look for /usr/bin/python3 explicitly
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Create a directory for logs and config
RUN mkdir -p /etc/chrony && mkdir -p /var/log/gpsntp

COPY run.sh /run.sh
COPY chrony.conf.template /etc/chrony.conf.template

RUN chmod +x /run.sh

CMD ["/run.sh"]
