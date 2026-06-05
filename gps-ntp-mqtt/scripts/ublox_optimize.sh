#!/bin/bash

# Usage: ./ublox_optimize.sh /dev/ttyUSB0
GPS_DEVICE=$1

if [ -z "$GPS_DEVICE" ]; then
    echo "Error: No device specified. Usage: $0 /dev/ttyUSB0"
    exit 1
fi

echo "Starting UBLOX Optimization on $GPS_DEVICE..."

# We use ubxtool to send binary UBX messages directly to the chip.
# These settings are designed for UBLOX-7, 8, and M9 series.

# 1. Enable PPS output on the TXEN/PPS pin
# This ensures the hardware pulse is physically sent out for Chrony to see.
echo "Configuring PPS output..."
ubxtool -s CFG-MSG-PPS=1 > /dev/null

# 2. Multi-GNSS Configuration
# We want GPS, GLONASS, and Galileo enabled simultaneously to maximize 
# the number of visible satellites for better timing stability.
echo "Enabling Multi-GNSS (GPS + GLONASS + Galileo)..."
# CFG-GNSS: Enable GPS (bit 0), GLONASS (bit 1), Galileo (bit 2)
ubxtool -s CFG-GNSS_GPS_ENA=1 > /dev/null
ubxtool -s CFG-GNSS_GLO_ENA=1 > /dev/null
ubxtool -s CFG-GNSS_GAL_ENA=1 > /dev/null

# 3. Navigation Rate & Timing
# For NTP, consistency is better than speed. We set the measurement rate to 1Hz.
echo "Setting navigation rate to 1Hz..."
ubxtool -s CFG-NAV5_MEASRATE=1000 > /dev/null # 1000ms = 1Hz

# 4. NMEA Message Filtering (Optimization for the Web UI)
# We disable unnecessary messages to save bandwidth, but keep those needed for 
# antenna diagnostics and sky-view visualization (GGA, GSA, GSV).
echo "Filtering NMEA messages..."
ubxtool -s CFG-MSG-NMEA_GGA=1 > /dev/null # Fix data (Required)
ubxtool -s CFG-MSG-NMEA_GLL=0 > /dev/null # Geographic position (Disable)
ubxtool -s CFG-MSG-NMEA_GSA=1 > /dev/null # Dilution of precision (Required for Health)
ubxtool -s CFG-MSG-NMEA_GSV=1 > /dev/null # Satellites in view (Required for Sky-View UI)
ubxtool -s CFG-MSG-NMEA_RMC=0 > /dev/null # Recommended minimum (Disable)
ubxtool -s CFG-MSG-NMEA_VTG=0 > /dev/null # Course over ground (Disable)

# 5. Dynamic Model Configuration
# Set the chip to 'Stationary' mode. This tells the internal Kalman filter 
# that the antenna isn't moving, which significantly reduces timing jitter.
echo "Setting dynamic model to STATIONARY..."
ubxtool -s CFG-NAV5_DYNMODEL_FIXED=1 > /dev/null

# 6. Save configuration to permanent memory (BBR/Flash)
# This ensures that if the HA host reboots, the GPS chip keeps these settings.
echo "Saving configuration to flash..."
ubxtool -s CFG-SAVECONFIG=1 > /dev/null

echo "UBLOX Optimization Complete."
