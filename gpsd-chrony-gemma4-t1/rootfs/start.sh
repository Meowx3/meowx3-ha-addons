#!/bin/bash
set -e

# Start gpsd with specified device and baud rate
/usr/sbin/gpsd -N -F /etc/gpsd.socket "${DEVICE_PATH:-/dev/ttyACM0}"

# Start chrony for time synchronization (optional, if needed)
if [ -f /usr/bin/chronyd ]; then
    /usr/bin/chronyd -d
fi

# Echo GPS data to shell in NMEA format using gpspipe
echo "Starting GPS monitoring on ${DEVICE_PATH:-/dev/ttyACM0}..."
exec /usr/bin/gpspipe -r -d "${DEVICE_PATH:-/dev/ttyACM0}"