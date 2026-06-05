#!/usr/bin/with-contenv bash

DEVICES=$(python3 /usr/bin/gps_detect.py | jq -r '.gps | join(" ")')

exec gpsd -N -n $DEVICES
