#!/bin/bash

# 1. Auto-detect GPS Device
GPS_DEV=$(ls /dev/ttyUSB* /dev/ttyACM* | head -n 1)
if [ -z "$GPS_DEV" ]; then
    echo "No GPS device found. Waiting..."
fi

# 2. UBLOX Optimization (via ubxtool)
if [[ $GPS_DEV == *"USB"* ]]; then
    echo "Optimizing UBLOX receiver..."
    # Enable Galileo, GLONASS and maximize update rate (1Hz - 5Hz)
    ubxtool -p CFG-NAV5 > /dev/null
    ubxtool -s CFG-MSG-PPS=1 > /dev/null
fi

# 3. Start GPSD with PPS support
# -n: don't wait for client, -n: read from device immediately
gpsd -N -n $GPS_DEV

# 4. Apply Chrony config and start
chronyd -f /app/chrony.conf.template

# 5. Start Python Manager (MQTT & Web UI)
python3 /app/src/main.py
